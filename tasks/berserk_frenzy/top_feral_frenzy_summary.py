from utils import ranking
import json
from . import berserk_frenzy_calculater
import argparse

def save_summary(file_path='data_json/top_feral_frenzy_summary.json', input='data_json/top_ferals.json'):
    top_feral_encounters = ranking.load_top_feral_apex_data(input)
    if top_feral_encounters:
        fights = ranking.fights_parser(top_feral_encounters, {"key": "frenzy_per_berserk", "func": berserk_frenzy_calculater.frenzy_per_berserk_from_table})
        with open(file_path, 'w') as f:
            json.dump(fights, f, indent=4)
        print(f"Top feral apex summary data saved to '{file_path}'.")
    else:
        print("No data available to process.")

if __name__ == "__main__":
    # Save the summary of top feral frenzy data
    parser = argparse.ArgumentParser(description='Top Feral Frenzy Summary')
    parser.add_argument('-f', '--file_path', type=str, default='data_json/top_feral_frenzy_summary.json', help='Path to save the summary file')
    parser.add_argument('-i', '--input', type=str, help='Input file path for top feral data', required=True)
    args = parser.parse_args()
    save_summary(args.file_path, args.input)
    print("Top feral frenzy summary saved successfully.")