import cookielib
import urllib2


class sample_sms_provider():
    def __init__(self):
        # Set Cookie
        sms_cookie = cookielib.CookieJar()
        self.sms_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(sms_cookie))
        self.sms_opener.addheaders.append(('User-agent', 'Mozilla/5.0')).

    def login(self, username, password):
        # Login
        print "Login : ", username, password

    # Function to send SMS
    def send(self, message, mobile_num) :
        # success message
        print "Send message :", mobile_num, message
