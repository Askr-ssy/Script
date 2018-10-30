#!/usr/bin/env python3
import os
import re

def find_all_file(rootdir='', **kw):
    """
    遍历文件列表

    --
    :param rootpath: "THIS_FOLDER" 绝对路径,默认为文件当前路径

    :param suffix_filter: ['XLSX'] 文件后缀筛选,需要的文件后缀

    :param name_filter: [''] 文件名关键字筛选，含有关键字的文件不会被返回
    :returns: ["",""] 绝对文件路径
    """

    files_dir = os.listdir(rootdir)
    __files = []
    suffix_filter = kw['suffix_filter'] if 'suffix_filter' in kw.keys() else [
        'xls', 'xlsx', 'xlsm']
    name_fileter = kw['name_filter'] if 'name_filter' in kw.keys() else []
    for i in range(0, len(files_dir)):

        path = os.path.join(rootdir, files_dir[i])
        if os.path.isdir(path):
            __files.extend(find_all_file(path, suffix_filter=suffix_filter))
        if os.path.isfile(path):
            # 过滤文件名
            for each in name_fileter:
                if each in os.path.splitext(files_dir[i])[0]:
                    continue
            if os.path.splitext(path)[1][1:] in suffix_filter:
                # os.remove(path)
                if os.path.splitext(files_dir[i])[0].find('~') == 0:
                    continue
                __files.append(path)
    return __files

def isurl(url=None):
    """ 
    判断是否是url

    --
    :param url: None 默认为空

    :returns: Bool 是返回True,否者返回False
    """
    if url == None:
        return False
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配模式
    strs = re.findall(pattern, str(url))
    if strs:
        if url == strs[0]:
            return True
    else:
        return False
    pass

def cut_filename(path):
    """
    传入绝对路径文件名

    --

    :param path: str 绝对路径

    :returns: str 绝对路径

    :returns: str 文件名

    :returns: str 文件后缀
    """
    if not os.path.isfile(path):
        return ("not file")
    path = os.path.split(path)
    cut = os.path.splitext(path[1])
    return (path[0], cut[0], cut[1])

def html_filter(input_text):
    """
    过滤html标签
    
    --
    :param input_text: str 输入html文本

    :returns: str 去除html标签文本
    """
    return re.sub('<\/?[\s\S]*?(?:".*")*>','',input_text)

