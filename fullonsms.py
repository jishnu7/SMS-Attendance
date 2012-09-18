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

import cookielib
import urllib
import urllib2
import re
from BeautifulSoup import BeautifulSoup


class fullonsms():
    def __init__(self):
        # Set Cookie for FullOnSMS and log in.
        sms_cookie = cookielib.CookieJar()
        self.sms_opener = urllib2.build_opener( \
                                urllib2.HTTPCookieProcessor(sms_cookie))
        self.sms_opener.addheaders.append(('User-agent', 'Mozilla/5.0'))

    def login(self, username, password):
        # Login
        print "----------------------\n" + \
              "Login : " + username + "\n"\
              "----------------------"

        sms_data = urllib.urlencode({
            'MobileNoLogin': username,
            'LoginPassword': password
            })
        sms_login = self.sms_opener.open('http://www.fullonsms.com/login.php', \
                                         sms_data)

        # Check Login is success or not.
        login_detail = BeautifulSoup(sms_login.read())
 
        try:
            if login_detail.script.contents[0] == \
                "window.location.href = 'http://www.fullonsms.com/action_main.php';":
                # Login success
                return True
        except:
            # Login Failed
            print "Login Failed"
        return False

    # Function to send SMS
    def send(self, message, mobile_num):
        sms_data = urllib.urlencode({
            'ActionScript': '/home.php',
            'CancelScript': '/home.php',
            'HtmlTemplate': '/var/www/html/fullonsms/StaticSpamWarning.html',
            'MessageLength': '140',
            'MobileNos': mobile_num,
            'SelGroup': "",
            'Message': message,
            "Gender": "0",
            "FriendName": "Your Friend Name",
            "ETemplatesId": "",
            "TabValue": "contacts",
            'IntSubmit': 'I agree - Send SMS'
            })
        sms_page = self.sms_opener.open('http://www.fullonsms.com/home.php', \
                                         sms_data)

        # To test whether message is sent or not
        success_page = self.sms_opener.open( \
                                       'http://www.fullonsms.com/MsgSent.php')
        success_page = BeautifulSoup(success_page)

        try:
            if success_page.find(text=re.compile("SMS Sent successfully")):
                # Success
                print "Message Sent!"
                return True
        except:
            # Message sent failed
            pass
        print "MESSAGE SENT FAILED!"
        return False
