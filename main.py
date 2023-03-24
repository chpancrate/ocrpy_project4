"""Chess Tournaments management software"""
from controllers.controller import Controller
from views.views import Menu


def main():
    menu = Menu()
    game = Controller(menu)
    game.run()


if __name__ == "__main__":
    main()
