from typing import List, Optional
import time

from pynput.keyboard import KeyCode, Key
from physim.models.objects import Object

BLOCK_EMPTY = " "


class Canvas:
    def __init__(
        self,
        width: int,
        height: int,
        objects: Optional[List[Object]] = None,
        fps: int = 20,
        g: Optional[List[int]] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.objects = objects or []
        self.fps = fps
        self.g = g or [0, 0.1]

    def __repr__(self) -> str:
        return f"<Canvas: width={self.width}, height={self.height}, objects=[{', '.join(str(object_) for object_ in self.objects)}]>"

    def add_objects(self, *kwargs: List[Object]) -> None:
        self.objects.extend(kwargs)
        for kwarg in kwargs:
            kwarg.canvas = self

    def update(self) -> None:
        for object_ in self.objects:
            object_.update()

    def handle_key_press(self, key) -> None:
        for object_ in self.objects:
            if object_.user_input:
                if key in [KeyCode(char="a"), Key.left]:
                    object_.move_sideways(-1)
                if key in [KeyCode(char="d"), Key.right]:
                    object_.move_sideways(1)
                if key == Key.space:
                    object_.jump()

    def render_list(self) -> str:
        pixel = Object("Pixel")

        result = [[BLOCK_EMPTY for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                pixel.position = [x, y]
                for object_ in self.objects:
                    if object_.check_collision(pixel):
                        result[y][x] = object_.texture
                        break

        return result

    def render(self, render_list: List[List[str]] = None) -> str:
        render_list = render_list or self.render_list()
        print("\n".join(["".join(row) for row in render_list]))

    def render_loop(self) -> None:
        while True:
            self.render()
            self.update()
            time.sleep(1 / self.fps)
