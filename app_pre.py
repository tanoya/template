# coding:utf-8
import os
import re
import random

TYPE = 0 # 0：百万险 1：交通 2：财险 3：意外

FILE_PRE_DIR = "./text/doc_pre_in"
FILE_OUT_DIR = "./text/doc_pre_out"
ARCHITECTURE_DIR = "./architecture" # 模板路径

TEMPLATE_MARK = "##template##"
IMG_MARK = "##img##" # 图片替换表标签
TEMPLATE_MARK_STR = "##oral##\n@@oral_desc(@@ORAL_VALUE@@)@@\n##link##\n@@link_img_src(@@LINK_IMG_VALUE@@)@@\n@@link_href(@@LINK_HREF_VALUE@@)@@\n@@link_desc(@@LINK_DESC_VALUE@@)@@\n@@link_title(@@LINK_TITLE_VALUE@@)@@\n@@data_id(@@DATA_ID_VALUE@@)@@\n"

ORAL_VALUE = "@@ORAL_VALUE@@"
LINK_IMG_VALUE = "@@LINK_IMG_VALUE@@"
LINK_HREF_VALUE = "@@LINK_HREF_VALUE@@"
LINK_DESC_VALUE = "@@LINK_DESC_VALUE@@"
LINK_TITLE_VALUE = "@@LINK_TITLE_VALUE@@"
DATA_ID_VALUE = "@@DATA_ID_VALUE@@"

IMG_SRC_PROPERTIES = "@@img_src@@" # 图片链接标签属性

IMG_SRC_PROPERTIES_REG = r'@@img_src[(](.*)[)]@@'

def get_oral(t):
    if t == 0:
        return ORALS_0
    elif t == 1:
        return ORALS_1
    elif t == 2:
        return ORALS_2
    elif t == 3:
        return ORALS_3

ORALS_0 = [
    "HELLO, WORLD",
    "HELLO, CHINA"
]

ORALS_1 = [
    "HELLO, WORLD",
    "HELLO, CHINA"
]

ORALS_2 = [
    "HELLO, WORLD",
    "HELLO, CHINA"
]

ORALS_3 = [
    "HELLO, WORLD",
    "HELLO, CHINA"
]

def get_link_img(t):
    if t == 0:
        return LINK_IMGS_0
    elif t == 1:
        return LINK_IMGS_1
    elif t == 2:
        return LINK_IMGS_2
    elif t == 3:
        return LINK_IMGS_3

LINK_IMGS_0 = [
    "WWW.NETEASE.COM/IMG",
    "WWW.BAIDU.COM/IMG"
]

LINK_IMGS_1 = [
    "WWW.NETEASE.COM/IMG",
    "WWW.BAIDU.COM/IMG"
]

LINK_IMGS_2 = [
    "WWW.NETEASE.COM/IMG",
    "WWW.BAIDU.COM/IMG"
]

LINK_IMGS_3 = [
    "WWW.NETEASE.COM/IMG",
    "WWW.BAIDU.COM/IMG"
]

def get_link_href(t):
    if t == 0:
        return LINK_HREFS_0
    elif t == 1:
        return LINK_HREFS_1
    elif t == 2:
        return LINK_HREFS_2
    elif t == 3:
        return LINK_HREFS_3

LINK_HREFS_0 = [
    "WWW.NETEASE.COM/HREF",
    "WWW.BAIDU.COM/HREF"
]

LINK_HREFS_1 = [
    "WWW.NETEASE.COM/HREF",
    "WWW.BAIDU.COM/HREF"
]

LINK_HREFS_2 = [
    "WWW.NETEASE.COM/HREF",
    "WWW.BAIDU.COM/HREF"
]

LINK_HREFS_3 = [
    "WWW.NETEASE.COM/HREF",
    "WWW.BAIDU.COM/HREF"
]

def get_link_desc(t):
    if t == 0:
        return LINK_DESCS_0
    elif t == 1:
        return LINK_DESCS_1
    elif t == 2:
        return LINK_DESCS_2
    elif t == 3:
        return LINK_DESCS_3

LINK_DESCS_0 = [
    "WWW.NETEASE.COM/DESC",
    "WWW.BAIDU.COM/DESC"
]

LINK_DESCS_1 = [
    "WWW.NETEASE.COM/DESC",
    "WWW.BAIDU.COM/DESC"
]

LINK_DESCS_2 = [
    "WWW.NETEASE.COM/DESC",
    "WWW.BAIDU.COM/DESC"
]

LINK_DESCS_3 = [
    "WWW.NETEASE.COM/DESC",
    "WWW.BAIDU.COM/DESC"
]

def get_link_title(t):
    if t == 0:
        return LINK_TITLE_0
    elif t == 1:
        return LINK_TITLE_1
    elif t == 2:
        return LINK_TITLE_2
    elif t == 3:
        return LINK_TITLE_3

LINK_TITLE_0 = [
    "WWW.NETEASE.COM/TITLE",
    "WWW.BAIDU.COM/TITLE"
]

LINK_TITLE_1 = [
    "WWW.NETEASE.COM/TITLE",
    "WWW.BAIDU.COM/TITLE"
]

LINK_TITLE_2 = [
    "WWW.NETEASE.COM/TITLE",
    "WWW.BAIDU.COM/TITLE"
]

LINK_TITLE_3 = [
    "WWW.NETEASE.COM/TITLE",
    "WWW.BAIDU.COM/TITLE"
]

DATA_IDS = [
    "1",
    "2"
]

def randomValue(list):
    if len(list) == 0 :
        return 
    index = random.randint(0, len(list) - 1 )
    return list[index]

def handle_one_by_one(src, template, targets):
    "if targets has nothing, will use default value."
    "if targets is not enough, we will use laste one."
    if src == "" or template == "" or len(targets) == 0:
        print("no data we need to handle.")
        return src
    
    target = randomValue(targets)
    while template in src:
        src = src.replace(template, target, 1)
        if len(targets) > 0: # outof index.
            targets.remove(target)
        if len(targets) > 0:
            target = targets[0]
    return src

def handle_one_by_one_sort(src, template, targets):
    "if targets has nothing, will use default value."
    "if targets is not enough, we will use laste one."
    if src == "" or template == "" or len(targets) == 0:
        print("no data we need to handle.")
        return src
    
    target = targets[0]
    while template in src:
        src = src.replace(template, target, 1)
        if len(targets) > 0: # outof index.
            targets.remove(target)
        if len(targets) > 0:
            target = targets[0]
    return src

def handle(src, template, target):
    "will modified the @src content, replace the @tmplate str to @target"
    if src == "":
        return ""
    return src.replace(template, target)

def read_img():
    "read img template"
    _path = os.path.join(ARCHITECTURE_DIR, "img.txt")
    with open(_path, "r", encoding='utf-8') as f:
        return f.read()

def read_content(file_name):
    _path = os.path.join(FILE_PRE_DIR, file_name)
    with open(_path, "r", encoding='utf-8') as f:
        return f.read()

def write_content(file_name, content):
    _path = os.path.join(FILE_OUT_DIR, file_name)
    with open(_path, "w", encoding='utf-8') as f:
        f.write(content)

def replace_template(_content):
    if len(_content) == 0:
        return 
    return _content.replace(TEMPLATE_MARK, TEMPLATE_MARK_STR)

def pipline(_content):

    _img_links = []
    _il = re.findall(IMG_SRC_PROPERTIES_REG, _content, re.M|re.I)
    if _il is not None and len(_il) > 0:
        _img_links = list(_il) # tuple -> list
        _content = re.sub(IMG_SRC_PROPERTIES_REG, '' , _content)
    
    if IMG_MARK in _content: ##img##
        _content = handle(_content, IMG_MARK, read_img())

    if ORAL_VALUE in _content:
            _content = handle_one_by_one(_content, ORAL_VALUE, get_oral(TYPE))
    if LINK_IMG_VALUE in _content:
        _content = handle_one_by_one(_content, LINK_IMG_VALUE, get_link_img(TYPE))
    if LINK_HREF_VALUE in _content:
        _content = handle_one_by_one(_content, LINK_HREF_VALUE, get_link_href(TYPE))
    if LINK_DESC_VALUE in _content:
        _content = handle_one_by_one(_content, LINK_DESC_VALUE, get_link_desc(TYPE))
    if LINK_TITLE_VALUE in _content:
        _content = handle_one_by_one(_content, LINK_TITLE_VALUE, get_link_title(TYPE))
    if DATA_ID_VALUE in _content:
        _content = handle_one_by_one(_content, DATA_ID_VALUE, DATA_IDS)
    if IMG_SRC_PROPERTIES in _content: # properties
        _content = handle_one_by_one_sort(_content, IMG_SRC_PROPERTIES, _img_links)
    return _content

def run():
    _files = os.listdir(FILE_PRE_DIR)
    if len(_files) == 0 :
        print("nothing to read.")
        return
    for _file in _files:
        _content = read_content(_file)
        _content = replace_template(_content)

        _content = pipline(_content)

        write_content(_file, _content)

if __name__ == "__main__":
    print( "start..." )
    run()
    print( "end." )