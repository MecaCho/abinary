#-*- coding=UTF-8 -*-
import sys
import os
import sqlite3
import time
from functools import wraps
import unittest
import logging
import logging.config
import ConfigParser
import sqlite3
import chardet
from pyh import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def createlog(name=__name__,log_file_name = 'test.log',debug=[],info=[],warn= [],error= [],fetal=[]):
    try:
        if os.path.getsize(log_file_name) > 1000000:
            os.remove(log_file_name)
    except BaseException:
        print 'txt can not be deleted'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        # create a file handler
        handler = logging.FileHandler(log_file_name)
        handler.setLevel(logging.DEBUG)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(handler)
        ########################解决日志重复的问题logger.removeHandler(handler)
    if info:logger.info(info)
    if debug:logger.debug(debug)
    if warn:logger.warning(warn)
    if error:logger.error(error)
    if fetal:logger.fatal(fetal)
def getConfig(section,key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]+'/fx.conf'
    config.read(path)
    try:
        return config.get(section,key)
    except BaseException as errorMessage:
        createlog('__dbconnect_getConfig__',debug=[errorMessage])
        return
#dbpath = './db/DB_cmdFunction_Test.db'
dbpath = getConfig('database','dbpath')
cx = sqlite3.connect(dbpath)
cu = cx.cursor()
cx.text_factory = str
now = time.strftime("%Y-%m-%d-%H:%M:%S")

def fn_timer(function):
    @wraps(function)
    def function_timer(*args,**kwargs):
        starttime = time.time()
        functionResult = function(*args,**kwargs)
        endtime = time.time()
        lostTime = functionResult[-1]
        testTime = round(endtime-starttime,3)-float(str(lostTime))
        testTime = str(testTime)+'s'
        FunctionTestInfo = function.func_name + ' totalTime: '+testTime+' function lost Time: '+str(lostTime)
        createlog(log_file_name='test.log', info=[function.func_name,functionResult,testTime])
        insertResult('GUIFunctionTest', [function.func_name, '', '', '',testTime])
        #createlog(log_file_name='time.log',info=[function.func_name,testTime])
        fp = open('log.txt','a+')
        now = time.strftime('%Y-%m-%d--%H:%M:%S')
        fp.writelines(now + " ## ")
        fp.writelines(FunctionTestInfo)
        fp.write('\n')
        return testTime
    return function_timer

def deleteDB(DBtable):
    #######删除数据库表格
    cu.execute('drop table if exists '+ DBtable+';')
    createlog(name='__dbconnect__',warn=['Warning##drop a database Table :',DBtable])
def createDB(DBtable,*dbinfo):
    #######创建数据库结果表格
    print dbinfo
    temp = str(dbinfo)
    try:
        cu.execute('Create table if not exists '+ DBtable+' '+temp+';')
    except sqlite3.OperationalError as errorMessage:
        cu.execute("INSERT INTO " + DBtable + " VALUES('This','is','a','New','Test','null')")
        createlog(name='__createDB__',error=[errorMessage])
        createlog(name='__createDB__', info=['create a DB successfully: ',DBtable])
def insertResult(DBtable,info):
    try:
        now = time.strftime("%Y-%m-%d-%H:%M:%S")
        info.append(now)
        n = len(info)-1
        dbinfo = '('+'?'+ ',?'*n + ')'
        cmd1 = "INSERT into %s VALUES %s" % (DBtable,dbinfo)
        #########################windows系统下,如果不是读取文件，则注释掉以下两句################################################
        #print chardet.detect(info[0])['encoding']
        print type(info[0])
        if isinstance(info[0],str):
            info[0] = info[0].decode('gbk')
            info[1] = info[1].decode('gbk')
        cu.execute(cmd1,info)
        print 'DB info 中文 : ',info[0]
        cx.commit()
        #cx.close()
    except Exception as error_Message:
        createlog(name= '__insertResult__',error=['databaseError',error_Message])

def createHtmlfromDB(dbTable='cmd'):
    try:
        page = PyH('summaryReport page')
        # page.addCSS('myStylesheet1.css', 'myStylesheet2.css')
        # page.addJS('myJavascript1.js', 'myJavascript2.js')
        page << h1(dbTable + ' Result Report', cl='center')
        dbpath = getConfig('database', 'dbpath')
        cx = sqlite3.connect(dbpath)
        cu = cx.cursor()
        cu.execute('select * from ' + dbTable)
        tab = page << table(border="1", cellspacing='0', align='center', width='1200', bordercolor='Blue')
        trTemp = tab << tr(align='center', bordercolor='Blue', bgColor='#0099ff')
        trTemp << td('sysTime') + td('funcName')+td('filename') + td('filepath')+ td('outputFile') + td('softInfo') +td('Result')
        for file in cu.fetchall():
            print file
            trTemp1 = tab << tr(align='center', bordercolor='Blue')
            result = file[-2]
            errorInfo = file[1]+'_screenshot.png'
            print errorInfo
            print file[-4].split('/')
            if result != 'Success':
                createlog(name="createHTML", debug=['Result', result])
                result = '<a href="' + errorInfo + '">' + '<font color="#0000FF">' + result + '</font></a>'
                createlog(name="createHTML", debug=['Result', result])
            trTemp1 << td(file[-1]) + td(file[0]) + td(file[1]) + td(file[2]) + td(file[3])+td('null')+td(file[4])
        fp = 'DetailPage.html'
        page.printOut(file=fp)
    except Exception as error_Message:
        createlog(name='__createHTMLfromDB__', error=['create HTML error', error_Message])

def createHtml(reportname = 'function',filename='TestResultPage.html',*hinfo):
    page = PyH('summaryReport page')
    page << h1(reportname+' Result Report', align='center')

    p1 = p('Start Time : '+hinfo[0], align='center')
    p2 = p('Duration : '+hinfo[1],align='center')
    p3 = p('Status : ' + hinfo[2], align='center')
    page << p1+p2+p3
    page << p('Summary : ', style='color:red;', align='center') << a('Detail', href='DetailPage.html')

    fp = filename
    page.printOut(file=fp)
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', filename='', filepath=''):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.filename = filename
        self.filepath = filepath
        print "Parametrize_init_"

    @staticmethod
    def parametrize(testcase_klass, filename='', filepath=''):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, filename=filename, filepath=filepath))
        return suite
if __name__ == "__main__":
    createHtml('中文','中文测试.html','1','2','3')


