from utils import ranking
import json
from . import frenzy_calculater

def save_summary(file_path='data_json/top_feral_frenzy_summary.json'):
    top_feral_encounters = ranking.load_top_feral_apex_data()
    if top_feral_encounters:
        fights = ranking.fights_parser(top_feral_encounters, {"key": "frenzy_per_berserk", "func": frenzy_calculater.frenzy_per_berserk_from_table})
        with open(file_path, 'w') as f:
            json.dump(fights, f, indent=4)
        print(f"Top feral apex summary data saved to '{file_path}'.")
    else:
        print("No data available to process.")

if __name__ == "__main__":
    # Save the summary of top feral frenzy data
    save_summary('data_json/top_feral_frenzy_summary.json')
    print("Top feral frenzy summary saved successfully.")