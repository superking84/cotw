import arcade

import game

if __name__ == "__main__":
    game = game.Game()
    game.show_view(game.views["world"])

    arcade.run()
