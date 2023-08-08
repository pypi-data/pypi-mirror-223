import math
import sys
sys.path.append('../../')

from connect_four_gymnasium.ConnectFourEnv import ConnectFourEnv
from connect_four_gymnasium.players import (
    BabyPlayer,
    BabySmarterPlayer,
    ChildPlayer,
    ChildSmarterPlayer,
    TeenagerPlayer,
    TeenagerSmarterPlayer,
    AdultPlayer,
    AdultSmarterPlayer,
    SelfTrained1Player,
    SelfTrained2Player,
    SelfTrained3Player,
    SelfTrained4Player,
    SelfTrained5Player,
    SelfTrained6Player,
    SelfTrained7Player,
)


class EloLeaderboard:
    def __init__(self):
        # Initialize the list of players
        self.players = [
            # BabyPlayer(),
            # BabySmarterPlayer(),
            # ChildPlayer(),
            # ChildSmarterPlayer(),
            # TeenagerPlayer(),
            # TeenagerSmarterPlayer(),
            AdultPlayer(),
            AdultSmarterPlayer(),
            # SelfTrained1Player(),
            SelfTrained2Player(),
            SelfTrained3Player(),
            SelfTrained4Player(),
            SelfTrained5Player(),
            SelfTrained6Player(),
            SelfTrained7Player(),
        ]
        # Initialize the Elo rankings for each player
        self.elo_rankings = {player.getName(): player.getElo() if player.getElo() is not None else 1500 for player in self.players}

    def update_elo(self, player_elo, opponent_elo, player_won, k_factor=32, draw=False):
        # Calculate the expected outcome based on the current Elo ratings
        expected_outcome = 1 / (1 + math.pow(10, (opponent_elo - player_elo) / 400))
        # Set the actual outcome based on whether the player won, lost, or drew
        if draw:
            actual_outcome = 0.5
        else:
            actual_outcome = 1 if player_won else 0
        # Update the player's Elo rating
        new_elo = player_elo + k_factor * (actual_outcome - expected_outcome)
        return new_elo

    def play_round(self, k_factor=32, move_elo_already_known=False):
        # Iterate through all possible player-opponent pairs
        for player in self.players:
            for opponent in self.players:
                if player != opponent:
                    # Skip the match if both players have known Elo ratings and we don't want to update them
                    if not move_elo_already_known and player.getElo() is not None and opponent.getElo() is not None:
                        continue
                    player_score = self.get_score(player, opponent)
                    player_won = player_score > 0.5
                    draw = player_score == 0.5
                    player_elo = self.elo_rankings[player.getName()]
                    opponent_elo = self.elo_rankings[opponent.getName()]
                    new_player_elo = self.update_elo(player_elo, opponent_elo, player_won, k_factor,draw)
                    new_opponent_elo = self.update_elo(opponent_elo, player_elo, not player_won, k_factor,draw)
                    if player.getElo() is None or move_elo_already_known:
                        self.elo_rankings[player.getName()] = new_player_elo
                    if opponent.getElo() is None or move_elo_already_known :
                        self.elo_rankings[opponent.getName()] = new_opponent_elo
                    # self.elo_rankings["BabyPlayer"] = 1000
                    self.elo_rankings["AdultPlayer"] = 1666

    def get_elo(self, new_players, num_matches=100, move_elo_already_known=False, display_log=True):
        # Add new players to the leaderboard
        self.players.extend(new_players)
        for player in new_players:
            self.elo_rankings[player.getName()] = player.getElo() if player.getElo() is not None else 1500

        # Play the specified number of matches
        for i in range(num_matches):
            k_factor = 0.2 / (1 + 1 / 10)
            if display_log:
                print(f"Elo rankings after {i} matches:")
                self.display_rankings()
                print("\n")
            self.play_round(k_factor, move_elo_already_known)
            

        # Return the updated Elo ratings for the new players
        new_player_elos = [self.elo_rankings[player.getName()] for player in new_players]
        return new_player_elos

    def display_rankings(self):
        # Sort the rankings in descending order of Elo ratings
        sorted_rankings = sorted(self.elo_rankings.items(), key=lambda x: x[1], reverse=True)
        # Display the sorted rankings
        for rank, (player_name, elo) in enumerate(sorted_rankings, start=1):
            print(f"{rank}. {player_name}: {round(elo)}")

    def get_score(self, player, opponent):
        # Initialize the game environment
        env = ConnectFourEnv(opponent=opponent)
        obs, _ = env.reset()
        # Play the game until it ends
        while True:
            action = player.play(obs)
            obs, rewards, dones, truncated, _ = env.step(action)
            if truncated or dones:
                obs, _ = env.reset()
                return rewards


if __name__ == "__main__":

    elo_leaderboard = EloLeaderboard()
    print(elo_leaderboard.get_elo([], num_matches=400,display_log=True,move_elo_already_known=True))


# 0. max 2966
# Elo rankings after 399 matches:
# 1. SelfTrained6Player: 2413
# 2. SelfTrained5Player: 2258
# 3. SelfTrained4Player: 2093
# 4. SelfTrained3Player: 2013
# 5. SelfTrained2Player: 1963
# 6. AdultSmarterPlayer: 1778
# 8. AdultPlayer: 1666
# 9. TeenagerPlayer: 1663
# 10. TeenagerSmarterPlayer: 1660
# 11. ChildSmarterPlayer: 1586
# 12. SelfTrained1Player: 1391
# 13. ChildPlayer: 1264
# 14. BabySmarterPlayer: 1058
# 15. BabyPlayer: 1000