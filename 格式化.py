# -*- coding: cp936 -*-
import re
import os

#格式化学号
def getMatchFromStu():
    if not os.path.exists('e:/UserFromSystem/'):
        os.mkdir(r'e:/UserFromSystem/')

    f = open("e:\\UserFromSystem\\1.html","r")
    fSave = open("e:\\UserFromSystem\\UserInfoAlpha.txt","w")
    #1M
    sizehint = 1024
    position = 0
    stuNumberPattern = re.compile(r'class=\"node_txt\" title="(.+?)@m.gduf.edu.cn">',re.S)
    stuNamePattern = re.compile(r'@m.gduf.edu.cn\">(.+?)</span>',re.S)
    while 1:
        lines = f.readlines(sizehint)
        if not lines:
            print '读取完毕'
            break
        for line in lines:
            stuNumber = re.findall(stuNumberPattern,line)
            stuName = re.findall(stuNamePattern,line)
            if not len(stuNumber)==len(stuName):
                print '解析出错'
                print len(stuNumber)
                print len(stuName)
                break
            for i in range(len(stuNumber)):
                fSave.write(stuNumber[i])
                fSave.write('    ')
                fSave.write(stuName[i])
                fSave.write('\n')
    print 'success'
    f.close()
    fSave.close()

#格式化班级号
def getMatchFromClass():
    if not os.path.exists('e:/UserFromSystem/'):
        os.mkdir(r'e:/UserFromSystem/')

    f = open("e:\\UserFromSystem\\2.html","r")
    fSave = open("e:\\UserFromSystem\\ClassInfo.txt","w")
    sizehint = 1024
    position = 0
    classNumberPattern = re.compile(r'<span class=\"node_txt\">(.+?)</span>',re.S)
    while 1:
        lines = f.readlines(sizehint)
        if not lines:
            print '读取完毕'
            break
        for line in lines:
            classNumber = re.findall(classNumberPattern,line)
            for i in range(len(classNumber)):
                fSave.write(classNumber[i])
                fSave.write('\n')
    print 'success'
    f.close()
    fSave.close()


if __name__ =="__main__":
    getMatchFromStu()
                
            

    

    
