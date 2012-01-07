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

class sample_sms_provider():
    def __init__(self):
        # Set Cookie
        print "Setting cookie"


    def login(self, username, password):
        # Login
        print "Login : ", username, password
        # return false if login is incorrect
        return True


    # Function to send SMS
    def send(self, message, mobile_num) :
        # success message
        print "Send message :", mobile_num, message
        # return false if sending failed
        return True
