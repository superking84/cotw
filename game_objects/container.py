from game_objects.item import Item


class Container(Item):
    """
    Items such as backpacks and chests that may contain other items.
    May or may not be wearable.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        super().__init__(img_src, center_x, center_y)

        self.size_capacity = 0
