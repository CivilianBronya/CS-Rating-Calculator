class RatingCalculator:
    """CS2 Rating计算模型（优化重复计算）"""

    class BaseRatingCalculator:
        """内部类：封装共享计算方法"""

        @staticmethod
        def calculate_kast(kills: int, deaths: int, assists: int, rounds: int) -> float:
            """标准KAST计算（所有算法共享）"""
            rounds = max(1, rounds)
            # 优化估算：考虑击杀和助攻可能发生在同一回合
            contribution_rounds = min(kills + assists, rounds * 1.2)
            survived_rounds = max(0, rounds - deaths)
            return min(100, (contribution_rounds + survived_rounds) / rounds * 100)

        @staticmethod
        def calculate_impact(kills_3k: int, kills_4k: int, kills_5k: int, rounds: int) -> float:
            """多杀影响计算（Rating 1.0和2.0共享）"""
            rounds = max(1, rounds)
            return min(
                (kills_3k * 3 + kills_4k * 5 + kills_5k * 5) / rounds,
                2.0
            )

        @staticmethod
        def calculate_rws_factor(rws: float) -> float:
            """RWS调整系数计算"""
            return 0.5 + (min(30.0, max(0.0, rws or 0)) / 20)

    @staticmethod
    def calculate_rating_1_0(kills: int, deaths: int, rounds: int,
                             kills_3k: int = 0, kills_4k: int = 0, kills_5k: int = 0) -> float:
        """
        Rating 1.0计算
        公式: (KPR + 0.7 * SPR + RMK) / 2.7
        """
        try:
            rounds = max(1, rounds)
            kpr = kills / rounds
            spr = (rounds - deaths) / rounds

            # 使用共享的多杀计算
            rmk = min(
                (kills_3k * 3 + kills_4k * 4 + kills_5k * 5) / rounds,
                1.5
            )

            return max(0.0, min(3.0, (kpr + 0.7 * spr + rmk) / 2.7))
        except Exception as e:
            print(f"[Rating 1.0] {str(e)}")
            return 1.0

    @staticmethod
    def calculate_rating_2_0(kills: int, deaths: int, assists: int,
                             rounds: int, adr: float,
                             kast: float = None,  # 可选参数
                             kills_3k: int = 0, kills_4k: int = 0, kills_5k: int = 0) -> float:
        """
        Rating 2.0计算
        公式: 0.3591*KPR - 0.5329*DPR + 0.2372*Impact + 0.0032*ADR + 0.0073*KAST + 0.1587
        """
        try:
            rounds = max(1, rounds)
            kpr = kills / rounds
            dpr = deaths / rounds

            # 使用共享的KAST计算（如果未提供）
            kast = kast or RatingCalculator.BaseRatingCalculator.calculate_kast(
                kills, deaths, assists, rounds)

            # 使用共享的Impact计算
            impact = (
                    0.6 * RatingCalculator.BaseRatingCalculator.calculate_impact(
                kills_3k, kills_4k, kills_5k, rounds) +
                    0.25 * kpr +
                    0.15 * (rounds - deaths) / rounds
            )

            rating = (
                    0.3591 * kpr -
                    0.5329 * dpr +
                    0.2372 * impact +
                    0.0032 * min(300.0, adr) +
                    0.0073 * kast +
                    0.1587
            )
            return max(0.0, min(3.0, rating))
        except Exception as e:
            print(f"[Rating 2.0] {str(e)}")
            return 1.0

    @staticmethod
    def calculate_custom_rating(kills: int, deaths: int, assists: int,
                                rounds: int, mvps: int, adr: float,
                                hs_percent: float, rws: float = None,
                                kills_3k: int = 0, kills_4k: int = 0, kills_5k: int = 0) -> float:
        """
        自定义算法
        公式: 0.6*KPR + 0.2*(1-DPR) + 0.1*APR + 0.05*(ADR/100) + 0.05*(HS%/100) + 0.05*MVP率
        """
        try:
            rounds = max(1, rounds)
            base = (
                    0.6 * (kills / rounds) +
                    0.2 * (1 - min(1, deaths / rounds)) +
                    0.1 * (assists / rounds) +
                    0.05 * (min(200, adr) / 100) +
                    0.05 * (min(100, hs_percent) / 100) +
                    0.05 * (mvps / rounds)
            )

            # 使用共享的RWS计算
            if rws is not None:
                base *= RatingCalculator.BaseRatingCalculator.calculate_rws_factor(rws)

            return max(0.0, min(3.0, base * 0.9 + 0.1))
        except Exception as e:
            print(f"[Custom Rating] {str(e)}")
            return 1.0

    @staticmethod
    def calculate_rating(kills: int, deaths: int, assists: int,
                         rounds: int, mvps: int, adr: float,
                         hs_percent: float,
                         kills_3k: int = 0, kills_4k: int = 0, kills_5k: int = 0,
                         rws: float = None) -> float:
        """综合评分（自动复用所有共享计算）"""
        try:
            # 统一计算共享数据
            shared_kast = RatingCalculator.BaseRatingCalculator.calculate_kast(
                kills, deaths, assists, rounds)
            shared_impact = RatingCalculator.BaseRatingCalculator.calculate_impact(
                kills_3k, kills_4k, kills_5k, rounds)

            rating1 = RatingCalculator.calculate_rating_1_0(
                kills, deaths, rounds, kills_3k, kills_4k, kills_5k)

            rating2 = RatingCalculator.calculate_rating_2_0(
                kills, deaths, assists, rounds, adr,
                kast=shared_kast,
                kills_3k=kills_3k, kills_4k=kills_4k, kills_5k=kills_5k)

            custom = RatingCalculator.calculate_custom_rating(
                kills, deaths, assists, rounds, mvps, adr, hs_percent, rws, kills_3k, kills_4k, kills_5k)

            return max(0.0, min(3.0, (rating1 + rating2 + custom) / 3))
        except Exception as e:
            print(f"[Composite Rating] {str(e)}")
            return 1.0

    @staticmethod
    def get_rating_description(rating: float) -> tuple:
        """评分描述（保持不变）"""
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