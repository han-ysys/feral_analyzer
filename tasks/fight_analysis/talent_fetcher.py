def talent_tree(playerDetails, player_name, server=None, guid=None):
    """
    Extracts the talent tree for a specific player from the player details.

    Args:
        playerDetails (dict): The player details containing talent information.
        player_name (str): The name of the player to extract the talent tree for.

    Returns:
        dict: The talent tree for the specified player.
    """
    pointer = None
    for role, players in playerDetails.items():
        for player in players:
            if guid and player.get('guid') != guid:
                continue
            if server and player.get('server') != server:
                continue
            if player['name'] != player_name:
                continue
        pointer = player.get('talentTree', None)
    return pointer

def check_talent(talentTree, talent_id):
    """
    Checks if a specific talent is present in the talent tree.

    Args:
        talentTree (dict): The talent tree to check.
        talent_id (int): The ID of the talent to check for.

    Returns:
        bool: True if the talent is present, False otherwise.
    """
    return any(talent['id'] == talent_id for talent in talentTree.get('talents', []))