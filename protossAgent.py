from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

class ProtossAgent(base_agent.BaseAgent):

    def __init__(self):
        super(ProtossAgent, self).__init__()
        self.attack_coordinates = None

    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    def step(self, obs):
        super(ProtossAgent, self).step(obs)

        if obs.first():
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()

            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (49, 49)
                self.first_pylon = (60, 60)
            else:
                self.attack_coordinates = (12, 16) #X, Y
                self.first_pylon = (10, 10)

        minerals = obs.observation.player.minerals
        vespene = obs.observation.player.vespene
        zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
        sentries = self.get_units_by_type(obs, units.Protoss.Sentry)
        probes = self.get_units_by_type(obs, units.Protoss.Probe)


        if len(zealots) >= 7:
            if self.unit_type_is_selected(obs, units.Protoss.Zealot):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates)

            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")
        
        
        if len(sentries) >= 1:
            if self.unit_type_is_selected(obs, units.Protoss.Sentry):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates)

            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")
            
        #Pylon
        gates = self.get_units_by_type(obs, units.Protoss.Gateway)
        cybernetic = self.get_units_by_type(obs, units.Protoss.CyberneticsCore)
        if len(gates) == 2 and minerals >= 150 and len(cybernetic) == 0:
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_CyberneticsCore_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_CyberneticsCore_screen("now", (x, y))
        pylons = self.get_units_by_type(obs, units.Protoss.Pylon)
        if len(pylons) < 4 and minerals >= 100:
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_Pylon_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_Pylon_screen("now", (x, y))

        #Gateways
        #gates = self.get_units_by_type(obs, units.Protoss.Gateway)
        if len(gates) < 2 and minerals >= 150:
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_Gateway_screen("now", (x, y))

        gas = self.get_units_by_type(obs, units.Protoss.Assimilator)
        if len(gates) == 2 and minerals >= 75 and len(gas) == 0:
            if self.unit_type_is_selected(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_Assimilator_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                return actions.FUNCTIONS.Build_Assimilator_screen("now", (x, y))
        

        #Units                   
        if len(gates) == 2 and minerals>=100:
            if self.unit_type_is_selected(obs, units.Protoss.Gateway):
                zealots = self.get_units_by_type(obs, units.Protoss.Zealot)
                if len(zealots) <= 7:
                    if self.can_do(obs, actions.FUNCTIONS.Train_Zealot_quick.id):
                        return actions.FUNCTIONS.Train_Zealot_quick("now")
            else:            
                z = random.choice(gates)
                return actions.FUNCTIONS.select_point("select_all_type", (z.x, z.y))
                 
        if len(cybernetic) == 1 and vespene>=100 and minerals>=50:
            if self.unit_type_is_selected(obs, units.Protoss.Gateway):
                sentry = self.get_units_by_type(obs, units.Protoss.Sentry)
                if len(sentry) <= 1:
                    if self.can_do(obs, actions.FUNCTIONS.Train_Sentry_quick.id):
                        return actions.FUNCTIONS.Train_Sentry_quick("now")

            z = random.choice(gates)
            return actions.FUNCTIONS.select_point("select_all_type", (z.x, z.y))
        
        #Select Probe units 
        if len(probes) > 0:
            probe = random.choice(probes)
            return actions.FUNCTIONS.select_point("select_all_type", (probe.x, probe.y))

        return actions.FUNCTIONS.no_op()



def main(unused_argv):
    agent = ProtossAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name ="Simple64",
                players=[sc2_env.Agent(sc2_env.Race.protoss),
                         sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.very_easy)],
                agent_interface_format = features.AgentInterfaceFormat(
                    feature_dimensions = features.Dimensions(screen=84, minimap=64),
                    use_feature_units = True
                ),
                step_mul = 16,
                game_steps_per_episode = 0,
                visualize=True
            ) as env:

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