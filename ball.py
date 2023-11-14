from pymunk import Shape

from physics_sprite import PhysicsSprite


class BallSprite(PhysicsSprite):
    def __init__(self, pymunk_shape: Shape, filename: str):
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2

