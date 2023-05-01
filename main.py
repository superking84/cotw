import arcade

import game
from db.db_manager import DBManager

if __name__ == "__main__":
    DBManager.generate_schema()
    
    game = game.Game()
    game.show_view(game.views["world"])

    arcade.run()
