class TennisGame4:
    def __init__(self, player1_name, player2_name):
        self.server = player1_name
        self.receiver = player2_name
        self.server_score = 0
        self.receiver_score = 0

    def won_point(self, player_name):
        if self.server == player_name:
            self.server_score += 1
        else:
            self.receiver_score += 1

    def score(self):
        scores = ["Love", "Fifteen", "Thirty", "Forty"]

        if self.server_score >= 3 and self.receiver_score >= 3:
            if self.server_score == self.receiver_score:
                return "Deuce"
            elif self.server_score - self.receiver_score == 1:
                return f"Advantage {self.server}"
            elif self.receiver_score - self.server_score == 1:
                return f"Advantage {self.receiver}"
            elif self.server_score - self.receiver_score >= 2:
                return f"Win for {self.server}"
            elif self.receiver_score - self.server_score >= 2:
                return f"Win for {self.receiver}"

        if self.server_score == self.receiver_score:
            return f"{scores[self.server_score]}-All"
        return f"{scores[self.server_score]}-{scores[self.receiver_score]}"