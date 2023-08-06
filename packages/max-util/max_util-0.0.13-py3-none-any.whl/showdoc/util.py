import os
from .entity import FileInfo
import zipfile

def create_dir(d: str):
    try:
        os.mkdir(d, 0x0777)
    except FileExistsError:
        Exception('d' + 'exist')


def create_file(title, content):
    # 打开文件
    fo = open(title, "w", encoding='utf8')
    fo.write(content)
    # 关闭文件
    fo.close()


def read_file(title):
    # 打开文件
    fo = open(title, "r", encoding='utf8')
    res = ''
    for line in fo.readlines():                          #依次读取每行
        res += line                          #去掉每行头尾空白
    fo.close()
    return res


def split_location(url: str, project: str):
    content = read_file(url)
    suffix = url[url.rindex('.')+1:]
    if project in url.split('\\'):
        loca = url[url.index(project) + len(project) + 1: url.index('.')]
        if loca.rfind('\\') == -1:
            title = loca
            dir = ''
        else:
            title = loca[loca.rindex('\\')+1:]
            dir = loca[0:loca.rindex('\\')]
    else:
        temp = url.split('\\')
        if len(temp) == 2:
            dir = ''
        else:
            dir = temp[len(temp) - 2]
        title = temp[len(temp) - 1].split('.')[0]

    return FileInfo(title, dir, content,suffix)

def create_zip(zipFilePath=None,srcPath=None,  includeDirInZip=True):
    if not zipFilePath:
        zipFilePath = srcPath + ".zip"
    parentDir, dirToZip = os.path.split(srcPath)

    # zipfile.write的第2个参数需要为相对路径，所以需要转换
    def trimPath(path):
        # 获取目录名称，前面带有\
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            # 去掉第一个字符
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return archivePath

    outFile = zipfile.ZipFile(zipFilePath, "w", compression=zipfile.ZIP_DEFLATED)

    if os.path.isdir(srcPath):
        # 目录的压缩包
        for (archiveDirPath, dirNames, fileNames) in os.walk(srcPath):
            for fileName in fileNames:
                filePath = os.path.join(archiveDirPath, fileName)
                # write的第2个参数需要为相对路径
                outFile.write(filePath, trimPath(filePath))
            # 包含空目录
            if not fileNames and not dirNames:
                zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
                outFile.writestr(zipInfo, "")
    else:
        # 文件的压缩包
        outFile.write(srcPath, trimPath(srcPath))
    outFile.close()
