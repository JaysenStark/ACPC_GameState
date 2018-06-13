import re
from itertools import chain


class MessageParser(object):
    """parse message following ACPC protocol"""
    def __init__(self):
        self.betting_regex = re.compile("c|f|r[\d]*")
        self.position, self.hand_number, self.betting_actions = None, None, None
        self.board_cards, self.hole_cards = None, None
        self.flatten_betting_actions, self.flatten_board_cards, self.flatten_hole_cards = None, None, None
    
    def parse(self, message):
        """parse position, hand_number into integer; parse betting_str into two-dim betting_actions list;
        parse hole_and_board_str into two-dim hole_cards list and two-dim board_cards respectively"""
        _, position_str, hand_number_str, betting_str, hole_and_board_str = message.split(":")

        self.position = int(position_str)
        self.hand_number = int(hand_number_str)
        self.betting_actions = self.parse_betting_action(betting_str)
        self.hole_cards, self.board_cards = self.parse_hole_and_board_cards(hole_and_board_str)

        self.flatten_betting_actions = list(chain.from_iterable(self.betting_actions))
        self.flatten_hole_cards = list(chain.from_iterable(self.hole_cards))
        self.flatten_board_cards = list(chain.from_iterable(self.board_cards))

    def parse_betting_action(self, betting_str):
        """parse betting_str into 2-dim betting actions list, dim-1 is round dim, dim-2 is action dim"""
        betting_actions = betting_str.split("/")
        for rd in range(len(betting_actions)):
            string = betting_actions[rd]
            betting_actions[rd] = self.betting_regex.findall(string)
        return betting_actions

    def parse_hole_and_board_cards(self, hb_str):
        """split whole str into parse hole_str and board_str, then parse them into list respectively"""
        idx = hb_str.index("/")
        hole_str, board_str = hb_str[:idx], hb_str[idx:]
        hole_cards, board_cards = self.parse_hole_str(hole_str), self.parse_board_str(board_str)
        return hole_cards, board_cards

    @staticmethod
    def parse_hole_str(hole_str):
        """return a two-dim list, dim-1 is player dim, dim-2 is card dim, element looks like '2c'"""
        holes = hole_str.split("|")
        for player in range(len(holes)):
            string = holes[player]
            holes[player] = [string[x:x+2] for x in range(0, len(string), 2)]
        return holes

    @staticmethod
    def parse_board_str(board_str):
        """return a two-dim list, dim-1 is round dim, dim-2 is card dim, element looks like '2c'"""
        boards = board_str.split("/")
        for rd in range(len(boards)):
            string = boards[rd]
            boards[rd] = [string[x:x+2] for x in range(0, len(string), 2)]
        return boards

    def get_position(self):
        return self.position

    def get_hand_number(self):
        return self.hand_number

    def get_betting_action(self, rd=None):
        """return betting string of given round, if round is not specified, return betting string of all round"""
        if rd is not None:
            if 0 <= rd < len(self.betting_actions):
                return self.betting_actions[rd]
            raise Exception
        return self.betting_actions

    def get_hole_card(self, position=None):
        if position is not None:
            if 0 <= position < len(self.hole_cards):
                return self.hole_cards[position]
            raise Exception
        return self.hole_cards

    def get_board_card(self, rd=None):
        if rd is not None:
            if 0 <= rd < len(self.board_cards):
                return self.board_cards[rd]
            raise Exception
        return self.board_cards

    def get_flatten_board_cards(self):
        return self.flatten_board_cards

    def get_flatten_hole_cards(self):
        return self.flatten_hole_cards

    def get_flatten_betting_actions(self):
        return self.flatten_betting_actions
