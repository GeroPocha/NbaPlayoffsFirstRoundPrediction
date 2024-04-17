from openai import OpenAI
import re
from data import teams_data, matchups
from formats import standingsFormat, teamVsTeamFormat
from output import append_prediction, write_predictions_to_file, all_predictions, add_divider
import playins

results = {}
api_key = "Insert your OpenAI API Key here :)"
client = OpenAI(api_key=api_key)


def predict_winner(team1, team2):
    team1_name = teams_data[team1]['name']
    team2_name = teams_data[team2]['name']

    prompt = f"""
Based on the comprehensive season data for NBA teams, specifically focusing on the performance of {team1_name} and {team2_name}, predict the winner of their best of 7 series. Consider their standings, which have the following format: {standingsFormat} ({teams_data[team1]['standings']}, {teams_data[team2]['standings']}), and how they played against every other team, the data will be in this format: {teamVsTeamFormat} ({teams_data[team1]['playedAgainstEveryTeam']}, {teams_data[team2]['playedAgainstEveryTeam']}). It is crucial to make a definitive prediction between '{team1_name}', '{team2_name}'. At the end of your response, indicate the result with 'Final Prediction: followed by the winners team name' 
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[
            {"role": "system", "content": "AI is asked to predict NBA series winners based on detailed team data."},
            {"role": "user", "content": prompt}
        ]
    )

    prediction_response = response.choices[0].message.content.strip()
    print(prediction_response)  # I was curious regarding the reasoning

    regex = rf"Final Prediction:\s*({re.escape(team1_name)}|{re.escape(team2_name)})\s*\.*"
    match = re.search(regex, prediction_response, re.IGNORECASE | re.DOTALL)
    final_prediction = match.group(1).strip() if match else "No clear prediction"

    final_prediction_normalized = final_prediction.lower()
    matchup_key = f"{team1} vs {team2}"
    if matchup_key not in results:
        results[matchup_key] = {team1: 0, team2: 0}

    if final_prediction_normalized == team1_name.lower():
        results[matchup_key][team1] += 1
    elif final_prediction_normalized == team2_name.lower():
        results[matchup_key][team2] += 1

    return final_prediction


def display_win_percentages():
    print("Displaying win percentages...")
    for matchup, counts in results.items():
        print(f"Processing results for {matchup}")
        total_predictions = sum(counts.values())
        if total_predictions == 0:
            print("No predictions to display for this matchup.")
            continue
        print(f"Results for {matchup}:")
        for team, count in counts.items():
            percentage = (count / total_predictions) * 100
            print(f"  {team}: {percentage:.2f}%")


def update_playoff_matchups(playin_winners):
    for matchup in matchups:
        if matchup['b'] == '':

            if 'east' in matchup['name']:
                if '1' in matchup['name']:
                    matchup['b'] = playin_winners['playin_east_1']
                elif '2' in matchup['name']:
                    matchup['b'] = playin_winners['playin_east_2']
            elif 'west' in matchup['name']:
                if '1' in matchup['name']:
                    matchup['b'] = playin_winners['playin_west_1']
                elif '2' in matchup['name']:
                    matchup['b'] = playin_winners['playin_west_2']

def predict_playoffs():
    for matchup in matchups:
        if matchup['b'] != '':
            print(f"Predicting {matchup['name']}: {matchup['a']} vs {matchup['b']}")
            winner = predict_winner(matchup['a'], matchup['b'])
            print(f"Winner of {matchup['name']}: {winner}")
            append_prediction(matchup['name'], winner)

if __name__ == "__main__":
    for i in range(50):
        playin_winners = playins.predict_playins()
        update_playoff_matchups(playin_winners)
        predict_playoffs()
        display_win_percentages()
        write_predictions_to_file()
        add_divider()