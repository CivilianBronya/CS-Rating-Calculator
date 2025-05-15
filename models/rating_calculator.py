class RatingCalculator:
    """CS2 Rating计算模型"""

    @staticmethod
    def calculate_rating(kills: int, deaths: int, assists: int,
                         rounds: int, mvps: int, adr: float,
                         hs_percent: float) -> float:
        """计算CS2 Rating值，增加安全性检查"""
        try:
            # 确保所有值为非负数
            kills = max(0, kills)
            deaths = max(0, deaths)
            assists = max(0, assists)
            rounds = max(1, rounds)  # 至少1回合
            mvps = max(0, mvps)
            adr = max(0.0, adr)
            hs_percent = max(0.0, min(100.0, hs_percent))  # 限制在0-100%

            # 计算各项指标
            kpr = kills / rounds
            dpr = deaths / rounds
            apr = assists / rounds
            mvp_rate = mvps / rounds

            # 主计算逻辑
            rating = (
                    0.7 * kpr +
                    0.2 * (1 - min(1, dpr)) +  # 限制dpr不超过1
                    0.1 * apr +
                    0.1 * (min(200, adr) / 100 +  # 限制ADR不超过200
                           0.05 * (hs_percent / 100) +
                           0.05 * mvp_rate
                           )
            )
            # 标准化调整
            return max(0, min(3.0, rating * 0.9 + 0.1))  # 限制在0-3.0范围内

        except Exception as e:
            # 如果出现任何计算错误，返回中性值1.0
            print(f"Rating calculation error: {str(e)}")
            return 1.0

    @staticmethod
    def get_rating_description(rating: float) -> tuple:
        """
        根据Rating值返回描述和颜色
        返回: (描述, 颜色代码)
        """
        if rating > 1.3:
            return ("超凡表现! (职业级)", "#FF5722")
        elif rating > 1.15:
            return ("优秀表现! (高水准)", "#4CAF50")
        elif rating > 1.0:
            return ("良好表现 (高于平均)", "#8BC34A")
        elif rating > 0.85:
            return ("普通表现 (平均水平)", "#FFC107")
        else:
            return ("需要改进 (低于平均)", "#F44336")