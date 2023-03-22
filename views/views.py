"""views classes for chess tournament management software"""
import os
import time
import datetime
from prettytable import PrettyTable
from models.models import DEFAULT_NUMBER_OF_ROUND

DATE_FORMAT = "%d/%m/%Y"
WRONG_ID_FORMAT_MESSAGE = (
    "Le format du l'indentifiant n'est pas bon (ex : AB12345)"
)
WRONG_DATE_FORMAT_MESSAGE = (
    "Date ou format de date incorrects,"
    " le format de la date doit être JJ/MM/DDDD"
)


def check_national_chess_id_format(checked_id):
    """check if checked_id is in the following format
    AAXXXXX where A are alphabet character and X are digits
    ex : DG12345"""
    if len(checked_id) != 7:
        return False
    elif not checked_id[0:2].isalpha():
        return False
    elif not checked_id[2:7].isdigit():
        return False
    else:
        return True


def check_tournament_id_format(checked_id):
    """check if parameter is in the following format
    TOUXXXXX where XXXXX are digits ex : TOU00009"""

    if len(checked_id) != 8:
        return False
    elif checked_id[0:3] != "TOU":
        return False
    elif not checked_id[3:8].isdigit():
        return False
    else:
        return True


class Menu:
    def header(self):
        """dipslay the general header of the application"""
        os.system("cls")
        print("************************************************************")
        print("*               Gestion de tournois d'échecs               *")
        print("************************************************************")

    def header_creation(self):
        """display the header of the tournament creation"""
        self.header()
        print("*                   Création de tournoi                    *")
        print("------------------------------------------------------------")

    def header_update(self):
        """display the header of the tournament update"""
        self.header()
        print("*                 Modification de tournoi                  *")
        print("------------------------------------------------------------")

    def header_tournament(self, tournament):
        """dispay the header for tournament update
        displaying additional data of the tournament
        """
        print("Tournoi :", tournament.name)
        print(
            "Nombre de rondes : ",
            tournament.number_of_rounds,
            " |  ronde actuelle:",
            tournament.current_round,
        )
        self.separator()

    def tournament_info(self, tournament):
        print("Nom du tournoi :", tournament.name)
        print("Lieu :", tournament.location)
        print(
            "Date de début :",
            tournament.start_date,
            " |  Date de fin :",
            tournament.end_date,
        )
        print(
            "Nombre de rondes:",
            tournament.number_of_rounds,
            " |  Ronde actuelle:",
            tournament.current_round,
        )
        print("Description :", tournament.description)
        self.separator()

    def separator(self):
        print("------------------------------------------------------------")

    def start(self):
        """dispaly the start menu"""
        self.header()
        print("1 - Créer un tournoi")
        print("2 - Visualiser ou modifier un tournoi")
        print("3 - Liste des tournois")
        print("4 - Liste des joueurs")
        print("s - Sortir")
        self.separator()
        choice = input("Quel est votre choix ? : ")
        if choice == "1":
            return "create_tournament"
        elif choice == "2":
            return "manage_tournament"
        elif choice == "3":
            return "tournaments_list"
        elif choice == "4":
            return "players_list"
        elif choice == "s":
            return "exit"
        else:
            return "invalid"

    def tournament_creation(self):
        """display the tournament creation query"""
        self.header_creation()
        tournament_data = []
        name = input("Quel est le nom du tournoi ? : ")
        tournament_data.append(name)
        location = input("Ou aura-t-il lieu ? : ")
        tournament_data.append(location)

        good_format = False
        while not good_format:
            start_date = input("A quelle date commencera-t-il ? : ")
            try:
                datetime.datetime.strptime(start_date, DATE_FORMAT)
                good_format = True
            except ValueError:
                print(WRONG_DATE_FORMAT_MESSAGE)
        tournament_data.append(start_date)

        good_format = False
        while not good_format:
            end_date = input("Quand se terminera-t-il ? : ")
            try:
                datetime.datetime.strptime(end_date, DATE_FORMAT)
                good_format = True
            except ValueError:
                print(WRONG_DATE_FORMAT_MESSAGE)
            if end_date < tournament_data[-1]:
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
        self.header_update()
        table = PrettyTable()
        table.field_names = [
            "Identifiant",
            "Nom",
            "lieu",
            "Date de début",
            "Date de fin",
        ]
        for tournament in tournament_list:
            table.add_row(
                [
                    tournament[0],
                    tournament[1],
                    tournament[2],
                    tournament[3],
                    tournament[4],
                ]
            )

        print(table.get_string(sortby="Date de début"))

        choice = input("Entrer l'Id du tournoi que voulez-vous modifier : ")
        choice = choice.upper()
        if not check_tournament_id_format(choice):
            print("format de numero de tournoi érroné")
            time.sleep(1)
            self.tournaments_list(tournament_list)
        else:
            tournament_in_list = False
            for tournament in tournament_list:
                if tournament[0] == choice:
                    tournament_in_list = True
                    break
            if not tournament_in_list:
                print("Ce tournoi n'est pas dans la liste")
                time.sleep(1)
                self.tournaments_list(tournament_list)
            else:
                print(choice)
                return choice

    def display_tournaments_list(self, tournament_list):
        """display the tournaments list report"""
        self.header_update()
        table = PrettyTable()
        table.field_names = [
            "Identifiant",
            "Nom",
            "lieu",
            "Date de début",
            "Date de fin",
            "nombre de ronde",
            "ronde en cours",
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
                ]
            )

        print(table.get_string(sortby="Date de début"))

        input("Appuyer sur entrée pour revenir au menu précédent")

    def tournament_update(self, tournament):
        """display the tournament update menu"""
        good_choice = False
        while not good_choice:
            self.header_update()
            self.header_tournament(tournament)
            print("1 - Gérer les données générales du tournoi")
            print("2 - Visualiser la liste des joueurs")
            print("3 - Modifier la liste des joueurs")
            print("4 - Liste des rondes et des matchs")
            print("5 - Créer la prochaine ronde")
            print("6 - Entrer les résultats de la ronde en cours")
            print("7 - terminer la ronde en cours")
            print("r - revenir au menu précédent")
            print("p - revenir au menu principal")
            self.separator()
            choice = input("Quel est votre choix ? : ")
            if choice == "1":
                return "manage_tournament"
            elif choice == "2":
                return "display_players"
            elif choice == "3":
                if tournament.rounds == []:
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
            elif choice == "r":
                return "back"
            elif choice == "p":
                return "mainmenu"
            else:
                print("Choix non valide")
                time.sleep(1)

    def manage_tournament(self, tournament):
        """display the tournament data management screen"""
        self.header()
        self.header_update()
        self.tournament_info(tournament)
        if tournament.rounds == []:
            print("pour modifier saisir la lettre correspondante :")
            print("(n)om, (l)ieu, (d)ébut, (f)in =), (r)ondes, d(e)scritpion")
            choice = input(
                (
                    "Quelle information doit être modifier ?"
                    " (xx pour sortir) : "
                )
            )
            if choice == "n":
                tournament.name = input("Entrer le nouveau nom : ")
                self.manage_tournament(tournament)
            elif choice == "l":
                tournament.location = input("Entrer le nouveau lieu : ")
                self.manage_tournament(tournament)
            elif choice == "d":
                good_format = False
                while not good_format:
                    start_date = input("Entrer la nouvelle date de début : ")
                    try:
                        datetime.datetime.strptime(start_date, DATE_FORMAT)
                        good_format = True
                    except ValueError:
                        print(WRONG_DATE_FORMAT_MESSAGE)
                tournament.start_date = start_date
                self.manage_tournament(tournament)
            elif choice == "f":
                good_format = False
                while not good_format:
                    end_date = input("Entrer la nouvelle date de fin : ")
                    try:
                        datetime.datetime.strptime(end_date, DATE_FORMAT)
                        good_format = True
                    except ValueError:
                        print(WRONG_DATE_FORMAT_MESSAGE)
                    if end_date < tournament.start_date:
                        print(
                            (
                                "La date de fin doit être posterieure"
                                " à la date de début"
                            )
                        )
                        good_format = False
                tournament.end_date = end_date
                self.manage_tournament(tournament)
            elif choice == "r":
                tournament.number_of_rounds = input(
                    "Entrer le nouveau nombre de rondes : "
                )
                self.manage_tournament(tournament)
            elif choice == "e":
                tournament.description = input(
                    "Entrer la nouvelle description : "
                )
                self.manage_tournament(tournament)
            elif choice == "xx":
                return
            else:
                print("choix invalide")
                time.sleep(1)
                self.manage_tournament(tournament)
        else:
            print(
                (
                    "Le tournoi est démarré, seule la description"
                    " peut être modifiée"
                )
            )
            choice = input(
                ("taper d pour modifier la description" "ou xx pour sortir : ")
            )
            if choice == "xx":
                return
            elif choice == "d":
                tournament.description = input(
                    "Saisir la nouvelle description : "
                )
                self.manage_tournament(tournament)
            else:
                print("choix invalide")
                time.sleep(1)
                self.manage_tournament(tournament)

    def display_tournament_players_list(
        self, tournament, tournament_players_list
    ):
        """display the tournament players report"""
        self.header_update()
        self.header_tournament(tournament)
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

    def tournament_players_list(self, tournament, tournament_players_list):
        """display the tournament players list screen for update of the list"""
        self.header_update()
        self.header_tournament(tournament)
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

    def add_player_from_file(self, player_to_add, tournament):
        """display the questions to add a player from the players file"""
        self.header_update()
        self.header_tournament(tournament)
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

    def add_new_player(self, tournament, player_id):
        """display the questions to create a new player"""
        self.header_update()
        self.header_tournament(tournament)
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
                datetime.datetime.strptime(birth_date, DATE_FORMAT)
                good_format = True
            except ValueError:
                print(WRONG_DATE_FORMAT_MESSAGE)

        player_data.append(birth_date)

        return player_data

    def round_list(self, round_players_list):
        """display a table containing all the games for a round"""
        table = PrettyTable()
        table.field_names = [
            "Premier joueur",
            "Résultat 1",
            "Deuxième joueur",
            "Résultat 2",
        ]
        table.align = "c"
        table.align["Premier joueur"] = "l"
        table.align["Deuxième joueur"] = "l"

        for game in round_players_list:
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

    def created_round(self, tournament, round_players_list):
        """display the end screen of the round creation process"""
        self.header_update()
        self.header_tournament(tournament)
        self.separator()
        print("Détails de la nouvelle ronde :")
        self.round_list(round_players_list)
        input("Appuyer sur entrée pour revenir au menu précédent")

    def input_result(self, tournament, round_players_list):
        """display the screen for result input"""
        self.header_update()
        self.header_tournament(tournament)
        print("Détails de la ronde actuelle :")
        self.round_list(round_players_list)
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
            self.input_result(tournament)
        return result

    def display_players_list(self, players_list):
        """display the full players list report"""
        self.header()
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

    def display_rounds(self, tournament, full_rounds_list):
        """display the full round and match report"""
        self.header()
        self.header_tournament(tournament)
        print("*                Liste complète des Rondes                 *")
        print("------------------------------------------------------------")
        table = PrettyTable()

        table.field_names = [
            "Premier joueur",
            "Résultat 1",
            "Deuxième joueur",
            "Résultat 2",
        ]
        table.align = "c"
        table.align["Premier joueur"] = "l"
        table.align["Deuxième joueur"] = "l"

        for round in full_rounds_list:
            table.clear_rows()
            print()
            print("***", round)
            for game in full_rounds_list[round]:
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
        """ask fo round closure confiration"""
        choice = input("voulez-vous terminer la ronde en cours? (o/n) : ")
        if choice == "o":
            return True
        else:
            return False
