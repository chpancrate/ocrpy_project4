import time
import json
from views.views import Menu
from models.models import Json2Object, Tournament, JSON_TOUR_ID_FILENAME


class Controller:
    def control_start(self, menu):
        choice = menu.start()
        if choice == "option1":
            tournament_data = menu.tournament_creation()

            with open(JSON_TOUR_ID_FILENAME, "r") as json_tournament_id_file:
                tournament_json = json.load(json_tournament_id_file)
                tournament_id = tournament_json["tournament_id_ref"]

            new_tournament = Tournament(
                tournament_id,
                tournament_data[0],
                tournament_data[1],
                tournament_data[2],
                tournament_data[3],
                tournament_data[4],
                tournament_data[5],
            )
            new_tournament.json_save()

            with open(JSON_TOUR_ID_FILENAME, "w") as json_tournament_id_file:
                tournament_json["tournament_id_ref"] = tournament_id + 1
                json.dump(tournament_json, json_tournament_id_file)

            # print(new_tournament.__dict__)
            print("le tournoi a été créé")
            time.sleep(1)
            self.control_start(menu)
        elif choice == "option2":
            self.control_tournaments_list(menu)
        elif choice == "exit":
            print("Au revoir")
        else:
            print("choix non valide")
            time.sleep(1)
            self.control_start(menu)

    def control_tournaments_list(self, menu):
        tournament_id = menu.tournaments_list()
        print(tournament_id)
        json2object = Json2Object()
        tournament = json2object.tournament(tournament_id)
        self.control_update_tournament(menu, tournament)

    def control_update_tournament(self, menu, tournament):
        choice = menu.tournament_update(tournament)
        if choice == "option1":
            self.control_user_list(menu, tournament)
        elif choice == "option2":
            pass
        elif choice == "option3":
            pass
        elif choice == "back":
            self.control_tournaments_list(menu)
        elif choice == "mainmenu":
            self.control_start(menu)
        else:
            print("choix non valide")
            self.control_update_tournament(menu, tournament)

    def control_user_list(self, menu, tournament):
        player_id = menu.user_list(tournament)
        print(player_id)

    def run(self):
        menu = Menu()
        self.control_start(menu)
