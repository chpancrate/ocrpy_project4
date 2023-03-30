"""Chess Tournaments management software"""
from controllers.controller import Controller
from views.views import Menu, Report


def main():
    menu = Menu()
    report = Report()
    game = Controller(menu, report)
    game.run()


if __name__ == "__main__":
    main()
