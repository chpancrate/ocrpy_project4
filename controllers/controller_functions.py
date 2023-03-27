"""functions used by the controller"""
import json
import time
from models.models import JSON_PLAY_FILENAME


def build_tournament_id(tournament_id_ref):
    """create the tournament id with the following format
    TOUXXXXX where XXXXX is an integer
    ex TOU12345
    """
    return "TOU" + str(tournament_id_ref).zfill(5)


def build_tournament_info(tournament):
    """collect the tournament info data except rounds and ranking
    for transfer to the view
    """
    tournament_info = {}
    tournament_info["tournament_id"] = tournament.tournament_id
    tournament_info["name"] = tournament.name
    tournament_info["location"] = tournament.location
    tournament_info["start_date"] = tournament.start_date
    tournament_info["end_date"] = tournament.end_date
    tournament_info["number_of_rounds"] = tournament.number_of_rounds
    tournament_info["current_round"] = tournament.current_round
    tournament_info["description"] = tournament.description
    return tournament_info


def retrieve_tournament_players_data(tournament):
    """Create the players list from the tournament ranking
    additional data come from the players file : JSON_PLAY_FILENAME
    """
    tournament_players_list = {}
    try:
        # load the players data from the file
        with open(JSON_PLAY_FILENAME, "r") as file_json:
            json_players_list_dict = json.load(file_json)
            players_list = json_players_list_dict["players_list"]
            # for each player_id in the ranking, complete the data
            for rank in tournament.ranking:
                player_data = []
                for player in players_list:
                    if rank.national_chess_id == player["national_chess_id"]:
                        player_data.append(player["name"])
                        player_data.append(player["surname"])
                        player_data.append(player["birth_date"])
                        player_update = {}
                        player_update[
                            player["national_chess_id"]
                        ] = player_data
                        tournament_players_list.update(player_update)
                        break
    except FileNotFoundError:
        pass
    return tournament_players_list


def update_score(tournament, result):
    """update the score in a tournament ranking
    check that the game has not been entered yet
    if yes remove the result from the ranking
    add the new result to the ranking
    """
    round = tournament.rounds[-1]
    player_id = result[1]
    result_type = result[0]

    if result_type == "v":
        player_score = 1
        other_player_score = 0
    else:
        player_score = 0.5
        other_player_score = 0.5

    player_id_found = False
    for game in round.games:
        if player_id in game.result:
            player_id_found = True
            for key in game.result.keys():
                if key != player_id:
                    other_player_id = key

            player_old_score = game.result[player_id]
            other_player_old_score = game.result[other_player_id]

            if player_old_score != 0 or other_player_old_score != 0:
                # there's already a result, remove old score from ranking
                player_old_score = -1 * player_old_score
                other_player_old_score = -1 * other_player_old_score
                tournament.ranking.store_score(player_id, player_old_score)
                tournament.ranking.store_score(
                    other_player_id, other_player_old_score
                )

            # store the new score
            game.store_result(
                player_id,
                player_score,
                other_player_id,
                other_player_score,
            )
            tournament.ranking.store_score(player_id, player_score)
            tournament.ranking.store_score(other_player_id, other_player_score)
            tournament.json_save()
            break
    if not player_id_found:
        print("joueur inexistant!")
        time.sleep(2)


def create_round_players_list(round):
    """retrieve all the data for the players of a round
    in the players file
    """
    with open(JSON_PLAY_FILENAME, "r") as file_json:
        json_players_list_dict = json.load(file_json)
        players_list = json_players_list_dict["players_list"]

    round_players_list = []
    for game in round.games:
        players_id = []
        # get the two players id from the game
        for key in game.result.keys():
            players_id.append(key)
        player_id = players_id[0]
        other_player_id = players_id[1]

        player_score = game.result[player_id]
        other_player_score = game.result[other_player_id]

        # get the data corresponding to the players
        for player in players_list:
            if player["national_chess_id"] == player_id:
                player_name = player["name"]
                player_surname = player["surname"]
                break
        for player in players_list:
            if player["national_chess_id"] == other_player_id:
                other_player_name = player["name"]
                other_player_surname = player["surname"]
                break

        game_data = {}
        game_data["player1_id"] = player_id
        game_data["player1_name"] = player_name
        game_data["player1_surname"] = player_surname
        game_data["player1_score"] = player_score
        game_data["player2_id"] = other_player_id
        game_data["player2_name"] = other_player_name
        game_data["player2_surname"] = other_player_surname
        game_data["player2_score"] = other_player_score
        round_players_list.append(game_data)

    return round_players_list
