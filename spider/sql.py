#!/usr/bin/env python
import logging
import MySQLdb as mdb


con = mdb.connect('localhost', 'root', 'ubuntu', 'sound', charset='utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")

sql = 'SELECT albumurl FROM albumbackup '
#sql2 = 'SELECT albumurl FROM allsound1 WHERE albumurl = (%s)'
albumnumber = cur.execute(sql)
info = cur.fetchall()
for url in info:
    args =  url[0]
#    print args

    sql1 = 'select sound_time from voice where albumurl= (%s)'
    sumtime = cur.execute(sql1, args)
    sumtimes = cur.fetchall()
    sumtime=0
    for sum in sumtimes:
        sumtime = sumtime + int(sum[0].encode('utf-8'))
    avgtime = sumtime/len(sumtimes)
    #sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
#    cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s", ("Guy de Maupasant", "4"))  

#UPDATE albumbackup set alltime='12345' where albumurl = 'http://www.ximalaya.com/1000324/album/3544633'
    cur.execute('update albumbackup set sumtime=%s where albumurl=%s', (sumtime, args))
    cur.execute('update albumbackup set avgtime=%s where albumurl=%s',  (avgtime, args))
    con.commit()
    print '%s write ok' % args 



cur.close()
con.commit()
con.close()
print 'all ok!!'
