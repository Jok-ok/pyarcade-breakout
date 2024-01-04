"""Very simple breakout clone. A circle shape serves as the paddle, then
breakable bricks constructed of Poly-shapes.

The code showcases several pymunk concepts such as elasitcity, impulses,
constant object speed, joints, collision handlers and post step callbacks.
"""

import random
import neat
import os
from functools import partial
from datetime import datetime
from sources.visualize import *

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d


class GenerationCounter:
    generation_num: int = 0
    current_time: str

    @staticmethod
    def add_generation():
        GenerationCounter.generation_num += 1

    @staticmethod
    def set_current_time(time: str):
        GenerationCounter.current_time = time


width, height = 1000, 800

collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4,
}


def spawn_ball(space, position, direction):
    global ball_body
    ball_body = pymunk.Body(1, float("inf"))
    ball_body.position = position

    ball_shape = pymunk.Circle(ball_body, 5)
    ball_shape.color = pygame.Color("green")
    ball_shape.elasticity = 1.0
    ball_shape.collision_type = collision_types["ball"]

    ball_body.apply_impulse_at_local_point(Vec2d(*direction))

    # Keep ball velocity at a static value
    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 2000

    ball_body.velocity_func = constant_velocity

    space.add(ball_body, ball_shape)
    return ball_shape


def setup_level(space, player_body, brick_destroyed_callback):
    # Remove balls and bricks
    for s in space.shapes[:]:
        if s.body.body_type == pymunk.Body.DYNAMIC and s.body not in [player_body]:
            space.remove(s.body, s)

    # Spawn a ball for the player to have something to play with
    spawn_ball(
        space, player_body.position + (0, 40), random.choice([(1, 10), (-1, 10)])
    )

    # Spawn bricks
    for x in range(0, 41):
        x = x * 20 + 100
        for y in range(0, 10):
            y = y * 10 + height - 200
            brick_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            brick_body.position = x, y
            brick_shape = pymunk.Poly.create_box(brick_body, (20, 10))
            brick_shape.elasticity = 1.0
            brick_shape.color = pygame.Color("blue")
            brick_shape.group = 1
            brick_shape.collision_type = collision_types["brick"]
            space.add(brick_body, brick_shape)

    # Make bricks be removed when hit by ball
    def remove_brick(arbiter, space, data):
        brick_shape = arbiter.shapes[0]
        space.remove(brick_shape, brick_shape.body)
        brick_destroyed_callback()

    h = space.add_collision_handler(collision_types["brick"], collision_types["ball"])
    h.separate = remove_brick


def main(game_end_callback, game_update_callback, brick_destroyed_callback, ball_collision_callback, gen_id):
    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)
    ### Physics stuff
    space = pymunk.Space()
    pymunk.pygame_util.positive_y_is_up = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ### Game area
    # walls - the left-top-right walls

    static_lines = [
        pymunk.Segment(space.static_body, (50, 50), (50, height - 50), 10),
        pymunk.Segment(space.static_body, (50, height - 50), (width - 50, height - 50), 10),
        pymunk.Segment(space.static_body, (width - 50, height - 50), (width - 50, 50), 10),
    ]
    for line in static_lines:
        line.color = pygame.Color("lightgray")
        line.elasticity = 1.0

    space.add(*static_lines)

    # bottom - a sensor that removes anything touching it
    bottom = pymunk.Segment(space.static_body, (50, 50), (width - 50, 50), 10)
    bottom.sensor = True
    bottom.collision_type = collision_types["bottom"]
    bottom.color = pygame.Color("red")

    def remove_first(arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        space.remove(ball_shape, ball_shape.body)
        game_end_callback()
        return True

    h = space.add_collision_handler(collision_types["ball"], collision_types["bottom"])
    h.begin = remove_first
    space.add(bottom)

    ### Player ship
    global player_body
    player_body = pymunk.Body(500, float("inf"))
    player_body.position = width / 2, 100

    player_shape = pymunk.Segment(player_body, (-50, 0), (50, 0), 15)
    player_shape.color = pygame.Color("red")
    player_shape.elasticity = 1.0
    player_shape.collision_type = collision_types["player"]

    def pre_solve(arbiter, space, data):
        # We want to update the collision normal to make the bounce direction
        # dependent of where on the paddle the ball hits. Note that this
        # calculation isn't perfect, but just a quick example.
        set_ = arbiter.contact_point_set
        if len(set_.points) > 0:
            player_shape = arbiter.shapes[0]
            width = (player_shape.b - player_shape.a).x
            delta = (player_shape.body.position - set_.points[0].point_a).x
            normal = Vec2d(0, 1).rotated(delta / width / 2)
            set_.normal = normal
            set_.points[0].distance = 0
        arbiter.contact_point_set = set_
        ball_collision_callback()
        return True

    h = space.add_collision_handler(collision_types["player"], collision_types["ball"])
    h.pre_solve = pre_solve

    # restrict movement of player to a straigt line
    # move_joint = pymunk.GrooveJoint(
    #     space.static_body, player_body, (100, 100), (width - 100, 100), (0, 0)
    # )
    space.add(player_body, player_shape)
    global state
    # Start game
    setup_level(space, player_body, brick_destroyed_callback)
    while running:
        game_update_callback()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                running = False
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and (
                    event.key in [pygame.K_ESCAPE, pygame.K_q]
            ):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "breakout.png")

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player_body.velocity = (-1500, 0)
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                player_body.velocity = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player_body.velocity = (1000, 0)
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                player_body.velocity = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                setup_level(space, player_body)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spawn_ball(
                    space,
                    player_body.position + (0, 40),
                    random.choice([(1, 10), (-1, 10)]),
                )

        ### Clear screen
        screen.fill(pygame.Color("black"))

        ### Draw stuff
        space.debug_draw(draw_options)

        state = []
        for x in space.shapes:
            s = "%s %s %s" % (x, x.body.position, x.body.velocity)
            state.append(s)

        ### Update physics
        fps = 200
        dt = 1.0 / fps
        space.step(dt)

        ### Info and flip screen
        screen.blit(
            font.render("fps: " + str(clock.get_fps()), 1, pygame.Color("white")),
            (0, 0),
        )
        screen.blit(
            font.render(
                "Move with left/right arrows, space to spawn a ball",
                1,
                pygame.Color("darkgrey"),
            ),
            (5, height - 35),
        )
        screen.blit(
            font.render(
                "Press R to reset, ESC or Q to quit", 1, pygame.Color("darkgrey")
            ),
            (5, height - 20),
        )

        pygame.display.flip()
        clock.tick(fps)
    return genomes[gen_id]


def eval_genomes(raw_genomes: list[neat.DefaultGenome], config):
    global genomes, networks, tries

    tries = 0
    networks = []
    genomes = raw_genomes

    for _, g in raw_genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        networks.append(net)
        g.fitness = 0

    genomes = raw_genomes
    run = True
    for i in range(len(genomes)):
        main(partial(restart_game, i),
             partial(update_event, i),
             partial(add_val_to_fitness, i, 0),
             partial(add_val_to_fitness, i, 15), i)

    genomes = sorted(genomes, key=lambda x: x[1].fitness)
    winner = genomes[0][1]
    node_names = {-1: "Кооордината мяча X", -2: "Коррдината мяча Y", -3: "Разница между X шарика и X платформы",
                  -4: "Разница между Y шарика и Y платформы", 0: "Движение влево", 1: "Стоять на месте",
                  2: "Движение вправо"}
    checkpoints_dir_name = f"checkpoints {GenerationCounter.current_time}"
    draw_net(config, winner, True, node_names=node_names,
             filename=f"{checkpoints_dir_name}/neuro_schemes/winner_{GenerationCounter.generation_num}.svg")
    GenerationCounter.add_generation()

    # visualise.plot_stats(stats, ylog=False, view=True)
    # visualise.plot_species(stats, view=True)
    # with multiprocessing.Pool(multiprocessing.cpu_count() - 1,
    #                           initializer=initialize_values, initargs=(raw_genomes, networks)) as pool:
    #     genomes = genomes
    #     tries = tries
    #     networks = networks
    #     # restart_cb = lambda: restart_game(i)
    #     # update_cb = lambda: update_event(i)
    #     # add_val2 = lambda: add_val_to_fitness(i, 2)
    #     # add_val15 = lambda: add_val_to_fitness(i, 15)
    #     p = pool.starmap(main, [[partial(restart_game, i),
    #                             partial(update_event, i),
    #                             partial(add_val_to_fitness, i, 2),
    #                             partial(add_val_to_fitness, i, 15), i] for i in range(len(raw_genomes))])
    #
    #     p.sort(key=lambda x: x[0], reverse=True)
    #
    # for raw_genome in raw_genomes:
    #     trained = p.pop(-1)
    #     raw_genome[1].fitness = trained[1].fitness


def initialize_values(g, n):
    global genomes, networks
    genomes = g
    networks = n


def restart_game(gen_id):
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, code=0))
    add_val_to_fitness(gen_id, -10)


def add_val_to_fitness(gen_id, val):
    try:
        genomes[gen_id][1].fitness += val
    except Exception:
        print(genomes)
        print(gen_id)
        raise ValueError()


def update_event(gen_id):
    global genomes, player_body, ball_body
    add_val_to_fitness(gen_id, 0.001)
    # if not (player_body.position.x > 100 and player_body.position.x < width - 100):
    #     add_val_to_fitness(gen_id, -20)
    #     pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))

    output = networks[gen_id].activate(
        (ball_body.position.x, ball_body.position.y,
         abs(player_body.position.x - ball_body.position.x), abs(player_body.position.y - ball_body.position.y)))
    general_output = output.index(max(output)) - 1

    player_body.velocity = (general_output * 2000, 0)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    GenerationCounter.current_time = current_time
    checkpoints_dir_name = f"checkpoints {current_time}"
    if not os.path.exists(checkpoints_dir_name):
        os.mkdir(checkpoints_dir_name)

    checkpointer = neat.Checkpointer(True, filename_prefix=f"{checkpoints_dir_name}/checkpoint_generation_")
    checkpointer.generation = True
    checkpointer.show_species_detail = True

    p = neat.Population(config)

    reporter = neat.reporting.StdOutReporter(True)
    reporter.generation = True
    reporter.show_species_detail = True
    p.add_reporter(neat.reporting.StdOutReporter(True))
    p.add_reporter(checkpointer)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes)

    plot_stats(stats)

    print("Best fitness -> {}".format(winner))


def run_learning(file_name: str):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, file_name)
    run(config_path)


def run_generation():
    checkpoint_paths = []
    for path in os.walk("../"):
        if path[0].startswith("./checkpoints"):
            checkpoint_paths.append(path)

    path_to_chkp = ""

    chosen_dir = choose_checkpoint_directory([pths[0] for pths in checkpoint_paths])
    for pth in checkpoint_paths:
        if pth[0] == chosen_dir:
            path_to_chkp = choose_checkpoint_directory(pth[2])
            break

    checkpoint_path = f"{chosen_dir}/{path_to_chkp}"
    run_generation_checkpoint(checkpoint_path)


def run_generation_checkpoint(checkpoint_path: str):

    population = neat.Checkpointer.restore_checkpoint(checkpoint_path)
    reporter = neat.reporting.StdOutReporter(True)
    reporter.generation = True
    reporter.show_species_detail = True
    population.add_reporter(reporter)
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    try:

        winner = population.run(eval_genomes, n=1)
    except Exception:
        pygame.quit()

    # plot_stats(stats)

    print("Best fitness -> {}".format(winner))


def choose_checkpoint_directory(chckpoints: [str]) -> str:
    value = ""
    while not (type(value) is int):
        c = 1
        print("Выьерите нужный путь к чекпоинту: ")
        for chkp in chckpoints:
            print(f"{c}. {chkp}")
            c += 1
        value = input("Выберите нужный чекпоинит.")
        if value.isalnum():
            if len(chckpoints) >= int(value) > 0:
                value = int(value) - 1
                break
        print("Вы ввели что-то не то (((. Но всегда можно попробовать еще раз!")
    return chckpoints[value]


if __name__ == "__main__":
    run_learning("../NeatConf.txt")
