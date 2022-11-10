from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

#obs is the object that contains all the observactions we need it

class TerranAgent(base_agent.BaseAgent):

  # Constructor
  def __init__(self):
    super(TerranAgent, self).__init__()  
    self.attack_coordinates = None
  
  # Checar si el tipo de unidad es seleccionada
  def unit_type_is_selected(self, obs, unit_type):
  
    """utility fuction to simply sintax of unit type 
    selected check"""
    if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
        return True
        
    if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
        return True
        
    return False

  def get_units_by_type(self, obs, unit_type):
    return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]
    
  def can_do(self, obs, action):
    return action in obs.observation.available_actions

  def build_refinery(self, obs):
    vespene_geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
    refineries = self.get_units_by_type(obs, units.Terran.Refinery)

    if len(refineries) < 1 and len(vespene_geysers) > 0:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          if self.can_do(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
            geyser = random.choice(vespene_geysers)
            return actions.FUNCTIONS.Build_Refinery_screen("now", (geyser.x, geyser.y))

        scvs = self.get_units_by_type(obs, units.Terran.SCV)

        if len(scvs) > 0:
          scv = random.choice(scvs)
          return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

  def gather_vespene_gas(self,obs):
    refinery = self.get_units_by_type(obs, units.Terran.Refinery)
    if len(refinery) > 0:
      refinery = random.choice(refinery)
      if refinery['assigned_harvesters'] < 3:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          if len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) < 2:
            if self.can_do(obs,actions.FUNCTIONS.Harvest_Gather_screen.id):

              return actions.FUNCTIONS.Harvest_Gather_screen("now",(refinery.x, refinery.y))
                            
        scvs = self.get_units_by_type(obs, units.Terran.SCV)
        if len(scvs) > 0 :
          scv = random.choice(scvs)
          return actions.FUNCTIONS.select_point("select",(scv.x,scv.y))

  # def build_infantry_weapons(self, obs):
  #   enbase = self.get_units_by_type(obs, units.Terran.Infantry)

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

    # Create attack conditions
    marines = self.get_units_by_type(obs, units.Terran.Marine)
    if len(marines) >= 10:
      if self.unit_type_is_selected(obs, units.Terran.Marine):
        if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
          return actions.FUNCTIONS.Attack_minimap('now', self.attack_coordinates)  
      if self.can_do(obs, actions.FUNCTIONS.select_army.id):
        return actions.FUNCTIONS.select_army('select')

    # Obtain quantity of minerals
    minerals = obs.observation.player.minerals

    # Get Supply Depot as terrenian. Minerals available needed.                          
    terranian = self.get_units_by_type(obs, units.Terran.SupplyDepot)
    if len(terranian) < 2 and minerals >= 100:
      if self.unit_type_is_selected(obs, units.Terran.SCV):
        if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
          x = random.randint(0, 83)
          y = random.randint(0, 83)
          return actions.FUNCTIONS.Build_SupplyDepot_screen('now', ( x, y))
 
                                
    # Check if there are barracks, if there is no barraks build one. Minerals available needed.
    barracks = self.get_units_by_type(obs, units.Terran.Barracks)
    if len (barracks) < 3 and minerals >= 150:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
            x = random.randint(0, 83)
            y = random.randint(0, 83)
            return actions.FUNCTIONS.Build_Barracks_screen('now', ( x, y))

# Check if there are barracks, if there is no barraks build one. Minerals available needed.
    enbase = self.get_units_by_type(obs, units.Terran.EngineeringBay)
    if len (enbase) < 2 and minerals >= 125:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          if self.can_do(obs, actions.FUNCTIONS.Build_EngineeringBay_screen.id):
            x = random.randint(0, 83)
            y = random.randint(0, 83)
            return actions.FUNCTIONS.Build_EngineeringBay_screen('now', ( x, y))


    if len(barracks) >= 3:
      if self.unit_type_is_selected(obs, units.Terran.Barracks):
        marines = self.get_units_by_type(obs, units.Terran.Marine)
        if len(marines) <= 10:
          if self.can_do(obs, actions.FUNCTIONS.Train_Marine_quick.id):
            return actions.FUNCTIONS.Train_Marine_quick('now')
      b = random.choice(barracks)
      return actions.FUNCTIONS.select_point('select_all_type', (b.x, b.y))
        
        
    b_refinery = self.build_refinery(obs)
    if b_refinery:
        return b_refinery

    #Select SCV units 
    scvs = self.get_units_by_type(obs, units.Terran.SCV)
    if len(scvs) > 0:
        scv = random.choice(scvs)
        return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

    # Gather Vespene Gas
    g_refinery = self.gather_vespene_gas(obs)
    if g_refinery:
          return g_refinery
    
    return actions.FUNCTIONS.no_op()

def main(unused_argv):
  agent = TerranAgent()
  try:
    while True:
      with sc2_env.SC2Env(
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.terran),
                   sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.easy)],
          agent_interface_format=features.AgentInterfaceFormat(
              feature_dimensions=features.Dimensions(screen=84, minimap=64),
              use_feature_units=True),
          step_mul=16,
          game_steps_per_episode=0,
          visualize=True) as env:
          
        agent.setup(env.observation_spec(), env.action_spec())
        
        timesteps = env.reset()
        agent.reset()
        
        while True:
          step_actions = [agent.step(timesteps[0])]
          if timesteps[0].last():
            break
          timesteps = env.step(step_actions)
      
  except KeyboardInterrupt:
    pass
  
if __name__ == "__main__":
    app.run(main)