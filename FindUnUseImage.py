# coding:utf-8
# 发现项目中未使用的图片资源文件
import os
import os.path
import sys
import getopt
import FindAllAPartFiles

findImageTypes = ['.png', '.jpg', '.jpeg']
exceptPathNames = ['.bundle', 'Assets.xcassets', 'Pods']


# 获取入参参数
def getInputParm():
    opts, args = getopt.getopt(sys.argv[1:], '-p:-t:', ['fromFilePath='])
    # 获取输入的参数
    for opt_name, opt_value in opts:
        if opt_name in ('-p', '--fromFilePath'):
            fromFilePath = opt_value

    if not os.path.exists(fromFilePath):
        print("\033[0;31;40m\t输入的压缩文件路径不存在\033[0m")
        exit(1)

    return fromFilePath


def findAllImages(fromFilePath):
    allImageNameList = []
    allImageFilePathList = []

    # 获取项目中，除了bundle和Assets.xcassets下面的图片
    # findImageTypes = ['.png', '.jpg', '.jpeg']
    # exceptPathNames = ['.bundle', 'Assets.xcassets', 'Pods']
    finalData = FindAllAPartFiles.checkFileInfo(findImageTypes, fromFilePath, exceptPathNames)

    # 处理数据源，将找到的图片名字存储起来
    for findType in findImageTypes:
        list = finalData[findType]
        for filePath in list:
            # filepath:文件路径，不包含文件名  tmpFileName:文件名，包含后缀名
            filepath, tmpFileName = os.path.split(filePath)
            # shotName:文件名，不包含扩展名.   extension:文件扩展名
            shotName, extension = os.path.splitext(tmpFileName)
            shotName = shotName.split("@")[0]
            allImageNameList.append(shotName)
            allImageFilePathList.append(filePath)

    for root, dirs, files in os.walk(fromFilePath):

        # 检测 Assets.xcassets 下的图片
        for fileName in dirs:
            if '.imageset' in fileName:
                shotName, extension = os.path.splitext(fileName)
                allImageNameList.append(shotName)
                allImageFilePathList.append(root + '/' + fileName)

    return allImageNameList, allImageFilePathList


def checkUnUseImage(fromFilePath, allImageNameList, allImageFilePathList):
    unUsedImageList = []
    index = 1
    for imageName in allImageNameList:
        # 去工程里面就去找吧
        isFinded = findStrAtFilePath(fromFilePath, imageName)
        if not isFinded:
            # 没有找到
            unUsedImageList.append(imageName)

        percent = index / len(allImageNameList)
        sys.stdout.write("\r# 共【%d 张】已分析完【%d 张】| 当前完成进度: %.1f %%" % (len(allImageNameList), index, percent * 100))
        sys.stdout.flush()
        index = index + 1

    return unUsedImageList


# 查找某个文件夹下面所有的文件中是否使用了image
def findStrAtFilePath(fromFilePath, imageName):
    # 去工程里面就去找吧
    for root, dirs, files in os.walk(fromFilePath):
        isFind = False
        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # print("--- " + os.path.join(root, name))
            # 获取文件名，扩展名
            fileName, fileSuffix = os.path.splitext(name)
            if fileSuffix == '.m' or fileSuffix == '.xib' or fileSuffix == '.storyboard' or fileSuffix == '.swift':
                tempStr = '\"' + imageName
                isFinded = findStrAtFileLine(root + '/' + name, tempStr)
                if isFinded:
                    # 如果找到了立即返回
                    return True

    return False


# 查找文件内容是否包含某个字符串
def findStrAtFileLine(filePath, findStr):
    # global _resNameMap
    file = open(filePath, 'r')
    isFind = False
    # print("findStr == " + findStr)
    # print("filePath == " + filePath)
    for line in file:
        # print(line)
        # exit(1)
        if findStr in line:
            isFind = True
            break
    file.close()
    return isFind


if __name__ == '__main__':
    # 获取入参
    fromFilePath = getInputParm()
    allImageNameList, allImageFilePathList = findAllImages(fromFilePath)

    # 开始搞事情
    unUsedImageList = checkUnUseImage(fromFilePath, allImageNameList, allImageFilePathList)

    print("\n\n共扫描项目中图片【%s】【%d张】<不包含%s> " % (', '.join(findImageTypes), len(allImageNameList), ', '.join(exceptPathNames)))
    print("\033[0;31;40m  扫描出【%d张】未使用图片，请在项目中再次验证  \033[0m" % len(unUsedImageList))

    index = 1
    for unUseImage in unUsedImageList:
        print("【%d】 - %s" % (index, unUseImage))
        index = index + 1
