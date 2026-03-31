import sys
import os
import json

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QLineEdit, QHBoxLayout, QButtonGroup
)
from PySide6.QtCore import QTimer

from ui_form import Ui_Widget
from price_update import update_price_and_diff, load_json_and_print
from show_message import show_message, BubbleToast
from input import json_inputs, update_price_mode
from fill import fill_excel_with_template
from compute import fill_prices_in_excel
import globals
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCompleter
from PySide6.QtGui import QIcon

# 主键 翻转
def invert_data(data: dict):
    result = {}
    for shop, items in data.items():
        for item, value in items.items():
            result.setdefault(item, {})[shop] = value
    return result


class ItemRowByShop(QWidget):
    def __init__(self, index, item_name, shop_name, parent=None,
                 default_option=None, default_val1="", default_val2=""):
        super().__init__(parent)
        self.toast = None # 我修改了这里
        self.index = index
        self.shop_name = shop_name
        self.item_name = item_name

        layout = QHBoxLayout(self)
        self.label = QLabel(shop_name) # 直接显示店名
        layout.addWidget(self.label)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.radio_price = QRadioButton("价格")
        self.label_price_suffix = QLabel("")
        layout.addWidget(self.radio_price)
        layout.addWidget(self.label_price_suffix)

        self.radio_diff = QRadioButton("差价")
        self.label_diff_suffix = QLabel("")
        layout.addWidget(self.radio_diff)
        layout.addWidget(self.label_diff_suffix)

        self.radio_fixed = QRadioButton("固定值")
        layout.addWidget(self.radio_fixed)
        self.le1 = QLineEdit()
        self.le1.setFixedWidth(60)
        layout.addWidget(self.le1)

        self.radio_fixed_diff = QRadioButton("固定差价")
        layout.addWidget(self.radio_fixed_diff)
        self.le2 = QLineEdit()
        self.le2.setFixedWidth(60)
        layout.addWidget(self.le2)

        self.btn_group.addButton(self.radio_price)
        self.btn_group.addButton(self.radio_diff)
        self.btn_group.addButton(self.radio_fixed)
        self.btn_group.addButton(self.radio_fixed_diff)

        if default_option:
            self.set_selected_option(default_option)
        self.set_value1(default_val1)
        self.set_value2(default_val2)

        # 监听单选框变化
        self.btn_group.buttonClicked.connect(self.on_option_changed)
        # 监听文本框变化（即时保存）
        self.le1.textChanged.connect(self.on_text_changed)
        self.le2.textChanged.connect(self.on_text_changed)

    def on_option_changed(self):
        from input import update_price_mode  # 避免循环导入
        opt = self.get_selected_option()
        if opt == "价格":
            update_price_mode(self.shop_name, self.item_name, "价格")
        elif opt == "差价":
            update_price_mode(self.shop_name, self.item_name, "差价")
        elif opt == "固定值":
            try:
                val = float(self.get_value1())
            except ValueError:
                val = self.get_value1()
            update_price_mode(self.shop_name, self.item_name, {"固定价格": val})
        elif opt == "固定差价":
            try:
                val = float(self.get_value2())
            except ValueError:
                val = self.get_value2()
            update_price_mode(self.shop_name, self.item_name, {"固定差价": val})

    def on_text_changed(self):
        """当输入框变化时，如果对应单选框被选中，就立即更新 JSON"""
        selected = self.get_selected_option()
        if selected == "固定值":
            self.on_option_changed()
        elif selected == "固定差价":
            self.on_option_changed()

    # --- 新增方法 ---
    def set_price_label_text(self, text):
        """设置价格单选框后面的额外标签文本（仅代码可改）"""
        self.label_price_suffix.setText(text)

    def set_diff_label_text(self, text):
        """设置差价单选框后面的额外标签文本（仅代码可改）"""
        self.label_diff_suffix.setText(text)

    # --- 原有方法 ---
    def get_selected_option(self):
        """获取当前选中的单选框的文本"""
        checked_button = self.btn_group.checkedButton()
        return checked_button.text() if checked_button else None

    def set_selected_option(self, option_text):
        """根据文本设置对应的单选框为选中状态"""
        for btn in self.btn_group.buttons():
            if btn.text() == option_text:
                btn.setChecked(True)
                return

    def get_value1(self):
        return self.le1.text()

    def set_value1(self, text):
        self.le1.setText(text)

    def get_value2(self):
        return self.le2.text()

    def set_value2(self, text):
        self.le2.setText(text)

    def get_values(self):
        return self.get_value1(), self.get_value2()


class ItemRow(QWidget):
    def __init__(self, index, shop_name, item_name, parent=None,
                 default_option=None, default_val1="", default_val2=""):
        super().__init__(parent)
        self.toast = None # 我修改了这里
        self.index = index
        self.shop_name = shop_name
        self.item_name = item_name

        layout = QHBoxLayout(self)
        self.label = QLabel(item_name)  # 直接显示菜名
        layout.addWidget(self.label)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.radio_price = QRadioButton("价格")
        self.label_price_suffix = QLabel("")
        layout.addWidget(self.radio_price)
        layout.addWidget(self.label_price_suffix)

        self.radio_diff = QRadioButton("差价")
        self.label_diff_suffix = QLabel("")
        layout.addWidget(self.radio_diff)
        layout.addWidget(self.label_diff_suffix)

        self.radio_fixed = QRadioButton("固定值")
        layout.addWidget(self.radio_fixed)
        self.le1 = QLineEdit()
        self.le1.setFixedWidth(60)
        layout.addWidget(self.le1)

        self.radio_fixed_diff = QRadioButton("固定差价")
        layout.addWidget(self.radio_fixed_diff)
        self.le2 = QLineEdit()
        self.le2.setFixedWidth(60)
        layout.addWidget(self.le2)

        self.btn_group.addButton(self.radio_price)
        self.btn_group.addButton(self.radio_diff)
        self.btn_group.addButton(self.radio_fixed)
        self.btn_group.addButton(self.radio_fixed_diff)

        if default_option:
            self.set_selected_option(default_option)
        self.set_value1(default_val1)
        self.set_value2(default_val2)

        # 监听单选框变化
        self.btn_group.buttonClicked.connect(self.on_option_changed)
        # 监听文本框变化（即时保存）
        self.le1.textChanged.connect(self.on_text_changed)
        self.le2.textChanged.connect(self.on_text_changed)

    def on_option_changed(self):
        from input import update_price_mode  # 避免循环导入
        opt = self.get_selected_option()
        if opt == "价格":
            update_price_mode(self.shop_name, self.item_name, "价格")
        elif opt == "差价":
            update_price_mode(self.shop_name, self.item_name, "差价")
        elif opt == "固定值":
            try:
                val = float(self.get_value1())
            except ValueError:
                val = self.get_value1()
            update_price_mode(self.shop_name, self.item_name, {"固定价格": val})
        elif opt == "固定差价":
            try:
                val = float(self.get_value2())
            except ValueError:
                val = self.get_value2()
            update_price_mode(self.shop_name, self.item_name, {"固定差价": val})

    def on_text_changed(self):
        """当输入框变化时，如果对应单选框被选中，就立即更新 JSON"""
        selected = self.get_selected_option()
        if selected == "固定值":
            self.on_option_changed()
        elif selected == "固定差价":
            self.on_option_changed()

    # --- 新增方法 ---
    def set_price_label_text(self, text):
        """设置价格单选框后面的额外标签文本（仅代码可改）"""
        self.label_price_suffix.setText(text)

    def set_diff_label_text(self, text):
        """设置差价单选框后面的额外标签文本（仅代码可改）"""
        self.label_diff_suffix.setText(text)

    # --- 原有方法 ---
    def get_selected_option(self):
        """获取当前选中的单选框的文本"""
        checked_button = self.btn_group.checkedButton()
        return checked_button.text() if checked_button else None

    def set_selected_option(self, option_text):
        """根据文本设置对应的单选框为选中状态"""
        for btn in self.btn_group.buttons():
            if btn.text() == option_text:
                btn.setChecked(True)
                return

    def get_value1(self):
        return self.le1.text()

    def set_value1(self, text):
        self.le1.setText(text)

    def get_value2(self):
        return self.le2.text()

    def set_value2(self, text):
        self.le2.setText(text)

    def get_values(self):
        return self.get_value1(), self.get_value2()


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.toast = None

        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollAreaWidgetContents.resize(540, 1000)
        layout = self.ui.scrollAreaWidgetContents.layout()
        self.rows = []
        # for i in range(20):
        #     row = ItemRow(i, "默认菜名", self.ui.scrollAreaWidgetContents, default_option="差价")

        #     layout.addWidget(row)
        #     self.rows.append(row)

        self.ui.pushButton_update.clicked.connect(self.on_update_clicked)
        self.ui.pushButton_update.setToolTip("根据同文件夹下 总表.xlsx 计算差价表与价格表，并更新price_mode")

        self.ui.pushButton_input.clicked.connect(self.on_input_clicked)

        self.ui.pushButton_fill.clicked.connect(self.on_fill_clicked)
        self.ui.pushButton_fill.setToolTip("根据同文件夹下 草稿.xlsx 与 模版.xlsx 生成填充后的模板填充表")
        self.ui.pushButton_compute.clicked.connect(self.on_compute_clicked)
        self.ui.pushButton_compute.setToolTip("根据配置文件下的数据与模板填充表 生成最终结果.xlsx")
        self.ui.pushButton_all.clicked.connect(self.on_all_clicked)
        # 监听变化
        self.ui.comboBox.currentIndexChanged.connect(self.on_shop_changed)
        self.ui.comboBox_2.currentIndexChanged.connect(self.on_item_changed)

        self.ui.comboBox_3.currentIndexChanged.connect(self.on_item3_changed)

    def show_toast(self, message, duration=2500):
        # 关闭之前的气泡（如果有）
        if self.toast is not None and self.toast.isVisible():
            self.toast.close()

        self.toast = BubbleToast(message, self, duration)
        self.toast.show_center(self)

    def on_update_clicked(self):
        try:
            update_price_and_diff()
            #self.show_toast("差价表与价格表重新计算完成")
            #show_message(None,"差价表与价格表重新计算完成")
        except Exception as e:
            print(f"出错了：{e}")

    def on_fill_clicked(self):
        fill_excel_with_template()
        self.show_toast("填充完成！")

    def on_compute_clicked(self):
        fill_prices_in_excel()
        self.show_toast("计算结果填入完成！")

    def on_all_clicked(self):
        fill_excel_with_template()
        fill_prices_in_excel()
        self.show_toast("数据填入完成！")



    def on_input_clicked(self):
        try:
            json_inputs()  # 会更新 globals 的变量

            item_names = list(globals.mode_by_item.keys())
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(item_names)
            self.ui.comboBox_2.setCurrentIndex(0)
            self.ui.comboBox_2.setEditable(True)
            completer2 = self.ui.comboBox_2.completer()
            completer2.setFilterMode(Qt.MatchContains)
            completer2.setCompletionMode(QCompleter.PopupCompletion)
            # 调整下拉列表大小
            self.ui.comboBox_2.view().setMinimumWidth(150)
            self.ui.comboBox_2.view().setMinimumHeight(400)

            shop_names = list(globals.price_mode.keys())
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(shop_names)
            self.ui.comboBox.setCurrentIndex(0)
            self.ui.comboBox.setEditable(True)
            completer1 = self.ui.comboBox.completer()
            completer1.setFilterMode(Qt.MatchContains)
            completer1.setCompletionMode(QCompleter.PopupCompletion)
            # 调整下拉列表大小
            self.ui.comboBox.view().setMinimumWidth(150)
            self.ui.comboBox.view().setMinimumHeight(300)

            self.ui.comboBox_3.clear()  # 先清空
            self.ui.comboBox_3.setEditable(True)
            completer3 = self.ui.comboBox_3.completer()
            completer3.setFilterMode(Qt.MatchContains)
            completer3.setCompletionMode(QCompleter.PopupCompletion)


        except Exception as e:
            print(f"出错了：{e}")

            # 在后面，这样后触发以商店优先的哦


        except Exception as e:
            print(f"出错了：{e}")
            self.show_toast("导入失败，请检查 JSON 文件")

    def rebuild_rows_for_item(self, item_name):
        layout = self.ui.scrollAreaWidgetContents.layout()
        # 清理旧行
        for row in self.rows:
            layout.removeWidget(row)
            row.setParent(None)
        self.rows.clear()

        idx = 0
        for shop_name, shop_data in globals.price_mode.items():
            if item_name not in shop_data:
                continue
            setting = shop_data[item_name]
            price_val = globals.price_table.get(shop_name, {}).get(item_name, "")
            diff_val = globals.diff_table.get(shop_name, {}).get(item_name, "")

            if isinstance(setting, str):
                row = ItemRowByShop(idx, item_name, shop_name,
                                    self.ui.scrollAreaWidgetContents,
                                    default_option=setting)
            elif isinstance(setting, dict):
                if "固定价格" in setting:
                    row = ItemRowByShop(idx, item_name, shop_name,
                                        self.ui.scrollAreaWidgetContents,
                                        default_option="固定值", default_val1=str(setting["固定价格"]))
                elif "固定差价" in setting:
                    row = ItemRowByShop(idx, item_name, shop_name,
                                        self.ui.scrollAreaWidgetContents,
                                        default_option="固定差价", default_val2=str(setting["固定差价"]))
                else:
                    continue
            else:
                continue

            row.set_price_label_text(f"￥{price_val}" if price_val != "" else "")
            row.set_diff_label_text(f"{diff_val}" if diff_val != "" else "")

            layout.addWidget(row)
            self.rows.append(row)
            idx += 1

    def rebuild_rows_for_shop(self, shop_name):
        if not globals.price_mode or shop_name not in globals.price_mode:
            print("找不到对应店铺数据")
            return

        layout = self.ui.scrollAreaWidgetContents.layout()
        for row in self.rows:
            layout.removeWidget(row)
            row.setParent(None)
        self.rows.clear()

        shop_data = globals.price_mode[shop_name]

        for i, (item_name, setting) in enumerate(shop_data.items()):
            price_val = globals.price_table.get(shop_name, {}).get(item_name, "")
            diff_val = globals.diff_table.get(shop_name, {}).get(item_name, "")

            if isinstance(setting, str):
                row = ItemRow(i, shop_name, item_name,
                              self.ui.scrollAreaWidgetContents,
                              default_option=setting)
            elif isinstance(setting, dict):
                if "固定价格" in setting:
                    row = ItemRow(i, shop_name, item_name,
                                  self.ui.scrollAreaWidgetContents,
                                  default_option="固定值", default_val1=str(setting["固定价格"]))
                elif "固定差价" in setting:
                    row = ItemRow(i, shop_name, item_name,
                                  self.ui.scrollAreaWidgetContents,
                                  default_option="固定差价", default_val2=str(setting["固定差价"]))
                else:
                    continue
            else:
                continue

            row.set_price_label_text(f"￥{price_val}" if price_val != "" else "")
            row.set_diff_label_text(f"{diff_val}" if diff_val != "" else "")

            layout.addWidget(row)
            self.rows.append(row)

    # 槽函数 用户在店铺名称的下拉框（comboBox）中选择了一个不同的店铺
    def on_shop_changed(self, index):
        shop_name = self.ui.comboBox.itemText(index)
        self.rebuild_rows_for_shop(shop_name)
        print(f"已加载店铺配置：{shop_name}")

        # 更新 comboBox_3 货物列表
        if shop_name in globals.price_mode:
            items = list(globals.price_mode[shop_name].keys())
        else:
            items = []

        self.ui.comboBox_3.blockSignals(True)  # 阻止信号，避免触发 on_item3_changed
        self.ui.comboBox_3.clear()
        self.ui.comboBox_3.addItem("")  # 默认空项
        self.ui.comboBox_3.addItems(items)
        self.ui.comboBox_3.setCurrentIndex(0)  # 默认选空
        self.ui.comboBox_3.blockSignals(False)

        # 刚选店铺时全部显示
        for row in self.rows:
            row.show()

    def on_item_changed(self, index):
        item_name = self.ui.comboBox_2.itemText(index)
        self.rebuild_rows_for_item(item_name)
        print(f"已加载菜品配置：{item_name}")

    def on_item3_changed(self, index):
        selected_item = self.ui.comboBox_3.currentText().strip()
        if selected_item == "":
            # 没选，显示全部
            for row in self.rows:
                row.show()
        else:
            # 只显示对应选中货物的行，隐藏其他
            for row in self.rows:
                if hasattr(row, 'item_name'):
                    if row.item_name == selected_item:
                        row.show()
                    else:
                        row.hide()

def resource_path(relative_path):
    """打包后和源码运行时都能找到资源"""
    if hasattr(sys, '_MEIPASS'):
        # 如果 sys 里有 _MEIPASS 属性，说明是 PyInstaller 打包运行
        # 返回临时目录里的文件路径
        return os.path.join(sys._MEIPASS, relative_path)
    # 否则是源码运行，直接返回当前目录下的文件路径
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyle('Fusion')  # 设置 Fusion 主题

    widget = Widget()
    widget.setWindowTitle("可爱萝卜价格配置系统")
    widget.setWindowIcon(QIcon(resource_path("萝卜.png")))
    widget.show()

    sys.exit(app.exec())


