from playoffs import predict_winner, teams_data
from data import play_in_matchups
from output import append_prediction


def predict_playins():
    winners = {}
    losers = {}

    for matchup in play_in_matchups:
        winner = predict_winner(matchup['a'], matchup['b'])
        winners[matchup['name']] = winner
        append_prediction(matchup['name'], winner)
        losers[matchup['name']] = matchup['a'] if winner == matchup['b'] else matchup['b']


    east_loser_match_name = 'playin_east_loser'
    east_loser_winner = predict_winner(losers['playin_east_1'], winners['playin_east_2'])
    winners[east_loser_match_name] = east_loser_winner
    append_prediction(east_loser_match_name, east_loser_winner)

    west_loser_match_name = 'playin_west_loser'
    west_loser_winner = predict_winner(losers['playin_west_1'], winners['playin_west_2'])
    winners[west_loser_match_name] = west_loser_winner
    append_prediction(west_loser_match_name, west_loser_winner)

    return winners


if __name__ == "__main__":
    playin_results = predict_playins(play_in_matchups)
    print("Play-In Gewinner und nächste Matchups:", playin_results)