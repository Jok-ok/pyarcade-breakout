from consts import SCREEN_WIDTH, SCREEN_HEIGHT


class Wall:
    def __init__(self,
                 point_1: tuple[float, float],
                 point_2: tuple[float, float],
                 radius: float,
                 friction: float,
                 elasticity: float):
        self.point_1 = point_1
        self.point_2 = point_2
        self.radius = radius
        self.friction = friction
        self.elasticity = elasticity


class WallConfigurator:
    @staticmethod
    def horizontal(y_pos: float, radius: float = 10, friction: float = 0, elasticity: float = 1) -> Wall:
        return Wall((0, y_pos), (SCREEN_WIDTH, y_pos), radius, friction, elasticity)

    @staticmethod
    def vertical(x_pos: float, radius: float = 10, friction: float = 0, elasticity: float = 1) -> Wall:
        return Wall((x_pos, 0), (x_pos, SCREEN_HEIGHT), radius,  friction, elasticity)