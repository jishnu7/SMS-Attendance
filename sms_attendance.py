#!/usr/bin/python
'''
    SMS Attendance
    Copyright (C) 2010-2012 jishnu7@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
# SMS Attendance
# Author  : jishnu7@gmail.com

import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import datetime
import cPickle
import os
from db import *
from fullonsms import *
from accounts import *

# To avoid continous deletion of accounts,
# incase college website is not accessible
DEL_MAX = 2
DEL_COUNT = 0
DEL_QUEUE = []
DEL_FILENAME = 'attendance-account-delete.log'
PICKLE_FILE = 'attendance-lastupdate.pck'
DETAIL_FAILED_FILE = 'attendance-detail-failed.log'

class Pickle():
    ''' Class to manage pickling operations '''
    def __init__(self, filename):
        self.filename = filename

    def pickling(self, data, permission='wb'):
        ''' Save to pickle file '''
        pfile = open(self.filename, permission)
        cPickle.dump(data, pfile)
        pfile.close()
        return

    def unpickling(self):
        ''' Get values from pickle file '''
        data = []
        if os.path.isfile(self.filename):
            pfile = open(self.filename, 'rb')
            data = cPickle.load(pfile)
            pfile.close()
            return data['last_user']
        else:
            return 0


# Function to fetch info from college website
def fetch_attendance(username, passwd, mobnum):
    global DEL_MAX
    global DEL_QUEUE
    global DEL_COUNT
    global DEL_FILENAME

    print username
    # Set Cookie and log into college website
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'txtLogin': username, 'txtPass': passwd})
    login = opener.open('http://www.mesce.ac.in/MainLoginValidation.php',
                        login_data)

    # Page for attendance summary
    attendance_page = opener.open('http://www.mesce.ac.in/departments/'\
                                  'student.php?option=attendanceSummary')
    attendance_var = attendance_page.read()
    attendance_var = BeautifulSoup(attendance_var)
    search = attendance_var.findAll(
             attrs={"align": "center", "class": "head1"})

    # If login was unsucessfull skip current user
    try:
        len_search = len(search)
        numHours = search[len_search - 3].contents[0]
        totHours = search[len_search - 2].contents[0]
        percent = search[len_search - 1].contents[0].next
        detail_sem = search[len_search - 4].contents[0]['value']
    except:
        DEL_COUNT += 1
        # If continuous deletion not reached DEL_MAX
        if DEL_COUNT < DEL_MAX:
            # Write to log file
            f = open(DEL_FILENAME, 'a+')
            f.write(str(datetime.date.today().day) + "-" + \
                    str(datetime.date.today().month) + \
                    " DELETE " + username + " " + str(mobnum) + "\n")
            f.close()
            # Delete from database
            delete_db = database()
            delete_db.delete(username)
            # Send message to user
            msg = "SMS Attendance \r\n" + username + ", Invalid username. " \
                  "Your current registraion is deleted. " \
                  "Please re-register at http://attendance.thecodecracker.com"
            return msg
        else:
            # Restore from account delete log
            db = database()
            db.restore(DEL_FILENAME)
            # Print error, and exit from program
            print "ERROR : " + str(DEL_MAX) + " accounts deletd continuously"
            sys.exit(1)

    DEL_COUNT = 0
    # set date values for detail info
    # From date
    d1 = "1"
    m1 = datetime.date.today().month
    y1 = datetime.date.today().year
    # If 1st day of the month, then we need data from 1st day of prev month
    if datetime.date.today().day == 1:
        m1 = m1 - 1
        if m1 == 0:
            m1 = "12"
            y1 = y1 - 1
    # To date, today
    d2 = datetime.date.today().day
    m2 = datetime.date.today().month
    y2 = datetime.date.today().year

    # Submit data and retrieve detailed information in the date range we set.
    details_data = urllib.urlencode({
                                        'subSemester': detail_sem,
                                        'selDay1': d1,
                                        'selMonth1': m1,
                                        'selYear1': y1,
                                        'selDay2': d2,
                                        'selMonth2': m2,
                                        'selYear2': y2
                                    })
    details_page = opener.open('http://www.mesce.ac.in/departments/' \
                               'student.php?option=attendanceDetail',
                                details_data)
    details_var = details_page.read()
    details_var = BeautifulSoup(details_var)

    # Default SMS Message. without detailed information
    msg = "SMS Attendance \r\nName : " + username.split(".")[0].capitalize() \
          + " \r\nNo of Hours Attended : " + numHours \
          + " \r\nTotal Hours Engaged : " + totHours \
          + " \r\nAttendance : " + percent + "%"

    try:
        # If there is no error message
        search_detail = details_var.find('td', 'errfont')
        if search_detail == None:
            search_details = details_var.findAll(attrs={"class": "tfont"})
            temp_detail = list()
            # Total length of table
            len_detail = len(search_details)
            for x in range(len_detail - 17, len_detail - 2):
                try:
                    temp_detail.append( \
                        str(search_details[x].contents[0].contents[0]))
                except:
                    try:
                        temp_detail.append(str(search_details[x].contents[0]))
                    except:
                        temp_detail.append("-")
            detail = list()
            update_day = temp_detail[8].split("-")[0]
            update_month = temp_detail[8].split("-")[1]
            update_year = temp_detail[8].split("-")[2]
            update_date = update_year + '-' + update_month + '-' + update_day
            update_check = database()
            # Send message only if there is a new update.
            if update_check.update_check(username, update_date):
                # date in date-month format
                detail.append(update_day + "/" + update_month)
                if temp_detail[0] == temp_detail[8]:
                    for x in range(1, 7):
                        if temp_detail[x] == "-":
                            detail.append(temp_detail[x + 8])
                        else:
                            detail.append(temp_detail[x])
                else:
                    for x in range(9, 15):
                        detail.append(temp_detail[x])
                # add today to database
                update_check.update(username, update_date)
                # Append the detailed info to the message
                msg = msg + " \r\nLast Day " \
                          + detail[0] + ": " \
                          + detail[1] + " " \
                          + detail[2] + " " \
                          + detail[3] + " " \
                          + detail[4] + " " \
                          + detail[5] + " " \
                          + detail[6]
                return msg
    except:
        print  "----------------------\n" + \
               "ERROR while getting details" + \
               "\n----------------------"
    print "Details not found. Skipping user"
    f = open(DETAIL_FAILED_FILE, 'a+')
    f.write(str(d2) + "-" + str(m2) + "-" + str(y2) + " " + username + "\n")
    f.close()
    return None


def send_one_by_one(previous, pck):
    db = database()
    last_user_num = previous

    for account in ACCOUNTS:
        # Import message sender class
        exec('import ' + account['class'] + ' as import_file')
        sms_class = getattr(import_file, account['class'])
        sms = sms_class()
        if sms.login(account['username'], account['password']) == True:
            # To avoid infinite loop
            loop = 0
            while loop < 2:
                user = db.fetch_one(last_user_num)
                if user == None:
                    last_user_num = 0
                    loop += 1
                    continue
                message = fetch_attendance(user[0], user[1], user[3])
                if message:
                    if sms.send(message, user[3]) == False:
                        break
                last_user_num += 1
                pck.pickling({'last_user': last_user_num})
                # In case, message sent to all accounts.
                if last_user_num == previous:
                    return last_user_num
            if loop == 2:
                return last_user_num


if __name__ == "__main__":
    pck = Pickle(PICKLE_FILE)
    previous = pck.unpickling()

    db = database()
    last_user = send_one_by_one(previous, pck)
    pck.pickling({'last_user': last_user})

    # Limit number of account on each run. 0 for all accounts
    #LIMIT = 100
    #users, last_user_num = db.fetch(previous['last_user'], LIMIT)
