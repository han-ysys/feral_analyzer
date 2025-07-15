# check logs with or without skyfury
from tasks.ravage_proc.normalization import Normalization, fetch_normalize_data, regression_plot, normalization_index_regression, check_model
from tasks.ravage_proc.catcher import catcher

def ravge_counter(code, fight_id, threshold=100, normalization_file='data_json/normalization.json'):
    """
    Main function to run the Ravage counter analysis.
    
    Args:
        code (str): The code to identify the player or instance.
        fight_id (int): The ID of the fight to analyze.
        threshold (int): The maximum number of fights to consider for normalization.
        normalization_file (str): Path to the normalization data file.
    """
    check_model(code, fight_id, threshold, normalization_file)