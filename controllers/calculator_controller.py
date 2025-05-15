from PyQt5.QtWidgets import QMessageBox
from models.rating_calculator import RatingCalculator


class CalculatorController:
    """计算器控制器，处理业务逻辑"""

    def __init__(self, view):
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        """连接信号与槽"""
        self.view.calculate_btn.clicked.connect(self.calculate_rating)
        self.view.about_btn.clicked.connect(self.show_about)

    def calculate_rating(self):
        """处理Rating计算，增加错误处理"""
        try:
            inputs = self.view.get_input_values()

            # 调试打印，检查输入值
            print("Input values:", inputs)

            # 确保回合数有效
            if inputs['rounds'] <= 0:
                inputs['rounds'] = 1  # 设置为默认值

            # 计算Rating
            rating = RatingCalculator.calculate_rating(**inputs)

            # 准备详细数据
            details = self._prepare_details(inputs)

            # 更新视图
            self.view.update_results(rating, details)

        except Exception as e:
            QMessageBox.critical(
                self.view,
                "计算发生错误",
                f"发生意外错误:\n{str(e)}\n\n请检查输入值是否有效。"
            )
            # 打印完整错误信息以便调试
            import traceback
            traceback.print_exc()

    def _prepare_details(self, inputs: dict) -> str:
        """准备详细统计信息"""
        rounds = inputs['rounds']
        details = (
            f"详细统计:\n"
            f"KPR (每回合击杀): {inputs['kills'] / rounds:.2f}\n"
            f"DPR (每回合死亡): {inputs['deaths'] / rounds:.2f}\n"
            f"APR (每回合助攻): {inputs['assists'] / rounds:.2f}\n"
            f"ADR (平均伤害): {inputs['adr']:.1f}\n"
            f"爆头率: {inputs['hs_percent']:.1f}%\n"
            f"MVP率: {inputs['mvps'] / rounds:.2f}"
        )
        return details

    def show_about(self):   
        """显示关于信息"""
        about_text = (
            "CS2 Rating 计算器 专业版 v2.0\n\n"
            "基于改进的HLTV Rating 2.0算法\n"
            "Rating 解释:\n"
            "1.30+ → 超凡表现 (职业级)\n"
            "1.15-1.30 → 优秀表现\n"
            "1.00-1.15 → 良好表现\n"
            "0.85-1.00 → 平均水平\n"
            "<0.85 → 需要改进\n\n"
            "注意: 这不是官方工具，计算结果仅供参考。"
        )
        QMessageBox.about(self.view, "关于CS2 Rating计算器", about_text)