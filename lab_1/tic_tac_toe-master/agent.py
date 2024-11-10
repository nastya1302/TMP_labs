import ast

import numpy as np

from utils import log


class Agent(object):
    def __init__(
        self,
        sym,
        exploration_rate=0.90,
        decay=0.01,
        learning_rate=0.5,
        discount_factor=0.01,
    ) -> None:
        """
        An agent is a problem solver.
        It should perform actions like:
            - plotting a symbol on the tic-tac-toe board if it is vacant.
            - Remember which states are more profitable than the others.
            - Explore better states
            - Exploit for maximum profit

        params:
        - exploration_rate: A floating point number < 1
                which defines the agents probability to explore.
        - learning_rate: Used for assessing the value of intermediate
                states during temporal difference learning.
        - discount_factor: The factor by which a reward must be reduced
                to be passed on for intermediate states
        """
        self.sym = sym
        self.states = {}
        self.state_order = []
        self.learning_rate = learning_rate
        self.decay = decay
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    @staticmethod
    def serialize_board(board) -> str:
        """
        convert the matrix

            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ]

            to the form: "123456789" i.e. flatten and stringify
        """
        serialized_board = board.flatten()
        return ''.join([str(i) for i in serialized_board.flatten().tolist()])

    def get_serious(self) -> None:
        """
        Quit exploring states and start exploiting
        Use this if you want to play with the agent.
        """
        self.exploration_rate = 0

    def learn_by_temporal_difference(self, reward, new_state_key, state_key):
        """
        Implementation of the temporal difference formula.
        https://en.wikipedia.org/wiki/Temporal_difference_learning
        https://detailed.af/reinforcement/
        """
        old_state = self.states.get(state_key, np.zeros((3, 3)))
        self.exploration_rate = max(self.exploration_rate - self.decay, 0.3)
        return self.learning_rate * ((reward * self.states[new_state_key]) - old_state)

    def set_state(self, old_board, action) -> None:
        """
        Store the action performed for a given state
        """
        state_key = Agent.serialize_board(old_board)
        self.state_order.append((state_key, action))

    def on_reward(self, reward) -> None:
        """
        Assign rewards to actions performed on intermediate states.
        """
        if len(self.state_order) == 0:
            return None
        new_state_key, new_action = self.state_order.pop()

        self.states[new_state_key] = np.zeros((3, 3))

        self.states[new_state_key].itemset(new_action, reward)

        while self.state_order:
            state_key, action = self.state_order.pop()

            reward *= self.discount_factor

            if state_key in self.states:
                reward += self.learn_by_temporal_difference(
                    reward, new_state_key, state_key
                ).item(new_action)
                log("update learning", state_key, action, reward)
                log(self.states[state_key])
                self.states[state_key].itemset(action, reward)
            else:
                self.states[state_key] = np.zeros((3, 3))
                reward = self.learn_by_temporal_difference(
                    reward, new_state_key, state_key
                ).item(new_action)
                self.states[state_key].itemset(action, reward)
            new_state_key = state_key
            new_action = action

    def select_move(self, board) -> tuple:
        """
        Choose from exploration and exploitation.
        Epsilon greedy implementation for policy.
        http://home.deib.polimi.it/restelli/MyWebSite/pdf/rl5.pdf
        http://tokic.com/www/tokicm/publikationen/papers/AdaptiveEpsilonGreedyExploration.pdf
        """
        explore_message = 'Exploration turn'
        missing_experience_message = 'No experience for this state: explore'
        experience_present_message = 'Using previous experience'
        state_key = Agent.serialize_board(board)
        log("-" * 100)
        log("state key", state_key)
        p = np.random.random()
        exploration = p < self.exploration_rate
        log(p, "<", self.exploration_rate)
        message = (
            explore_message
            if exploration
            else (
                missing_experience_message
                if state_key not in self.states
                else experience_present_message
            )
        )

        log(message)
        action = (
            self.explore_board(board)
            if exploration or state_key not in self.states
            else self.exploit_board(state_key, board)
        )
        log("Choose cell", action)
        self.set_state(board, action)
        return action

    def explore_board(self, board, depth=0) -> tuple:
        """
        Find an empty cell from the board
        """
        zero_x, zero_y = np.where(board == 0)
        vacant_cells = [(x, y) for x, y in zip(zero_x, zero_y)]
        pseudo_board = np.array(board, copy=True)
        randomly_selected_vacant_cell = np.random.choice(len(vacant_cells))
        selected_cell = vacant_cells[randomly_selected_vacant_cell]
        pseudo_board[selected_cell[0]][selected_cell[1]] = 1 if self.sym == 'O' else 2
        state_key = Agent.serialize_board(pseudo_board)
        log(state_key)
        if state_key not in self.states or depth == 9:
            return selected_cell
        depth += 1
        return self.explore_board(board, depth=depth)

    def exploit_board(self, state_key, board):
        """
        Find the best action for the given state
        """
        state_values = self.states[state_key]
        log('State rewards', state_values)
        free_cells = np.argwhere(board == 0)
        best_values = {}
        for idx, value in np.ndenumerate(state_values):
            if idx in free_cells:
                best_values[str(idx)] = value

        best_value_indices = [
            key
            for m in [max(best_values.values())]
            for key, val in best_values.items()
            if val == m
        ]

        log('best_value_indices', best_value_indices)
        select_index = np.random.choice(len(best_value_indices))
        return ast.literal_eval(best_value_indices[select_index])
 