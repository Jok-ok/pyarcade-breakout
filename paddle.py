
class Paddle:
    def __init__(self, pos: tuple[float, float],
                 width: float = 100,
                 height: float = 25,
                 friction: float = 0,
                 elasticity: float = 1):
        self.pos = pos
        self.width = width
        self.height = height
        self.friction = friction
        self.elasticity = elasticity
