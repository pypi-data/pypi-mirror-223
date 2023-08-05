# -*- coding: utf-8 -*-
import re  # For regex(regular expression)
import json  # For json data/file
import configparser  # For .ini file

# from time import strftime


# ? String(search/replace/regex)
# ?-----------------------------------------------------------------------------
def replace_re(maps={}, s=""):
    """Replace by Regex
    :param maps: (dict, {}) 치환 패턴 목록  예) {r'\s*\n+\s*': ';', r';{2,}': ';'}
    :param s: (str, "") 치환 대상 문자열

    :return: 치환후 문자열
    :usages: replace_re(maps={r'\s*\n+\s*': ';', r';{2,}': ';'}, s=" \n\n abc;;;def")
      =>
    """
    for key, val in maps.items():
        s = re.sub(key, val, s)
    return s


def replace(maps, s):
    """문자열 치환
    _str: 대상 문자열
    _rep: 치환 규칙 dictionary {'A': 'a', 'r_(\d+)', '\1-'} / list [('A', 'a'), ('r_(\d+)', '\1-'), ...]
    """

    def _replace(p, r, s):
        (p, p_re) = (p[2:] if p[:2] == "r_" else p, p[:2] == "r_")
        s = re.sub(p, r, s) if p_re else s.replace(p, r)

    if type(maps) == dict:
        for p, r in maps.items():
            s = _replace(p, r, s)
    else:
        for p, r in maps:
            s = _replace(p, r, s)

    return s


def _insert_join(patterns=[], replacements=[], content=""):
    """
    content(문자열)에 포함된 patterns들을 replacements로 대체(replace(X) insert and join)
    NOTE: 속도(성능) 차이 분석
    content = "abcdefghijklmnopqrstuvwxyz"*10000
    patterns=['d', 'j', 'm', 'x']
    replacements=['D', 'J', 'M', 'X']
        insert_join time : 0.0003902912139892578
        replace time : 0.0005877017974853516
    """
    if len(patterns) == len(replacements):
        splits = []
        for pattern in patterns:
            (piece, content) = content.split(pattern, 1)
            splits.append(piece)
        splits.append(content)
    else:
        return None

    result = splits[0]
    for i, repl in enumerate(replacements):
        result = repl.join([result, splits[i + 1]])

    return result


def digit(s=""):
    """Convert String to Number(Remove char except digit(number, '.', ','))
    - s(str, ''): 추출 대상 문자열  예) "100,500.5원"
    """
    s = re.sub("[^\d.\-]", "", s)
    s = "0" if s == "" else s
    return float(s) if "." in s else int(s)


# ? Functions For File
# ?-----------------------------------------------------------------------------
def load_file(path, encoding="utf-8"):
    """Load File(Read File)"""
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def save_file(path, data, encoding="utf-8"):
    """Save File(Write File)"""
    with open(path, "w", encoding=encoding) as f:
        f.write(data)


def load_json(path, encoding="utf-8"):
    """Load Json File(Read Json File)"""
    with open(path, "r", encoding=encoding) as f:
        return json.load(f)


def save_json(path, data, encoding="utf-8"):
    """Save Data to Json File"""
    json.dump(data, open(path, "w", encoding=encoding), ensure_ascii=False, indent="\t")


def load_ini(path):
    """Load Ini File(Read Ini File)"""
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    return config


# & TODO: check
def save_ini(path, data):
    """Save Data to Ini File"""
    config = configparser.ConfigParser()
    config = data
    # 설정파일 저장
    with open(path, "w", encoding="utf-8") as f:
        config.write(f)


# def config_generator():
#     # 설정파일 만들기
#     config = configparser.ConfigParser()

#     # 설정파일 오브젝트 만들기
#     config["system"] = {}
#     config["system"]["title"] = "Neural Networks"
#     config["system"]["version"] = "1.2.42"
#     config["system"]["update"] = strftime("%Y-%m-%d %H:%M:%S")

#     config["video"] = {}
#     config["video"]["width"] = "640"
#     config["video"]["height"] = "480"
#     config["video"]["type"] = "avi"

#     # 설정파일 저장
#     with open("config.ini", "w", encoding="utf-8") as configfile:
#         config.write(configfile)
