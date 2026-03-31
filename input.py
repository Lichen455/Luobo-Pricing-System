# This Python file uses the following encoding: utf-8

import json
import os
import globals
# 主键 翻转
def invert_data(data: dict):
    result = {}
    for shop, items in data.items():
        for item, value in items.items():
            result.setdefault(item, {})[shop] = value
    return result

def json_inputs():
    diff_path = os.path.join(os.getcwd(), "配置文件/差价表.json")
    price_path = os.path.join(os.getcwd(), "配置文件/价格表.json")
    mode_path = os.path.join(os.getcwd(), "配置文件/price_mode.json")

    with open(diff_path, 'r', encoding='utf-8') as f:
        globals.diff_table = json.load(f)

    with open(price_path, 'r', encoding='utf-8') as f:
        globals.price_table = json.load(f)

    with open(mode_path, 'r', encoding='utf-8') as f:
        globals.price_mode = json.load(f)



    globals.diff_by_item = invert_data(globals.diff_table)
    globals.price_by_item = invert_data(globals.price_table)
    globals.mode_by_item = invert_data(globals.price_mode)


    print("差价表：", globals.diff_by_item)
    print("价格表：", globals.price_by_item)
    print("价格模式表：", globals.mode_by_item)

    return globals.diff_table, globals.price_table, globals.price_mode

def update_price_mode(shop_name, item_name, new_value):
    if shop_name not in globals.price_mode:
        globals.price_mode[shop_name] = {}

    globals.price_mode[shop_name][item_name] = new_value

    mode_path = os.path.join(os.getcwd(), "配置文件/price_mode.json")
    with open(mode_path, 'w', encoding='utf-8') as f:
        json.dump(globals.price_mode, f, ensure_ascii=False, indent=2)

    print(f"[已更新] {shop_name} - {item_name} => {new_value}")
