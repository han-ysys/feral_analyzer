from utils import catcher
from common import spell
import json

def bloodtalon_coverage(report_code, fight_ids):
    """
    Calculate the Bloodtalon coverage for a given report code and fight IDs.

    :param report_code: The report code of the fight.
    :param fight_ids: The IDs of the fights.
    :return: A dictionary with fight IDs as keys and Bloodtalon coverage as values.
    """
    for finisher in spell.ids['Finisher'].values():
        events = catcher.events_data(
            report_code=report_code,
            fight_ids=fight_ids,
            ability_id=finisher,
            event_type='Casts',
            source_auras_present=145152
        )
        with open(f'data_json/finisher_casts_bt_{finisher}.json', 'w') as f:
            data = {
                'report_code': report_code,
                'fight_ids': fight_ids,
                'finisher': finisher,
                'events': events
            }
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculate Bloodtalon coverage.")
    parser.add_argument("-r", "--report_code", type=str, required=True, help="The report code to fetch data for.")
    parser.add_argument("-f", "--fight_ids", type=int, nargs='+', required=True, help="The IDs of the fights.")
    args = parser.parse_args()

    bloodtalon_coverage(args.report_code, args.fight_ids)