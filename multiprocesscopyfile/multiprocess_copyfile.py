# coding:utf-8

from multiprocessing import Pool,Manager
import os

def CopyFile(oldPath,newPath,fileName,queue):
    fr = open(oldPath+'/'+fileName)
    fw = open(newPath+'/'+fileName,'w')

    # 当然如果是较大文件时，不要一次性读写
    content = fr.read()
    fw.write(content)

    fr.close()
    fw.close()

    queue.put(fileName)

def Main():
    oldPath = input('please input folder path：')
    newPath = oldPath+'-backups'
    os.makedirs(newPath)

    fileNames = os.listdir(oldPath)

    pool = Pool(5)
    queue = Manager().Queue()

    for name in fileNames:
        pool.apply_async(CopyFile,args=(oldPath,newPath,name,queue))

    num = 0
    allNum = len(fileNames)
    while num<allNum:
        queue.get()
        num += 1
        copyRate = num/allNum
        print('\r当前copy进度：%.2f%%'%(copyRate*100),end='')

    print('\n 已完成copy！')

if __name__ == '__main__':
    Main()