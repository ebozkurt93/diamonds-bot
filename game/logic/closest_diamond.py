import random
from ..util import get_direction
from math import sqrt


class ClosestDiamondLogic(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1
        self.max_capacity = 5


    @staticmethod
    def manhattan(a, b):
        return sum(abs(val1 - val2) for val1, val2 in zip(a, b))

    def get_distance_between_positions(self, a, b):
        return self.manhattan(a, b)

    def get_distance_to_home(self, board_bot):
        base = board_bot["properties"]["base"]
        current_position = board_bot["position"]
        cur_x = current_position["x"]
        cur_y = current_position["y"]

        return self.get_distance_between_positions((base["x"], base["y"]), (cur_x, cur_y))

    def get_distance_to_reset_button(self, board_bot, board):
        current_position = board_bot["position"]
        cur_x = current_position["x"]
        cur_y = current_position["y"]
        diamond_x = board.diamondButton['position']['x']
        diamond_y = board.diamondButton['position']['y']

        return board.diamondButton['position'], self.get_distance_between_positions((diamond_x, diamond_y), (cur_x, cur_y))

    # millisecondsLeft
    # get best diamond (closest to us and base), naively sum distance to base and us, take lowest
    def get_closest_diamond_position_and_distance(self, board_bot, board, current_capacity):
        current_position = board_bot["position"]
        cur_x = current_position["x"]
        cur_y = current_position["y"]

        selected_diamond = None
        distance = None
        selected_diamond_pos = None
        for diamond in board.diamonds:
            diamond_pos = diamond.get('position')
            if current_capacity == self.max_capacity - 1 and diamond["properties"]["points"] == 2:
                continue

            manhattan_dist = self.manhattan((cur_x, cur_y), (diamond_pos["x"], diamond_pos["y"]))
            if selected_diamond is None or distance > manhattan_dist:
                selected_diamond = diamond
                distance = manhattan_dist
                selected_diamond_pos = diamond_pos

        # if we have diamonds in bag and there is no time left

        return selected_diamond_pos, distance

    # todo: if there isn't enough time left, go to base
    # todo: if reset button is closer than any diamond, go to there
    # todo: if the bag is closer to full, prefer going to base instead of going to a diamond further

    def next_move(self, board_bot, board):
        # print(board_bot)

        # if len(board.bots) > 0:
        def get_bot(name):
            for item in board.bots:
                if item.get("properties", {}).get("name") == name:
                    return item
        our_bot = get_bot("bango")
        try:
            time_left = our_bot["properties"]["millisecondsLeft"]
        except:
            time_left = 100000
        print(our_bot)

        props = board_bot["properties"]
        closest_diamond_distance = 99999
        base = props["base"]

        # Analyze new state
        if props["diamonds"] >= self.max_capacity:
            # Move to base if we are full of diamonds
            self.goal_position = base

        # elif props["diamonds"] > 0 and
        else:
            closest_diamond_position, closest_diamond_distance = self.get_closest_diamond_position_and_distance(board_bot, board, props["diamonds"])
            home_distance = self.get_distance_to_home(board_bot)
            reset_button_position, reset_distance = self.get_distance_to_reset_button(board_bot, board)
            if props["diamonds"] == 0:
                # print('aaaaaaaaa', closest_diamond_position, reset_button_position)
                if closest_diamond_distance < reset_distance:
                    self.goal_position = closest_diamond_position
                else:
                    self.goal_position = reset_button_position
            elif props["diamonds"] > 0 and (time_left / 10) + 2 <= home_distance:
                self.goal_position = base
            # elif props["diamonds"] > 0 and self.get_distance_to_home(board_bot) <= closest_diamond_distance:
            #     self.goal_position = base
            else:
                self.goal_position = closest_diamond_position

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
