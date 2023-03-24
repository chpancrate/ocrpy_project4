"""functions used by the views"""
import os
from prettytable import PrettyTable


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


def header():
    """dipslay the general header of the application"""
    os.system("cls")
    print("************************************************************")
    print("*               Gestion de tournois d'échecs               *")
    print("************************************************************")


def header_creation():
    """display the header of the tournament creation"""
    header()
    print("*                   Création de tournoi                    *")
    print("------------------------------------------------------------")


def header_update():
    """display the header of the tournament update"""
    header()
    print("*                 Modification de tournoi                  *")
    print("------------------------------------------------------------")


def header_tournament(tournament_info):
    """dispay the header for tournament update
    displaying additional data of the tournament
    """
    print("Tournoi :", tournament_info["name"])
    print(
        "Nombre de rondes : ",
        tournament_info["number_of_rounds"],
        " |  ronde actuelle:",
        tournament_info["current_round"],
    )
    separator()


def tournament_information(tournament_info):
    """display the informations from a tournament
    excepts rounds content and ranking"""
    print("Nom du tournoi :", tournament_info["name"])
    print("Lieu :", tournament_info["location"])
    print(
        "Date de début :",
        tournament_info["start_date"],
        " |  Date de fin :",
        tournament_info["end_date"],
    )
    print(
        "Nombre de rondes:",
        tournament_info["number_of_rounds"],
        " |  Ronde actuelle:",
        tournament_info["current_round"],
    )
    print("Description :", tournament_info["description"])
    separator()


def separator():
    """a separator"""
    print("------------------------------------------------------------")


def round_list(round_players_list):
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
