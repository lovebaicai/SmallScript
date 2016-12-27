#-*- coding:utf-8 -*-

import xlwt
import MySQLdb as mdb
from datetime import datetime, timedelta


con = mdb.connect('localhost', 'root', 'ubuntu', 'spider', charset='utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")

tabname = 'sound_20161122'

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font

    return style

def write_excel(tabname):
    try:
        f = xlwt.Workbook() #创建工作簿
        sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True) #创建sheet
        row0 = [u'专辑名称',u'第一个免费节目播放量',u'第一个付费节目播放量']
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    except:
        pass

    i = 1
    sql2 = """select distinct Albumtitle from {}""".format(tabname)
    number = cur.execute(sql2)
    info = cur.fetchall()
    for title in info:
        sheet1.write(i, 0, title[0])
        #print title[0]
        try:
            sql = """select * from {} where (Albumtitle='{}' and isFree='True') limit 1""".format(tabname, title[0].encode('utf-8'))
            number = cur.execute(sql)
            info1 = cur.fetchone()
            sheet1.write(i, 1, info1[3])
        except:
            sheet1.write(i, 1, 0)

        try:
            sql1 = """select * from {} where (Albumtitle='{}' and isFree='False') limit 1""".format(tabname, title[0].encode('utf-8'))
            number1 = cur.execute(sql1)
            info2 = cur.fetchone()
            sheet1.write(i, 2, info2[3])
        except:
            sheet1.write(i, 2, 0)
        i += 1
        #print title[0] + 'write ok'

        f.save(str(tabname) + '.xls')


if __name__ == '__main__':
    for i in range(13):
        try:
            tabname = 'sound_' + (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
            write_excel(tabname)
        except:
            pass
        print '%s ok' % tabname
    print 'ok'




