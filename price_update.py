import json
import openpyxl
import os
from show_message import show_message  # 导入函数

def update_price_and_diff():
    file_path = "总表.xlsx"
    diff_record_file = "配置文件/priceDifferenceTable.json"
    diff_simple_file = "配置文件/差价表.json"
    price_record_file = "配置文件/fixedPriceTable.json"
    price_simple_file = "配置文件/价格表.json"
    mode_file = "配置文件/price_mode.json"
    default_mode = "价格"

    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb.worksheets[0]

    diff_result = {}
    diff_simple = {}
    price_result = {}
    price_simple = {}

    for row in sheet.iter_rows(min_row=9, values_only=True):
        store_name = row[3]
        aux_name = row[6]
        quantity = row[8]
        price = row[9]
        diff = row[16]

        try:
            if not store_name or not aux_name:
                continue
            quantity = float(quantity)
            price = float(price)
            diff = float(diff)
        except (TypeError, ValueError):
            continue

        price_result.setdefault(store_name, {}).setdefault(aux_name, {"记录": []})["记录"].append({
            "数量": quantity,
            "价格": price
        })
        price_result[store_name][aux_name]["推荐价格"] = price

        diff_result.setdefault(store_name, {}).setdefault(aux_name, {"记录": []})["记录"].append({
            "数量": quantity,
            "差价": diff
        })
        diff_result[store_name][aux_name]["推荐差价"] = diff

        price_simple.setdefault(store_name, {})[aux_name] = price
        diff_simple.setdefault(store_name, {})[aux_name] = diff

    with open(diff_record_file, "w", encoding="utf-8") as f:
        json.dump(diff_result, f, ensure_ascii=False, indent=4)
    with open(diff_simple_file, "w", encoding="utf-8") as f:
        json.dump(diff_simple, f, ensure_ascii=False, indent=4)
    with open(price_record_file, "w", encoding="utf-8") as f:
        json.dump(price_result, f, ensure_ascii=False, indent=4)
    with open(price_simple_file, "w", encoding="utf-8") as f:
        json.dump(price_simple, f, ensure_ascii=False, indent=4)

    base_source = price_simple
    if os.path.exists(mode_file):
        with open(mode_file, "r", encoding="utf-8") as f:
            mode_data = json.load(f)
    else:
        mode_data = {}

    for store_name, items in base_source.items():
        mode_data.setdefault(store_name, {})
        for aux_name in items:
            mode_data[store_name].setdefault(aux_name, default_mode)

    with open(mode_file, "w", encoding="utf-8") as f:
        json.dump(mode_data, f, ensure_ascii=False, indent=4)
    show_message(None, "提示", "差价与价格文件已保存，价格模式表已更新。")
    print("差价与价格文件已保存，价格模式表已更新。")


def load_json_and_print():
    try:
        with open("test我.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print(json.dumps(data, indent=4, ensure_ascii=False))
        show_message(None, "提示", "差价与价格文件已保存，价格模式表已更新。")
        print("差价与价格文件已保存，价格模式表已更新。")
    except Exception as e:
        print(f"读取失败：{e}")

