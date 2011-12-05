DBHOST = "localhost"

DBPASS = "root"
DBUSER = "root"
DB = "dbname"


import MySQLdb

db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)

f = open('attendance-log.txt', 'r')

for line in f.readlines():
    a = line.split('DELETE')[1].split('\n')[0]
    account = a.split(' ')[0]
    password = account.split('.')[1]
    mob = a.split(' ')[1]

    cursor = db.cursor()
    cursor.execute("SELECT username, passwd FROM users WHERE `username`='"+account+"' AND `mob`='"+mob+"'")
    rows = int(cursor.rowcount)
    if rows > 0:
        continue

    cursor.execute("INSERT INTO `users` (`username` ,`passwd` , `mob`) VALUES ( '"+account+"', '"+password+"', '"+mob+"')")

    print account+'--'+password+'--'+mob
~                                                    
