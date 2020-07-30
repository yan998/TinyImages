# coding:utf-8
# 图片批量压缩

import tinify
import os
import os.path
import shutil
import sys
import getopt
import FindAllImages


# 获取入参参数
def getInputParm():
    opts, args = getopt.getopt(sys.argv[1:], '-k:-f:-t:', ['key=', 'fromFilePath=', 'toFilePath:'])
    # 获取输入的参数
    for opt_name, opt_value in opts:
        if opt_name in ('-k', '--key'):
            tinifyKey = opt_value
        if opt_name in ('-f', '--fromFilePath'):
            fromFilePath = opt_value
        if opt_name in ('-t', '--toFilePath'):
            toFilePath = opt_value

    if len(tinifyKey) == 0 or len(fromFilePath) == 0 or len(toFilePath) == 0:
        print("\033[0;31;40m 请按照格式输入: python/python3 " + sys.argv[
            0] + " -k <tinifyKey>  -f<fromFilePath> -t<toFilePath>\033[0m")
        exit(1)

    if not os.path.exists(fromFilePath):
        print("\033[0;31;40m\t输入的压缩文件路径不存在\033[0m")
        exit(1)

    return tinifyKey, fromFilePath, toFilePath


# tinify.key = "jSrjT94QC4f4Sdqn0JFTrclj2tbXxWh3"
# fromFilePath = "/Users/a58/Desktop/Tools/TestFile"
# toFilePath = "/Users/a58/Desktop/Tools/FinalFile"


def compress(tinifyKey, fromFilePath, toFilePath, allFileNum):
    print("\n压缩中 ........")

    # 首先删除 toFilePath 文件下面的内容
    if os.path.exists(toFilePath):  # 如果文件存在
        shutil.rmtree(toFilePath)
        os.mkdir(toFilePath)

    pngSum = 0
    jpgSum = 0
    toFileSize = 0
    hasOperateNum = 0

    # 压缩图片的key
    tinify.key = tinifyKey

    for root, dirs, files in os.walk(fromFilePath):
        for name in files:
            # os.path.join路径拼接   os.path.join(root, name) 直接获取最里面一层文件
            # print("--- " + os.path.join(root, name))
            # 获取文件名，扩展名
            fileName, fileSuffix = os.path.splitext(name)
            # 最终要保存的目标路径构造   root[len(fromFilePath):]  获取的是当前路径下面的子路径
            toFullPath = toFilePath + root[len(fromFilePath):]
            # 最终要保存的文件全路径
            toFullName = toFullPath + '/' + name
            # 如果文件不存在就创建文件
            if not os.path.exists(toFullPath):
                os.makedirs(toFullPath)

            # 如果扩展名是 png 或者是 jpg 的 再去压缩，其他的不管
            if fileSuffix == '.png' or fileSuffix == '.jpg':
                # 使用 tinify 进行压缩和写入
                source = tinify.from_file(root + '/' + name)
                source.to_file(toFullName)

                # 统计文件大小
                toFileSize = toFileSize + os.path.getsize(toFullName)

                if fileSuffix == '.png':
                    pngSum = pngSum + 1;
                elif fileSuffix == '.jpg':
                    jpgSum = jpgSum + 1
            else:
                # 非  png 和 jpg的文件，原路拷贝回去
                shutil.copy2(root + '/' + name, toFullName)

                # if name != '.DS_Store' and fileSuffix != '.json':
                #     # 打印出当前是否有异常的文件

                # 统计文件大小
                toFileSize = toFileSize + os.path.getsize(toFullName)

            # 处理过的文件数量统计
            hasOperateNum = hasOperateNum + 1

            percent = hasOperateNum / allFileNum
            sys.stdout.write("\r# 已压缩png【%d 张】已压缩jpg【%d张】| 当前完成进度: %.1f %%" % (pngSum, jpgSum, percent * 100))
            sys.stdout.flush()

    return pngSum, jpgSum, toFileSize, hasOperateNum


# 打印最终的处理结果
def printOperateResult(oldPngSum, newPngSum, oldJpgSum, newJpgSum, fromFileSize, toFileSize, oldFileSum, newFileSum):
    print("\n\n压缩完成 ........")
    print("png图片：压缩前【%d 张】压缩后【%d 张】" % (oldPngSum, newPngSum))
    print("jpg图片：压缩前【%d 张】压缩后【%d 张】" % (oldJpgSum, newJpgSum))
    print("压缩前图片总数【%d 张】压缩后【%d 张】" % ((oldPngSum + oldJpgSum), (newPngSum + newJpgSum)))
    print("压缩前文件总数【%d 张】压缩后【%d 张】" % (oldFileSum, newFileSum))

    # 压缩前和压缩后的文件大小对比
    unit = 'KB'
    fromFileSize = fromFileSize / float(1000)
    toFileSize = toFileSize / float(1000)
    if fromFileSize > 1000:
        fromFileSize = fromFileSize / float(1000)
        toFileSize = toFileSize / float(1000)
        unit = 'M'

    print("压缩前大小【%.2f %s】,压缩后大小【%.2f %s】" % (fromFileSize, unit, toFileSize, unit))


if __name__ == '__main__':
    # 获取入参
    tinifyKey, fromFilePath, toFilePath = getInputParm();
    # 检测当前将要压缩的文件下文件基本情况
    map = FindAllImages.checkFile(fromFilePath)

    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    # 询问是否将要继续压缩
    inputStr = input("待压缩文件已检测完毕，是否继续下一步压缩操作（1/0）:")
    if inputStr != '1':
        exit(1)
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    # 开始压缩
    pngSum, jpgSum, toFileSize, fileSum = compress(tinifyKey, fromFilePath, toFilePath, map["allFileSum"])
    printOperateResult(map["pngSum"], pngSum, map["jpgSum"], jpgSum, map["fileSize"], toFileSize, map["allFileSum"],
                       fileSum)
