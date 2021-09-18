from typing import TYPE_CHECKING, List, Optional

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
        texture: Optional[str] = "█"
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
        if abs(self.velocity[0]) <= self.canvas.fps / 7:
            self.velocity[0] += 1.5 * direction
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

    def update(self) -> None:
        if not self.movable:
            return

        if self.gravity:
            if not self.any_collision():
                self.velocity = [sum(i) for i in zip(self.velocity, self.canvas.g)]
        self.position = [sum(i) for i in zip(self.position, self.velocity)]

        if self.collisions:
            while object_ := self.any_collision():
                self.velocity[0] *= 1 - object_.friction_coeff / self.canvas.fps
                while self.check_collision(object_):  # Gravity
                    self.velocity[1] = -1
                    self.position = [sum(i) for i in zip(self.position, self.velocity)]
                    self.velocity[1] = 0
