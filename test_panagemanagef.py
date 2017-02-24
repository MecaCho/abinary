#-*-coding=UTF-8-*-
import time
import sys
import os
import subprocess
from dbconnect import *
from casestep import *
from addFile import allFile
def add(a='1', b='2'):
    print a + b
    return ['null','Success']

def run(func):
    dbpath = './db/DB_GUI_Test.db'
    cu = sqlite3.connect(dbpath)
    curs = cu.cursor()
    dir = os.getcwd()
    createlog(name='__main__', info=['Current path: ', dir])
    createDB('GUIFunctionTest1', 'input', 'output', 'Result', 'sysTime')
    curs.execute("select * from ofdFiles where id<3")
    for file in curs.fetchall():
        print file
        print func.__name__
        func(file[2],file[1])
##################################################从ofdFiles数据库读取数据，执行cases，将结果写入结果数据库，并生成html##################################
class runcase(object):
    def __init__(self,func,resultDB='GUItest',resultHtml='Detail.html'):
        self.func = func
        self.resultDB = resultDB
        self.resultHtml = resultHtml
        self.funcname = self.func.__name__
    def run(self):
        startTime = time.time()
        total = 0
        totalPass = 0
        dbpath = './db/DB_GUI_Test.db'
        cu = sqlite3.connect(dbpath)
        curs = cu.cursor()
        dir = os.getcwd()
        createlog(name='__main__', info=['Current path: ', dir])
        deleteDB(self.resultDB)
        createDB(self.resultDB,'funcname', 'filename','filepath', 'output', 'Result', 'sysTime')
        curs.execute("select * from ofdFiles where id<3")
        for file in curs.fetchall():
            total += 1
            print file
            print self.func.__name__
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            ResultInfo = self.func(file[2],file[1])
            if ResultInfo[-1] == 'Success':
                totalPass += 1
            dbinfo = [self.funcname,file[1],file[2]]
            dbinfo = dbinfo+ResultInfo
            createlog(name='dbinfo',debug=['dbinfo : ',dbinfo])
            insertResult(self.resultDB,dbinfo)
        summaryResult = 'Total:' + str(total) + '  Pass:' + str(totalPass)
        duration = time.time() - startTime
        createHtmlfromDB(self.resultDB)
        createHtml(self.funcname, self.resultHtml, str(now), str(duration), summaryResult)
def test_insertBlankPage(filepath='',filename=''):
    ###################,local='',pageSize='',pageNum=''
    filename = filename
    filepath = filepath
    if openfile(filepath,filename) == 'Success':
        ########pageManage and insert Blank Page
        try:
            os.system('xdotool key alt')
            time.sleep(1)
            os.system('xdotool key o')
            time.sleep(1)
            os.system('xdotool key i')
            time.sleep(1)
            os.system('xdotool key b')
            time.sleep(1)
            os.system('xdotool getactivewindow')
            os.system('xdotool key alt+o')
            outputFilePath = saveas(filename, function='insertBlankPage')
            sleep(1)
            os.system('xdotool key ctrl+q')
            closeFile()
            createlog(name='__insertBlankPage__', debug=[filename, outputFilePath])
            lostTime = 5 + 4.036 + 0.072
            result = 'Success'
            return [outputFilePath,result]
        except BaseException as errorMessage:
            createlog(name='__insertBlankPage__',error=[errorMessage,'line:81'])
            return ['null','Error']
    return ['null','OpenFileError']

if __name__ =='__main__':
    #test_insertBlankPage('/mnt/Ubuntu_Share/GitLab_Linux_Workspace/GUI_linux/testofd/saveas.ofd','saveas.ofd')
    try:
        op = sys.argv[1]
    except BaseException as e:
        op = ''
        createlog(name='__', info=['python shell argvs : ', op, e])
    if op == 'insert':
        case = runcase(test_insertBlankPage,resultDB='insertBlankPage',resultHtml='insertBlankPage.html')
        case.run()
        #run(test_insertBlankPage)



