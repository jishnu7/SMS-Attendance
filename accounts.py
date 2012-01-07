#!/usr/bin/python
'''
add accounts in format { class : '', username : '', password : '' }

'class' is used to import the message service provider class in the attendance program.
It must be the file name which contains functions to login and send sms.
The class file should contain 
    * __init_ function to initialise cookie
    * login function to do login and return true if login is success, else false.
    * send function to send given message to passed mobile number.
'''
ACCOUNTS = [
                {
                'class' : 'sample_sms_provider',
                'username' : 'test_user',
                'password' : 'test_password'
                },

                {
                'class' : 'fullonsms',
                'username' : ' ',
                'password' : ' '
                }
            ]
