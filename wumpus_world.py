# WumpusWorld
# A simulated representation of a real Wumpus World, aligned with the specified
# characteristics in the AIMA text.
# Note: This is not a state model. It _is_ the real world / environment within
# which the agent operates. Think of it as actual, physical, reality.
# Note 2: This simulation will not include the modeling of time, for the sake of
# simplicity. This only affects the 'Bump' and 'Scream' percepts. In the case of
# 'Bump', we assume that when an agent is in a room facing a wall, it should receive
# the 'Bump' percept. For 'Scream', when the wumpus is killed we let the scream
# linger throughout the cave indefinitely.
# YOUR NAME

class WumpusWorld:

    EXIT_LOCATION = (1, 1)

    def __init__(self, agent_location=None, agent_direction='East',
                 agent_alive=True, wumpus_alive=None,
                 wumpus_location=None, gold_location=None,
                 pit_locations=None):
        self.agent_location = agent_location if agent_location is not None else (1, 1)
        self.agent_direction = agent_direction
        self.agent_alive = agent_alive
        self.wumpus_alive = wumpus_alive
        self.wumpus_location = wumpus_location
        self.gold_location = gold_location
        self.pit_locations = pit_locations or []
        self.arrow_available = True

    def percept(self, location):
        if not location:
            return None, None, None, None, None
        stench = "Stench" if self.stench_at(location) else None
        breeze = "Breeze" if self.breeze_at(location) else None
        glitter = "Glitter" if self.glitter_at(location) else None
        bump = "Bump" if self.agent_bumped_wall() else None
        scream = None if self.wumpus_alive else "Scream" 
        
        return stench, breeze, glitter, bump, scream

    def turned_left(self):
        directions = ['North', 'East', 'South', 'West']
        current_index = directions.index(self.agent_direction)
        self.agent_direction = directions[(current_index - 1) % 4]

    def turned_right(self):
        directions = ['North', 'East', 'South', 'West']
        current_index = directions.index(self.agent_direction)
        self.agent_direction = directions[(current_index + 1) % 4]

    def moved_forward(self):
        if self.agent_can_move_forward():
            self.agent_location = self.calculate_new_location()
            self.check_for_pit()
            self.check_for_wumpus()
        else:
            self.agent_bumped_wall()

    def grabbed(self):
        if self.gold_location == self.agent_location:
            self.gold_location = None

    def climbed(self):
        if self.agent_location == WumpusWorld.EXIT_LOCATION:
            self.agent_location = None

    def shot(self):
        if self.arrow_available:
            self.arrow_available = False
            if self.agent_direction == 'East':
                if self.wumpus_east_of_agent():
                    self.wumpus_alive = False

    def adjacent(self, location, target):
        if location is None or target is None:
            return False
        x, y = location
        tx, ty = target
        return (x == tx and abs(y - ty) == 1) or (y == ty and abs(x - tx) == 1)

    def agent_can_move_east(self):
        if self.agent_direction == 'East' and self.agent_location[0] == 4: return False
        if self.agent_location[0] < 4 and not self.wumpus_east_of_agent(): return True

    def agent_can_move_west(self):
        if self.agent_direction == 'West' and self.agent_location[0] == 1: return False
        if self.agent_location[0] > 1 and not self.wumpus_west_of_agent(): return True

    def agent_can_move_north(self):
        if self.agent_direction == 'North' and self.agent_location[1] == 4: return False
        if self.agent_location[1] < 4 and not self.wumpus_north_of_agent(): return True

    def agent_can_move_south(self):
        if self.agent_direction == 'South' and self.agent_location[1] == 1: return False
        if self.agent_location[1] > 1 and not self.wumpus_south_of_agent(): return True

    def agent_bumped_wall(self):
        if self.agent_direction == 'East' and self.agent_can_move_east():
            return False
        if self.agent_direction == 'West' and self.agent_can_move_west():
            return False
        if self.agent_direction == 'North' and self.agent_can_move_north():
            return False
        if self.agent_direction == 'South' and self.agent_can_move_south():
            return False
        return True


    def wumpus_east_of_agent(self):
        return self.wumpus_location and self.wumpus_location[0] > self.agent_location[0] and self.agent_location[1] == self.wumpus_location[1]

    def wumpus_west_of_agent(self):
        return self.wumpus_location and self.wumpus_location[0] < self.agent_location[0] and self.wumpus_location[1] == self.agent_location[1]

    def wumpus_north_of_agent(self):
        return self.wumpus_location and self.wumpus_location[1] > self.agent_location[1] and self.wumpus_location[0] == self.agent_location[0]

    def wumpus_south_of_agent(self):
        return self.wumpus_location and self.wumpus_location[1] < self.agent_location[1] and self.wumpus_location[0] == self.agent_location[0]


    def stench_at(self, location):
        return any(
            self.adjacent(location, wumpus) or location == wumpus
            for wumpus in [self.wumpus_location] if wumpus is not None
        )

    def breeze_at(self, location):
        return any(self.adjacent(location, pit) for pit in self.pit_locations if pit is not None)

    def glitter_at(self, location):
        return self.gold_location == location

    def calculate_new_location(self):
        x, y = self.agent_location
        if self.agent_direction == 'North':
            return x, y + 1
        elif self.agent_direction == 'South':
            return x, y - 1
        elif self.agent_direction == 'East':
            return x + 1, y
        elif self.agent_direction == 'West':
            return x - 1, y

    def agent_can_move_forward(self):
        return (self.agent_direction == 'North' and self.agent_can_move_north()) or \
               (self.agent_direction == 'South' and self.agent_can_move_south()) or \
               (self.agent_direction == 'East' and self.agent_can_move_east()) or \
               (self.agent_direction == 'West' and self.agent_can_move_west())

    def check_for_pit(self):
        if self.agent_location in self.pit_locations:
            self.agent_alive = False

    def check_for_wumpus(self):
        if self.wumpus_location == self.agent_location and self.wumpus_alive:
            self.agent_alive = False
