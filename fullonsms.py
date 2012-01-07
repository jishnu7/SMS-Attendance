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
from BeautifulSoup import BeautifulSoup


class fullonsms():
    def __init__(self):
        # Set Cookie for FullOnSMS and log in.
        sms_cookie = cookielib.CookieJar()
        self.sms_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(sms_cookie))
        self.sms_opener.addheaders.append(('User-agent', 'Mozilla/5.0'))

    def login(self, username, password):
        # Login
        sms_login = self.sms_opener.open('http://www.fullonsms.com/CheckLogin.php?MobileNoLogin='+username+'&LoginPassword='+password)

        print "----------------------\n"+"Login : "+username+"\n----------------------"
        # Check Login is success or not.
        sms_login = BeautifulSoup(sms_login)
        redirect = sms_login.find('meta', {'http-equiv' : "Refresh"})
        try:
            if redirect['content'] != '5;URL= http://www.fullonsms.com/login.php':
                # Login success
                return True
        except:
            # Login Failed
            print "Login Failed"
        return False


    # Function to send SMS
    def send(self, message, mobile_num) :
        # success message, to check whether message is sent or not.
        MSG = { 'h1' : 'Hurray!!', 'div' : 'SMS sent successfully' }
        
        sms_data = urllib.urlencode({
                                        'ActionScript' : '/home.php',
                                        'CancelScript' : '/home.php',
                                        'HtmlTemplate' : '/var/www/html/fullonsms/StaticSpamWarning.html',
                                        'MessageLength': '140',
                                        'MobileNos' : mobile_num,
                                        'SelGroup' : "",
                                        'Message' : message,
                                        "Gender" : "0",
                                        "FriendName" : "Your Friend Name",
                                        "ETemplatesId" : "",
                                        "TabValue" : "contacts",
                                        'IntSubmit' : 'I agree - Send SMS'
                                    })
        sms_page = self.sms_opener.open('http://www.fullonsms.com/home.php',sms_data)

        # To test whether message is sent or not
        success_page = self.sms_opener.open('http://www.fullonsms.com/MsgSent.php')
        success_page = BeautifulSoup(success_page)
        success_page = success_page.find('div', {'class' : 'dhtmlgoodies', 'id' : 'div1'})

        try:
            # added 'or' intentionally, just incase they changed text
            if success_page.find('h1').contents[0].strip() == MSG['h1'] or success_page.find('div', 'lightbox_black_point').contents[0].strip() == MSG['div']:
                # Success
                print message
                return True
        except:
            # Message sent failed
            print "MESSAGE SENT FAILED!"
        return False
