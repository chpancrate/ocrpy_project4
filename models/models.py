""" models classes for chess tournament management software"""
import random
import datetime
import copy
import os
import json
from typing import List

# define the name and path for the JSON players and tournaments files
JSON_DIR_NAME = "data/"
JSON_PLAY_FILENAME = "data/players.json"
JSON_TOUR_FILENAME = "data/tournaments.json"
# define the name and path for the file that store the next tournament index
JSON_TOUR_ID_FILENAME = "data/tournaments_id_ref.json"

ROUND_LABEL = "Ronde "
DEFAULT_NUMBER_OF_ROUND = 4


def obj_dict(obj):
    return obj.__dict__


class Player:
    """chess player class
    Chess player are uniquely identified by their national_chess_id"""

    def __init__(self, name, surname, national_chess_id, birth_date):
        """Player has a name,
        a surname,
        a birt date and
        a national chess identification number"""
        self.name = name
        self.surname = surname
        self.national_chess_id = national_chess_id
        self.birth_date = birth_date

    def __str__(self):
        """Used in print."""
        return (
            f"{self.surname} {self.name} né le {self.birth_date} "
            f"Chess ID {self.national_chess_id}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)

    def json_save(self):
        """save the Player to the players.json file"""
        # create the json

        if not os.path.exists(JSON_DIR_NAME):
            os.makedirs(JSON_DIR_NAME)

        # create the jason string from the object
        # json_newline = json.dumps(self.__dict__) + "\n"

        if not os.path.exists(JSON_PLAY_FILENAME):
            # players file does not exist we create it directly
            players_list = []
            players_list.append(self)

            # create a dictionary of object
            players_list_dict = {}
            players_list_dict["players_list"] = players_list
            # transform it in json including contained objects
            json_players_list = json.dumps(players_list_dict, default=obj_dict)
            # convert the string to a dictionnary
            json_players_list_dict = json.loads(json_players_list)

            with open(JSON_PLAY_FILENAME, "w") as file_json:
                json.dump(json_players_list_dict, file_json)
        else:
            # players file exist
            player_found = False
            with open(JSON_PLAY_FILENAME, "r") as file_json:
                json_players_list_dict = json.load(file_json)
                for player in json_players_list_dict["players_list"]:
                    if player["national_chess_id"] == self.national_chess_id:
                        player_found = True
                        player["name"] = self.name
                        player["surname"] = self.surname
                        player["birth_date"] = self.birth_date
                        break

                if not player_found:
                    json_player = json.dumps(self, default=obj_dict)
                    json_player_dict = json.loads(json_player)
                    json_players_list_dict["players_list"].append(
                        json_player_dict
                    )

            with open(JSON_PLAY_FILENAME, "w") as file_json:
                json.dump(json_players_list_dict, file_json)


class Game:
    """chess game class, 2 players identified by their national chess id
    and their score at the end of the game
    the winner gets 1 point the loser 0
    in a draw both player get 0.5 pts"""

    def __init__(self, national_chess_id1, national_chess_id2):
        """game opposes two players identified by their id
        the result of the game is given by the score of each player"""
        self.result = {national_chess_id1: 0, national_chess_id2: 0}

    def store_result(self, player_id1, score1, player_id2, score2):
        """the scores are stored next to the player id"""
        self.result[player_id1] = score1
        self.result[player_id2] = score2


class Round:
    """tournament round class"""

    def __init__(self, name):
        """a round tournament has a name, a start gate and an end date
        it contains a list of games"""
        self.name = name
        # the round starts when generated
        self.start_date = datetime.datetime.today().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.end_date = None
        self.games = []

    def add_game(self, game):
        """add a game to the list of games of the round"""
        self.games.append(game)

    def check_existing_game(self, searched_game):
        """check if a game already exist in the round"""
        game_found = False
        for game in self.games:
            number_key_found = 0
            for key in game.result.keys():
                # compare player id in game with player id in searched_game
                if key in searched_game.result.keys():
                    # print(key)
                    number_key_found += 1
                    # print(number_key_found)
            if number_key_found == 2:
                # the 2 player ids have been found in the same game
                game_found = True
                break
        return game_found

    def end_round(self):
        """allow to close a round when needed"""
        self.end_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")


class PlayerRank:
    """Player ranking class
    use the national chess ID to reference the player
    store the current score of the player in the tournament"""

    def __init__(self, national_chess_id):
        """A player rank has a player_id and a corresponding score"""
        self.national_chess_id = national_chess_id
        self.total_score = 0

    def update_score(self, score):
        """update the score correponding to the player id"""
        self.total_score = self.total_score + score

    def __str__(self):
        """Used in print."""
        return f"Id {self.national_chess_id} score {self.total_score}"

    def __repr__(self):
        """Used in print."""
        return str(self)


class Ranking(list):
    """Tournament ranking class"""

    def append(self, object):
        """ensure only player rank are added"""
        if not isinstance(object, PlayerRank):
            return ValueError("vous ne pouvez ajouter que score de joueur")
        return super().append(object)

    def sort_by_score(self):
        """sort all the ranks by their score"""
        self.sort(key=lambda x: x.total_score)

    def add_player_rank(self, player_rank):
        """add a olayer rank to the ranking"""
        self.append(player_rank)

    def shuffle(self):
        """shuffle the ranking"""
        random.shuffle(self)

    def store_score(self, player_id, score):
        """update the score of a player in the ranking"""
        for rank in self:
            if rank.national_chess_id == player_id:
                rank.update_score(score)
                break


class Tournament:
    """tournament class"""

    def __init__(
        self,
        tournament_id,
        name,
        location,
        star_date,
        end_date,
        number_of_rounds=DEFAULT_NUMBER_OF_ROUND,
        description=" ",
    ):
        """need tournament_id, name, location,
        start and end date and description"""
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = star_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.current_round = 0
        # self.rounds = []
        self.rounds: List[Round] = []
        self.ranking = Ranking()

    def register_player(self, player_id):
        """register a player in the tournament"""
        rank = PlayerRank(player_id)
        self.ranking.append(rank)

    def create_round(self):
        """create a round for the tournament"""
        # shuffle the ranking to shuffle player with same score
        random.shuffle(self.ranking)
        # sort the ranking by score
        self.ranking.sort_by_score()
        # read ranking and create game making sure previous round do not
        # have same game
        self.current_round += 1
        if self.current_round > self.number_of_rounds:
            print("le nombre de tour maximum est atteint")
            return ValueError("le nombre de tour maximum est atteint")
        else:
            round_name = ROUND_LABEL + str(self.current_round)
            new_round = Round(round_name)
            work_ranking = copy.deepcopy(self.ranking)
            # loop in the ranking getting the first player in the list
            # then try to match it with another player in the ranking
            # when a pair is found it's removed from the working ranking
            # we then do the process again until the working ranking is empty
            while len(work_ranking) > 1:
                # get the first id in the working ranking
                first_player = work_ranking.pop(0).national_chess_id
                i = 0
                for rank in work_ranking:
                    # read the next ranking
                    second_player = rank.national_chess_id
                    new_game = Game(first_player, second_player)
                    match_exist = False
                    for round in self.rounds:
                        # check if players already played against each other
                        match_exist = round.check_existing_game(new_game)
                        if match_exist:
                            break
                    if not match_exist:
                        # the players did not play against each other
                        # we remove the second player from the list
                        work_ranking.pop(i)
                        # and add the game to the round
                        new_round.add_game(new_game)
                        break
                    else:
                        # the players have already played against each other
                        # in the tournament we take the next one
                        i += 1
            self.rounds.append(new_round)

    def json_save(self):
        """save the tournament to the JSON_TOUR_FILENAME file"""
        # create the json

        if not os.path.exists(JSON_DIR_NAME):
            os.makedirs(JSON_DIR_NAME)

        if not os.path.exists(JSON_TOUR_FILENAME):
            # tournament file does not exist create it and write the line
            tournaments_list = []
            tournaments_list.append(self)

            # create a dictionary of object
            tournaments_list_dict = {}
            tournaments_list_dict["tournaments_list"] = tournaments_list
            # transform it in json including contained objects
            json_tournaments_list = json.dumps(
                tournaments_list_dict, default=obj_dict
            )
            # convert the string to a dictionnary
            json_tournaments_list_dict = json.loads(json_tournaments_list)
            with open(JSON_TOUR_FILENAME, "w") as file_json:
                json.dump(json_tournaments_list_dict, file_json)
        else:
            # tournament file exist
            tournament_found = False
            with open(JSON_TOUR_FILENAME, "r") as file_json:
                json_tournaments_list_dict = json.load(file_json)
                # load the file in a json object
                # search if the tournament already exist
                for tournament in json_tournaments_list_dict[
                    "tournaments_list"
                ]:
                    if tournament["tournament_id"] == self.tournament_id:
                        # the tournament exist
                        tournament_found = True

                        # replace the data with the new one and stop the search
                        tournament["name"] = self.name
                        tournament["location"] = self.location
                        tournament["start_date"] = self.start_date
                        tournament["end_date"] = self.end_date
                        tournament["number_of_rounds"] = self.number_of_rounds
                        tournament["description"] = self.description
                        tournament["current_round"] = self.current_round
                        json_rounds = json.dumps(self.rounds, default=obj_dict)
                        json_rounds_dict = json.loads(json_rounds)
                        tournament["rounds"] = json_rounds_dict
                        json_ranking = json.dumps(
                            self.ranking, default=obj_dict
                        )
                        json_ranking_dict = json.loads(json_ranking)
                        tournament["ranking"] = json_ranking_dict
                        break

                if not tournament_found:
                    # the tournament was not found add it at the end
                    json_tournament = json.dumps(self, default=obj_dict)
                    json_tournament_dict = json.loads(json_tournament)
                    json_tournaments_list_dict["tournaments_list"].append(
                        json_tournament_dict
                    )

            # save the new json data to the file
            with open(JSON_TOUR_FILENAME, "w") as file_json:
                json.dump(json_tournaments_list_dict, file_json)


class Json2Object:
    """retrieve tournament data from the json file
    and create a tournament object with it"""

    def tournament(self, tournament_id):
        with open(JSON_TOUR_FILENAME, "r") as file_json:
            json_tournaments_list_dict = json.load(file_json)
            for tournament_json in json_tournaments_list_dict[
                "tournaments_list"
            ]:
                if tournament_json["tournament_id"] == tournament_id:
                    # get the information from the file
                    name = tournament_json["name"]
                    location = tournament_json["location"]
                    start_date = tournament_json["start_date"]
                    end_date = tournament_json["end_date"]
                    number_of_rounds = tournament_json["number_of_rounds"]
                    description = tournament_json["description"]

                    # use the information to create an instance of tournament
                    tournament = Tournament(
                        tournament_id,
                        name,
                        location,
                        start_date,
                        end_date,
                        number_of_rounds,
                        description,
                    )

                    tournament.current_round = int(
                        tournament_json["current_round"]
                    )

                    # rebuild the rounds list and add it to the tournament
                    if tournament_json["rounds"] == []:
                        tournament.rounds = []
                    else:
                        for round_json in tournament_json["rounds"]:
                            # scan for the round create them
                            # and add them to the list
                            round = Round(round_json["name"])
                            round.start_date = round_json["start_date"]
                            round.end_date = round_json["end_date"]
                            for game_json in round_json["games"]:
                                players_data = []
                                for key in game_json["result"]:
                                    players_data.append(key)
                                    players_data.append(
                                        game_json["result"][key]
                                    )
                                # rebuild the games and add them to the rounds
                                game = Game(players_data[0], players_data[2])
                                game.result[players_data[0]] = players_data[1]
                                game.result[players_data[2]] = players_data[3]
                                round.games.append(game)
                            tournament.rounds.append(round)

                    # rebuild the ranking
                    if tournament_json["ranking"] == []:
                        tournament.ranking = Ranking()
                    else:
                        # scan for the player rank rebuild them
                        # and add them to the ranking list
                        for rank_json in tournament_json["ranking"]:
                            rank = PlayerRank(rank_json["national_chess_id"])
                            rank.update_score(rank_json["total_score"])
                            tournament.ranking.append(rank)
                    return tournament
