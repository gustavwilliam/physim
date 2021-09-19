from typing import TYPE_CHECKING, List, Optional
from decimal import Decimal

if TYPE_CHECKING:
    from models.canvas import Canvas


class Object:
    def __init__(
        self,
        name: Optional[str] = "Object",
        mass: Optional[int] = 1,
        width: Optional[int] = 1,
        height: Optional[int] = 1,
        friction_coeff: Optional[int] = 0,
        velocity: Optional[List] = None,
        position: Optional[List] = None,
        gravity: Optional[bool] = False,
        collisions: Optional[bool] = True,
        movable: Optional[bool] = False,
        user_input: Optional[bool] = False,
        texture: Optional[str] = "█",
    ) -> None:
        self.name = name
        self.mass = mass
        self.width = width
        self.height = height
        self.friction_coeff = friction_coeff
        self.velocity = velocity or [0, 0]
        self.position = position or [0, 0]
        self.canvas: Optional[Canvas] = None
        self.gravity = gravity
        self.collisions = collisions
        self.movable = movable
        self.user_input = user_input
        self.texture = texture

    @property
    def center_pos(self) -> List[int]:
        return [
            (2 * self.position[0] + self.width) / 2,
            (2 * self.position[1] + self.height) / 2,
        ]

    @property
    def collision_lines(self) -> List[callable]:
        return [
            get_line(
                self.position,
                [self.position[0] + self.width, self.position[1] + self.height],
            ),
            get_line(
                [self.position[0], self.position[1] + self.height],
                [self.position[0] + self.width, self.position[1]],
            ),
        ]

    def __repr__(self) -> str:
        return f"<Object: name={self.name}, mass={self.mass}, velocity={self.velocity}, width={self.width}, height={self.height}, position={self.position}, friction_coeff={self.friction_coeff}, gravity={self.gravity}>"

    def __str__(self) -> str:
        return f"<Object '{self.name}': mass={self.mass}, position={self.position}, velocity={self.velocity}>"

    def check_collision(self, object_2: "Object") -> bool:
        return (
            self.position[0] + self.width > object_2.position[0]
            and object_2.position[0] + object_2.width > self.position[0]
            and self.position[1] + self.height > object_2.position[1]
            and object_2.position[1] + object_2.height > self.position[1]
        )

    def jump(self) -> None:
        self.position[1] += 1
        if self.any_collision():
            self.velocity[1] = -1.2 * self.canvas.fps * self.canvas.g[1]
        self.position[1] -= 1

    def move_sideways(self, direction: int) -> None:
        if abs(self.velocity[0]) <= self.canvas.fps / 5:
            self.velocity[0] += 1.1 * direction
        else:
            self.velocity[0] = (
                self.velocity[0] / abs(self.velocity[0]) * self.canvas.fps / 10
            )

    def any_collision(self) -> Optional["Object"]:
        for object_ in self.canvas.objects:
            if not object_.collisions or object_ == self:
                return

            if self.check_collision(object_):
                return object_

    def collision_side(self, other) -> str:
        collision_lines = other.collision_lines
        center_pos = self.center_pos

        side = "".join(
            [
                str(int(collision_lines[0](center_pos[0]) < center_pos[1])),
                str(int(collision_lines[1](center_pos[0]) < center_pos[1])),
            ]
        )
        return {
            "00": "D",
            "01": "R",
            "10": "L",
            "11": "U",
        }[side]

    def update(self) -> None:
        if not self.movable:
            return

        if self.gravity:
            if not self.any_collision():
                self.velocity = [sum(i) for i in zip(self.velocity, self.canvas.g)]
        self.position = [sum(i) for i in zip(self.position, self.velocity)]

        if self.collisions:
            while object_ := self.any_collision():
                collision_side = self.collision_side(object_)
                side = 1 if collision_side in ["U", "D"] else 0

                self.velocity[0 if side == 1 else 1] *= (
                    1 - object_.friction_coeff / self.canvas.fps
                )  # Friction

                while self.check_collision(object_):  # Repel from collision objects
                    self.velocity[side] = 1 if collision_side in ["U", "R"] else -1
                    self.position = [sum(i) for i in zip(self.position, self.velocity)]
                    self.velocity[side] = 0


def get_line(point_1, point_2) -> callable:
    m = float(Decimal((point_2[1] - point_1[1])) / Decimal(point_2[0] - point_1[0]))
    c = point_2[1] - (m * point_2[0])
    return lambda x: m * x + c
