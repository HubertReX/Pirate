import logging

class State():
    def __init__(self, game):
        self.game = game
        if len(self.game.state_stack) > 0:
            self.prev_state = self.game.state_stack[-1]
        else:
            self.prev_state = None

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 0:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        self.list_stack()

    def exit_state(self):
        self.game.state_stack.pop()
        if len(self.game.state_stack) == 0:
            self.game.quit()
        self.list_stack()

    def list_stack(self):
        stk = ""
        for s in self.game.state_stack:
            stk += " -> " + s.__class__.__name__
        logging.debug(stk)