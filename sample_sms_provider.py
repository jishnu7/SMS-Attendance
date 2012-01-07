#!/usr/bin/python

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
