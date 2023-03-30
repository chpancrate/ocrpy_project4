import time
from datetime import datetime
import json
from .controller_functions import (
    build_tournament_id,
    retrieve_tournament_players_data,
    update_score,
    build_tournament_info,
    create_round_players_list,
    retrieve_tournament_list,
)
from models.models import (
    Json2Object,
    Player,
    Tournament,
    JSON_TOUR_FILENAME,
    JSON_TOUR_ID_FILENAME,
    JSON_PLAY_FILENAME,
)


class Controller:
    def __init__(self, view, report):
        self.menu = view
        self.report = report

    def control_start(self):
        """start menu of the aplication"""
        choice = self.menu.start()
        if choice == "create_tournament":
            tournament_data = self.menu.tournament_creation()
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

            print("le tournoi a été créé")
            time.sleep(1)
            self.control_start()
        elif choice == "manage_tournament":
            self.control_tournaments_list()
        elif choice == "tournaments_list":
            self.display_tournaments_list()
        elif choice == "players_list":
            self.display_players_list()
        elif choice == "reports":
            self.control_reports_list()
        elif choice == "exit":
            print("Au revoir")
        else:
            print("choix non valide")
            time.sleep(1)
            self.control_start()

    def control_tournaments_list(self):
        """tournament lists used to select the tournament to update
        the list is retrieved from the json file
        """
        tournament_list = retrieve_tournament_list()

        if tournament_list != []:
            # if the file exist we can display the list
            # and ask for the tournament to update
            tournament_id = self.menu.tournaments_list(tournament_list)
            # with the id we recreate the tournament object
            json2object = Json2Object()
            tournament = json2object.tournament(tournament_id)
            self.control_update_tournament(tournament)
        else:
            # if the list is empty no tournament can be updated
            print("Aucun tournoi n'existe pour l'instant")
            time.sleep(1)
            self.control_start()

    def display_tournaments_list(self):
        """create the full tournament list report
        and call the view to display it
        """
        tournament_list = []
        file_exist = False
        try:
            with open(JSON_TOUR_FILENAME, "r") as file_json:
                file_exist = True
                json_tournament_list_dict = json.load(file_json)
                for tournament in json_tournament_list_dict[
                    "tournaments_list"
                ]:
                    sorting_date = datetime.strptime(
                        tournament["start_date"], "%d/%m/%Y"
                    )
                    tournament_list.append(
                        [
                            tournament["tournament_id"],
                            tournament["name"],
                            tournament["location"],
                            tournament["start_date"],
                            tournament["end_date"],
                            tournament["number_of_rounds"],
                            tournament["current_round"],
                            sorting_date,
                        ]
                    )
        except FileNotFoundError:
            file_exist = False

        if file_exist:
            # the file exist there is data
            # call the view to display the data
            self.menu.display_tournaments_list(tournament_list)
        else:
            print("Aucun tournoi n'existe pour l'instant")
            time.sleep(1)

        # we are back from the view or no list exist
        # we go back to the start menu
        self.control_start()

    def display_players_list(self):
        """create full list of user and call the view to display it"""
        players_list = {}
        try:
            # load the player list
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                players_list = json_players_list_dict["players_list"]
        except FileNotFoundError:
            pass

        # call the view to display the data
        self.menu.display_players_list(players_list)

        # we are back from the view we go back to the start menu
        self.control_start()

    def control_update_tournament(self, tournament):
        """control the menu for all the options concerning a tournament"""
        tournament_info = build_tournament_info(tournament)
        if tournament.rounds == []:
            rounds_exist = False
        else:
            rounds_exist = True
        choice = self.menu.tournament_update(tournament_info, rounds_exist)
        if choice == "manage_tournament":
            self.control_manage_tournament(tournament)
        elif choice == "display_players":
            self.display_tournament_players_list(tournament)
        elif choice == "add_players":
            self.control_tournament_players_list(tournament)
        elif choice == "list_rounds":
            self.display_rounds(tournament)
        elif choice == "create_round":
            self.control_create_round(tournament)
        elif choice == "input_results":
            self.control_input_result(tournament)
        elif choice == "close_current_round":
            self.control_close_round(tournament)
        elif choice == "tournament_ranking":
            self.display_tournament_ranking(tournament)
        elif choice == "back":
            self.control_tournaments_list()
        elif choice == "mainmenu":
            self.control_start()

    def control_manage_tournament(self, tournament):
        """control the tournament information management screen"""
        tournament_info = build_tournament_info(tournament)
        if tournament.rounds == []:
            rounds_exist = False
        else:
            rounds_exist = True
        self.menu.manage_tournament(tournament_info, rounds_exist)
        tournament.name = tournament_info["name"]
        tournament.location = tournament_info["location"]
        tournament.start_date = tournament_info["start_date"]
        tournament.end_date = tournament_info["end_date"]
        tournament.number_of_rounds = tournament_info["number_of_rounds"]
        tournament.current_round = tournament_info["current_round"]
        tournament.description = tournament_info["description"]
        tournament.json_save()
        self.control_update_tournament(tournament)

    def display_tournament_players_list(self, tournament):
        """control the report on tournament players list
        only display the data
        """
        tournament_players_list = retrieve_tournament_players_data(tournament)
        tournament_info = build_tournament_info(tournament)
        self.menu.display_tournament_players_list(
            tournament_info, tournament_players_list
        )
        self.control_update_tournament(tournament)

    def control_tournament_players_list(self, tournament):
        """control tournament players list managment screen
        retrieve information in order to add player to tournament ranking
        """
        tournament_players_list = retrieve_tournament_players_data(tournament)
        tournament_info = build_tournament_info(tournament)
        player_id = self.menu.tournament_players_list(
            tournament_info, tournament_players_list
        )
        if player_id == "back":
            self.control_update_tournament(tournament)
        else:
            self.control_create_player(tournament, player_id)

    def control_create_player(self, tournament, player_id):
        """control the addition of player in a tournament ranking
        check if the player already exist in the players file
        if yes : propose to add it
        if not : propose to create it
        """
        player_found = False
        try:
            # open the players file and check if the palyer exist
            # if yes retrieve the data for the player
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
                        break
        except FileNotFoundError:
            pass

        tournament_info = build_tournament_info(tournament)
        if player_found:
            # the player was found, propose to register it, if yes do it
            choice = self.menu.add_player_from_file(
                player_to_add, tournament_info
            )
            if choice:
                tournament.register_player(player_id)
                tournament.json_save()
            self.control_tournament_players_list(tournament)
        else:
            # the player was not found ask for the information
            # needed to create it, and add it to the tournament
            player_data = self.menu.add_new_player(tournament_info, player_id)
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
            self.control_tournament_players_list(tournament)

    def control_create_round(self, tournament):
        """control the round creation, check if the previous round is closed
        if not alert the user
        if yes create the round
        """
        if tournament.rounds != []:
            # rounds exist
            previous_round = tournament.rounds[-1]
            if previous_round.end_date is None:
                # previous round is not closed
                print(
                    "Merci de fermer la ronde précédente",
                    "avant de créer la nouvelle",
                )
                time.sleep(2)
                self.control_update_tournament(tournament)
            elif tournament.current_round < tournament.number_of_rounds:
                tournament.create_round()
                tournament.json_save()
                round = tournament.rounds[-1]
                round_players_list = create_round_players_list(round)

                tournament_info = build_tournament_info(tournament)
                self.menu.created_round(tournament_info, round_players_list)
                self.control_update_tournament(tournament)
            else:
                print("le nombre de rondes maximum est atteint")
                time.sleep(2)
                self.control_update_tournament(tournament)
        else:
            # no rounds exist and
            if tournament.ranking == []:
                # the ranking is empty no players are registered
                print(
                    "Aucun joueur n'est inscris. Merci de procéder aux",
                    " inscriptions avant de créer la nouvelle ronde",
                )
                time.sleep(2)
                self.control_update_tournament(tournament)
            else:
                # the ranking is not empty we can create a round
                tournament.create_round()
                tournament.json_save()
                round = tournament.rounds[-1]
                round_players_list = create_round_players_list(round)

                tournament_info = build_tournament_info(tournament)
                self.menu.created_round(tournament_info, round_players_list)
                self.control_update_tournament(tournament)

    def control_input_result(self, tournament):
        """control the result input screen"""

        if tournament.rounds == []:
            # there is no round, input result is not possible
            print("aucune ronde n'existe pour ce tournoi !")
            time.sleep(2)
            self.control_update_tournament(tournament)
        else:
            round = tournament.rounds[-1]
            round_players_list = create_round_players_list(round)

            tournament_info = build_tournament_info(tournament)
            result = self.menu.input_result(
                tournament_info, round_players_list
            )
            if result[0] == "back":
                self.control_update_tournament(tournament)
            else:
                update_score(tournament, result)
                print("résultats mis à jour.")
                time.sleep(1)
                self.control_input_result(tournament)

    def display_rounds(self, tournament):
        """control the full rounds and matchs report"""
        full_rounds_list = {}
        for round in tournament.rounds:
            round_players_list = create_round_players_list(round)
            round_data = {round.name: round_players_list}
            full_rounds_list.update(round_data)

        # print(full_rounds_list)
        tournament_info = build_tournament_info(tournament)
        self.menu.display_rounds(tournament_info, full_rounds_list)
        self.control_update_tournament(tournament)

    def control_close_round(self, tournament):
        """control the round closure process
        all the results of the round must be entered to allow closure
        """
        if tournament.rounds == []:
            # there is no round, impossible to close one
            print("aucune ronde n'existe pour ce tournoi !")
            time.sleep(2)
            self.control_update_tournament(tournament)
        else:
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
                choice = self.menu.close_round()
                if choice:
                    round.end_round()
                    tournament.json_save()
                    print("Ronde close")
                    time.sleep(1)
            else:
                print(
                    "Veuillez compléter tous les résultats de la ronde",
                    " avant de la clore",
                )
                time.sleep(2)
            self.control_update_tournament(tournament)

    def display_tournament_ranking(self, tournament):
        """control the display of the tournament ranking"""
        tournament_ranking = {}
        try:
            # load the players data from the file
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                players_list = json_players_list_dict["players_list"]
                # for each player_id in the ranking, complete the data
                for rank in tournament.ranking:
                    player_data = []
                    for player in players_list:
                        if (
                            rank.national_chess_id
                            == player["national_chess_id"]
                        ):
                            player_data.append(player["name"])
                            player_data.append(player["surname"])
                            player_data.append(float(rank.total_score))
                            player_update = {}
                            player_update[
                                player["national_chess_id"]
                            ] = player_data
                            tournament_ranking.update(player_update)
                            break
        except FileNotFoundError:
            pass

        tournament_info = build_tournament_info(tournament)
        self.menu.display_tournament_ranking(
            tournament_info, tournament_ranking
        )
        self.control_update_tournament(tournament)

    def control_reports_list(self):
        choice = self.menu.reports_list()
        if choice == "players_list_report":
            self.report_players_list()
        elif choice == "tournaments_list_report":
            self.report_tournaments_list()
        elif choice == "tournament_report":
            self.control_report_tournament(choice)
        elif choice == "tournament_players_report":
            self.control_report_tournament(choice)
        elif choice == "tournament_rounds_report":
            self.control_report_tournament(choice)
        elif choice == "back":
            self.control_start()

    def control_report_tournament(self, choice):
        tournament_list = retrieve_tournament_list()

        if tournament_list != []:
            # if the file exist we can display the list
            # and ask for the tournament to update
            tournament_id = self.menu.tournaments_list(tournament_list)
            # with the id we recreate the tournament object
            json2object = Json2Object()
            tournament = json2object.tournament(tournament_id)
            if choice == "tournament_report":
                tournament_info = {}
                tournament_info["tournament_id"] = tournament.tournament_id
                tournament_info["name"] = tournament.name
                tournament_info["start_date"] = tournament.start_date
                tournament_info["end_date"] = tournament.end_date
                self.report.tournament(tournament_info)
                self.control_reports_list()
            elif choice == "tournament_players_report":
                tournament_players_list = retrieve_tournament_players_data(
                    tournament
                )
                tournament_info = build_tournament_info(tournament)
                self.report.tournament_players(
                    tournament_info, tournament_players_list
                )
                self.control_reports_list()
            elif choice == "tournament_rounds_report":
                tournament_info = build_tournament_info(tournament)
                full_rounds_list = {}
                for round in tournament.rounds:
                    round_players_list = create_round_players_list(round)
                    round_data = {round.name: round_players_list}
                    full_rounds_list.update(round_data)

                self.report.tournament_rounds(
                    tournament_info, full_rounds_list
                )
                self.control_reports_list()
        else:
            # if the list is empty no tournament can be updated
            print("Aucun tournoi n'existe pour l'instant")
            time.sleep(1)
            self.control_reports_list()

    def report_players_list(self):
        """create the full list of players
        and call the report to print it in a file
        """
        players_list = {}
        try:
            # load the player list
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                players_list = json_players_list_dict["players_list"]
        except FileNotFoundError:
            pass

        # call the view to create the report file
        self.report.players_list(players_list)

        # we are back from the view we go back to the start menu
        self.control_reports_list()

    def report_tournaments_list(self):
        """create the full tournament list of players
        and call the report to print it in a file
        """
        tournament_list = []
        try:
            with open(JSON_TOUR_FILENAME, "r") as file_json:
                json_tournament_list_dict = json.load(file_json)
                for tournament in json_tournament_list_dict[
                    "tournaments_list"
                ]:
                    sorting_date = datetime.strptime(
                        tournament["start_date"], "%d/%m/%Y"
                    )
                    tournament_list.append(
                        [
                            tournament["tournament_id"],
                            tournament["name"],
                            tournament["location"],
                            tournament["start_date"],
                            tournament["end_date"],
                            tournament["number_of_rounds"],
                            tournament["current_round"],
                            sorting_date,
                        ]
                    )
        except FileNotFoundError:
            pass

        # call the view to create the report file
        self.report.tournaments_list(tournament_list)

        # we are back from the view we go back to the start menu
        self.control_reports_list()

    def run(self):
        self.control_start()
