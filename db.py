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

import MySQLdb
import sys
import datetime

DBHOST = "localhost"
DBUSER = " "
DBPASS = " "
DB = " "


class database():
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)


    def delete(self, username):
        try:
            query = "DELETE FROM users WHERE username = '"+username+"' LIMIT 1"
            error = self.db.cursor()
            error.execute(query)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])


    def restore(self,DEL_FILENAME):
        # Restore accounts from delete log file
        f = open(DEL_FILENAME, 'r')
        for line in f.readlines():
            if line.split(' DELETE ')[0] == str(datetime.date.today().day)+"-"+str(datetime.date.today().month):
                a = line.split(' DELETE ')[1].split('\n')[0]
                account = a.split(' ')[0]
                password = account.split('.')[1]
                mob = a.split(' ')[1]

                try:
                    cursor = self.db.cursor()
                    cursor.execute("SELECT `username` FROM `users` WHERE `username`='"+account+"' AND `mob`='"+mob+"'")
                    rows = int(cursor.rowcount)
                    if rows > 0:
                        continue

                    cursor.execute("INSERT INTO `users` (`username` ,`passwd` , `mob`) VALUES ( '"+account+"', '"+password+"', '"+mob+"')")

                    print "RESTORE DELETED ACCOUNTS "+account+'--'+password+'--'+mob
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    continue
        # Empty the file
        open(DEL_FILENAME, 'w').close()


    def fetch(self, start, limit):
        users = []
        end = limit
        i=0
        while True:
            cursor = self.db.cursor()
            query = "SELECT `username`, `passwd`, `sem`, `mob` FROM `users` WHERE `disabled`=0 ORDER BY `id` ASC "
            if limit !=0:
                query = query + " LIMIT "+str(start)+','+str(end)
            try:
                cursor.execute(query)
                rows = int(cursor.rowcount)

                print start, end, rows

                for x in range(0,rows):
                    i+=1
                    row = cursor.fetchone()
                    print i, x+1, row[0], row[1], row[2], row[3]
                    users.append(row[0], row[1], row[2], row[3])
                if i>=limit:
                   break;

                if rows<limit:
                    start = 0
                    end = limit-rows

            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit (1)
        return users, end


    def fetch_one(self, num = 0):
        print num
        cursor = self.db.cursor()
        query = "SELECT `username`, `passwd`, `sem`, `mob` FROM `users` WHERE `disabled`=0 ORDER BY `id` ASC "
        if num !=0:
                query = query + " LIMIT "+str(num)+',1'
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            # username, password, semester, mobile
            return row[0], row[1], row[2], row[3]
        except:
            return None


    def update_check(self, username, date):
        # Check whether there is an update after last access
        print "Update check : ",username, date
        cursor = self.db.cursor()
        query = "SELECT `mob` FROM `users` WHERE ( `last_update` < '"+date+"' OR  `last_update` IS NULL ) AND `username` = '"+username+"' LIMIT 1"
        try:
            cursor.execute(query)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        rows = int(cursor.rowcount)
        if rows > 0:
            return True
        else:
            print "No update"
            return False


    def update(self, username, date):
        # Update last access date in user account
        cursor = self.db.cursor()
        query = "UPDATE `users` SET `last_update`='"+date   +"' WHERE `username`='"+username+"' LIMIT 1"
        try:
            cursor.execute(query)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return
