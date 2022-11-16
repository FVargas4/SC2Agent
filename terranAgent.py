""" Import necessary libraries """

from pysc2.agents import base_agent
from pysc2.env import sc2_env, run_loop
from pysc2.lib import actions, features, units
from absl import app
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
class TerranAgent(base_agent.BaseAgent):

  # Constructor function
  def __init__(self):
    # Initiate Agent 
    super(TerranAgent, self).__init__()
    # TerranAgent.atack_coordinates (array): Coordinates to where the attack heading.  
    self.attack_coordinates = None
  
  """
  
  Function unit_type_is_selected(self, observation object, Tag) [UTIS]

  Send a boolean flag to let the agent know if the given tag (unit_type) is the object selected in-game.
  
    self (class): Allows the agent to access itself.
    obs (object): Object that acts as the sensors of the agent.
    unit_type (Tag): API's internal Tag that identifies the type of unit. 
  
  """
  def unit_type_is_selected(self, obs, unit_type):
  
    # Single selection conditional
    if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
        return True
    # Multi selection conditional
    if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
        return True
        
    return False

  """
  
  Function get_units_by_type(self, observation object, Tag)

    Function that get a tag and confirms that that tag (unit_type) exists in the unit library, if this tag exists.
  
    self (class): Allows the agent to access itself.
    obs (object): Object that acts as the sensors of the agent.
    unit_type (Tag): API's internal Tag that identifies the type of unit. 
  
  """
  def get_units_by_type(self, obs, unit_type):
    return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]
  """
  
  Function can_do(self, observation object, Tag)

    Function that determines whether the agent can do an action or not.
  
    self (class): Allows the agent to access itself.
    obs (object): Object that acts as the sensors of the agent.
    action (Tag): API's internal Tag that identifies the action desired. 
  _________________________________________________________________________________________
  
  """
  def can_do(self, obs, action):
    return action in obs.observation.available_actions

  """
  H-i I

  Function build_refinery(self, observation object)

    Function that make SCVs build a refinery at some vespene geyser in the screen. 
  
    self (class): Allows the agent to access itself.
    obs (object): Object that acts as the sensors of the agent.
  _________________________________________________________________________________________

    vespene_geysers (array): Array that contain the vespene geysers in the screen.
    refineries (array): Array that contain the refineries in the screen.

  """
  def build_refinery(self, obs):

    vespene_geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
    refineries = self.get_units_by_type(obs, units.Terran.Refinery)
    
    # If there is at least a refinery and there are any vespene geysers
    if len(refineries) < 1 and len(vespene_geysers) > 0:

        # If the SCV is selected by the agent
        if self.unit_type_is_selected(obs, units.Terran.SCV):

          # If the agent can build a Refinery
          if self.can_do(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
            # Choose a random geyser
            geyser = random.choice(vespene_geysers)
            # Build a refinery at the chosen geyser 
            return actions.FUNCTIONS.Build_Refinery_screen("now", (geyser.x, geyser.y))
        
        # Find the SCVs and store it in variable scvs
        scvs = self.get_units_by_type(obs, units.Terran.SCV)

        # If the scvs array is not empty
        if len(scvs) > 0:

          # Choose a random SCV
          scv = random.choice(scvs)
          # Tell the agent to select all SCVs
          return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))
  """
  H-i I

  Function gather_vespene_gas(self, observation object)

    Function that makes the SCVs gather vespene gas from the refinery to the command center.
  ________________________________________________________________________
  
    self (class): Allows the agent to access itself.
    obs (object): Object that acts as the sensors of the agent.
    refineries (array): Array that contain the fineries in the screen.
  
  """
  def gather_vespene_gas(self,obs):
    
    # Find Refineries in the screen and save it as an array in variable refineries
    refineries = self.get_units_by_type(obs, units.Terran.Refinery)

    # If refineries is not empty
    if len(refineries) > 0:
      # Choose a refinery where the vespene gas will be recollected and store it in variable refinery
      refinery = random.choice(refineries)
      # If there are at least 3 harvesters
      if refinery['assigned_harvesters'] < 3:
        # If the SCV is selected 
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          # If the observation objects selects (multi or single) 
          if len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) < 2:
            # If the agent can do "harvest_gather" function
            if self.can_do(obs,actions.FUNCTIONS.Harvest_Gather_screen.id):
              # Use the actuators library actions to make the agent gather gas
              return actions.FUNCTIONS.Harvest_Gather_screen("now",(refinery.x, refinery.y))

        # Find the SCVs and store it in variable scvs         
        scvs = self.get_units_by_type(obs, units.Terran.SCV)

        # If the scvs array is not empty
        if len(scvs) > 0 :
          # Choose a random SCV
          scv = random.choice(scvs)
          # Tell the agent to select all SCVs
          return actions.FUNCTIONS.select_point("select",(scv.x,scv.y))

  """
  
  Function step(self, observation object)
    Function that determines what does the agent does/ trys to do each step of the game.
  ________________________________________________________________________
    self (class): Allows the agent to access itself.
    obs (object): Object that acts as the sensors of the agent.
  
  """
  def step(self, obs):

    super(TerranAgent, self).step(obs)
    
    #select/guess the location of the enemies
    if obs.first():
        player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
        xmean = player_x.mean()
        ymean = player_y.mean()

        print(" \n means\n ", xmean, ymean)                        
        if xmean <= 31 and ymean <= 31:
            #set pair of coordintates
            self.attack_coordinates = [49,49]
        else:
            #set pair of coordintates
            self.attack_coordinates = [12,16]

    # Obtain quantity of minerals
    minerals = obs.observation.player.minerals

    # Get Supply Depot as terrenian. Minerals available needed.                          
    terranian = self.get_units_by_type(obs, units.Terran.SupplyDepot)

    # Check if there are marine, if there is no marine build one. Minerals available needed.
    marines = self.get_units_by_type(obs, units.Terran.Marine)

    # Check if there are barracks, if there is no barraks build one. Minerals available needed.
    barracks = self.get_units_by_type(obs, units.Terran.Barracks)
    
    # Check if there are barracks, if there is no barraks build one. Minerals available needed.
    enbase = self.get_units_by_type(obs, units.Terran.EngineeringBay)

    # Select SCV units ing-game 
    scvs = self.get_units_by_type(obs, units.Terran.SCV)

    # Call GVG function to gather Vespene Gas
    g_refinery = self.gather_vespene_gas(obs)

    # Call BR function to build Refinary
    b_refinery = self.build_refinery(obs)

    """Create attack conditions"""
    # If there are at least 10 marines
    if len(marines) >= 15:
      # Select Marines
      if self.unit_type_is_selected(obs, units.Terran.Marine):
        # If you can check enemies' location on the minimap
        if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
          # Send marines to attack them
          return actions.FUNCTIONS.Attack_minimap('now', self.attack_coordinates)  
      # If the selected unit is not Marine
      if self.can_do(obs, actions.FUNCTIONS.select_army.id):
        # Select the army (marines)
        return actions.FUNCTIONS.select_army('select')
    
    """Supply Depot (spawner) conditions"""
    # If there are not at least 2 supply depots and the agent has 100 materials
    if len(terranian) < 2 and minerals >= 100:
      # If the unit selected is a SCV
      if self.unit_type_is_selected(obs, units.Terran.SCV):
        # If it is possible to build a Supply Depot
        if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
          # Get [x, y] values randomly from 0 to 83 in both cases
          x = random.randint(0, 83)
          y = random.randint(0, 83)
          # Build the supply depot on the random coordinates
          return actions.FUNCTIONS.Build_SupplyDepot_screen('now', ( x, y))
      
    """Building barracks conditions"""
    # If there are not at least 3 barracks and the agent has 150 materials
    if len (barracks) < 3 and minerals >= 150:
      # If the unit selected is a SCV
      if self.unit_type_is_selected(obs, units.Terran.SCV):
        # If it is possible to build a Barrak
        if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
          # Get [x, y] values randomly from 0 to 83 in both cases
          x = random.randint(0, 83)
          y = random.randint(0, 83)
          # Build the supply depot on the barracks coordinates
          return actions.FUNCTIONS.Build_Barracks_screen('now', ( x, y))

    """Build Engineering Bay conditions"""
    # If there are not at least 2 engineering bay and the agent has 125 materials
    if len (enbase) < 2 and minerals >= 125:
      # If the unit selected is a SCV
      if self.unit_type_is_selected(obs, units.Terran.SCV):
        # If it is possible to build a Engineering Bay
        if self.can_do(obs, actions.FUNCTIONS.Build_EngineeringBay_screen.id):
          # Get [x, y] values randomly from 0 to 60 in both cases
          x = random.randint(0, 83)
          y = random.randint(0, 83)
          # Build the Engineering Bay on the random coordinates
          return actions.FUNCTIONS.Build_EngineeringBay_screen('now', ( x, y))
     
    """Training marines conditions"""
    # If there are not at least 2 engineering bay and the agent has 125 materials
    if len(barracks) >= 3:
      # If the unit selected is a Barrak
      if self.unit_type_is_selected(obs, units.Terran.Barracks):
        # If there are less than 10 marines
        if len(marines) <= 15:
          # If it is possible to build a train (create) mairnes
          if self.can_do(obs, actions.FUNCTIONS.Train_Marine_quick.id):
            # Spawn Marines
            return actions.FUNCTIONS.Train_Marine_quick('now')
      # Choose a random barrack
      b = random.choice(barracks)
      # Select point at barracks coordinates
      return actions.FUNCTIONS.select_point('select_all_type', (b.x, b.y))

    """Building refinery conditions"""
    # if b_refinery runs correctly, return it  
    if b_refinery:
        return b_refinery
    
    """Gathering gas from refinery conditions"""
    # if g_refinery runs correctly, return it  
    if g_refinery:
          return g_refinery

    # If the scvs array is not empty
    if len(scvs) > 0:
        # Choose a random SCV
        scv = random.choice(scvs)
        # Tell the agent to select all SCVs
        return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

    # If there is nothing left to do, run the no_op function
    return actions.FUNCTIONS.no_op()

  """
  
  Function main(unused argument)
    Principal code in the file. It is the code that runs to open the game, create the agents, let the agents 
    play and then restarts the agents once one of them is defeated. Conditional on line 356 only tells the 
    interpreter to run the main function when this file is run in Python.
  
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