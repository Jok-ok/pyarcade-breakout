import random

import pymunk
from arcade import Sprite
from typing import Protocol, Callable, Optional
from pymunk import Shape, Vec2d, Body, Poly, Circle, moment_for_circle
from consts import CollisionTypes, BodyTypes, ShapeTypes


class PhysicsSprite(Sprite):
    def __init__(self, pymunk_shape: Shape, filename: str):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape


class GameObject(Protocol):
    # sprite: Sprite = Sprite(sprite_path)
    # sprite
    pass


class PhysicsObjectProtocol(Protocol):
    body: Body
    shape: Shape


# class PhysicsConfiguration:
#     def __init__(self,
#                  body_type: int,
#                  shape_type: int,
#                  position: Vec2d,
#                  friction: float, elasticity: float,
#                  collision_type: int,
#                  width: Optional[float] = None, height: Optional[float] = None,
#                  mass: Optional[float] = None, radius: Optional[float] = None,
#                  point_a: Optional[tuple[float, float]] = None, point_b: Optional[tuple[float, float]] = None,
#                  line_collision_radius: Optional[float] = None):
#
#         if body_type in (Body.STATIC, Body.KINEMATIC):
#             assert width and height, ("ERROR: Rect can't be created. "
#                                       "Use width and height arguments to create rect.")
#             self.body = self.__create_rectangle_static_or_kinematic_body(body_type)
#         elif body_type == Body.DYNAMIC:
#             assert mass and radius, ("ERROR: Sphere can't be created. "
#                                      "Use radius and mass arguments to create sphere.")
#             self.body = self.__create_circular_dynamic_body(mass, radius)
#
#         if shape_type == ShapeTypes.RECTANGLE:
#             self.shape = self.__create_rectangle_shape(self.body, width, height)
#         elif shape_type == ShapeTypes.SPHERE:
#             self.shape = self.__create_circular_shape(self.body, radius)
#         elif shape_type == ShapeTypes.LINE:
#             assert point_a and point_b and line_collision_radius, ("ERROR: Line can't be created. "
#                                                                    "Use point_a, point_b, "
#                                                                    "and line_collision_radius arguments to create line.")
#             self.shape = self.__create_line_shape(self.body, point_a, point_b, line_collision_radius)
#
#         self.shape.friction = friction
#         self.shape.elasticity = elasticity
#         self.body.position = pymunk.Vec2d(position.x, position.y)
#         self.shape.collision_type = collision_type
#
#     def __create_circular_shape(self, body: Body, radius: float) -> Shape:
#         shape = Circle(body, radius=radius)
#         return shape
#
#     def __create_circular_dynamic_body(self, mass: float, radius: float) -> Body:
#         inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
#         body = Body(mass, inertia)
#         return body
#
#     def __create_rectangle_shape(self, body: Body, width: float, height: float) -> Shape:
#         shape = Poly.create_box(body, (width, height))
#         return shape
#
#     def __create_rectangle_static_or_kinematic_body(self, body_type: int) -> Body:
#         body = pymunk.Body(body_type=body_type)
#         return body
#
#     def __create_line_shape(self, body: Body, point_a: tuple[float, float], point_b: tuple[float, float],
#                             line_collision_radius: float) -> Shape:
#         shape = pymunk.Segment(body, point_a, point_b, line_collision_radius)
#         return shape


class PhysicalGameObject(Protocol):
    shape: Shape
    body: Body
    sprite: Sprite


class Ball:
    def __init__(self, position_x: float,
                 position_y: float,
                 radius: float,
                 sprite_img_path: str,
                 mass: float = 1, friction: float = 0, elasticity: float = 1,
                 fixed_velocity: float = 500):
        self.fixed_velocity = fixed_velocity

        inertia = moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = (position_x, position_y)

        x_velocity = (-1, 1)[random.randint(0, 1)]
        y_velocity = 1
        start_impulse = Vec2d(x_velocity, y_velocity)

        self.body.apply_impulse_at_local_point(start_impulse)
        self.body.velocity_func = self.__velocity_func
        self.shape = Circle(self.body, radius)
        self.shape.collision_type = CollisionTypes.BALL
        self.shape.friction = friction
        self.shape.elasticity = elasticity
        self.sprite = Sprite(sprite_img_path, center_x=self.body.position.x, center_y=self.body.position.y)

    def __velocity_func(self, body: Body, gravity: Vec2d, damping: float, dt: float) -> None:
        body.velocity = body.velocity.normalized() * self.fixed_velocity

    def configure_physics(self, configuration: PhysicsConfiguration):
        self.body = configuration.body
        self.shape = configuration.shape


class ArkanoidObjectsFactoryProtocol(Protocol):
    def create_ball(self,
                    position_x: float,
                    position_y: float,
                    radius: float, mass: float) -> PhysicalGameObject:
        ...

    def create_paddle(self,
                      position_x: float,
                      position_y: float,
                      width: float,
                      height: float) -> PhysicalGameObject:
        ...

    def create_wall(self,
                    position_x: float,
                    position_y: float,
                    width: float,
                    height: float) -> PhysicalGameObject:
        ...

    def create_brick(self,
                     position_x: float,
                     position_y: float,
                     width: float,
                     height: float,
                     armor: int) -> PhysicalGameObject:
        ...


class DefaultArkanoidObjectFactory:
    def create_ball(self,
                    position_x: float,
                    position_y: float,
                    radius: float, mass: float) -> PhysicalGameObject:
        ball = Ball(position_x, position_y, radius, "Resources/ball.png", mass)
        phys_conf = PhysicsConfiguration(Body.DYNAMIC, ShapeTypes.SPHERE, (position_x, position_y), )
        ball.configure_physics()

    def create_paddle(self,
                      position_x: float,
                      position_y: float,
                      width: float,
                      height: float) -> PhysicalGameObject:
        return
        ...

    def create_wall(self,
                    position_x: float,
                    position_y: float,
                    width: float,
                    height: float) -> PhysicalGameObject:
        ...

    def create_brick(self,
                     position_x: float,
                     position_y: float,
                     width: float,
                     height: float,
                     armor: int) -> PhysicalGameObject:
        ...

    # def create_ball(self, x: float, y: float, radius: float = 10, mass: float = 1) -> None:
    #     mass = mass
    #     radius = radius
    #     inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    #     body = pymunk.Body(mass, inertia)
    #     body.position = x, y
    #     body.apply_impulse_at_local_point(pymunk.Vec2d(500,500))
    #     shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
    #     shape.collision_type = CollisionTypes.BALL
    #     shape.friction = 1000
    #     shape.elasticity = 1

    # def create_wall(self, wall: Wall) -> None:
    #     body = pymunk.Body(body_type=pymunk.Body.STATIC)
    #     shape = pymunk.Segment(body, wall.point_1, wall.point_2, radius=wall.radius)
    #     shape.friction = wall.friction
    #     shape.elasticity = wall.elasticity
    #     shape.collision_type = CollisionTypes.WALL

    #     body = pymunk.Body(mass, inertia)
    #     shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
    #     shape = pymunk.Segment(body, wall.point_1, wall.point_2, radius=wall.radius)
