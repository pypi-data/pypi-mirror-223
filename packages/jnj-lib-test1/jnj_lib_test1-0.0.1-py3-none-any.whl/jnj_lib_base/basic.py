"""
A library for Basic (Package Without Importing) Utility Functions

Conventions:

    FileTypes(Extensions)
    - srt:  SubRipText  동영상 자막용 데이터
    - tsv:  Tab-Separated Values  tab으로 분리된 테이블 형식 데이터
    - csv:  Comma-Separated Values  `comma`으로 분리된 테이블 형식 데이터

    DataTypes
    - s:  String  문자열
    - ss:  Array of String  문자열 배열
    - arr:  Array  1차원 배열
    - arrs:  Array of Array  2차원 배열(테이블 형식 데이터)
    - dic:  Dictionary  key: value 쌍으로 이루어진 데이터
    - dics:  Array of Dictionary  dict 배열
    - pair: [keys, vals]
    - pairs: [keys, valss], valss: array of vals
"""

# & test
"""
Ping(Test)
"""


def ping():
    """
    Returns 'pong'
    """
    return "pong"


# & Deal with DataType
def pop_dict(obj, key):
    """
    Pop Dict By Key

    :param obj: dict
    :param key: string

    :return: dict
    """
    val = obj[key]
    del obj[key]
    return val


# & Convert Format of String
def tsv_from_srt(s):
    """
    Convert SubRipText(`srt`) format string => Tab-Separated Values(`tsv`) format string

    :param s: string

    :return: string
    """
    return "\n".join(
        line.replace("\n", "\t").strip() for line in s.split("\n\n") if line
    )


def srt_from_tsv(s):
    """
    Convert Tab-Separated Values(`tsv`) => SubRipText(`srt`)

    :param str: string

    :return: string
    """
    return "\n\n".join(line.replace("\t", "\n") for line in s.split("\n"))


def arrs_from_csv(csv, sep=",", has_quote=True, newline="\n"):
    """
    Convert Comma-Separated Values(`csv`) => Array of Array(`arrs`)

    :param csv: string
    :param sep: string, default=','
    :param has_quote: bool
    :param newline: string

    :return: list[list]
    """
    arrs = []
    for line in csv.split(newline):
        if has_quote:
            arrs.append([s.strip() for s in line[1:-1].split(f'"{sep}"')])
        else:
            arrs.append([s.strip() for s in line.split(sep)])
    return arrs


def csv_from_arrs(arrs, sep=",", has_quote=True, newline="\n"):
    """
    Array of Array(`arrs`) => Convert Comma-Separated Values(`csv`)

    :param arrs: list[list]
    :param sep: string, default=','
    :param has_quote: bool
    :param newline: string

    :return: string
    """
    rows = []
    for arr in arrs:
        if has_quote:
            row = f'"{sep}"'.join(str(s) for s in arr)
            rows.append(f'"{row}"')
        else:
            rows.append(sep.join(str(s) for s in arr))
    return newline.join(rows)


def arr_from_arrs(arrs, index=0, has_header=False):
    """
    Returns arr From arrs (array of array).

    :param arrs: list[list]
    :param index: int, default=0
    :param has_header: bool, default=False

    :return: list
    """
    arr = [c[index] for c in arrs]
    return arr[1:] if has_header else arr


def arr_from_dicts(dics, key):
    """
    Arr From Dicts (Extract array By Key)

    :param dicts: list[dict]
    :param key: string

    :return: list
    """
    return [d[key] for d in dics]


def dict_from_pair(keys, vals):
    """
    Returns Dict (object) From Pair (Keys, Vals)

    :param keys: list
    :param vals: list

    :return: dict
    """
    return {k: v for k, v in zip(keys, vals)}


def dicts_from_pairs(keys, valss):
    """
    Returns Dicts (objects) From Pairs (Keys, Valss)

    :param keys: list
    :param valss: list[list]

    :return: list[dict]
    """
    return [dict(zip(keys, vals)) for vals in valss]


def arrs_from_dict(dic):
    """
    Arrs From Dict

    :param dct: dict

    :return: list[list]
    """
    if dic is None or not isinstance(dic, dict):
        return []
    keys = list(dic.keys())
    values = list(dic.values())
    return [keys, values]


def arrs_from_dicts(dics):
    """
    Arrs From Dicts

    :param dics: list[dict]

    :return: list[list]
    """
    arrs = []
    if dics is None or not isinstance(dics, list) or len(dics) == 0:
        return []
    keys = list(dics[0].keys())
    arrs.append(keys)
    for dct in dics:
        row = [dct[key] for key in keys]
        arrs.append(row)
    return arrs


def arrs_added_defaults(arrs, defaults={}, is_push=False):
    """
    Arrs Added Default Values

    :param arrs: list[list]
    :param defaults: dict, default={}
    :param is_push: bool, default=False

    :return: list[list]
    """
    add_keys = list(defaults.keys())
    add_vals = list(defaults.values())
    if is_push:
        return [
            arr + add_keys if i == 0 else arr + add_vals for i, arr in enumerate(arrs)
        ]
    else:
        return [
            add_keys + arr if i == 0 else add_vals + arr for i, arr in enumerate(arrs)
        ]


def convert_str(data, src_type, dst_type):
    """
    Main Converter

    :param data: string
    :param src_type: string
    :param dst_type: string

    :return: string
    """
    if src_type == "srt" and dst_type == "tsv":
        return tsv_from_srt(data)
    elif src_type == "tsv" and dst_type == "srt":
        return srt_from_tsv(data)


# & Dict, Dicts
def swap_dict(dic):
    """
    Swap Dict Key-Value

    :param dic: dict

    :return: dict
    """
    return {v: k for k, v in dic.items()}


def get_upsert_dicts(olds, news, keys):
    """
    Get Upsert Dicts

    :param olds: list[dict]
    :param news: list[dict]
    :param keys: list

    :return: dict
    """
    upserts = {"adds": [], "dels": [], "upds": []}
    for new_dict in news:
        matching_old_dict = next(
            (
                old_dict
                for old_dict in olds
                if all(new_dict[key] == old_dict[key] for key in keys)
            ),
            None,
        )
        if not matching_old_dict:
            upserts["adds"].append(new_dict)
        elif not all(
            new_dict[key] == matching_old_dict[key] for key in new_dict.keys()
        ):
            upserts["upds"].append(new_dict)

    for old_dict in olds:
        matching_new_dict = next(
            (
                new_dict
                for new_dict in news
                if all(old_dict[key] == new_dict[key] for key in keys)
            ),
            None,
        )
        if not matching_new_dict:
            upserts["dels"].append(old_dict)

    return upserts


def remove_dict_keys(dic, keys):
    """
    Remove Keys From Dict

    :param dic: dict
    :param keys: list

    :return: dict
    """
    return {k: v for k, v in dic.items() if k not in keys}
