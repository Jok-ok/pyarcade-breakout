from typing import Set

import arcade
import pymunk
import timeit
import math

from block import Block
from wall import WallConfigurator, Wall
from ball import BallSprite
from paddle import Paddle
from physics_sprite import PhysicsSprite

from consts import *


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, 0.0)

        # List of pressed now keys
        self.pressed_keys: Set[int] = set()

        # Lists of sprites or lines
        self.sprite_list: arcade.SpriteList[PhysicsSprite] = arcade.SpriteList()
        self.static_lines: list[pymunk.Segment] = []

        # Used for dragging shapes around with the mouse
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        self.draw_time = 0
        self.processing_time = 0

        self.paddle = Paddle((SCREEN_WIDTH/2, 100))
        # Create the walls
        up_wall = WallConfigurator.horizontal(y_pos=SCREEN_HEIGHT)
        left_wall = WallConfigurator.vertical(x_pos=0)
        right_wall = WallConfigurator.vertical(x_pos=SCREEN_WIDTH)

        self.create_wall(up_wall)
        self.create_wall(left_wall)
        self.create_wall(right_wall)

        # Create the paddle
        self.paddle_body = self.create_paddle(self.paddle)

        # Create blocks
        self.blocks = []
        block_x = 50
        block_y = SCREEN_HEIGHT-50
        for i in range(5):
            for j in range(18):
                block = Block((block_x, block_y), 50, 25, 0, 1, 1)
                block_body = self.create_block(block)
                self.blocks.append(block_body)
                block_x += 52
            block_x = 50
            block_y -= 27

        self.score = 0
        collision_handler = self.space.add_collision_handler(CollisionTypes.BALL, CollisionTypes.BRICK)
        collision_handler.separate = self.on_brick_hit

    def on_brick_hit(self, arbiter, space, data) -> None:
        """
        On brick hit event
        delete a brick from space
        :param arbiter:
        :param space:
        :param data:
        :return:
        """
        brick_shape = arbiter.shapes[1]
        space.remove(brick_shape, brick_shape.body)
        self.score += 10

    def on_draw(self) -> None:
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # Draw all the sprites
        self.sprite_list.draw()

        # Draw the lines that aren't sprites
        for line in self.static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 2)

        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 20, arcade.color.WHITE, 12)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 12)

        output = f"Score: {self.score}"
        arcade.draw_text(output, SCREEN_WIDTH/2-20, SCREEN_HEIGHT - 20, arcade.color.GOLD, 16)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.last_mouse_position = x, y
            # See if we clicked on anything
            shape_list = self.space.point_query((x, y), 1, pymunk.ShapeFilter())

            # If we did, remember what we clicked on
            if len(shape_list) > 0:
                self.shape_being_dragged = shape_list[0]

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # With right mouse button, shoot a heavy coin fast.
            radius = 10
            self.create_ball(x, y, radius)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.LEFT:
            self.set_paddle_x_velocity(-1000)
            if arcade.key.RIGHT in self.pressed_keys:
                self.pressed_keys.remove(arcade.key.RIGHT)
        elif symbol == arcade.key.RIGHT:
            self.set_paddle_x_velocity(1000)
            if arcade.key.LEFT in self.pressed_keys:
                self.pressed_keys.remove(arcade.key.LEFT)

        self.pressed_keys.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol in self.pressed_keys:
            self.pressed_keys.remove(symbol)
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT) and len(self.pressed_keys) == 0:
            self.set_paddle_x_velocity(0)

    def create_wall(self, wall: Wall) -> None:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, wall.point_1, wall.point_2, radius=wall.radius)
        shape.friction = wall.friction
        shape.elasticity = wall.elasticity
        shape.collision_type = CollisionTypes.WALL

        self.space.add(shape, body)
        self.static_lines.append(shape)

    def on_update(self, delta_time: float) -> None:
        start_time = timeit.default_timer()

        # Check for balls that fall off the screen
        for sprite in self.sprite_list:
            if sprite.pymunk_shape.body.space == None:
                sprite.remove_from_sprite_lists()
            if sprite.pymunk_shape.body.position.y < 0:
                # Remove balls from physics space
                self.space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
                # Remove balls from physics list
                sprite.remove_from_sprite_lists()

        # Update physics
        # Use a constant time step, don't use delta_time
        # See "Game loop / moving time forward"
        # https://www.pymunk.org/en/latest/overview.html#game-loop-moving-time-forward
        self.space.step(1 / 60.0)

        # If we are dragging an object, make sure it stays with the mouse. Otherwise
        # gravity will drag it down.
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = 0, -100

        # Move sprites to where physics objects are
        for sprite in self.sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

    def create_ball(self, x: float, y: float, radius: float = 10, mass: float = 1) -> None:
        mass = mass
        radius = radius
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        body.apply_impulse_at_local_point(pymunk.Vec2d(500,500))
        shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
        shape.collision_type = CollisionTypes.BALL
        shape.friction = 1000
        shape.elasticity = 1
        self.space.add(body, shape)

        sprite = BallSprite(shape, "Resources/ball.png")
        self.sprite_list.append(sprite)

    def set_paddle_x_velocity(self, x_velocity: float) -> None:
        self.paddle_body.velocity = (x_velocity, 0)

    def create_paddle(self, paddle: Paddle) -> pymunk.Body:
        paddle_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        shape = pymunk.Poly.create_box(paddle_body, (paddle.width, paddle.height))
        shape.friction = paddle.friction
        shape.elasticity = paddle.elasticity
        paddle_body.position = pymunk.Vec2d(paddle.pos[0], paddle.pos[1])
        shape.collision_type = CollisionTypes.PLAYER

        sprite = PhysicsSprite(shape, "Resources/paddle.png")

        self.space.add(paddle_body, shape)
        self.sprite_list.append(sprite)

        return paddle_body

    def create_block(self, block: Block) -> pymunk.Body:
        block_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Poly.create_box(block_body, (block.width, block.height))
        shape.friction = block.friction
        shape.elasticity = block.elasticity
        block_body.position = pymunk.Vec2d(block.pos[0], block.pos[1])
        shape.collision_type = CollisionTypes.BRICK
        sprite = PhysicsSprite(shape, "Resources/brick.png")


        self.space.add(block_body, shape)
        self.sprite_list.append(sprite)

        return block_body


def main() -> None:
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.run()


if __name__ == "__main__":
    main()