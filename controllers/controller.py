import time
import json
from models.models import (
    Json2Object,
    Player,
    Tournament,
    JSON_TOUR_FILENAME,
    JSON_TOUR_ID_FILENAME,
    JSON_PLAY_FILENAME,
)


def build_tournament_id(tournament_id_ref):
    return "TOU" + str(tournament_id_ref).zfill(5)


class Controller:
    def control_start(self, menu):
        choice = menu.start()
        if choice == "create_tournament":
            tournament_data = menu.tournament_creation()
            # tournament_data:
            # 0-> name
            # 1-> location
            # 2-> start_date
            # 3-> end_date
            # 4-> number_of_rounds
            # 5-> description
            try:
                with open(
                    JSON_TOUR_ID_FILENAME, "r"
                ) as json_tournament_id_file:
                    tournament_json = json.load(json_tournament_id_file)
                    tournament_id_ref = tournament_json["tournament_id_ref"]
                    tournament_id = build_tournament_id(tournament_id_ref)

                    new_tournament = Tournament(
                        tournament_id,
                        tournament_data[0],
                        tournament_data[1],
                        tournament_data[2],
                        tournament_data[3],
                        int(tournament_data[4]),
                        tournament_data[5],
                    )
                    new_tournament.json_save()

            except FileNotFoundError:
                tournament_json = json.loads('{"tournament_id_ref": 1}')
                tournament_id_ref = 1
                tournament_id = build_tournament_id(tournament_id_ref)
                new_tournament = Tournament(
                    tournament_id,
                    tournament_data[0],
                    tournament_data[1],
                    tournament_data[2],
                    tournament_data[3],
                    int(tournament_data[4]),
                    tournament_data[5],
                )
                new_tournament.json_save()

            tournament_json["tournament_id_ref"] = tournament_id_ref + 1
            with open(JSON_TOUR_ID_FILENAME, "w") as json_tournament_id_file:
                json.dump(tournament_json, json_tournament_id_file)

            # print(new_tournament.__dict__)
            print("le tournoi a été créé")
            time.sleep(1)
            self.control_start(menu)
        elif choice == "manage_tournament":
            self.control_tournaments_list(menu)
        elif choice == "tournaments_list":
            self.display_tournaments_list(menu)
        elif choice == "players_list":
            self.display_players_list(menu)
        elif choice == "exit":
            print("Au revoir")
        else:
            print("choix non valide")
            time.sleep(1)
            self.control_start(menu)

    def control_tournaments_list(self, menu):
        tournament_list = []
        file_exist = False
        try:
            with open(JSON_TOUR_FILENAME, "r") as file_json:
                file_exist = True
                json_tournament_list_dict = json.load(file_json)
                for tournament in json_tournament_list_dict[
                    "tournaments_list"
                ]:
                    tournament_list.append(
                        [
                            tournament["tournament_id"],
                            tournament["name"],
                            tournament["location"],
                            tournament["start_date"],
                            tournament["end_date"],
                        ]
                    )
        except FileNotFoundError:
            file_exist = False

        if file_exist:
            tournament_id = menu.tournaments_list(tournament_list)
            # print(tournament_id)
            json2object = Json2Object()
            tournament = json2object.tournament(tournament_id)
            self.control_update_tournament(menu, tournament)
        else:
            print("Aucun tournoi n'existe pour l'instant")
            time.sleep(1)
            self.control_start(menu)

    def display_tournaments_list(self, menu):
        tournament_list = []
        file_exist = False
        try:
            with open(JSON_TOUR_FILENAME, "r") as file_json:
                file_exist = True
                json_tournament_list_dict = json.load(file_json)
                for tournament in json_tournament_list_dict[
                    "tournaments_list"
                ]:
                    tournament_list.append(
                        [
                            tournament["tournament_id"],
                            tournament["name"],
                            tournament["location"],
                            tournament["start_date"],
                            tournament["end_date"],
                            tournament["number_of_rounds"],
                            tournament["current_round"],
                        ]
                    )
        except FileNotFoundError:
            file_exist = False

        if file_exist:
            menu.display_tournaments_list(tournament_list)
        else:
            print("Aucun tournoi n'existe pour l'instant")
            time.sleep(1)

        self.control_start(menu)

    def display_players_list(self, menu):
        players_list = {}
        try:
            # load the player list
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                players_list = json_players_list_dict["players_list"]
        except FileNotFoundError:
            pass

        menu.display_players_list(players_list)
        self.control_start(menu)

    def control_update_tournament(self, menu, tournament):
        choice = menu.tournament_update(tournament)
        if choice == "manage_tournament":
            self.control_manage_tournament(menu, tournament)
        elif choice == "display_players":
            self.display_tournament_players_list(menu, tournament)
        elif choice == "add_players":
            self.control_tournament_players_list(menu, tournament)
        elif choice == "list_rounds":
            self.display_rounds(menu, tournament)
        elif choice == "create_round":
            self.control_create_round(menu, tournament)
        elif choice == "input_results":
            self.control_input_result(menu, tournament)
        elif choice == "close_current_round":
            self.control_close_round(menu, tournament)
        elif choice == "back":
            self.control_tournaments_list(menu)
        elif choice == "mainmenu":
            self.control_start(menu)

    def control_manage_tournament(self, menu, tournament):
        menu.manage_tournament(tournament)
        tournament.json_save()
        self.control_update_tournament(menu, tournament)

    def display_tournament_players_list(self, menu, tournament):
        # Dispay the players list from the tournament ranking
        # additional data come from the players file : JSON_PLAY_FILENAME
        tournament_players_list = {}
        try:
            # load the player list
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                players_list = json_players_list_dict["players_list"]
                for rank in tournament.ranking:
                    player_data = []
                    for player in players_list:
                        if (
                            rank.national_chess_id
                            == player["national_chess_id"]
                        ):
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
        # print(tournament_players_list)
        menu.display_tournament_players_list(
            tournament, tournament_players_list
        )
        self.control_update_tournament(menu, tournament)

    def control_tournament_players_list(self, menu, tournament):
        # Create the players list from the tournament ranking
        # additional data come from the players file : JSON_PLAY_FILENAME
        tournament_players_list = {}
        try:
            # load the player list
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                players_list = json_players_list_dict["players_list"]
                for rank in tournament.ranking:
                    player_data = []
                    for player in players_list:
                        if (
                            rank.national_chess_id
                            == player["national_chess_id"]
                        ):
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
        # print(tournament_players_list)
        player_id = menu.tournament_players_list(
            tournament, tournament_players_list
        )
        # print("control_player_list :", player_id)
        # time.sleep(1)
        if player_id == "back":
            self.control_update_tournament(menu, tournament)
        else:
            # print("control_player_list with Player ID")
            # time.sleep(1)
            self.control_create_player(menu, tournament, player_id)

    def control_create_player(self, menu, tournament, player_id):
        # print("control_create_player")
        # time.sleep(1)
        player_found = False
        try:
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                players_list = json_players_list_dict["players_list"]
                player_to_add = []
                for player in players_list:
                    if player_id == player["national_chess_id"]:
                        player_to_add.append(player_id)
                        player_to_add.append(player["name"])
                        player_to_add.append(player["surname"])
                        player_to_add.append(player["birth_date"])
                        player_found = True
                        # print("control_create_player player_found =",
                        #  player_found)
                        # print(player_to_add)
                        # time.sleep(1)
                        break
        except FileNotFoundError:
            pass

        # print("control_create_player player_found =", player_found)
        # time.sleep(1)
        if player_found:
            # print("control_create_player add_player_from_file")
            # time.sleep(1)
            choice = menu.add_player_from_file(player_to_add, tournament)
            if choice:
                tournament.register_player(player_id)
                tournament.json_save()
            self.control_tournament_players_list(menu, tournament)
        else:
            player_data = menu.add_new_player(tournament, player_id)
            # create player with data from view
            # 0-> name
            # 1-> surname
            # 2-> birth date
            new_player = Player(
                player_data[0], player_data[1], player_id, player_data[2]
            )
            new_player.json_save()
            tournament.register_player(player_id)
            tournament.json_save()
            self.control_tournament_players_list(menu, tournament)

    def round_players_list(self, round):
        with open(JSON_PLAY_FILENAME, "r") as file_json:
            json_players_list_dict = json.load(file_json)
            players_list = json_players_list_dict["players_list"]

        round_players_list = []
        for game in round.games:
            players_id = []
            # get the players id from the game
            for key in game.result.keys():
                players_id.append(key)
            player_id = players_id[0]
            other_player_id = players_id[1]

            player_score = game.result[player_id]
            other_player_score = game.result[other_player_id]

            # get the player data corresponding to the players
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

    def control_create_round(self, menu, tournament):
        previous_round = tournament.rounds[-1]
        if previous_round.end_date is None:
            print(
                "Merci de fermer la ronde précédente",
                "avant de créer la nouvelle",
            )
            time.sleep(2)
            self.control_update_tournament(menu, tournament)
        else:
            tournament.create_round()
            tournament.json_save()
            round = tournament.rounds[-1]
            round_players_list = self.round_players_list(round)

            menu.created_round(tournament, round_players_list)
            self.control_update_tournament(menu, tournament)

    def update_score(self, tournament, result):
        round = tournament.rounds[-1]
        player_id = result[1]
        result_type = result[0]

        if result_type == "v":
            player_score = 1
            other_player_score = 0
        else:
            player_score = 0.5
            other_player_score = 0.5

        for game in round.games:
            if player_id in game.result:
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

                game.store_result(
                    player_id,
                    player_score,
                    other_player_id,
                    other_player_score,
                )
                tournament.ranking.store_score(player_id, player_score)
                tournament.ranking.store_score(
                    other_player_id, other_player_score
                )
                tournament.json_save()
                break

    def control_input_result(self, menu, tournament):
        round = tournament.rounds[-1]
        round_players_list = self.round_players_list(round)

        result = menu.input_result(tournament, round_players_list)
        if result[0] == "back":
            self.control_update_tournament(menu, tournament)
        else:
            self.update_score(tournament, result)
            print("résultats mis à jour.")
            time.sleep(1)
            self.control_input_result(menu, tournament)

    def display_rounds(self, menu, tournament):
        full_rounds_list = {}
        for round in tournament.rounds:
            round_players_list = self.round_players_list(round)
            round_data = {round.name: round_players_list}
            full_rounds_list.update(round_data)

        # print(full_rounds_list)

        menu.display_rounds(tournament, full_rounds_list)
        self.control_update_tournament(menu, tournament)

    def control_close_round(self, menu, tournament):
        round = tournament.rounds[-1]
        # first check if all the results are stored
        all_results_in = True
        for game in round.games:
            sum_scores = 0
            for key in game.result.keys():
                sum_scores = sum_scores + game.result[key]
            # if the sum of all the score of the game is zero
            # it means no score has been stored
            if sum_scores == 0:
                all_results_in = False
                break

        if all_results_in:
            choice = menu.close_round()
            if choice:
                round.end_round()
                print("Ronde close")
                time.sleep(1)
        else:
            print(
                "Veuillez compléter tous les résultats de la ronde",
                " avant de la clore",
            )
            time.sleep(2)
        self.control_update_tournament(menu, tournament)

    def run(self, menu):
        self.control_start(menu)