""" Import necessary libraries """

from pysc2.agents import base_agent
from pysc2.env import sc2_env, run_loop
from pysc2.lib import actions, features, units
from absl import app
from terranAgent import TerranAgent
from protossAgent import ProtossAgent
from hydras import ZergAgent
import random


#obs is the object that contains all the observactions we need it

"""

  Hand-in II: StarCraft II: Agents clash
    Author: Fernando Vargas

    :)
  ________________________________________________________________________

  main (class): Main code that creates, runs and confronts the terran and the protoss
                Agents against each other.
  
"""
def main(unused_argv):
    agent = TerranAgent()
    agent2 = ProtossAgent()
    agent3 = ZergAgent()
    agent4 = None

    print(
        "Welcome to Clash of Agents!!!\nTerran Agent(1)\nProtoss Agent(2)\nZerg Agent - Hydras(3)\nProtoss Agent - Yizu5(4)"
    )
    ag1 = str(input('Which agent goes first? (StarCraft Viewer available) ', ))
    ag2 = str(input('Which agent goes second? ', ))

    print(ag1.isdigit(), type(ag2))

    if ag1.isdigit() and ag2.isdigit():
        firstAgent = None
        secondAgent = None 
        command1 = "sc2_env.Race."
        command2 = "sc2_env.Race."
        if ag1 == ag2:
            print('Same agent')
            breakpoint
        
        if ag1 == "1":
            firstAgent = TerranAgent()
            command1 = command1 + "terran"
        elif ag1 == '2':
            firstAgent = ProtossAgent()
            command1 = command1 + "protoss"
        elif ag1 == '3':
            firstAgent = ZergAgent()
            command1 = command1 + "zerg"
        elif ag1 == '4':
            print('N/A')
        
        if ag2 == '1':
            secondAgent = TerranAgent()
            command2 = command2 + "terran"
        elif ag2 == '2':
            secondAgent = ProtossAgent()
            command2 = command2 + "protoss"
        elif ag2 == '3':
            secondAgent = ZergAgent()
            command2 = command2 + "zerg"
        elif ag2 == '4':
            print('N/A')
        print(firstAgent, secondAgent)
        # command1 = "sc2_env.Race."

    try:
      while True:
        with sc2_env.SC2Env(
            map_name="Simple64",
            players=[sc2_env.Agent(sc2_env.Race.terran),
                     sc2_env.Agent(sc2_env.Race.zerg)
                    #  sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.very_easy)
                     ],
            agent_interface_format=features.AgentInterfaceFormat(
                feature_dimensions=features.Dimensions(screen=84, minimap=64),
                use_feature_units=True),
            step_mul=16,
            game_steps_per_episode=0,
            visualize=True) as env:
            run_loop.run_loop([firstAgent,secondAgent], env)

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
#   Tells the interpreter to run the main function when this file is run in Python.
if __name__ == "__main__":
      app.run(main)