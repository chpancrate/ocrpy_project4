"""views classes for chess tournament management software"""
import time
from datetime import datetime
import os
from prettytable import PrettyTable
from .views_functions import (
    check_national_chess_id_format,
    check_tournament_id_format,
    header,
    header_creation,
    header_update,
    header_tournament,
    tournament_information,
    separator,
    round_list,
)
from models.models import DEFAULT_NUMBER_OF_ROUND

DATE_FORMAT = "%d/%m/%Y"
WRONG_ID_FORMAT_MESSAGE = (
    "Le format du l'indentifiant n'est pas bon (ex : AB12345)"
)
WRONG_DATE_FORMAT_MESSAGE = (
    "Date ou format de date incorrects,"
    " le format de la date doit être JJ/MM/DDDD"
)
REPORT_DIR_NAME = "rapports/"
REPORT_FULL_PLAYER_LIST_NAME = "liste_complete_des_joueurs_"
REPORT_FULL_TOURNAMENT_LIST_NAME = "liste_complete_des_tournois_"
REPORT_TOURNAMENT_INFO_NAME = "Informations_tournoi_"
REPORT_TOURNAMENT_PLAYERS_NAME = "liste_des_joueurs_"
REPORT_TOURNAMENT_ROUNDS_NAME = "liste_des rondes_"


class Menu:
    def start(self):
        """dispaly the start menu"""
        header()
        print("1 - Créer un tournoi")
        print("2 - Visualiser ou modifier un tournoi")
        print("3 - Liste des tournois")
        print("4 - Liste des joueurs")
        print("5 - Rapports")
        print("s - Sortir")
        separator()
        choice = input("Quel est votre choix ? : ")
        if choice == "1":
            return "create_tournament"
        elif choice == "2":
            return "manage_tournament"
        elif choice == "3":
            return "tournaments_list"
        elif choice == "4":
            return "players_list"
        elif choice == "5":
            return "reports"
        elif choice == "s":
            return "exit"
        else:
            return "invalid"

    def tournament_creation(self):
        """display the tournament creation query"""
        header_creation()
        tournament_data = []
        name = input("Quel est le nom du tournoi ? : ")
        tournament_data.append(name)
        location = input("Ou aura-t-il lieu ? : ")
        tournament_data.append(location)

        good_format = False
        while not good_format:
            start_date = input("A quelle date commencera-t-il ? : ")
            try:
                tournament_start = datetime.strptime(start_date, DATE_FORMAT)
                good_format = True
            except ValueError:
                print(WRONG_DATE_FORMAT_MESSAGE)
        tournament_data.append(start_date)

        good_format = False
        while not good_format:
            end_date = input("Quand se terminera-t-il ? : ")
            try:
                tournament_end = datetime.strptime(end_date, DATE_FORMAT)
                good_format = True
            except ValueError:
                print(WRONG_DATE_FORMAT_MESSAGE)
            if tournament_end < tournament_start:
                print(
                    (
                        "La date de fin doit être posterieure"
                        " à la date de début"
                    )
                )
                good_format = False

        tournament_data.append(end_date)

        good_format = False
        while not good_format:
            number_of_rounds = input(
                "Combien de rondes voulez vous (défaut = 4)? : "
            )
            if number_of_rounds == "":
                number_of_rounds = DEFAULT_NUMBER_OF_ROUND
                good_format = True
            elif number_of_rounds.isdigit():
                good_format = True
            else:
                print("Entrer un nombre entier.")
        tournament_data.append(number_of_rounds)

        description = input("Informations complémentaires : ")
        tournament_data.append(description)

        return tournament_data

    def tournaments_list(self, tournament_list):
        """display the tournaments list for selection
        of a tournament by the user
        """
        header()
        print("*            Listes des tournois pour sélection            *")
        print("------------------------------------------------------------")
        table = PrettyTable()
        table.field_names = [
            "Identifiant",
            "Nom",
            "lieu",
            "Date de début",
            "Date de fin",
            "tri",
        ]
        for tournament in tournament_list:
            table.add_row(
                [
                    tournament[0],
                    tournament[1],
                    tournament[2],
                    tournament[3],
                    tournament[4],
                    tournament[5],
                ]
            )

        print(
            table.get_string(
                fields=[
                    "Identifiant",
                    "Nom",
                    "lieu",
                    "Date de début",
                    "Date de fin",
                ],
                sortby="tri",
            )
        )

        choice = input(
            "Entrer l'Id du tournoi que voulez-vous sélectionner : "
        )
        choice = choice.upper()
        if not check_tournament_id_format(choice):
            print("format de numero de tournoi érroné")
            time.sleep(1)
            choice = self.tournaments_list(tournament_list)
            return choice
        else:
            tournament_in_list = False
            for tournament in tournament_list:
                if tournament[0] == choice:
                    tournament_in_list = True
                    break
            if not tournament_in_list:
                print("Ce tournoi n'est pas dans la liste")
                time.sleep(1)
                choice = self.tournaments_list(tournament_list)
                return choice
            else:
                return choice

    def display_tournaments_list(self, tournament_list):
        """display the tournaments list report"""
        header()
        print("*               Liste complète des tournois                *")
        print("------------------------------------------------------------")
        table = PrettyTable()
        table.field_names = [
            "Identifiant",
            "Nom",
            "lieu",
            "Date de début",
            "Date de fin",
            "nombre de ronde",
            "ronde en cours",
            "tri",
        ]
        for tournament in tournament_list:
            table.add_row(
                [
                    tournament[0],
                    tournament[1],
                    tournament[2],
                    tournament[3],
                    tournament[4],
                    tournament[5],
                    tournament[6],
                    tournament[7],
                ]
            )

        print(
            table.get_string(
                fields=[
                    "Identifiant",
                    "Nom",
                    "lieu",
                    "Date de début",
                    "Date de fin",
                    "nombre de ronde",
                    "ronde en cours",
                ],
                sortby="tri",
            )
        )

        input("Appuyer sur entrée pour revenir au menu précédent")

    def tournament_update(self, tournament_info, rounds_exist):
        """display the tournament update menu"""
        good_choice = False
        while not good_choice:
            header_update()
            header_tournament(tournament_info)
            print("1 - Gérer les données générales du tournoi")
            print("2 - Visualiser la liste des joueurs")
            print("3 - Modifier la liste des joueurs")
            print("4 - Liste des rondes et des matchs")
            print("5 - Créer la prochaine ronde")
            print("6 - Entrer les résultats de la ronde en cours")
            print("7 - terminer la ronde en cours")
            print("8 - afficher le classement du tournoi")
            print("r - revenir au menu précédent")
            print("p - revenir au menu principal")
            separator()
            choice = input("Quel est votre choix ? : ")
            if choice == "1":
                return "manage_tournament"
            elif choice == "2":
                return "display_players"
            elif choice == "3":
                if not rounds_exist:
                    return "add_players"
                else:
                    print(
                        "une ronde existe pour ce tournoi la liste de",
                        "joueurs ne peut pas être modifiée",
                    )
                    time.sleep(2)
            elif choice == "4":
                return "list_rounds"
            elif choice == "5":
                return "create_round"
            elif choice == "6":
                return "input_results"
            elif choice == "7":
                return "close_current_round"
            elif choice == "8":
                return "tournament_ranking"
            elif choice == "r":
                return "back"
            elif choice == "p":
                return "mainmenu"
            else:
                print("Choix non valide")
                time.sleep(1)

    def manage_tournament(self, tournament_info, rounds_exist):
        """display the tournament data management screen"""
        header_update()
        tournament_information(tournament_info)
        if not rounds_exist:
            print("pour modifier saisir la lettre correspondante :")
            print("(n)om, (l)ieu, (d)ébut, (f)in =), (r)ondes, d(e)scritpion")
            choice = input(
                (
                    "Quelle information doit être modifier ?"
                    " (xx pour sortir) : "
                )
            )
            if choice == "n":
                tournament_info["name"] = input("Entrer le nouveau nom : ")
                self.manage_tournament(tournament_info, rounds_exist)
            elif choice == "l":
                tournament_info["location"] = input(
                    "Entrer le nouveau lieu : "
                )
                self.manage_tournament(tournament_info, rounds_exist)
            elif choice == "d":
                good_format = False
                while not good_format:
                    start_date = input("Entrer la nouvelle date de début : ")
                    try:
                        tournament_start = datetime.strptime(
                            start_date, DATE_FORMAT
                        )
                        good_format = True
                    except ValueError:
                        print(WRONG_DATE_FORMAT_MESSAGE)
                tournament_info["start_date"] = start_date
                self.manage_tournament(tournament_info, rounds_exist)
            elif choice == "f":
                good_format = False
                while not good_format:
                    end_date = input("Entrer la nouvelle date de fin : ")
                    try:
                        tournament_end = datetime.strptime(
                            end_date, DATE_FORMAT
                        )
                        good_format = True
                    except ValueError:
                        print(WRONG_DATE_FORMAT_MESSAGE)
                    tournament_start = datetime.strptime(
                        tournament_info["start_date"], DATE_FORMAT
                    )
                    if tournament_end < tournament_start:
                        print(
                            (
                                "La date de fin doit être posterieure"
                                " à la date de début"
                            )
                        )
                        good_format = False
                tournament_info["end_date"] = end_date
                self.manage_tournament(tournament_info, rounds_exist)
            elif choice == "r":
                tournament_info["number_of_rounds"] = input(
                    "Entrer le nouveau nombre de rondes : "
                )
                self.manage_tournament(tournament_info, rounds_exist)
            elif choice == "e":
                tournament_info["description"] = input(
                    "Entrer la nouvelle description : "
                )
                self.manage_tournament(tournament_info, rounds_exist)
            elif choice == "xx":
                return
            else:
                print("choix invalide")
                time.sleep(1)
                self.manage_tournament(tournament_info, rounds_exist)
        else:
            print(
                (
                    "Le tournoi est démarré, seule la description"
                    " peut être modifiée"
                )
            )
            choice = input(
                ("taper d pour modifier la description ou xx pour sortir : ")
            )
            if choice == "xx":
                return
            elif choice == "d":
                tournament_info["description"] = input(
                    "Saisir la nouvelle description : "
                )
                self.manage_tournament(tournament_info, rounds_exist)
            else:
                print("choix invalide")
                time.sleep(1)
                self.manage_tournament(tournament_info, rounds_exist)

    def display_tournament_players_list(
        self, tournament_info, tournament_players_list
    ):
        """display the tournament players report"""
        header_update()
        header_tournament(tournament_info)
        print("Liste des joueurs du Tournoi :")
        table = PrettyTable()
        table.field_names = [
            "Identifiant",
            "Nom",
            "Prènom",
            "Date de naissance",
        ]

        for player_id in tournament_players_list.keys():
            table.add_row(
                [
                    player_id,
                    tournament_players_list[player_id][0],
                    tournament_players_list[player_id][1],
                    tournament_players_list[player_id][2],
                ]
            )

        table.align["Identifiant"] = "c"
        table.align["Nom"] = "l"
        table.align["Prènom"] = "l"
        table.align["Date de naissance"] = "c"
        print(table.get_string(sortby="Nom"))

        input("Appuyer sur entrée pour revenir au menu précédent")

    def tournament_players_list(
        self, tournament_info, tournament_players_list
    ):
        """display the tournament players list screen for update of the list"""
        header_update()
        header_tournament(tournament_info)
        print("Liste des joueurs du Tournoi :")
        table = PrettyTable()
        table.field_names = [
            "Identifiant",
            "Nom",
            "Prènom",
            "Date de naissance",
        ]

        for player_id in tournament_players_list.keys():
            table.add_row(
                [
                    player_id,
                    tournament_players_list[player_id][0],
                    tournament_players_list[player_id][1],
                    tournament_players_list[player_id][2],
                ]
            )

        table.align["Identifiant"] = "c"
        table.align["Nom"] = "l"
        table.align["Prènom"] = "l"
        table.align["Date de naissance"] = "c"
        print(table.get_string(sortby="Nom"))

        print("Entrer l'identifiant national d'echec du joueur à ajouter")
        good_format = False
        while not good_format:
            player_id = input("Entrer xx pour revenir en arrière : ")
            player_id = player_id.upper()
            if player_id == "XX":
                return "back"
            elif check_national_chess_id_format(player_id):
                player_already_registered = False
                for list_player_id in tournament_players_list.keys():
                    if list_player_id == player_id:
                        player_already_registered = True
                        print("Le joueur est déjà inscrit.")
                if not player_already_registered:
                    return player_id
            else:
                print(WRONG_ID_FORMAT_MESSAGE)

    def add_player_from_file(self, player_to_add, tournament_info):
        """display the questions to add a player from the players file"""
        header_update()
        header_tournament(tournament_info)
        print("Le joueur suivant a été trouvé dans le fichier des joueurs :")
        print("Identifiant nationale d'èchec :", player_to_add[0])
        print("Nom :", player_to_add[1])
        print("Prénom :", player_to_add[2])
        print("Date de naissance :", player_to_add[3])
        choice = input("voulez-vous l'ajouter ? (o/n) : ")
        if choice == "o":
            return True
        else:
            return False

    def add_new_player(self, tournament_info, player_id):
        """display the questions to create a new player"""
        header_update()
        header_tournament(tournament_info)
        player_data = []
        print(
            "Création du joueur avec l'identifiant national d'échecs :",
            player_id,
        )
        name = input("Quel est son nom? : ")
        player_data.append(name)
        surname = input("Quel est son prénom ? : ")
        player_data.append(surname)

        good_format = False
        while not good_format:
            birth_date = input("Quelle est sa date de naissance ? : ")
            try:
                datetime.strptime(birth_date, DATE_FORMAT)
                good_format = True
            except ValueError:
                print(WRONG_DATE_FORMAT_MESSAGE)

        player_data.append(birth_date)

        return player_data

    def created_round(self, tournament_info, round_players_list):
        """display the end screen of the round creation process"""
        header_update()
        header_tournament(tournament_info)
        separator()
        print("Détails de la nouvelle ronde :")
        round_list(round_players_list)
        input("Appuyer sur entrée pour revenir au menu précédent")

    def input_result(self, tournament_info, round_players_list):
        """display the screen for result input"""
        header_update()
        header_tournament(tournament_info)
        print("Détails de la ronde actuelle :")
        round_list(round_players_list)
        print("v : Saisir une victoire")
        print("n : Saisir un match nul")
        print("r : pour revenir en arrière")
        choice = input("quel est votre choix? : ")
        result = []
        if choice == "r":
            result = ["back"]
        elif choice == "v":
            good_format = False
            while not good_format:
                player_id = input("Saisir l'id du joueur victorieux : ")
                player_id = player_id.upper()
                if check_national_chess_id_format(player_id):
                    result = [choice, player_id]
                    good_format = True
                else:
                    print(WRONG_ID_FORMAT_MESSAGE)
        elif choice == "n":
            good_format = False
            while not good_format:
                player_id = input("Saisir l'id de l'un des deux joueurs : ")
                player_id = player_id.upper()
                if check_national_chess_id_format(player_id):
                    result = [choice, player_id]
                    good_format = True
                else:
                    print(WRONG_ID_FORMAT_MESSAGE)
        else:
            print("Choix invalide")
            time.sleep(1)
            result = self.input_result(tournament_info, round_players_list)
        return result

    def display_players_list(self, players_list):
        """display the full players list report"""
        header()
        print("*                Liste complète des joueurs                *")
        print("------------------------------------------------------------")
        table = PrettyTable()

        table.field_names = [
            "Identifiant",
            "Nom",
            "Prènom",
            "Date de naissance",
        ]

        for player in players_list:
            table.add_row(
                [
                    player["national_chess_id"],
                    player["name"],
                    player["surname"],
                    player["birth_date"],
                ]
            )

        table.align["Identifiant"] = "c"
        table.align["Nom"] = "l"
        table.align["Prènom"] = "l"
        table.align["Date de naissance"] = "c"
        print(table.get_string(sortby="Nom"))

        input("Appuyer sur entrée pour revenir au menu précédent")

    def display_rounds(self, tournament_info, full_rounds_list):
        """display the full round and match report"""
        header()
        header_tournament(tournament_info)
        print("*                Liste complète des Rondes                 *")
        print("------------------------------------------------------------")
        table = PrettyTable()

        table.field_names = [
            "Premier joueur",
            "Score 1",
            "Deuxième joueur",
            "Score 2",
        ]
        table.align = "c"
        table.align["Premier joueur"] = "l"
        table.align["Deuxième joueur"] = "l"
        for round in full_rounds_list:
            table.clear_rows()
            print()
            round_data = full_rounds_list[round]
            if round_data["status"] == "opened":
                status = "ouverte"
            else:
                status = "close"
            print("***", round, "   ", status)
            for game in round_data["players_list"]:
                player1 = (
                    game["player1_id"]
                    + " "
                    + game["player1_name"]
                    + " "
                    + game["player1_surname"]
                )
                score1 = game["player1_score"]
                player2 = (
                    game["player2_id"]
                    + " "
                    + game["player2_name"]
                    + " "
                    + game["player2_surname"]
                )
                score2 = game["player2_score"]
                table.add_row([player1, score1, player2, score2])

            print(table)

        input("Appuyer sur entrée pour revenir au menu précédent")

    def close_round(self):
        """ask for round closure confiration"""
        choice = input("voulez-vous terminer la ronde en cours? (o/n) : ")
        if choice == "o":
            return True
        else:
            return False

    def display_tournament_ranking(self, tournament_info, tournament_ranking):
        """display the full tournament ranking"""
        header_update()
        header_tournament(tournament_info)
        print("*                   Classement du tournoi                   *")
        print("------------------------------------------------------------")
        table = PrettyTable()

        table.field_names = [
            "Identifiant",
            "Nom",
            "Prénom",
            "Score",
        ]
        table.align = "c"

        for key in tournament_ranking.keys():
            table.add_row(
                [
                    key,
                    tournament_ranking[key][0],
                    tournament_ranking[key][1],
                    tournament_ranking[key][2],
                ]
            )

        print(table.get_string(sortby="Score", reversesort=True))

        input("Appuyer sur entrée pour revenir au menu précédent")

    def reports_list(self):
        """display the reports menu"""
        header()
        print("*                         Rapports                         *")
        print("------------------------------------------------------------")
        print("1 - Liste de tous les joueurs")
        print("2 - Liste de tous les tournois")
        print("3 - nom et date d'un tournoi")
        print("4 - liste des joueurs d'un tournoi")
        print("5 - listes des rondes et matchs d'un tournoi")
        print("s - Sortir")
        separator()
        choice = input("Quel est votre choix ? : ")
        if choice == "1":
            return "players_list_report"
        elif choice == "2":
            return "tournaments_list_report"
        elif choice == "3":
            return "tournament_report"
        elif choice == "4":
            return "tournament_players_report"
        elif choice == "5":
            return "tournament_rounds_report"
        elif choice == "s":
            return "back"
        else:
            print("choix invalide")
            time.sleep(2)
            choice = self.reports_list()


class Report:
    """contains the view class creating reports"""

    def players_list(self, players_list):
        """export the full players list report in a file"""
        if not os.path.exists(REPORT_DIR_NAME):
            os.makedirs(REPORT_DIR_NAME)
        now = datetime.now()  # current date and time
        timestamp = now.strftime("%Y-%m-%d-%H_%M_%S")
        report_file_name = (
            REPORT_DIR_NAME + REPORT_FULL_PLAYER_LIST_NAME + timestamp + ".txt"
        )

        with open(report_file_name, "w", encoding="utf-8") as report_file:
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write(
                "*               Gestion de tournois d'échecs               *"
                "\n"
            )
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write("\n")
            report_file.write(
                "*****     Liste complète des joueurs     *****" "\n"
            )
            report_file.write("\n")

            table = PrettyTable()

            table.field_names = [
                "Identifiant",
                "Nom",
                "Prènom",
                "Date de naissance",
            ]

            for player in players_list:
                table.add_row(
                    [
                        player["national_chess_id"],
                        player["name"],
                        player["surname"],
                        player["birth_date"],
                    ]
                )

            table.align["Identifiant"] = "c"
            table.align["Nom"] = "l"
            table.align["Prènom"] = "l"
            table.align["Date de naissance"] = "c"
            report_file.write(table.get_string(sortby="Nom"))

        print("votre rapport a été créé dans le répertoire rapports")
        input("Appuyer sur entrée pour revenir au menu précédent")

    def tournaments_list(self, tournament_list):
        """export the full tournament list report in a file"""

        if not os.path.exists(REPORT_DIR_NAME):
            os.makedirs(REPORT_DIR_NAME)

        now = datetime.now()  # current date and time
        timestamp = now.strftime("%Y-%m-%d-%H_%M_%S")
        report_file_name = (
            REPORT_DIR_NAME
            + REPORT_FULL_TOURNAMENT_LIST_NAME
            + timestamp
            + ".txt"
        )

        with open(report_file_name, "w", encoding="utf-8") as report_file:
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write(
                "*               Gestion de tournois d'échecs               *"
                "\n"
            )
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write("\n")
            report_file.write(
                "*****     Liste complète des tournois     *****\n"
            )
            report_file.write("\n")

            table = PrettyTable()
            table.field_names = [
                "Identifiant",
                "Nom",
                "Lieu",
                "Date de début",
                "Date de fin",
                "Nb de rondes",
                "Actuelle",
                "tri",
            ]
            for tournament in tournament_list:
                table.add_row(
                    [
                        tournament[0],
                        tournament[1],
                        tournament[2],
                        tournament[3],
                        tournament[4],
                        tournament[5],
                        tournament[6],
                        tournament[7],
                    ]
                )

            report_file.write(
                table.get_string(
                    fields=[
                        "Identifiant",
                        "Nom",
                        "Lieu",
                        "Date de début",
                        "Date de fin",
                        "Nb de rondes",
                        "Actuelle",
                    ],
                    sortby="tri",
                )
            )
        print("votre rapport a été créé dans le répertoire rapports")
        input("Appuyer sur entrée pour revenir au menu précédent")

    def tournament(self, tournament_info):
        if not os.path.exists(REPORT_DIR_NAME):
            os.makedirs(REPORT_DIR_NAME)

        now = datetime.now()  # current date and time
        timestamp = now.strftime("%Y-%m-%d-%H_%M_%S")
        report_file_name = (
            REPORT_DIR_NAME
            + tournament_info["tournament_id"]
            + "_"
            + REPORT_TOURNAMENT_INFO_NAME
            + timestamp
            + ".txt"
        )

        with open(report_file_name, "w", encoding="utf-8") as report_file:
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write(
                "*               Gestion de tournois d'échecs               *"
                "\n"
            )
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write("\n")
            line = (
                "*****     Informations du tournoi : "
                + tournament_info["tournament_id"]
                + "     *****\n"
            )
            report_file.write(line)
            report_file.write("\n")
            line = "Nom du tournoi : " + tournament_info["name"] + "\n"
            report_file.write(line)
            line = "Date de début : " + tournament_info["start_date"] + "\n"
            report_file.write(line)
            line = "Date de fin : " + tournament_info["end_date"] + "\n"
            report_file.write(line)

        print("votre rapport a été créé dans le répertoire rapports")
        input("Appuyer sur entrée pour revenir au menu précédent")

    def tournament_players(self, tournament_info, tournament_players_list):
        if not os.path.exists(REPORT_DIR_NAME):
            os.makedirs(REPORT_DIR_NAME)

        now = datetime.now()  # current date and time
        timestamp = now.strftime("%Y-%m-%d-%H_%M_%S")
        report_file_name = (
            REPORT_DIR_NAME
            + tournament_info["tournament_id"]
            + "_"
            + REPORT_TOURNAMENT_PLAYERS_NAME
            + timestamp
            + ".txt"
        )

        with open(report_file_name, "w", encoding="utf-8") as report_file:
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write(
                "*               Gestion de tournois d'échecs               *"
                "\n"
            )
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write("\n")
            line = (
                "******     Liste de joueurs du tournoi : "
                + tournament_info["tournament_id"]
                + "     *****\n"
            )
            report_file.write(line)
            report_file.write("\n")
            line = "     " + tournament_info["name"] + "\n"
            report_file.write(line)
            line = (
                "     du "
                + tournament_info["start_date"]
                + " au "
                + tournament_info["end_date"]
                + "\n"
            )
            report_file.write(line)
            report_file.write("\n")

            table = PrettyTable()
            table.field_names = [
                "Identifiant",
                "Nom",
                "Prènom",
                "Date de naissance",
            ]

            for player_id in tournament_players_list.keys():
                table.add_row(
                    [
                        player_id,
                        tournament_players_list[player_id][0],
                        tournament_players_list[player_id][1],
                        tournament_players_list[player_id][2],
                    ]
                )

            table.align["Identifiant"] = "c"
            table.align["Nom"] = "l"
            table.align["Prènom"] = "l"
            table.align["Date de naissance"] = "c"
            report_file.write(table.get_string(sortby="Nom"))

        print("votre rapport a été créé dans le répertoire rapports")
        input("Appuyer sur entrée pour revenir au menu précédent")

    def tournament_rounds(self, tournament_info, full_rounds_list):
        if not os.path.exists(REPORT_DIR_NAME):
            os.makedirs(REPORT_DIR_NAME)

        now = datetime.now()  # current date and time
        timestamp = now.strftime("%Y-%m-%d-%H_%M_%S")
        report_file_name = (
            REPORT_DIR_NAME
            + tournament_info["tournament_id"]
            + "_"
            + REPORT_TOURNAMENT_ROUNDS_NAME
            + timestamp
            + ".txt"
        )

        with open(report_file_name, "w", encoding="utf-8") as report_file:
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write(
                "*               Gestion de tournois d'échecs               *"
                "\n"
            )
            report_file.write(
                "************************************************************"
                "\n"
            )
            report_file.write("\n")
            line = (
                "*****     Liste des rondes du tournoi : "
                + tournament_info["tournament_id"]
                + "     *****\n"
            )
            report_file.write(line)
            report_file.write("\n")
            line = "     " + tournament_info["name"] + "\n"
            report_file.write(line)
            line = (
                "     Du "
                + tournament_info["start_date"]
                + " au "
                + tournament_info["end_date"]
                + "\n"
            )
            report_file.write(line)
            report_file.write("\n")

            table = PrettyTable()

            table.field_names = [
                "Premier joueur",
                "Score 1",
                "Deuxième joueur",
                "Score 2",
            ]
            table.align = "c"
            table.align["Premier joueur"] = "l"
            table.align["Deuxième joueur"] = "l"

            for round in full_rounds_list:
                table.clear_rows()
                report_file.write("\n")
                round_data = full_rounds_list[round]
                if round_data["status"] == "opened":
                    status = "ouverte"
                else:
                    status = "close"
                line = "*** " + round + "   " + status + " ***\n"
                report_file.write(line)
                report_file.write("\n")

                for game in round_data["players_list"]:
                    player1 = (
                        game["player1_id"]
                        + " "
                        + game["player1_name"]
                        + " "
                        + game["player1_surname"]
                    )
                    score1 = game["player1_score"]
                    player2 = (
                        game["player2_id"]
                        + " "
                        + game["player2_name"]
                        + " "
                        + game["player2_surname"]
                    )
                    score2 = game["player2_score"]
                    table.add_row([player1, score1, player2, score2])
                report_file.write(str(table))
                report_file.write("\n")

        print("votre rapport a été créé dans le répertoire rapports")
        input("Appuyer sur entrée pour revenir au menu précédent")
