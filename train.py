from pong_env import PongEnv
from nn import Agent
import torch

env = PongEnv()
env.render_enabled = True
state_size = 7
action_size = 3
agent = Agent(state_size, action_size)

episodes = 500

for e in range(episodes):
    state = env.reset()
    total_reward = 0
    done = False
    while not done:
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
        agent.replay()
    agent.update_target()
    print(f"Episode {e+1}/{episodes} — Score: {total_reward}, Epsilon: {agent.epsilon:.2f}")

torch.save(agent.model.state_dict(), "pong_model.pth")
