
class Block:
    def __init__(self, pos: tuple[float, float],
                 width: float, height: float,
                 friction: float,
                 elasticity: float,
                 armor: int,
                 image_path: str = "Resources/brick.png"):
        self.pos = pos
        self.width = width
        self.height = height
        self.armor = armor
        self.friction = friction
        self.elasticity = elasticity
        self.image_path = image_path

        # block_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # shape = pymunk.Poly.create_box(block_body, (block.width, block.height))
        # shape.friction = block.friction
        # shape.elasticity = block.elasticity
        # block_body.position = pymunk.Vec2d(block.pos[0], block.pos[1])
        # shape.collision_type = CollisionTypes.BRICK
        # sprite = PhysicsSprite(shape, "Resources/brick.png")
        #
        #
        # self.space.add(block_body, shape)
        # self.sprite_list.append(sprite)
        #
        # return block_body

# class BlockController:



