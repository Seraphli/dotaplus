import random
from math import sqrt, log
from dataproc.ban_pick import BanPick
from cv.img_proc import HeroMatchCV
from tqdm import trange
import sys
import copy


class BanPickGame(object):
    def __init__(self, ban_pick, available, teams, team_no):
        self.bp = ban_pick
        self.available = available
        # remove none before initialize
        self.teams = self.bp.remove_none(*teams)
        self.team_no = team_no

    def get_moves(self):
        if len(self.teams[0]) == 5 and len(self.teams[1]) == 5:
            return []
        return copy.deepcopy(self.available)

    def do_move(self, move):
        self.available.remove(move)
        if len(self.teams[0]) < 5:
            self.teams[0].append(move)
        elif len(self.teams[1]) < 5:
            self.teams[1].append(move)

    def clone(self):
        return BanPickGame(self.bp, copy.deepcopy(self.available),
                           copy.deepcopy(self.teams), self.team_no)

    def is_game_over(self):
        return sum([len(t) for t in self.teams if t != 'none']) == 10

    def get_result(self):
        teammates = self.teams[self.team_no]
        match_ups = self.teams[1 - self.team_no]
        _, _, wr, _ = self.bp.win_rate(match_ups, teammates)
        return wr


class Node(object):
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent_node = parent
        self.child_nodes = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_moves()

    def uct_select_child(self):
        s = sorted(self.child_nodes, key=lambda c: c.wins / c.visits + sqrt(
            2 * log(self.visits) / c.visits))[-1]
        return s

    def add_child(self, m, s):
        n = Node(move=m, parent=self, state=s)
        self.untried_moves.remove(m)
        self.child_nodes.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result

    @property
    def q(self):
        return self.wins / self.visits

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(
            self.visits) + " U:" + str(self.untried_moves) + "]"

    def tree_to_string(self, indent):
        s = self.indent_string(indent) + str(self)
        for c in self.child_nodes:
            s += c.tree_to_string(indent + 1)
        return s

    def indent_string(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def children_to_string(self):
        s = ""
        for c in self.child_nodes:
            s += str(c) + "\n"
        return s


def uct(root_state, iter_max, verbose=False):
    root_node = Node(state=root_state)

    for _ in trange(iter_max, file=sys.stdout):
        node = root_node
        state = root_state.clone()

        # Select
        while node.untried_moves == [] and node.child_nodes:
            node = node.uct_select_child()
            state.do_move(node.move)

        # Expand
        if node.untried_moves:
            m = random.choice(node.untried_moves)
            state.do_move(m)
            node = node.add_child(m, state)

        while state.get_moves():
            state.do_move(random.choice(state.get_moves()))

        # Backpropagate
        while node is not None:
            node.update(state.get_result())
            node = node.parent_node

    if verbose:
        print(root_node.tree_to_string(0))
    else:
        print(root_node.children_to_string())

    sorted_child = sorted(root_node.child_nodes, key=lambda c: c.q,
                          reverse=True)

    return [(sorted_child[i].move, sorted_child[i].q) for i in range(3)]


def uct_ban_pick():
    team_no = 0
    cv = HeroMatchCV()
    bp = BanPick()
    available, teams = cv.find_heroes()
    print('Available: {}'.format(len(available)))
    print('Teams: {}'.format(teams))
    state = BanPickGame(bp, available, teams, team_no)
    m = uct(root_state=state, iter_max=200, verbose=False)
    print("Result: " + str(m) + "\n")


def main():
    uct_ban_pick()


if __name__ == '__main__':
    main()
