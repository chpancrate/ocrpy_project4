"""views classes for chess tournament management software"""
import os
import json
import time
from models.models import JSON_TOUR_FILENAME, JSON_PLAY_FILENAME


class Menu:
    def header(self):
        os.system("cls")
        print("************************************************************")
        print("*               Gestion de tournois d'échecs               *")
        print("************************************************************")

    def header_creation(self):
        self.header()
        print("*                   Création de tournoi                    *")
        print("------------------------------------------------------------")

    def header_update(self):
        self.header()
        print("*                 Modification de tournoi                  *")
        print("------------------------------------------------------------")

    def header_tournament(self, tournament):
        print("tournoi :", tournament.name)
        print(
            "nombre de rondes:",
            tournament.number_of_rounds,
            "ronde actuelle:",
            tournament.current_round,
        )
        self.separator()

    def separator(self):
        print("------------------------------------------------------------")

    def start(self):
        self.header()
        print("1 - Créer un tournoi")
        print("2 - Modifier un tournoi")
        print("s - Sortir")
        self.separator()
        choice = input("Quel est votre choix ? : ")
        if choice == "1":
            return "option1"
        elif choice == "2":
            return "option2"
        elif choice == "s":
            return "exit"
        else:
            return "invalid"

    def tournament_creation(self):
        self.header_creation()
        tournament_data = []
        name = input("Quel est le nom du tournoi ? :")
        tournament_data.append(name)
        location = input("Ou aura-t-il lieu ? :")
        tournament_data.append(location)
        start_date = input("A quelle date commencera-t-il ? :")
        tournament_data.append(start_date)
        end_date = input("Quand se terminera-t-il ? :")
        tournament_data.append(end_date)
        number_of_rounds = input("Combien de rondes voulez vous ? :")
        tournament_data.append(number_of_rounds)
        description = input("Informations complémentaires :")
        tournament_data.append(description)

        return tournament_data

    def tournaments_list(self):
        self.header_update()
        tournament_list = []
        with open(JSON_TOUR_FILENAME, "r") as tournament_file:
            for line in tournament_file:
                tournament = json.loads(line)
                tournament_list.append(
                    [tournament["tournament_id"], tournament["name"]]
                )
        option = 1
        for tournament in tournament_list:
            # option give the number to be tuped to access the tournament
            print(option, ":", tournament[0], tournament[1])
            option += 1
        self.separator()
        choice = input("Quel tournoi voulez-vous modifier ? :")
        if choice.isnumeric():
            if int(choice) < len(tournament_list) + 1:
                return tournament_list[int(choice) - 1][0]
            else:
                print(
                    "numero de tournoi érroné, entrer un nombre entre 1 et",
                    len(tournament_list),
                )
                time.sleep(1)
                self.tournaments_list()
        else:
            print(
                "Entrer un nombre entre  et",
                len(tournament_list),
            )
            time.sleep(1)
            self.tournaments_list()

        return tournament_list[choice - 1][0]

    def tournament_update(self, tournament):
        self.header_update()
        self.header_tournament(tournament)
        print("1 - Entrer la liste des joueurs")
        print("2 - Créer le prochain tour")
        print("3 - Entrer les résultats du tour")
        print("r - revenir au menu précédent")
        print("p - revenir au menu principal")
        self.separator()
        choice = input("Quel est votre choix ? : ")
        if choice == "1":
            return "option1"
        elif choice == "2":
            return "option2"
        elif choice == "3":
            return "option3"
        elif choice == "r":
            return "back"
        elif choice == "p":
            return "mainmenu"
        else:
            return "invalid"

    def user_list(self, tournament):
        # print headers
        self.header_update()
        self.header_tournament(tournament)
        print("Tournament players list :")
        # print the players list from the tournament ranking
        # additional data are come from the players file : JSON_PLAY_FILENAME
        tournament_players_list = {}
        with open(JSON_PLAY_FILENAME, "r") as players_file:
            for line in players_file:
                players = json.loads(line)
                for rank in tournament.ranking:
                    player_data = []
                    if rank.national_chess_id == players["national_chess_id"]:
                        player_data.append(players["name"])
                        player_data.append(players["surname"])
                        player_data.append(players["birth_date"])
                        player_update = {}
                        player_update[
                            players["national_chess_id"]
                        ] = player_data
                        tournament_players_list.update(player_update)
                        break
        # print(tournament_players_list)

        for player_id in tournament_players_list.keys():
            print(
                player_id,
                ":",
                tournament_players_list[player_id][0],
                ",",
                tournament_players_list[player_id][1],
                ",",
                tournament_players_list[player_id][2],
            )
        self.separator()

        player_id = input(
            "Entrer l'identifiant national d'echec du joueur à ajouter : "
        )
        return player_id
