from math import prod

games = open("2").readlines()

cube_count = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def get_game_number(game: str) -> int:
    return int(game.split(":")[0].split(" ")[1])


def get_game_draws(game: str) -> list[str]:
    return game.split(":")[1].replace(";", ",").split(",")


def is_draw_valid(draw: str) -> bool:
    count, colour = draw.strip().split(" ")
    return int(count) <= cube_count[colour]


def is_game_valid(game: str) -> bool:
    return all(map(is_draw_valid, get_game_draws(game)))


def get_game_power(game: str) -> int:
    min_cube_count = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for draw in get_game_draws(game):
        count, colour = draw.strip().split(" ")
        min_cube_count[colour] = max([min_cube_count[colour], int(count)])
    return prod(min_cube_count.values())


print(f"Part 1: {sum(map(get_game_number, filter(is_game_valid, games)))}")
print(f"Part 2: {sum(map(get_game_power, games))}")
