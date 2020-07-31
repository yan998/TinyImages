# coding:utf-8
# 查找某一类的文件

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
    fileNum = 0

    # 构建将要返回的数据源，这里使用Dictionary，分组返回
    finalData = {}
    for findTyte in findTypes:
        finalData[findTyte] = []

    for root, dirs, files in os.walk(fromFilePath):

        # 查找是否有相同的文件名比如 .bundle
        for fileName in dirs:
            filePath = root + '/' + fileName
            # 检查某个数组中的文件名是否包含于路径中
            isContinue = checkSomeFileNamesIsInPath(exceptPathNames, filePath)
            if isContinue:
                continue

            for willFindName in findTypes:
                if willFindName in fileName:
                    # 文件大小+文件路径拼接
                    finalStr = getFilePathSize(filePath) + filePath
                    finalData[willFindName].append(finalStr)
                    fileNum = fileNum + 1
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
                fileSize = os.path.getsize(filePath)

                finalStr = ("%dB*" % (fileSize)) + filePath
                finalData[fileSuffix].append(finalStr)
                fileNum = fileNum + 1

    return finalData


# 检查某个数组中的文件名是否包含于路径中
def checkSomeFileNamesIsInPath(exceptPathNames, filePath):
    # 判断查找的文件是否在将要过滤的文件中
    for exceptPathName in exceptPathNames:
        if exceptPathName + '/' in filePath:
            return True
            break
    return False


# 获取文件夹存储内容大小
def getFilePathSize(filePathStr):
    fileSize = 0
    for root, dirs, files in os.walk(filePathStr):
        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # 文件的路径
            filePath = root + '/' + name
            # 统计文件大小
            fileSize = fileSize + os.path.getsize(filePath)
    return ("%dB*" % (fileSize))


def bubbleSort(arr):
    for i in range(1, len(arr)):

        for j in range(0, len(arr) - i):

            findFilePathJ1 = arr[j]
            fileSizeIJ1 = int(findFilePathJ1.split("B*")[0])

            findFilePathJ2 = arr[j + 1]
            fileSizeJ2 = int(findFilePathJ2.split("B*")[0])

            if fileSizeIJ1 > fileSizeJ2:
                tempStr = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = tempStr
    return arr


def transformUnit(sizeStr):
    size = int(sizeStr)
    unit = "B"
    if (size > 1000):
        size = size / 1000
        unit = "KB"
        if size > 1000:
            size = size / 1000;
            unit = "M"

    return ('%d%s' % (size, unit))


if __name__ == '__main__':
    # 获取输入的参数
    findTypes, path, exceptPathNames = getInputParm()
    finalData = checkFileInfo(findTypes, path, exceptPathNames)

    print("\n\n当前路径 " + path + " 中，排除 " + ', '.join(exceptPathNames) + "\n找到文件 " + ', '.join(
        findTypes))

    for findType in findTypes:
        list = finalData[findType]
        print("\n\n发现 %s  %d个" % (findType, len(list)))
        list = bubbleSort(list)
        index = 1
        for findFilePath in list:
            # 对文件的大小进行加工
            strList = findFilePath.split("B*")
            sizeStr = transformUnit(strList[0])
            print("%d - %s %s" % (index, sizeStr, strList[1]))
            index = index + 1
