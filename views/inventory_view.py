import arcade


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_draw(self):
        pass

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, key: int, modifiers: int):
        match key:
            case arcade.key.ESCAPE:
                self.window.show_view(self.window.views["world"])
