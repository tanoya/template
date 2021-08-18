# coding:utf-8
import os
import re

DOC_MARK = "##doc##" # 文章主体替换标签
IMG_MARK = "##img##" # 图片替换表标签
LINK_MARK = "##link##" # 链接替换标签
ORAL_MARK = "##oral##" # 口播

IMG_SRC_PROPERTIES = "@@img_src@@" # 图片链接标签属性
LINK_IMG_SRC_PROPERTIES = "@@link_img_src@@" # 推广链接中的图片链接属性
LINK_HREF_PROPERTIES = "@@link_href@@" # 推广链接标签属性
LINK_DESC_PROPERTIES = "@@link_desc@@" # 推广链接描述
LINK_TITLE_PROPERTIES = "@@link_title@@" # 推广链接名称
ORAL_DESC_PROPERTIES = "@@oral_desc@@" # 口播描述
DATA_POSITION_PROPERTIES = "@@data_position@@" # 自增
DATA_ID_PROPERTIES = "@@data_id@@" # 估计目前用不到

# regular expression
IMG_SRC_PROPERTIES_REG = r'@@img_src[(](.*)[)]@@'
LINK_IMG_SRC_PROPERTIES_REG = r'@@link_img_src[(](.*)[)]@@'
LINK_HREF_PROPERTIES_REG = r'@@link_href[(](.*)[)]@@'
LINK_DESC_PROPERTIES_REG = r'@@link_desc[(](.*)[)]@@'
LINK_TITLE_PROPERTIES_REG = r'@@link_title[(](.*)[)]@@'
ORAL_DESC_PROPERTIES_REG = r'@@oral_desc[(](.*)[)]@@'
DATA_ID_PROPERTIES_REG = r'@@data_id[(](.*)[)]@@'

LINK_HREF_MAP = {
    0: "https://m.tk.cn/tkproperty/prd/S202006830/"
}

LINK_DESC_MAP = {
    0: "详情请看"
}

LINK_TITLE_MAP = {
    0: "重疾绿色通道，更快获得治疗的机会，赶快行动"
}

IMG_SRC_MAP = {
    0: "http://cms-bucket.ws.126.net/2021/0813/9ee24956p00qxrvzp000oc000dv007tc.png"
}

DATA_POSITION_LIST = ["201", "202", "203", "204", "205", "206", "207", "208", "209",
                        "210", "211", "212", "213", "214", "215", "216", "217", "218", "219"]

# Checker special will not add tag P
Checker = {
    DOC_MARK,
    IMG_MARK,
    LINK_MARK,
    ORAL_MARK,
    IMG_SRC_PROPERTIES,
    LINK_HREF_PROPERTIES,
    LINK_DESC_PROPERTIES,
    LINK_TITLE_PROPERTIES,
    DATA_POSITION_PROPERTIES, 
    DATA_ID_PROPERTIES,
    ORAL_DESC_PROPERTIES
}

ARCHITECTURE_DIR = "./architecture" # 模板路径

FILE_IN_DIR = "./text/doc_in"
FILE_OUT_DIR = "./text/doc_out"

def read_main():
    "读取整体框架"
    _path = ARCHITECTURE_DIR + "/" + "main.txt"
    with open(_path, "r") as f:
        _data = f.read()
        return _data

def read_img():
    "read img template"
    _path = os.path.join(ARCHITECTURE_DIR, "img.txt")
    with open(_path, "r", encoding='utf-8') as f:
        return f.read()

def read_link():
    "read link template"
    _path = os.path.join(ARCHITECTURE_DIR, "link.txt")
    with open(_path, "r", encoding='utf-8') as f:
        return f.read()

def read_oral():
    "read oral template"
    _path = os.path.join(ARCHITECTURE_DIR, "oral.txt")
    with open(_path, "r", encoding='utf-8') as f:
        return f.read()

def read_img_src(key):
    "read img src property"
    return IMG_SRC_MAP[key]

def read_link_href(key):
    "read link href property"
    return LINK_HREF_MAP[key]

def read_link_title(key):
    "read link title property"
    return LINK_TITLE_MAP[key]

def read_link_desc(key):
    "read link desc property"
    return LINK_DESC_MAP[key]

def read_keywords():
    "read keywords from file."
    _path = os.path.join("./text", "keywords.txt")
    _ret = []
    with open(_path, "r", encoding='utf-8') as f:
        _data = f.read()
        _ret = _data.split(",")
    return _ret

def find_keywords(content):
    "find whether is keyword in the content."
    _keywords = read_keywords()
    _ret = []
    for k in _keywords:
        if k in content:
            _ret.append(k)
    return _ret

def find_keywords_format(content):
    ks = find_keywords(content)
    _ret = ""
    if len(ks) > 0:
        for k in ks:
            _ret = _ret + k + ","
        _ret = _ret[:-1]
        return _ret
    return ""

def find_property_key(content):
    "find wich property key will be, default zero."
    return 0

def handle(src, template, target):
    "will modified the @src content, replace the @tmplate str to @target"
    if src == "":
        return ""
    return src.replace(template, target)

def handle_one_by_one(src, template, targets):
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

def read_content(file_name):
    _path = os.path.join(FILE_IN_DIR, file_name)
    with open(_path, "r", encoding='utf-8') as f:
        return f.read()

def write_content(file_name, content):
    _path = os.path.join(FILE_OUT_DIR, file_name)
    with open(_path, "w", encoding='utf-8') as f:
        f.write(content)

def is_mark(content):
    if content in Checker:
        return True
    if content.startswith("@@") and content.endswith("@@"):
        return True
    if content.startswith("<") and content.endswith(">"):
        return True
    return False

def preContent(content):
    if len(content) == 0:
        return ""
    _lines = content.split("。")
    _ret = ""
    for line in _lines:
        _in_lines = line.split("\n")
        for il in _in_lines:
            il = il.strip(' ')
            if il == '':
                continue
            if not is_mark(il) :
                if not il.endswith("？") and not il.endswith("。") and not il.endswith("：") and not il.endswith("，"):
                    il = il + "。"
                il = "<p>" + il + "</p>\n"
            else:
                il = il + "\n"
            _ret = _ret + il
    return _ret

def pipline(_content):
    "batch replace all the data."
    property_key = find_property_key(_content)
    if IMG_MARK in _content: ##img##
        _content = handle(_content, IMG_MARK, read_img())
    if LINK_MARK in _content: ##link##
        _content = handle(_content, LINK_MARK, read_link())
    if ORAL_MARK in _content: ##oral##
        _content = handle(_content, ORAL_MARK, read_oral())
    if IMG_SRC_PROPERTIES in _content: # properties
        _content = handle(_content, IMG_SRC_PROPERTIES, read_img_src(property_key))
    if LINK_HREF_PROPERTIES in _content:
        _content = handle(_content, LINK_HREF_PROPERTIES, read_link_href(property_key))
    if LINK_DESC_PROPERTIES in _content:
        _content = handle(_content, LINK_DESC_PROPERTIES, read_link_desc(property_key))
    if LINK_TITLE_PROPERTIES in _content:
        _content = handle(_content, LINK_TITLE_PROPERTIES, read_link_title(property_key))
    return _content

def indent(content):
    """
        delete multi \n char
    """
    ret = []
    l = len(content)
    i = 0
    for c in content:
        if c == '\n' and i + 1 < l and content[i+1] == '\n':
            i += 1
            continue
        else:
            ret.append(c)
            i += 1
    return ''.join(ret)
        

def pipline_one_by_one(content):
    "handle data one by one."
    _img_links = []
    _link_img_links = []
    _link_srcs = []
    _link_titles = []
    _link_descs = []
    _oral_descs = []
    _data_ids = []

    _il = re.findall(IMG_SRC_PROPERTIES_REG, content, re.M|re.I)
    if _il is not None and len(_il) > 0:
        _img_links = list(_il) # tuple -> list
        content = re.sub(IMG_SRC_PROPERTIES_REG, '' ,content)
    _ls = re.findall(LINK_HREF_PROPERTIES_REG, content, re.M|re.I)
    if _ls is not None and len(_ls) > 0:
        _link_srcs = list(_ls)
        content = re.sub(LINK_HREF_PROPERTIES_REG, '', content)
    _lt = re.findall(LINK_TITLE_PROPERTIES_REG, content, re.M|re.I)
    if _lt is not None and len(_lt) > 0:
        _link_titles = list(_lt)
        content = re.sub(LINK_TITLE_PROPERTIES_REG, '', content)
    _ld = re.findall(LINK_DESC_PROPERTIES_REG, content, re.M|re.I)
    if _ld is not None and len(_ld) > 0:
        _link_descs = list(_ld)
        content = re.sub(LINK_DESC_PROPERTIES_REG, '', content)
    _od = re.findall(ORAL_DESC_PROPERTIES_REG, content, re.M|re.I)
    if _od is not None and len(_od) > 0:
        _oral_descs = list(_od)
        content = re.sub(ORAL_DESC_PROPERTIES_REG, '', content)
    _di = re.findall(DATA_ID_PROPERTIES_REG, content, re.M|re.I)
    if _di is not None and len(_di) > 0:
        _data_ids = list(_di)
        content = re.sub(DATA_ID_PROPERTIES_REG, '', content)
    _lil = re.findall(LINK_IMG_SRC_PROPERTIES_REG, content, re.M|re.I)
    if _lil is not None and len(_lil) > 0:
        _link_img_links = list(_lil)
        content = re.sub(LINK_IMG_SRC_PROPERTIES_REG, '', content)
    content = indent(content) # delete multi \n character.

    if IMG_MARK in content: ##img##
        content = handle(content, IMG_MARK, read_img())
    if LINK_MARK in content: ##link##
        content = handle(content, LINK_MARK, read_link())
    if ORAL_MARK in content: ##oral##
        content = handle(content, ORAL_MARK, read_oral())
    if IMG_SRC_PROPERTIES in content: # properties
        content = handle_one_by_one(content, IMG_SRC_PROPERTIES, _img_links)
    if LINK_HREF_PROPERTIES in content:
        content = handle_one_by_one(content, LINK_HREF_PROPERTIES, _link_srcs)
    if LINK_DESC_PROPERTIES in content:
        content = handle_one_by_one(content, LINK_DESC_PROPERTIES, _link_descs)
    if LINK_TITLE_PROPERTIES in content:
        content = handle_one_by_one(content, LINK_TITLE_PROPERTIES, _link_titles)
    if LINK_IMG_SRC_PROPERTIES in content:
        content = handle_one_by_one(content, LINK_IMG_SRC_PROPERTIES, _link_img_links)
    if ORAL_DESC_PROPERTIES in content:
        content = handle_one_by_one(content, ORAL_DESC_PROPERTIES, _oral_descs)
    if DATA_POSITION_PROPERTIES in content:
        content = handle_one_by_one(content, DATA_POSITION_PROPERTIES, DATA_POSITION_LIST)
    if DATA_ID_PROPERTIES in content:
        content = handle_one_by_one(content, DATA_ID_PROPERTIES, _data_ids)
    return content

def run():
    _files = os.listdir(FILE_IN_DIR)
    if len(_files) == 0 :
        print("nothing to read.")
        return
    _body = read_main()
    if len(_body) == 0 :
        print("need main architecture.")
        return
    for _file in _files:
        _content = read_content(_file) # read file
        _content = preContent(_content) # add p tag <p></p>
        _content = handle(_body, DOC_MARK, _content) # replace ##doc##

        # _content = pipline(_content) # handle all the template.
        _content = pipline_one_by_one(_content)
        
        # keywords
        _header = find_keywords_format(_content)
        _content = _header + "\n\n" + _content
        write_content(_file, _content)

if __name__ == "__main__":
    print( "start..." )
    run()
    print( "end." )