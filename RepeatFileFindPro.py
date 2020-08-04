# coding:utf-8

import os
import os.path
import sys
import getopt


# 获取入参参数
def getInputParm():
    opts, args = getopt.getopt(sys.argv[1:], '-f:-p:-e:', ['findTypes=', 'path=', 'exceptPathNames='])

    # 入参判断
    for opt_name, opt_value in opts:
        if opt_name in ('-f', '--findTypes'):
            # 查找文件类型
            findTypes = opt_value
        if opt_name in ('-p', '--path'):
            # 要检测的文件路径
            path = opt_value
        if opt_name in ('-e', '--exceptPathNames'):
            # 过滤的文件夹名称
            exceptPathNames = opt_value

    findTypeList = findTypes.split(",")
    exceptPathNameList = exceptPathNames.split(",")

    # for name in findTypeList:
    #     print('name = ' + name)
    #
    # for name in exceptPathNameList:
    #     print('exceptPathName = ' + name)
    #
    # print('path = ' + path)

    # 判断文件路径存不存在
    if not os.path.exists(path):
        print("\033[0;31;40m\t输入的文件路径不存在\033[0m")
        exit(1)

    return findTypeList, path, exceptPathNameList


# 检查文件相关信息
def checkFileInfo(findTypes, fromFilePath, exceptPathNames):
    returnFileNames = []
    returnFilePaths = []

    for root, dirs, files in os.walk(fromFilePath):

        # 查找是否有相同的文件名比如 .bundle
        for fileName in dirs:
            filePath = root + '/' + fileName
            # 检查某个数组中的文件名是否包含于路径中
            # isContinue = checkSomeFileNamesIsInPath(exceptPathNames, filePath)
            # if isContinue:
            #     continue

            for willFindName in findTypes:
                if willFindName in fileName:
                    # 文件名称和文件路径存储
                    returnFileNames.append(fileName)
                    returnFilePaths.append(filePath)
                    break

        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # print("--- " + os.path.join(root, name))
            # 获取文件名，扩展名
            fileName, fileSuffix = os.path.splitext(name)
            # print("=== %s" % (root + '/' + name))
            # 文件的路径
            filePath = root + '/' + name

            # 检查某个数组中的文件名是否包含于路径中
            isContinue = checkSomeFileNamesIsInPath(exceptPathNames, filePath)
            # 如果上面得出的结果是需要continue的，那么continue
            if isContinue:
                continue

            if fileSuffix in findTypes:
                # 找到相关的文件，进行统计
                filePath = root + '/' + name
                returnFileNames.append(name)
                returnFilePaths.append(filePath)

    return returnFileNames, returnFilePaths


# 检查某个数组中的文件名是否包含于路径中
def checkSomeFileNamesIsInPath(exceptPathNames, filePath):
    # 判断查找的文件是否在将要过滤的文件中
    for exceptPathName in exceptPathNames:
        if exceptPathName + '/' in filePath:
            return True
            break
    return False


if __name__ == '__main__':
    # 获取输入的参数
    findTypes, fromFilePath, exceptPathNames = getInputParm()
    returnFileNames, returnFilePaths = checkFileInfo(findTypes, fromFilePath, exceptPathNames)

    # 文件个数
    fileNumDic = {}
    # 文件路径
    filePathDic = {}
    for fileName, filePath in zip(returnFileNames, returnFilePaths):

        # 使用字典统计重复名字
        fileNum = 0
        filePaths = []
        if fileName in fileNumDic:
            fileNum = fileNumDic[fileName]
            filePaths = filePathDic[fileName]

        fileNum = fileNum + 1
        fileNumDic[fileName] = fileNum

        filePaths.append(filePath)
        filePathDic[fileName] = filePaths

    # 重复文件数量
    num = 0
    # 遍历map中文件数量大于2的，打印出来
    for fileName in fileNumDic:
        fileNum = fileNumDic[fileName]
        if fileNum > 1:
            print("\n 重复文件【%s】 重复数量-- 【%s个】" % (fileName, fileNum))
            filePaths = filePathDic[fileName]

            for filePath in filePaths:
                print(filePath)
                num = num + 1

    resultStr = "\n\n在路径 " + fromFilePath + " 中,排除文件夹类型【" + ', '.join(exceptPathNames) + "】 \n找到【" + ', '.join(
        findTypes) + "】类型的重复文件【%d】个" % num
    print("\033[0;31;40m   %s \033[0m" % resultStr)
