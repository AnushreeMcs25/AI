class VacuumEnvironment:
    def __init__(self, location_status):
        self.location_status = location_status
        self.agent_location = 'A'  # start at location A

    def get_percept(self):
        return (self.agent_location, self.location_status[self.agent_location])

    def execute_action(self, action):
        if action == 'Suck':
            self.location_status[self.agent_location] = 'Clean'
        elif action == 'MoveLeft':
            self.agent_location = 'A'
        elif action == 'MoveRight':
            self.agent_location = 'B'
        elif action == 'NoOp':
            pass

    def is_all_clean(self):
        return all(status == 'Clean' for status in self.location_status.values())


def simple_reflex_agent(percept):
    location, status = percept
    if status == 'Dirty':
        return 'Suck'
    elif location == 'A':
        return 'MoveRight'
    elif location == 'B':
        return 'MoveLeft'
    else:
        return 'NoOp'

def run_vacuum_agent(env, steps=10):
    print("Initial environment:", env.location_status)
    for step in range(steps):
        if env.is_all_clean():
            print("All locations are clean. Stopping simulation.")
            break
        percept = env.get_percept()
        action = simple_reflex_agent(percept)
        env.execute_action(action)
        print(f"Step {step+1}: Location={percept[0]}, Status={percept[1]}, Action={action}, Environment={env.location_status}")

if __name__ == "__main__":
    
    initial_status = {'A': 'Dirty', 'B': 'Dirty'}
    env = VacuumEnvironment(initial_status)
    run_vacuum_agent(env)
