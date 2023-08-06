from json import load as json_load
import importlib.resources
import time
import 结构解析

原始数据 = None
拆字 = None

def 初始化():
    global 拆字
    global 原始数据
    with importlib.resources.open_text('chinese_characters_words.数据', 'IDS-UCS-Basic.txt') as f:
        所有行 = f.read().split('\n')
        拆字 = {}
        for 行 in 所有行:
            字段 = 行.split('\t')
            # 待做：跳过了带 @apparent= 的部分
            if (len(字段) != 3):
                continue
            字 = 字段[1]
            信息 = 字段[2]
            if 信息 == 字:
                拆字[字] = {'字型': '独体', '部分': [信息]}
            else:
                try:
                    拆字[字] = 结构解析.结构数据解析(信息)
                except:
                    print(字)
                    拆字[字] = {'字型': 信息[0], '部分': 信息[1:]}

    with importlib.resources.open_text("chinese_characters_words.数据", "字典.json") as 文件:
        原始数据 = json_load(文件)

# API
def 查单字(字):
    if 原始数据 == None:
        初始化()
    for 字数据 in 原始数据:
        if 字 == 字数据['word']:
            信息 = {}
            信息['字'] = 字数据['word']
            信息['旧体'] = 字数据['oldword'] # 大多与现在相同
            信息['笔画数'] = 字数据['strokes']
            信息['拼音'] = 字数据['pinyin']
            信息['部首'] = 字数据['radicals']
            信息['释义'] = 字数据['explanation']
            信息['其他'] = 字数据['more']
            return 信息

# 待做：支持最小部分，而非直接部分。如查 五，得 语。
def 包含(部分):
    if 拆字 == None:
        初始化()

    所有字 = []
    for 字 in 拆字:
        if (拆字[字]['部分'].__contains__(部分)):
            所有字.append(字)
    return 所有字


def 左边(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 包含(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿰') and (拆字[字]['部分'][0] == 部分)):
            所有字.append(字)
    return 所有字


def 右边(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 包含(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿰') and (拆字[字]['部分'][1] == 部分)):
            所有字.append(字)
    return 所有字

# 待做：“上面是” 更可读
def 上面(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 包含(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿱') and (拆字[字]['部分'][0] == 部分)):
            所有字.append(字)
    return 所有字


def 下面(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 包含(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿱') and (拆字[字]['部分'][1] == 部分)):
            所有字.append(字)
    return 所有字

# 从结构到对应字 的反关系：从字到对应结构
def 的结构(字):
    if 拆字 == None:
        初始化()

    return 拆字[字]

# 待完善：
# U+4E9A	亚		@apparent=⿱一业

# print(的结构('叚'))  # 左边&CDP-8C7A，右边&CDP-8C79
# print(的结构('花'))
# print(的结构('日'))
# print(查单字('闇'))
# print(一个('音'))
# print(左边('甘'))
# print(右边('亘'))
# print(上面('口'))
# print(下面('天'))


# 𠤎 无拆字数据
def 的所有部分(字):
    if 拆字 == None:
        初始化()
    #拆字[字]
    所有部分 = set()
    #print(f"{字}的所有部分")

    结构 = None
    if type(字) == dict:
        结构 = 字
    else:
        if 字 in 拆字:
            结构 = 拆字[字]
        else:
            return [字]
 
    各部分 = 结构['部分']
    if 结构['字型'] == '独体':
        return 各部分
    else:
        #print(拆字[字])
        for 部分 in 各部分:
            所有部分.update(的所有部分(部分))
        return 所有部分


def 统计():
    print(的所有部分('语'))
    print(的所有部分('瑜'))
    print(的所有部分('卿'))
    print(的所有部分('覆'))
    所有字 = ''
    #for 笔画 in 字表:
    #    所有字 += 字表[笔画]
    for 字 in 拆字:
        所有字 += 字
    print(len(所有字))

    所有部分 = set()
    开始 = time.time()
    print(开始)
    for 字 in 所有字:
        所有部分.update(的所有部分(字))
    构件集 = set(所有部分)
    print(len(构件集))
    print(构件集)
    print(time.time() - 开始)

# 统计()
