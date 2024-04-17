
all_predictions = []

def append_prediction(matchup_name, prediction):
    all_predictions.append((matchup_name, prediction))

def write_predictions_to_file():
    with open('predictions.txt', 'a') as file:
        for matchup_name, prediction in all_predictions:
            file.write(f"{matchup_name}: {prediction}\n")
    all_predictions.clear()

def add_divider():
    with open('predictions.txt', 'a') as file:
        file.write("\n----------\n\n")