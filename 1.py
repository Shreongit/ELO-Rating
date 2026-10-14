class Elo:
    def __init__(self, k_factor: int = 32, c_value: int = 400, l_factor: int = 16):
        """
        ELO rating system implementation.

        :param k_factor: K factor (controls rating change speed).
        :param c_value: Constant used in expected score formula (usually 400).
        :param l_factor: L factor for score-based bonus in method 2.
        """
        self.k = float(k_factor)
        self.c = float(c_value)
        self.l = float(l_factor)

    def _expected_score(self, rating_a: float, rating_b: float) -> float:
        """
        Compute expected score of player A vs player B.
        """
        exponent = (rating_b - rating_a) / self.c
        return 1.0 / (1.0 + 10.0 ** exponent)

    def elo(self, rating_a: float, rating_b: float, outcome: int):
        """
        Update ratings based only on match outcome.

        :param rating_a: Current rating of player A.
        :param rating_b: Current rating of player B.
        :param outcome: 0 = draw, 1 = A wins, 2 = B wins.
        :return: (new_rating_a, new_rating_b)
        """
        if outcome == 0:
            s_a, s_b = 0.5, 0.5
        elif outcome == 1:
            s_a, s_b = 1.0, 0.0
        elif outcome == 2:
            s_a, s_b = 0.0, 1.0
        else:
            raise ValueError("outcome must be 0 (draw), 1 (A wins), or 2 (B wins)")

        e_a = self._expected_score(rating_a, rating_b)
        e_b = 1.0 - e_a

        new_a = rating_a + self.k * (s_a - e_a)
        new_b = rating_b + self.k * (s_b - e_b)

        return new_a, new_b

    def elo_with_points(
        self,
        rating_a: float,
        rating_b: float,
        points_a: float,
        points_b: float,
        method: int = 2,
        outcome: int | None = None,
    ):
        """
        Update ratings considering points scored.

        :param rating_a: Current rating of player A.
        :param rating_b: Current rating of player B.
        :param points_a: Points scored by player A.
        :param points_b: Points scored by player B.
        :param method: 0 = classic ELO, 1 = score fraction, 2 = bonus with L factor.
        :param outcome: Required for method 0 and 2 if you want strict win/draw/loss:
                        0 = draw, 1 = A wins, 2 = B wins.
                        If None and method != 1 → derived from points.
        :return: (new_rating_a, new_rating_b)
        """
        # Derive outcome from score if not provided (for convenience)
        if outcome is None:
            if points_a > points_b:
                outcome = 1
            elif points_b > points_a:
                outcome = 2
            else:
                outcome = 0

        # Determine match result S_a, S_b
        if outcome == 0:
            s_a, s_b = 0.5, 0.5
        elif outcome == 1:
            s_a, s_b = 1.0, 0.0
        elif outcome == 2:
            s_a, s_b = 0.0, 1.0
        else:
            raise ValueError("outcome must be 0 (draw), 1 (A wins), or 2 (B wins)")

        e_a = self._expected_score(rating_a, rating_b)
        e_b = 1.0 - e_a

        total_points = points_a + points_b
        if total_points > 0.0:
            frac_a = points_a / total_points
            frac_b = points_b / total_points
        else:
            # Avoid division by zero; treat as equal performance
            frac_a = frac_b = 0.5

        if method == 0:
            # Classic ELO, ignore points
            new_a = rating_a + self.k * (s_a - e_a)
            new_b = rating_b + self.k * (s_b - e_b)

        elif method == 1:
            # Replace S with score fraction
            new_a = rating_a + self.k * (frac_a - e_a)
            new_b = rating_b + self.k * (frac_b - e_b)

        elif method == 2:
            # Use S as usual, add bonus with L factor
            diff_a = s_a - e_a
            if diff_a > 0:
                p_a = 1.0
            elif diff_a < 0:
                p_a = -1.0
            else:
                p_a = 0.0

            diff_b = s_b - e_b
            if diff_b > 0:
                p_b = 1.0
            elif diff_b < 0:
                p_b = -1.0
            else:
                p_b = 0.0

            new_a = rating_a + self.k * diff_a + p_a * self.l * frac_a
            new_b = rating_b + self.k * diff_b + p_b * self.l * frac_b

        else:
            raise ValueError("method must be 0, 1, or 2")

        return new_a, new_b
