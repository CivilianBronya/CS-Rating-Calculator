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
        """根据选择的方法计算Rating"""
        try:
            inputs = self.view.get_input_values()
            method = self.view.get_selected_method()

            # 验证输入
            if inputs['rounds'] <= 0:
                raise ValueError("回合数必须大于0")

            # 准备基础参数
            base_params = {
                'kills': inputs['kills'],
                'deaths': inputs['deaths'],
                'assists': inputs['assists'],
                'rounds': inputs['rounds'],
                'mvps': inputs['mvps'],
                'adr': inputs['adr'],
                'hs_percent': inputs['hs_percent'],
                'kills_3k': inputs['kills_3k'],
                'kills_4k': inputs['kills_4k'],
                'kills_5k': inputs['kills_5k'],
                'rws': inputs['rws']
            }

            # 根据选择的方法计算
            if method == "综合评分 (三种算法平均)":
                rating = self._calculate_composite_rating(inputs)
                details = self.prepare_all_details(inputs)
            elif method == "Rating 1.0 (基础算法)":
                rating = RatingCalculator.calculate_rating_1_0(
                    inputs['kills'],
                    inputs['deaths'],
                    inputs['rounds'],
                    inputs['kills_3k'],
                    inputs['kills_4k'],
                    inputs['kills_5k']
                )
                details = self.prepare_rating1_details(inputs)
            elif method == "Rating 2.0 (HLTV算法)":
                rating = RatingCalculator.calculate_rating_2_0(
                    kills=inputs['kills'],
                    deaths=inputs['deaths'],
                    assists=inputs['assists'],
                    rounds=inputs['rounds'],
                    adr=inputs['adr'],
                    kills_3k=inputs['kills_3k'],
                    kills_4k=inputs['kills_4k'],
                    kills_5k=inputs['kills_5k']
                )
                details = self.prepare_rating2_details(inputs)
            else:  # 自定义算法
                rating = RatingCalculator.calculate_custom_rating(**base_params)
                details = self.prepare_custom_details(inputs)

            # 更新视图
            self.view.update_results(rating, details, method)

        except Exception as e:
            QMessageBox.warning(self.view, "输入错误", str(e))
            import traceback
            traceback.print_exc()

    def _calculate_composite_rating(self, inputs: dict) -> float:
        """计算综合评分"""
        rating1 = RatingCalculator.calculate_rating_1_0(
            inputs['kills'],
            inputs['deaths'],
            inputs['rounds'],
            inputs['kills_3k'],
            inputs['kills_4k'],
            inputs['kills_5k']
        )

        rating2 = RatingCalculator.calculate_rating_2_0(
            kills=inputs['kills'],
            deaths=inputs['deaths'],
            assists=inputs['assists'],
            rounds=inputs['rounds'],
            adr=inputs['adr'],
            kills_3k=inputs['kills_3k'],
            kills_4k=inputs['kills_4k'],
            kills_5k=inputs['kills_5k']
        )

        custom = RatingCalculator.calculate_custom_rating(
            kills=inputs['kills'],
            deaths=inputs['deaths'],
            assists=inputs['assists'],
            rounds=inputs['rounds'],
            mvps=inputs['mvps'],
            adr=inputs['adr'],
            hs_percent=inputs['hs_percent'],
            rws=inputs['rws']
        )

        return (rating1 + rating2 + custom) / 3

    def prepare_all_details(self, inputs: dict) -> str:
        """准备综合评分的详细数据"""
        rounds = inputs['rounds']
        rating1 = RatingCalculator.calculate_rating_1_0(
            inputs['kills'],
            inputs['deaths'],
            inputs['rounds'],
            inputs['kills_3k'],
            inputs['kills_4k'],
            inputs['kills_5k']
        )

        rating2 = RatingCalculator.calculate_rating_2_0(
            kills=inputs['kills'],
            deaths=inputs['deaths'],
            assists=inputs['assists'],
            rounds=inputs['rounds'],
            adr=inputs['adr'],
            kills_3k=inputs['kills_3k'],
            kills_4k=inputs['kills_4k'],
            kills_5k=inputs['kills_5k']
        )

        custom = RatingCalculator.calculate_custom_rating(
            kills=inputs['kills'],
            deaths=inputs['deaths'],
            assists=inputs['assists'],
            rounds=inputs['rounds'],
            mvps=inputs['mvps'],
            adr=inputs['adr'],
            hs_percent=inputs['hs_percent'],
            rws=inputs['rws']
        )

        return (
            f"综合评分 (三种算法平均)\n"
            f"Rating 1.0: {rating1:.2f}\n"
            f"Rating 2.0: {rating2:.2f}\n"
            f"自定义算法: {custom:.2f}\n\n"
            f"详细统计:\n"
            f"KPR: {inputs['kills'] / rounds:.2f}\n"
            f"DPR: {inputs['deaths'] / rounds:.2f}\n"
            f"APR: {inputs['assists'] / rounds:.2f}\n"
            f"ADR: {inputs['adr']:.1f}\n"
            f"爆头率: {inputs['hs_percent']:.1f}%\n"
            f"3杀回合: {inputs['kills_3k']}\n"
            f"4杀回合: {inputs['kills_4k']}\n"
            f"5杀回合: {inputs['kills_5k']}"
        )

    def prepare_rating1_details(self, inputs: dict) -> str:
        """准备Rating 1.0的详细数据"""
        rounds = max(1, inputs['rounds'])
        kpr = inputs['kills'] / rounds
        spr = (rounds - inputs['deaths']) / rounds
        rmk = min(
            (inputs['kills_3k'] * 2.0 + inputs['kills_4k'] * 3.0 + inputs['kills_5k'] * 4.0) / rounds,
            1.5
        )

        return (
            f"Rating 1.0 详细计算:\n"
            f"KPR (每回合击杀): {kpr:.2f}\n"
            f"SPR (每回合存活率): {spr:.2f}\n"
            f"RMK (多杀回合价值): {rmk:.2f}\n\n"
            f"公式: (KPR + 0.7*SPR + RMK) / 2.7\n\n"
            f"多杀统计:\n"
            f"3杀回合: {inputs['kills_3k']}\n"
            f"4杀回合: {inputs['kills_4k']}\n"
            f"5杀回合: {inputs['kills_5k']}"
        )

    def prepare_rating2_details(self, inputs: dict) -> str:
        """准备Rating 2.0的详细数据"""
        rounds = inputs['rounds']
        kpr = inputs['kills'] / rounds
        dpr = inputs['deaths'] / rounds
        kast = RatingCalculator.BaseRatingCalculator.calculate_kast(
            inputs['kills'],
            inputs['deaths'],
            inputs['assists'],
            rounds
        )
        impact = RatingCalculator.BaseRatingCalculator.calculate_impact(
            inputs['kills_3k'],
            inputs['kills_4k'],
            inputs['kills_5k'],
            rounds
        )

        return (
            f"Rating 2.0 (HLTV算法) 详细计算:\n"
            f"KPR: {kpr:.4f}\n"
            f"DPR: {dpr:.4f}\n"
            f"Impact: {impact:.4f}\n"
            f"ADR: {inputs['adr']:.1f}\n"
            f"KAST: {kast:.1f}%\n\n"
            f"公式: 0.3591*KPR - 0.5329*DPR + 0.2372*Impact + \n"
            f"0.0032*ADR + 0.0073*KAST + 0.1587\n\n"
            f"多杀统计:\n"
            f"3杀回合: {inputs['kills_3k']}\n"
            f"4杀回合: {inputs['kills_4k']}\n"
            f"5杀回合: {inputs['kills_5k']}"
        )

    def prepare_custom_details(self, inputs: dict) -> str:
        """准备自定义算法的详细数据"""
        rounds = inputs['rounds']
        kpr = inputs['kills'] / rounds
        dpr = inputs['deaths'] / rounds
        apr = inputs['assists'] / rounds
        mvp_rate = inputs['mvps'] / rounds
        rws_factor = RatingCalculator.BaseRatingCalculator.calculate_rws_factor(inputs['rws'])

        return (
            f"自定义算法详细计算:\n"
            f"KPR: {kpr:.2f}\n"
            f"DPR: {dpr:.2f}\n"
            f"APR: {apr:.2f}\n"
            f"ADR贡献: {inputs['adr'] / 100:.2f}\n"
            f"爆头率贡献: {inputs['hs_percent'] / 100:.2f}\n"
            f"MVP率: {mvp_rate:.2f}\n"
            f"RWS调整系数: {rws_factor:.2f}\n\n"
            f"公式: 0.6*KPR + 0.2*(1-DPR) + 0.1*APR + \n"
            f"0.05*(ADR/100) + 0.05*(HS%/100) + 0.05*MVP率\n"
            f"然后乘以RWS调整系数\n\n"
            f"多杀统计:\n"
            f"3杀回合: {inputs['kills_3k']}\n"
            f"4杀回合: {inputs['kills_4k']}\n"
            f"5杀回合: {inputs['kills_5k']}"
        )

    def show_about(self):
        """显示关于信息"""
        about_text = (
            "CS2 Rating 计算器 专业版\n\n"
            "包含三种计算算法:\n"
            "1. Rating 1.0 - 基础算法 (KPR/SPR/RMK)\n"
            "2. Rating 2.0 - HLTV改进算法 (含多杀影响)\n"
            "3. 自定义算法 - 综合评估 (含RWS调整)\n\n"
            "评分标准:\n"
            "1.30+ → 超凡表现 (职业级)\n"
            "1.15-1.30 → 优秀表现\n"
            "1.00-1.15 → 良好表现\n"
            "0.85-1.00 → 平均水平\n"
            "<0.85 → 需要改进\n\n"
            "开发信息:\n"
            "- 开发者: FinNank1ng\n"
            "- B站: Bilibili 星丶白羽莲\n\n"
            "注意: 这不是官方工具，计算结果仅供参考。"
            "由于单场比赛RWS，IMPACT, KAST都难以计算，数据仅供参考"
        )
        QMessageBox.about(self.view, "关于CS2 Rating计算器", about_text)