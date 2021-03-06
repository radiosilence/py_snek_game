import time

import pygame

from game_objects.food import Food
from game_objects.game_settings import GameSettings
from game_objects.snake import Snake
from utils.game_utils import snake_is_out_of_bounds


def game_loop(game_board: pygame, display, game_settings: GameSettings):
    display_size = game_settings.display_size
    pixel = game_settings.pixel_size
    colors = game_settings.colours
    font_style_large = game_board.font.SysFont(None, 50)
    font_style_small = game_board.font.SysFont(None, 25)

    snake = Snake(game_settings.starting_position, pixel)
    food = Food(display_size, pixel)
    clock = game_board.time.Clock()
    game_running = True
    game_playing = True

    def message(msg, color, font):
        mesg = font.render(msg, True, color)
        display.blit(mesg, game_settings.starting_position)

    # This section is the game intro screen
    while game_running:
        score = 0
        while game_playing:
            for event in game_board.event.get():
                if event.type == game_board.QUIT:
                    game_running = False
                if event.type == game_board.KEYDOWN:
                    if event.key == game_board.K_LEFT and not (snake.direction == snake.direction_right):
                        snake.move_left()
                    elif event.key == game_board.K_RIGHT and not (snake.direction == snake.direction_left):
                        snake.move_right()
                    elif event.key == game_board.K_UP and not (snake.direction == snake.direction_down):
                        snake.move_up()
                    elif event.key == game_board.K_DOWN and not (snake.direction == snake.direction_up):
                        snake.move_down()
            if food.position == snake.head_position:
                score = score + 1
                food.move_food(snake.tail)
            snake.resolve_position(score)
            if snake_is_out_of_bounds(snake.head_position, display_size):
                game_playing = False
            if snake.is_eating_itself():
                game_playing = False

            # Logging
            print(
                f"Snake Position: x={snake.head_position[0]}, y={snake.head_position[1]}"
            )
            print(f"Food Position: x={food.position[0]}, y={food.position[1]}")
            print(f"Score: {score}")
            if food.position == snake.head_position:
                print("Snake is on food!")
            if snake_is_out_of_bounds(snake.head_position, display_size):
                print("Snake out of bounds:")

            # Rendering Game
            display.fill(colors.background)
            game_board.draw.rect(
                display,
                colors.highlight,
                [food.position[0], food.position[1], pixel, pixel],
            )
            game_board.draw.rect(
                display,
                colors.main,
                [snake.head_position[0], snake.head_position[1], pixel, pixel],
            )
            for tail_position in snake.tail:
                game_board.draw.rect(
                    display,
                    colors.main,
                    [tail_position[0], tail_position[1], pixel, pixel],
                )
            game_board.display.update()
            clock.tick(10)

        # Rendering Lost Screen
        message("You Lost", colors.highlight, font_style_large)
        game_board.display.update()
        time.sleep(2)
        display.fill(colors.background)
        message(f"Score: {score}", colors.highlight, font_style_small)
        game_board.display.update()
        time.sleep(2)
        game_running = False

    game_board.quit()
    quit()
