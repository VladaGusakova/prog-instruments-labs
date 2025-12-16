class TennisGame2:
    score_names = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1points = 0
        self.p2points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.p1_score()
        else:
            self.p2_score()

    def score(self):
        if self.p1points == self.p2points:
            if self.p1points >= 3:
                return "Deuce"
            return f"{self.score_names[self.p1points]}-All"

        if self.p1points >= 4 or self.p2points >= 4:
            diff = self.p1points - self.p2points
            if diff == 1:
                return f"Advantage {self.player1_name}"
            elif diff == -1:
                return f"Advantage {self.player2_name}"
            elif diff >= 2:
                return f"Win for {self.player1_name}"
            else:
                return f"Win for {self.player2_name}"

        return f"{self.score_names[self.p1points]}-{self.score_names[self.p2points]}"

    def set_p1_score(self, number):
        for _ in range(number):
            self.p1_score()

    def set_p2_score(self, number):
        for _ in range(number):
            self.p2_score()

    def p1_score(self):
        self.p1points += 1

    def p2_score(self):
        self.p2points += 1
