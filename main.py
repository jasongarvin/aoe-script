#!usr/bin/env python3

"""
A quick script that retrieves someone's Age of Empires 4 player info
"""

import json
from pprint import pprint
import requests
from matplotlib import pyplot


API_URI = "https://aoe4world.com/api/v0/players"
ENDPOINT_STUB = "games?leaderboard=rm_solo"


def get_from_json(json_dict, selector, selector_two=None, selector_three=None):
    """
    Get some data from the json file based on specified selectors
    """
    selected_fields = json_dict.get(selector)
    if selector_two:
        selected_fields = selected_fields.get(selector_two)
    if selector_three:
        selected_fields = selected_fields.get(selector_three)

    return selected_fields


def get_game_data(player_id, ranked_matches):
    """
    Retrieves relevant game data from ranked results
    stored as JSON.
    """
    matches = []
    for match in ranked_matches:
        game_id = match.get("game_id")

        teams = match.get("teams")
        player_one = teams[0][0].get("player")
        player_two = teams[1][0].get("player")

        # Player 2 tends to be the player whose ID is passed, weirdly
        if player_id == player_two.get("profile_id"):
            player_result = player_two.get("rating")
        else:
            player_result = player_one.get("rating")

        player_values = (game_id, player_result)

        matches.append((player_values))

    return matches


def load_player_data(file_name="player_data.json"):
    """
    Retrieve player data from local .json file
    """
    with open(file_name, "r", encoding="utf-8") as file_in:
        player_data = json.load(file_in)

    return player_data


def prepare_to_graph(match_data):
    """
    Clean up match data to show sequence of results nicer
    """
    match_data.sort()
    print(match_data)

    neatly_spaced_results = []
    for i, match in enumerate(match_data):
        spaced_results = (i, match[1])
        neatly_spaced_results.append(spaced_results)

    print(neatly_spaced_results)
    return neatly_spaced_results


def retrieve_player_data(player_id):
    """
    Retrieve player data from aoe4world.com using their api

    Test for status code 200, then return json-formatted data
    for parsing
    """
    player_url = "/".join([API_URI, str(player_id), ENDPOINT_STUB])
    server_response = requests.get(player_url, timeout=5)
    print(f"server response {server_response.status_code}")

    if server_response.status_code == 200:
        return server_response.json()
    else:
        return None


def save_player_data(player_data, file_name="player_data.json"):
    """
    Save player data to .json file for local caching
    """
    with open(file_name, "w", encoding="utf-8") as file_out:
        json.dump(player_data, file_out)


if __name__ == "__main__":
    # player_id = input("Enter player id: ")
    PLAYER_ID = 2930552

    raw_player_data = {}
    try:
        raw_player_data = load_player_data()
    except FileNotFoundError:
        raw_player_data = retrieve_player_data(PLAYER_ID)
        save_player_data(raw_player_data)
    finally:
        print("player data retrieved")

    ranked_data = get_from_json(raw_player_data, "games")
    pprint(ranked_data)

    print("arranging data")

    game_data = get_game_data(PLAYER_ID, ranked_data)
    game_data = prepare_to_graph(game_data)

    # Split results into two lists, one of game ID and one of rating
    match_id, player_rating = zip(*game_data)

    pyplot.plot(match_id, player_rating)

    # naming the axes
    pyplot.xlabel('Game ID (ascending)')
    pyplot.ylabel('Rating')
    pyplot.title(f"Player: {PLAYER_ID} ranked solo results")

    # function to show the plot
    pyplot.show()
