# coding:utf-8
# 发现项目中未使用的图片资源文件
import os
import os.path
import sys
import re
import getopt

exceptPathNames = []
# 获取入参参数
def getInputParm():
    opts, args = getopt.getopt(sys.argv[1:], '-p:-e:', ['filePath=', 'exceptPathNames='])
    # 获取输入的参数
    for opt_name, opt_value in opts:
        if opt_name in ('-p', '--filePath'):
            filePath = opt_value
        if opt_name in ('-e', '--exceptPathNames'):
            # 过滤的文件夹名称
            exceptPathNames = opt_value

    exceptPathNameList = exceptPathNames.split(",")

    if not os.path.exists(filePath):
        print("\033[0;31;40m\t输入的文件路径不存在\033[0m")
        exit(1)

    return filePath, exceptPathNameList


def findAllDefines(filePath):
    # 找到工程里所有的宏定义
    for root, dirs, files in os.walk(filePath):
        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # print("--- " + os.path.join(root, name))
            # 获取文件名，扩展名
            fileName, fileSuffix = os.path.splitext(name)
            if fileSuffix == '.m' or fileSuffix == '.h':
                isFinded = findDefineAtFileLine(root + '/' + name)
                if isFinded:
                    # 如果找到了立即返回
                    return True

    return False


def checkUnUseDefine(filePath, allDefineList):
    unUsedDefineList = []
    index = 1
    resultDic = {}
    for defineName in allDefineList:

        # 设置初始值
        if defineName not in resultDic:
            resultDic[defineName] = 0

        # 去工程里面就去找吧
        num = findStrAtFilePath(filePath, defineName)
        # 计数累加
        resultDic[defineName] = resultDic[defineName] + num

        percent = index / len(allDefineList)
        sys.stdout.write("\r# 共查找到【%d 个】宏定义，已分析完【%d 个】| 当前完成进度: %.1f %%" % (len(allDefineList), index, percent * 100))
        sys.stdout.flush()
        index = index + 1

    for key in resultDic:
        if resultDic[key] == 1:
            unUsedDefineList.append(key)
    return unUsedDefineList


# 查找某个文件夹下面所有的文件中是否使用了define
def findStrAtFilePath(filePath, defineName):

    useNnm = 0
    # 去工程里面就去找吧
    for root, dirs, files in os.walk(filePath):
        isFind = False
        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # print("--- " + os.path.join(root, name))
            # 获取文件名，扩展名
            fileName, fileSuffix = os.path.splitext(name)

            if fileSuffix == '.m' or fileSuffix == '.h':
                tempStr = defineName
                filePath = root + '/' + name
                if checkSomeFileNamesIsInPath(exceptPathNames, filePath) :
                    continue
                # 在当前文件中找到几个宏定义
                num = findStrAtFileLineShowNum(filePath, tempStr)
                useNnm = useNnm + num

    return useNnm


# 查找文件中的#define
def findDefineAtFileLine(filePath):
    re_define1 = re.compile('#define\s+([A-Za-z0-9]+\()')
    re_define2 = re.compile('#define\s+([A-Za-z0-9]+)\s')
    define_list = []
    for root, dirs, files in os.walk(filePath):
        isFind = False
        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # print("--- " + os.path.join(root, name))
            # 获取文件名，扩展名
            fileName, fileSuffix = os.path.splitext(name)
            if fileSuffix == '.m' or fileSuffix == '.h':
                filePath = root + '/' + name
                if checkSomeFileNamesIsInPath(exceptPathNames, filePath) :
                    continue
                file = open(filePath, 'r')
                for line in file:
                    result1 = re_define1.findall(line)
                    if result1:
                        define_list.append(result1[0])
                    result2 = re_define2.findall(line)
                    if result2:
                        define_list.append(result2[0])
                file.close()

    return define_list


# 查找文件内容中某个字符串出现的次数
def findStrAtFileLineShowNum(filePath, findStr):
    # global _resNameMap
    # 宏定义前后都不为字母或者数字
    rule1 = '\W('+findStr+')\W'
    rule2 = '^('+findStr+')\W'
    # 判断有木有左括号
    if '(' in findStr:
        findStr = findStr.replace('(', '')
        rule1 = '\W(' + findStr + '\()'
        rule2 = '^(' + findStr + '\()'

    re_define1 = re.compile(rule1)
    re_define2 = re.compile(rule2)
    file = open(filePath, 'r')
    result_num = 0
    for line in file:
        # print(line)
        # exit(1)
        result_list1 = re_define1.findall(line)
        if result_list1:
            result_num = result_num+len(result_list1)

        result_list2 = re_define2.findall(line)
        if result_list2:
            result_num = result_num + len(result_list2)

    file.close()

    return result_num

# 检查某个数组中的文件名是否包含于路径中
def checkSomeFileNamesIsInPath(exceptPathNames, filePath):
    # 判断查找的文件是否在将要过滤的文件中
    for exceptPathName in exceptPathNames:
        if exceptPathName + '/' in filePath:
            return True
            break
    return False


if __name__ == '__main__':
    # 获取入参
    filePath, exceptPathNames = getInputParm()
    define_list = findDefineAtFileLine(filePath)

    # 开始搞事情
    unUsedDefineList = checkUnUseDefine(filePath, define_list)

    print("\n\n共扫描项目中#define【%d个】 " % (len(define_list)))
    print("\033[0;31;40m  扫描出【%d个】未使用 #define，请在项目中再次验证  \033[0m" % len(unUsedDefineList))

    index = 1
    for unUseDefine in unUsedDefineList:
        print("【%d】 - %s" % (index,unUseDefine))
        index = index + 1
