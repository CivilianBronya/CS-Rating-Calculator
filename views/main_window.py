from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QGroupBox,
                             QFormLayout, QDoubleSpinBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from models.rating_calculator import RatingCalculator


class MainWindow(QMainWindow):
    """主窗口视图"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS2 Rating 计算器 (专业版)")
        self.setFixedSize(600, 900)  # 稍微增大窗口以适应新控件
        self._init_ui()

    def _init_ui(self):
        """初始化用户界面"""
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self._create_method_selector()  # 添加计算方法选择
        self._create_input_group()
        self._create_calculate_button()
        self._create_result_group()
        self._create_about_button()

    def _create_method_selector(self):
        """创建计算方法选择区域"""
        method_group = QGroupBox("计算方法选择")
        method_layout = QHBoxLayout()

        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "综合评分 (三种算法平均)",
            "Rating 1.0 (基础算法)",
            "Rating 2.0 (HLTV算法)",
            "自定义算法"
        ])
        self.method_combo.setCurrentIndex(0)  # 默认选择综合评分

        method_layout.addWidget(QLabel("计算方法:"))
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()

        method_group.setLayout(method_layout)
        self.layout.addWidget(method_group)

    def _create_input_group(self):
        """创建输入区域"""
        self.input_group = QGroupBox("游戏数据输入")
        form_layout = QFormLayout()

        # 输入字段
        self.kills_input = QLineEdit()
        self.kills_input.setPlaceholderText("输入击杀数")
        self.kills_input.setValidator(QIntValidator(0, 999))

        self.deaths_input = QLineEdit()
        self.deaths_input.setPlaceholderText("输入死亡数")
        self.deaths_input.setValidator(QIntValidator(0, 999))

        self.assists_input = QLineEdit()
        self.assists_input.setPlaceholderText("输入助攻数")
        self.assists_input.setValidator(QIntValidator(0, 999))

        self.rounds_input = QLineEdit("16")
        self.rounds_input.setPlaceholderText("输入回合数")
        self.rounds_input.setValidator(QIntValidator(1, 999))

        self.mvps_input = QLineEdit()
        self.mvps_input.setPlaceholderText("输入MVP次数")
        self.mvps_input.setValidator(QIntValidator(0, 999))

        self.adr_input = QDoubleSpinBox()
        self.adr_input.setRange(0, 200)
        self.adr_input.setDecimals(1)
        self.adr_input.setValue(80.0)
        self.adr_input.setSuffix(" ADR")

        self.hs_input = QDoubleSpinBox()
        self.hs_input.setRange(0, 100)
        self.hs_input.setDecimals(1)
        self.hs_input.setValue(40.0)
        self.hs_input.setSuffix(" %")
        # 添加多杀输入
        self.kills_3k_input = QLineEdit("0")
        self.kills_3k_input.setPlaceholderText("3杀回合数")
        self.kills_3k_input.setValidator(QIntValidator(0, 999))

        self.kills_4k_input = QLineEdit("0")
        self.kills_4k_input.setPlaceholderText("4杀回合数")
        self.kills_4k_input.setValidator(QIntValidator(0, 999))

        self.kills_5k_input = QLineEdit("0")
        self.kills_5k_input.setPlaceholderText("5杀回合数")
        self.kills_5k_input.setValidator(QIntValidator(0, 999))

        # 添加RWS输入
        self.rws_input = QDoubleSpinBox()
        self.rws_input.setRange(0, 30)
        self.rws_input.setDecimals(1)
        self.rws_input.setSpecialValueText("无")  # 显示"无"当值为0
        self.rws_input.setSuffix(" RWS")

        # 添加到布局
        form_layout.addRow("击杀数 (K):", self.kills_input)
        form_layout.addRow("死亡数 (D):", self.deaths_input)
        form_layout.addRow("助攻数 (A):", self.assists_input)
        form_layout.addRow("回合数 (Rounds):", self.rounds_input)
        form_layout.addRow("MVP次数 (MVPs):", self.mvps_input)
        form_layout.addRow("平均每回合伤害 (ADR):", self.adr_input)
        form_layout.addRow("爆头率 (HS%):", self.hs_input)
        form_layout.addRow("3杀回合:", self.kills_3k_input)
        form_layout.addRow("4杀回合:", self.kills_4k_input)
        form_layout.addRow("5杀回合:", self.kills_5k_input)
        form_layout.addRow("回合胜利贡献:", self.rws_input)

        self.input_group.setLayout(form_layout)
        self.layout.addWidget(self.input_group)

    def _create_calculate_button(self):
        """创建计算按钮"""
        self.calculate_btn = QPushButton("计算 Rating")
        self.calculate_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        self.layout.addWidget(self.calculate_btn)

    def _create_result_group(self):
        """创建结果显示区域"""
        self.result_group = QGroupBox("计算结果")
        result_layout = QVBoxLayout()

        self.rating_label = QLabel("Rating: -")
        self.rating_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333;"
        )
        self.rating_label.setAlignment(Qt.AlignCenter)

        self.rating_desc = QLabel("")
        self.rating_desc.setStyleSheet("font-size: 16px; color: #666;")
        self.rating_desc.setAlignment(Qt.AlignCenter)

        self.detail_label = QLabel("等待计算...")
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("font-size: 14px;")

        result_layout.addWidget(self.rating_label)
        result_layout.addWidget(self.rating_desc)
        result_layout.addWidget(self.detail_label)
        self.result_group.setLayout(result_layout)

        self.layout.addWidget(self.result_group)

    def _create_about_button(self):
        """创建关于按钮"""
        self.about_btn = QPushButton("关于")
        self.about_btn.setStyleSheet(
            "background-color: #2196F3; color: white;"
        )
        self.layout.addWidget(self.about_btn)

    def get_input_values(self):
        """获取所有输入值，确保安全转换"""
        def safe_int(text, default=0):
            try:
                return int(text) if text else default
            except ValueError:
                return default

        def safe_float(text, default=0.0):
            try:
                return float(text) if text else default
            except ValueError:
                return default

        rws = self.rws_input.value()

        return {
            'kills': safe_int(self.kills_input.text()),
            'deaths': safe_int(self.deaths_input.text()),
            'assists': safe_int(self.assists_input.text()),
            'rounds': max(1, safe_int(self.rounds_input.text(), 16)),  # 确保至少1回合
            'mvps': safe_int(self.mvps_input.text()),
            'adr': self.adr_input.value(),
            'hs_percent': self.hs_input.value(),
            'kills_3k': safe_int(self.kills_3k_input.text()),
            'kills_4k': safe_int(self.kills_4k_input.text()),
            'kills_5k': safe_int(self.kills_5k_input.text()),
            'rws': rws if rws > 0 else None  # 0表示无RWS数据
        }

    def get_selected_method(self):
        """获取选择的计算方法"""
        return self.method_combo.currentText()

    def update_results(self, rating: float, details: str, method_name: str):
        """更新结果展示，显示使用的计算方法"""
        desc, color = RatingCalculator.get_rating_description(rating)

        self.rating_label.setText(f"{method_name}: {rating:.2f}")
        self.rating_desc.setText(desc)
        self.rating_desc.setStyleSheet(
            f"font-size: 16px; color: {color}; font-weight: bold;"
        )
        self.detail_label.setText(details)