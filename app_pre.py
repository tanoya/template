# coding:utf-8
import os
import re
import random

TYPE = 0 # 0：百万险 1：重疾险 2：交通意外 3：财产险

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
    "选择这款许多人都在用的百万医疗保险，解决您的后顾之忧",
    "面对花钱如流水的医院，我们应该早做准备;因此，为您推荐这款百万医疗保险，您的风险由保险来承担",
    "为您选择这款百万医疗保险，您的风险由保险来承担",
    "为你选择了这款百万医疗保险，百万治疗费用为您的健康保驾护航",
    "许多家庭难以承受高昂的检查费用，推荐这款许多人都在用的百万医疗保险，解决您的后顾之忧",
    "为了能够从容面对重大风险疾病，为大家推荐这款超值、超划算、许多人都在用的百万医疗险",
    "现在住院治疗的费用是特别昂贵的，因此为您推荐这款百万医疗险，你的治疗费用由保险来买单",
    "疾病不仅在折磨病人，也在折磨家人；为了减轻家庭经济负担，推荐这款百万医疗险，让生病的时候多一份从容",
    "为你选择了这款百万医疗保险，大病就医还有绿色通道","为你选择了这款百万医疗保险，质子重离子抗癌疗法也覆盖",
    "强烈推荐这款许多人都在用的百万医疗保险，解决您经济上的后顾之忧",
    "为你选择了这款百万医疗保险，可以垫付医院押金及医疗费",
    "住院治疗花费很大，推荐这款百万医疗险，让治疗更安心",
    "为你找到了这款百万医疗保险，让治疗费用不再困扰家庭",
    "为您选择了这款百万医疗保险，缴费少，保额高，不再担心治疗费用",
    "治疗很痛苦，就别再让治疗费用困扰您;为你选择了这款百万医疗保险，可以垫付医院押金及医疗费",
    "为你选择了这款百万医疗保险，“肿瘤特药”、“院外靶向药报销”也覆盖",
    "治疗癌症的费用是许多家庭都承担不起的，为大家选择这款百万医疗保险：",
    "发现癌症拿不出那么多现金怎么办？下面这款保险保障您",
    "推荐这款百万医疗保险，百万医疗为您的健康保驾护航",
    "为你选择了这款百万医疗保险，你的健康风险由保险来承担",
    "为你选择了这款百万医疗保险，重病风险由保险来承担",
    "疾病风险随时来临，要做好充分的准备，为您挑选了一份百万医疗保障",
    "防患于未然是生活之道，为了能够从容面对重大风险疾病，为大家推荐这款超值、超划算、许多人都在用的百万医疗保险：",
    "现在住院治疗的费用是特别昂贵的，因此为您推荐这款百万医疗险，你的治疗费用由保险来买单",
    "谁也不能保证自己和家人不会生病住院，做好预防措施，为您推荐这款更多人都加入的百万医疗险",
    "别让钱成为生死的决定因素；为您推荐这款许多人都在用的百万医疗保险",
    "面对花钱如流水的医院，我们应该早做准备；为您推荐这款百万医疗保险，您的风险由保险来承担",
    "生病别担心，百万医疗保险为您的家庭和人生保驾护航；为大家推荐这款百万医疗保险",
    "为了能够从容面对重大风险疾病，为大家推荐这款超值、超划算、许多人都在用的百万医疗险"
]

ORALS_1 = [
    "给大家特别推荐一下这款保障范围包括70种重大疾病的超值重疾险：",
    "给大家选择的这款覆盖范围包含70种重大疾病的重疾险，免费获取，可以放心领取",
    "为了从容面对重大风险疾病，为大家选择这款超值、超划算、许多人都在用的重疾险：",
    "疾病是超级危险的，因此为大家推荐保障范围包括70种重大疾病的超值重疾险",
    "重大疾病的治疗费用是许多家庭都承担不起的，因此为大家选择这款重疾险：",
    "癌症的监测现代医疗可以做到，但治疗它的费用确实许多家庭承担不起的，因此为大家选择这款重疾险：",
    "重大疾病不止会让我们承受巨大痛苦，而且会让一些家庭倾家荡产，给大家选择了一款超值、超划算的重疾险：",
    "癌症的医疗费用是许多家庭难以承受的；为大家选择这款免费重疾险，彻底解决后顾之忧：",
    "谁也不敢保证未来不患重大疾病；这份保障范围包括70种重大疾病的超值重疾险，可以解决你的后顾之忧",
    "我们一般认为按期检查既费钱又费时间，就会让重大疾病“钻空子”；为大家推荐这款免费的重疾险",
    "为大家推荐这款重疾险，让您的健康多一份保险：",
    "生活中疾病风险随时来临，我们要在健康时做好充分的准备，为您挑选了一份超值重疾险",
    "别让钱成为生死的决定因素；免费送你这款许多人都在用的重疾险",
    "疾病风险随时来临，要做好充分的准备，为您挑选了一份免费的重疾险",
    "为了能够从容面对重大风险疾病，为大家推荐这款免费、超划算、许多人都在用的重疾险",
    "住院治疗花费很大，推荐这款免费的重疾险，让治疗更安心",
    "强烈推荐这款许多人都在用的重疾险，不花钱，解决您未来的疾病风险",
    "面对花钱如流水的医院，我们应该早做准备；因此，为您推荐这款免费的重疾险，您的风险由保险来承担",
    "治疗很痛苦，就别再让治疗费用困扰您；为您准备好了免费的重疾险，提前为自己和家人找一个保障",
    "为您选择了这款重疾险，不花钱，保额高，不再担心治疗费用",
    "强烈推荐这款许多人都在用的重疾险，解决您经济上的后顾之忧，重点是投保全免费",
    "防患于未然是生活之道，为了能够从容面对重大风险疾病，为大家推荐这款超值、不花钱、许多人都在用的重疾险："
 
]

ORALS_2 = [
    "交通意外发生十分频繁，为您找到了这款免费的交通意外险，最高赔付100万",
    "出门在外，交通意外发生的概率是非常大的，为自己和家人免费领取这份交通意外险",
    "现在公路上各种车辆越来越多，交通事故极有可能发生，为您推荐这款交通意外险",
    "交通越来越便利，随之而来的是交通事故的高发，为您找到了这款免费的交通意外险",
    "意外事故带来的住院治疗费用是许多人无法承受的，为您推荐这款最高赔付100万的免费交通意外险",
    "谁也不能保证自己不会发生意外事故，为您推荐这款交通意外险，提前为自己保驾护航",
    "别等到发生交通意外才追悔莫及，这款最高赔付100万的交通意外险免费送给您",
    "交通意外已经成为中国人的主要杀手，因此特意为您找到这款免费的高额赔付的交通意外险"
]

ORALS_3 = [
    "给自己的财产加一份保障，为您准备了这份超值、许多人都在用的财产险",
    "在现在复杂的社会，我们的财产面临更大风险，为您推荐这款覆盖面超级广的财产险",
    "为您的支付宝、微信、银行卡加一个保障，免费赠送这款许多人都在用的财产险",
    "钓鱼链接、网络黑客、网络骗子不用怕，这款免费财产险为您保驾护航",
    "财产风险不要怕，为您推荐这款全年理赔不限次的财产险",
    "现在社会各种诈骗特别多，让这款免费的财产险来保护您的财产",
    "社会和网络上的财产诈骗特别多，你需要这款免费的财产险，最高赔付100万",
    "防止诈骗把我们辛辛苦苦赚的钱骗走，免费的财产险让你财产更加安全",
    "别等到财产失去才追悔莫及，为您找到了这款免费的财产险",
    "网络世界充满着危险，尤其是我们的财产；为您推荐这款最高赔付100万的财产险",
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
     "http://cms-bucket.ws.126.net/2021/0813/89ba1157j00qxrvzo0015c000k000b9c.jpg",
     "http://cms-bucket.ws.126.net/2021/0813/019cbb09p00qxrvzp001jc000e8005vc.png",
     "http://cms-bucket.ws.126.net/2021/0813/26191110p00qxrvzo000jc000df006rc.png"
]

LINK_IMGS_1 = [
    "http://cms-bucket.ws.126.net/2021/0813/9ee24956p00qxrvzp000oc000dv007tc.png",
    "http://cms-bucket.ws.126.net/2021/0813/7126757ep00qxrvzp002ec000ex00a4c.png"
]

LINK_IMGS_2 = [
    "http://cms-bucket.ws.126.net/2021/0813/aed78802p00qxrvzp001mc000cs008bc.png",
    "http://cms-bucket.ws.126.net/2021/0813/b8ef0964p00qxrvzo000mc000cs008bc.png"
]

LINK_IMGS_3 = [
    "http://cms-bucket.ws.126.net/2021/0813/9e562c26p00qxrvzp0011c000dq007rc.png",
    "http://cms-bucket.ws.126.net/2021/0813/407b9c4dp00qxrvzo000mc000c3008tc.png"
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
    "https://qingmang.abaobaoxian.com/health?version=1.3.002.01&utm_medium=wangyi&utm_source=wangyi&utm_campaign=message&utm_content=insurance&utm_term=article_wap_content_${data-position}_D"
]

LINK_HREFS_1 = [
   "https://qingmang.abaobaoxian.com/health?version=1.3.002.01&utm_medium=wangyi&utm_source=wangyi&utm_campaign=message&utm_content=insurance&utm_term=article_wap_content_${data-position}_D"
]

LINK_HREFS_2 = [
    "https://qingmang.abaobaoxian.com/health?version=1.3.002.01&utm_medium=wangyi&utm_source=wangyi&utm_campaign=message&utm_content=insurance&utm_term=article_wap_content_${data-position}_D"
]

LINK_HREFS_3 = [
     "https://qingmang.abaobaoxian.com/health?version=1.3.002.01&utm_medium=wangyi&utm_source=wangyi&utm_campaign=message&utm_content=insurance&utm_term=article_wap_content_${data-position}_D"
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
    "点击查看详情",
    "点击获取详细信息",
    "详情请查看",
    "点击免费获取"
]

LINK_DESCS_1 = [
   "点击查看详情",
    "点击获取详细信息",
    "详情请查看",
    "点击免费获取"
]

LINK_DESCS_2 = [
    "点击查看详情",
    "点击获取详细信息",
    "详情请查看",
    "点击免费获取"
]

LINK_DESCS_3 = [
   "点击查看详情",
    "点击获取详细信息",
    "详情请查看",
    "点击免费获取"
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
    "押金垫付，普通医疗保险的保费，高端医疗险的待遇",
    "保额300万，免赔额1万，赔偿比例100%，快来领",
    "重疾绿色通道，更快获得治疗的机会，赶快行动",
    "线上核保通过率高，生效快，快来加入",
    "更多人都在加入的百万医疗险，快来领",
    "覆盖百种特定疾病，赔偿比例100% ，快来加入",
    "院外靶向药，100%报销",
    "质子重离子医疗，100%报销"
]

LINK_TITLE_1 = [
    "限时赠送，尽快免费领取这份超值重疾险",
    "更多人使用的重疾险,快来免费加入",
    "包含70种重大疾病的超值保险，快来免费加入",
    "保障人群广，范围广，时间长的免费方案",
    "初次确诊，即一次性全额支付有效健康金，点击免费加入",
    "免费获取重疾险，让生活更加安心",
    "免费加入重疾险，省时省力省钱",
    "为大家的健康送福利，免费领取重疾保障",
    "符合条件，直接打钱，给付型保险，免费领取",
    "不用担心保费上涨，因为这里是免费的"
]

LINK_TITLE_2 = [
    "不止于便宜，免费领取交通意外险！",
    "保障全面，保障额度可到100万，快来免费领取",
    "动一下手指，换一份保障，点击链接免费领取交通意外险",
    "符合条件，直接打钱，给付型保险，免费领取",
    "不用担心，点击即免费获取超值交通意外险",
    "限时赠送，尽快免费领取",
    "免费领取，生效快，赔付高",
    "100万的最高赔付，请尽快免费获取"
]

LINK_TITLE_3 = [
    "限时赠送，尽快免费领取这份财产险",
    "账户安全保障，理赔不限次，免费领取",
    "账户安全保障 	，最高赔付100万 ，免费获取",
    "网银、银行卡、三方支付全覆盖，单账户保10万，免费领取",
    "免费送您财产险，最高赔付100万",
    "免费领：银行账户，微信、支付宝三方账户全保",
    "多次盗刷，可多次赔付限时，关键可以免费领取",
    "单张银行卡账户就能保10万，限时免费申请",
    "为大家的健康送福利，免费领取财产保障",
    "符合条件，直接打钱，给付型保险，免费领取",
    "不用担心保费上涨，因为这里是免费的"
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
    tt = targets[:]
    
    target = randomValue(tt)
    while template in src:
        src = src.replace(template, target, 1)
        if len(tt) > 0: # outof index.
            tt.remove(target)
        if len(tt) > 0:
            target = tt[0]
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