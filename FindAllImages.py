# coding:utf-8

import os
import os.path
import shutil
import sys
import getopt

# 文件检测，白名单过滤。不在白名单目录中的文件路径将会被输出，被视为异常扩展名的文件
whiteSuffixList = ['.json']
# 文件名白名单
whiteFileNameList = ['.DS_Store']


# 获取入参参数
def getInputParm():
    opts, args = getopt.getopt(sys.argv[1:], '-f:', ['filePath='])
    # 入参判断
    for opt_name, opt_value in opts:
        if opt_name in ('-f', '--filePath'):
            return opt_value
        else:
            print("\033[0;31;40m 请按照格式输入: python/python3 " + sys.argv[0] + " -f <filePath> \033[0m")
            exit(1)


# 检查文件相关信息
def checkFileInfo(fromFilePath):
    pngSum = 0
    jpgSum = 0
    unusualSum = 0
    allFileSum = 0
    fileSize = 0
    jpgArray = []
    # 异常文件
    abnormalArray = []

    for root, dirs, files in os.walk(fromFilePath):
        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # print("--- " + os.path.join(root, name))
            # 获取文件名，扩展名
            fileName, fileSuffix = os.path.splitext(name)

            # 文件大小
            fileSize = fileSize + os.path.getsize(root + '/' + name)
            # 所有文件的数量
            allFileSum = allFileSum + 1
            # 如果扩展名是 png 或者是 jpg 的 再去压缩，其他的不管
            if fileSuffix == '.png':
                pngSum = pngSum + 1
            elif fileSuffix == '.jpg':
                jpgSum = jpgSum + 1
                jpgArray.append((root + '/' + name))
                # print("jpg图片路径： %s" % (root + '/' + name))
            else:
                # 非  png 和 jpg的文件
                if not (name in whiteFileNameList) and not (fileSuffix in whiteSuffixList):
                    # 打印出当前是否有异常的文件
                    unusualSum = unusualSum + 1
                    abnormalArray.append((root + '/' + name))

    print("检测到png图片：%d 张" % pngSum)
    print("检测到jpg图片：%d 张" % jpgSum)
    print("合计图片：%d 张" % (pngSum + jpgSum))
    print("所有文件数：%d 个" % allFileSum)

    return {"pngSum": pngSum, "jpgSum": jpgSum, "unusualSum": unusualSum, "allFileSum": allFileSum,
            "fileSize": fileSize, "jpgArray": jpgArray,
            "abnormalArray": abnormalArray}


# 打印相关信息
def printFileInfo(fileSize, jpgArray, abnormalArray):
    # 文件大小
    unit = 'KB'
    fileSize = fileSize / float(1000)
    if fileSize > 1000:
        fileSize = fileSize / float(1000)
        unit = 'M'
    print("当前文件大小：%.2f %s\n" % (fileSize, unit))
    if len(jpgArray) > 0:
        for filePath in jpgArray:
            print(filePath)
        print("\033[0;31;40m 建议将检测到的【%d】张jpg图片转化成png图片，因为打包的时候jpg会自动转化成png图片，导致包变大\n \033[0m" % len(jpgArray))
    if len(abnormalArray) > 0:
        for filePath in abnormalArray:
            print(filePath)
        print("\033[0;31;40m 发现异常文件类型【%d】个\n \033[0m" % len(abnormalArray))


def checkFile(fromFilePath):
    # 检测当前路径下文件的信息
    map = checkFileInfo(fromFilePath)
    printFileInfo(map["fileSize"], map["jpgArray"], map["abnormalArray"])
    return map


if __name__ == '__main__':
    # 获取输入的参数
    fromFilePath = getInputParm()
    # 检测当前路径下文件的信息
    checkFile(fromFilePath)
