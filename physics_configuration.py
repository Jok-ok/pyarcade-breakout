from pymunk import Shape, Vec2d, Body, Circle, moment_for_circle, moment_for_box, moment_for_segment, Poly
from typing import Optional, Protocol


class PhysicsObjectConfiguration(Protocol):
    def __create_static_body(self):
        ...

    def __create_dynamic_body(self):
        ...

    def __create_kinematic_body(self):
        ...


class PhysicsConfigurator:
    def __init__(self, position: Vec2d,
                 shape: Shape,
                 body: Body,
                 friction: float, elasticity: float,
                 collision_type: Optional[int] = None):
        self.shape = shape
        self.body = body
        self.shape.friction = friction
        self.shape.elasticity = elasticity
        self.body.position = Vec2d(position.x, position.y)
        self.shape.collision_type = collision_type


class BoxPhysicsConfigurator(PhysicsConfigurator):
    def __init__(self, position: Vec2d, width: float, height: float,
                 body_type: int, friction: float, elasticity: float,
                 collision_type: Optional[int] = None, mass: Optional[float] = None):
        assert body_type in (Body.DYNAMIC, Body.STATIC, Body.KINEMATIC), ("ERROR: Body type does not exist. "
                                                                          "Please specify the correct body_type. "
                                                                          "EXAMPLE: pymunk.Body.STATIC or "
                                                                          "pymunk.Body.DYNAMIC")
        body = None

        if body_type is Body.DYNAMIC:
            assert mass is not None, ("ERROR: Unable to create an Dynamic object."
                                      "Specify 'mass' argument.")
            body = self.__create_dynamic_body(width, height, mass)
        elif body_type is Body.STATIC:
            body = self.__create_static_body()
        elif body_type is Body.KINEMATIC:
            body = self.__create_kinematic_body()

        shape = Poly.create_box(body, (width, height))
        super().__init__(position, shape, body, friction, elasticity, collision_type)

    def __create_static_body(self) -> Body:
        return Body(body_type=Body.STATIC)

    def __create_dynamic_body(self, width: float, height: float,
                              mass: float) -> Body:
        inertia = moment_for_box(mass, (width, height))
        body = Body(mass, inertia)
        return body

    def __create_kinematic_body(self) -> Body:
        return Body(body_type=Body.KINEMATIC)


class BallPhysicsConfigurator(PhysicsConfigurator):
    def __init__(self, position: Vec2d, radius: float, body_type: int, friction: float, elasticity: float,
                 collision_type: Optional[int] = None, mass: Optional[float] = None):
        assert body_type in (Body.DYNAMIC, Body.STATIC, Body.KINEMATIC), ("ERROR: Body type does not exist. "
                                                                          "Please specify the correct body_type. "
                                                                          "EXAMPLE: pymunk.Body.STATIC or "
                                                                          "pymunk.Body.DYNAMIC")
        body = None

        if body_type is Body.DYNAMIC:
            assert mass is not None, ("ERROR: Unable to create an Dynamic object."
                                      "Specify 'mass' argument.")
            body = self.__create_dynamic_body(radius, mass)
        elif body_type is Body.STATIC:
            body = self.__create_static_body()
        elif body_type is Body.KINEMATIC:
            body = self.__create_kinematic_body()

        shape = Circle(body, radius, (0, 0))
        super().__init__(position, shape, body, friction, elasticity, collision_type)

    def __create_static_body(self) -> Body:
        return Body(body_type=Body.STATIC)

    def __create_dynamic_body(self, radius: float,
                              mass: float) -> Body:
        inertia = moment_for_circle(mass, 0, radius, (0, 0))
        body = Body(mass, inertia)
        return body

    def __create_kinematic_body(self) -> Body:
        return Body(body_type=Body.KINEMATIC)

