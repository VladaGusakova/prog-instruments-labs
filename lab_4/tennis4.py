class TennisGame4:
    def __init__(self, player1_name, player2_name):
        self.server = player1_name
        self.receiver = player2_name
        self.server_score = 0
        self.receiver_score = 0
        self.scores = ["Love", "Fifteen", "Thirty", "Forty"]

    def won_point(self, player_name):
        if self.server == player_name:
            self.server_score += 1
        else:
            self.receiver_score += 1

    def score(self):
        if self.server_has_won():
            return f"Win for {self.server}"
        if self.receiver_has_won():
            return f"Win for {self.receiver}"
            
        if self.server_has_advantage():
            return f"Advantage {self.server}"
        if self.receiver_has_advantage():
            return f"Advantage {self.receiver}"
            
        if self.is_deuce():
            return "Deuce"
            
        server_score_str = self.scores[self.server_score]
        receiver_score_str = self.scores[self.receiver_score]
        
        if self.server_score == self.receiver_score:
            return f"{server_score_str}-All"
        return f"{server_score_str}-{receiver_score_str}"

    def receiver_has_advantage(self):
        return self.receiver_score >= 4 and (self.receiver_score - self.server_score) == 1

    def server_has_advantage(self):
        return self.server_score >= 4 and (self.server_score - self.receiver_score) == 1

    def receiver_has_won(self):
        return self.receiver_score >= 4 and (self.receiver_score - self.server_score) >= 2

    def server_has_won(self):
        return self.server_score >= 4 and (self.server_score - self.receiver_score) >= 2

    def is_deuce(self):
        return self.server_score >= 3 and self.receiver_score >= 3 and self.server_score == self.receiver_score