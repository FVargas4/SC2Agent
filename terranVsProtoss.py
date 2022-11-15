""" Import necessary libraries """

from pysc2.agents import base_agent
from pysc2.env import sc2_env, run_loop
from pysc2.lib import actions, features, units
from absl import app
from terranAgent import TerranAgent
from protossAgent import ProtossAgent
import random


#obs is the object that contains all the observactions we need it

"""

  Hand-in I: StarCraft II Terran Agent
    Author: Fernando Vargas

    :)
  ________________________________________________________________________

  TerranAgent (class): Agent object that contains all needed methods to win 
  vs an easy level Agent.

  main (class): Main code that creates and activates both Terran and an easy
  level (Random Race) Agent.
  
"""
def main(unused_argv):
  agent = TerranAgent()
  agent2 = ProtossAgent()
  try:
    while True:
      with sc2_env.SC2Env(
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.terran),
                   sc2_env.Agent(sc2_env.Race.protoss)
                  #  sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.very_easy)
                   ],
          agent_interface_format=features.AgentInterfaceFormat(
              feature_dimensions=features.Dimensions(screen=84, minimap=64),
              use_feature_units=True),
          step_mul=16,
          game_steps_per_episode=0,
          visualize=True) as env:
          run_loop.run_loop([agent,agent2], env)
          
        # agent.setup(env.observation_spec(), env.action_spec())
        
        # timesteps = env.reset()
        # agent.reset()
        
        # while True:
        #   step_actions = [agent.step(timesteps[0])]
        #   if timesteps[0].last():
        #     break
        #   timesteps = env.step(step_actions)
      
  # Interrupt the code from running using ctrl + C on the terminal the file is being run at.
  except KeyboardInterrupt:
    pass

  # If the agent trys to click on coordinates outside of the actual screen.
  except ValueError:
    print('Crash')
    pass
# Tells the interpreter to run the main function when this file is run in Python.
if __name__ == "__main__":
    app.run(main)