from arcade import Sprite
from pymunk import Shape


class PhysicsSprite(Sprite):
    def __init__(self, pymunk_shape: Shape, filename: str):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape



