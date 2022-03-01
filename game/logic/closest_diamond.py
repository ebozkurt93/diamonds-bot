import random
from ..util import get_direction
from math import sqrt


class ClosestDiamondLogic(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1

    @staticmethod
    def manhattan(a, b):
        return sum(abs(val1 - val2) for val1, val2 in zip(a, b))

    def get_closest_diamond_position(self, board_bot, board):
        current_position = board_bot["position"]
        cur_x = current_position["x"]
        cur_y = current_position["y"]

        selected_diamond = None
        distance = None
        selected_diamond_pos = None
        for diamond in board.diamonds:
            diamond_pos = diamond.get('position')

            delta_x, delta_y = get_direction(
                cur_x,
                cur_y,
                diamond_pos["x"],
                diamond_pos["y"],
            )
            manhattan_dist = self.manhattan((cur_x, cur_y), (diamond_pos["x"], diamond_pos["y"]))
            if selected_diamond is None or distance > delta_x + delta_y:
                selected_diamond = diamond
                distance = manhattan_dist
                selected_diamond_pos = diamond_pos
        return selected_diamond_pos

    def next_move(self, board_bot, board):
        print(board_bot)
        props = board_bot["properties"]

        # Analyze new state
        if props["diamonds"] == 5:
            # Move to base if we are full of diamonds
            base = props["base"]
            self.goal_position = base
        else:
            # Move towards first diamond on board
            # self.goal_position = board.diamonds[0].get('position')
            self.goal_position = self.get_closest_diamond_position(board_bot, board)
            print(self.goal_position)

        if self.goal_position:
            # Calculate move according to goal position
            current_position = board_bot["position"]
            cur_x = current_position["x"]
            cur_y = current_position["y"]
            delta_x, delta_y = get_direction(
                cur_x,
                cur_y,
                self.goal_position["x"],
                self.goal_position["y"],
            )

            if (cur_x, cur_y) == self.previous_position:
                # We did not manage to move, lets take a turn to hopefully get out stuck position
                if delta_x != 0:
                    delta_y = delta_x * self.turn_direction
                    delta_x = 0
                elif delta_y != 0:
                    delta_x = delta_y * self.turn_direction
                    delta_y = 0
                # Switch turn direction for next time
                self.turn_direction = -self.turn_direction
            self.previous_position = (cur_x, cur_y)

            return delta_x, delta_y

        return 0, 0
