from __future__ import annotations

from collections import defaultdict
from typing import Tuple

import numpy as np

from gym_minigrid.flexible_world_object import FBall, FWall, RuleProperty, RuleIs, RuleObject, RuleColor, Baba, make_obj
from gym_minigrid.utils import grid_random_position
from gym_minigrid.minigrid import MiniGridEnv, MissionSpace, Grid
from gym_minigrid.babaisyou import BabaIsYouGrid, BabaIsYouEnv
from gym_minigrid.flexible_world_object import Baba

RuleObjPos = Tuple[int, int]
RuleIsPos = Tuple[int, int]
RulePropPos = Tuple[int, int]



def random_rule_pos(size, margin):
    rule_pos = grid_random_position(size, n_samples=1, margin=margin)[0]
    rule_pos = [(rule_pos[0]-1, rule_pos[1]), rule_pos, (rule_pos[0]+1, rule_pos[1])]
    return rule_pos


class AdjExperiment1(BabaIsYouEnv):
    def __init__(self, win_obj=None, distract_obj=None, win_obj_color = None, static=True, randomize=False, size=8, **kwargs):
        if win_obj is None or distract_obj is None or win_obj_color is None:
            raise Exception("Objects or color not provided")
        self.win_obj = win_obj  # possible obj: fball, fwall, fdoor, fkey, baba - strings, not baba
        self.distract_obj = distract_obj  # win_obj != distract_obj, not baba
        self.win_obj_color = win_obj_color
        self.static = static  # TODO handle this element later
        self.randomize = randomize  # TODO handle this element later
        self.size = size

        default_ruleset = {
            "is_agent": {"baba": True}
        }
        super().__init__(grid_size=self.size, max_steps=4 * self.size * self.size, default_ruleset=default_ruleset,
                         **kwargs)

    def _gen_grid(self, width, height):
        self.grid = BabaIsYouGrid(width, height)
        self.grid.wall_rect(0, 0, width, height)

        # Rules - handle static/dynamic later
        self.put_obj(RuleColor(self.win_obj_color), 1, 1)
        self.put_obj(RuleObject(self.win_obj), 2, 1)
        self.put_obj(RuleIs(), 3, 1)
        self.put_obj(RuleProperty('is_goal'), 4, 1)

        # Place Objects - handle randomization later
        win_obj_pos = (width-2, height-2)
        self.win_obj_pos = win_obj_pos
        self.put_obj(make_obj(self.win_obj, obj_color=self.win_obj_color), *self.win_obj_pos)

        # # -------
        # new_cell = self.grid.get(6,6)
        # import pdb
        # if (1 == 1): pdb.set_trace()
        # # --------- 

        dist_obj_pos = (width-2, 1)
        self.dist_obj_pos = dist_obj_pos
        self.put_obj(make_obj(self.distract_obj), *self.dist_obj_pos)

        # Place agent - this may be wrong
        self.place_obj(Baba())
        self.place_agent()

    def get_obj_pos(self, obj_type):
        output = []
        for j in range(self.grid.height):
            for i in range(self.grid.width):
                c = self.grid.get(i, j)
                # output.append(type(c))
                # if isinstance(type(c), Baba):
                if type(c) == obj_type:
                    return i, j
        return output
        return None

    def reward(self):
        # return 0, False #CHANGE THIS
        return super().reward() 
        # baba_loc = self.get_obj_pos('Baba')
        # assert isinstance(baba_loc, tuple), "{} is not a tuple".format(baba_loc)
        # baba_i, baba_j = baba_loc
        # if baba_i == self.win_obj_pos[0] and baba_j == self.win_obj_pos[1]:
        #     return self.get_reward(), True
        # else:
        #     return 0, False






# ------------------------------ OLD EXPERIMENTS ---------------------------------------------
class Experiment1(BabaIsYouEnv):
    def __init__(self, size=6, randomize=False, object_count=None, rules=None, show_rules=True, static=True, **kwargs):
        if rules is None or object_count is None:
            raise Exception("Rules and/or Objects not provided")
        self.randomize = randomize
        self.object_count = object_count
        self.rules = rules
        self.show_rules = show_rules
        self.static=static
        super().__init__(size=size, max_steps=200, **kwargs)

    def _gen_grid(self, width, height):
        self.grid = BabaIsYouGrid(width, height)
        self.grid.wall_rect(0,0,width, height)

        # Three Rules
        # BABA IS YOU - not included in the input rules
        # X IS Y
        # Y IS WIN

        if self.static:
            self.rule1_pos = [(1, 1), (2, 1), (3, 1)]
            self.rule2_pos = [(1, 2), (2, 2), (3, 2)]
            self.rule3_pos = [(1, 3), (2, 3), (3, 3)]

        else:
            # TODO: implement the dynamic version later
            # TODO: rule construction - randomized? By position, by block? Both?
            self.rule1_pos = [(1, 1), (2, 1), (3, 1)]
            self.rule2_pos = [(1, 2), (2, 2), (3, 2)]
            self.rule3_pos = [(1, 3), (2, 3), (4, 3)] # make this rule

        if self.show_rules:
            self.put_rule(obj='baba', property='is_agent', positions=self)
            # TODO: not sure how to write the other rules

    def reward(self):
        pass


class Experiment2(BabaIsYouEnv):
    # modeled after OpenShutObjEnv & OpenAndGoToWinEnv(BabaIsYouEnv)
    def __init__(self, open_obj=None, shut_obj=None, static=True, randomize=False, size=8, **kwargs):
        if open_obj is None or shut_obj is None:
            raise Exception("Objects not provided")
        self.open_obj = open_obj  # possible obj: fball, fwall, fdoor, fkey, baba - strings
        self.shut_obj = shut_obj
        self.static = static
        self.randomize = randomize

        default_ruleset={
            "is_agent": {"baba": True}
        }
        self.size = size
        super().__init__(grid_size=self.size, max_steps=4 * self.size * self.size, default_ruleset=default_ruleset,
                         **kwargs)

    def _gen_grid(self, width, height):
        self.grid = BabaIsYouGrid(width, height)
        self.grid.wall_rect(0, 0, width, height)

        # Rules
        self.put_obj(RuleObject(self.open_obj), 1, 1)
        self.put_obj(RuleIs(), 2, 1)
        self.put_obj(RuleProperty('is_open'), 3, 1)
        self.put_obj(RuleObject(self.shut_obj), 1, 2)
        self.put_obj(RuleIs(), 2, 2)
        self.put_obj(RuleProperty('is_shut'), 3, 2)
        if self.static:
            self.put_obj(RuleObject(self.open_obj), 1, 3)
            self.put_obj(RuleIs(), 2, 3)
            self.put_obj(RuleProperty('is_push'), 3, 3)
        else:
            # TODO: create dynamic rule version of the experiment (change static implementation below)
            self.put_obj(RuleObject(self.open_obj), 1, 3)
            self.put_obj(RuleIs(), 2, 3)
            self.put_obj(RuleProperty('is_push'), 3, 3)

        # Place Objects
        # make_obj, place_obj
        if self.randomize:
            # TODO: create randomized version of this environment (change the static implementation below)
            shut_obj_pos = (width-2, height-2)
            self.shut_obj_pos = shut_obj_pos
            self.put_obj(make_obj(self.shut_obj), *self.shut_obj_pos)
            open_obj_pos = (width// 2, height // 3)
            assert(open_obj_pos != 3) # overlaps with the rules
            self.open_obj_pos = open_obj_pos
            self.put_obj(make_obj(self.open_obj), *self.open_obj_pos)
        else:
            # TODO: create randomized version of this environment (change the static implementation below)
            shut_obj_pos = (width - 2, height - 2)
            self.shut_obj_pos = shut_obj_pos
            self.put_obj(make_obj(self.shut_obj), *self.shut_obj_pos)
            open_obj_pos = (width // 2, height // 3)
            assert (open_obj_pos != 3)  # overlaps with the rules
            self.open_obj_pos = open_obj_pos
            self.put_obj(make_obj(self.open_obj), *self.open_obj_pos)


        # Place agent - this may be wrong
        self.place_obj(Baba())
        self.place_agent()



    def reward(self):
        # reward if pushes open object over shut object
        assert self.shut_obj_pos is not None
        # check if the shut obj is destroyed
        if self.grid.get(*self.shut_obj_pos) is None:
            return self.get_reward(), True
        else:
            return 0, False


class Experiment3(BabaIsYouEnv):
    def __init__(self, win_obj=None, distract_obj=None, static=True, randomize=False, size=8, **kwargs):
        if win_obj is None or distract_obj is None:
            raise Exception("Objects not provided")
        self.win_obj = win_obj  # possible obj: fball, fwall, fdoor, fkey, baba - strings, not baba
        self.distract_obj = distract_obj  # win_obj != distract_obj, not baba
        self.static = static
        self.randomize = randomize
        self.size = size

        default_ruleset = {
            "is_agent": {"baba": True}
        }
        super().__init__(grid_size=self.size, max_steps=4 * self.size * self.size, default_ruleset=default_ruleset,
                         **kwargs)

    def _gen_grid(self, width, height):
        self.grid = BabaIsYouGrid(width, height)
        self.grid.wall_rect(0, 0, width, height)

        # Rules
        if self.static:
            self.put_obj(RuleObject(self.win_obj), 1, 1)
            self.put_obj(RuleIs(), 2, 1)
            self.put_obj(RuleProperty('is_goal'), 3, 1)
        else:
            # TODO: create dynamic ruleset (change the static version below)
            self.put_obj(RuleObject(self.win_obj), 1, 1)
            self.put_obj(RuleIs(), 2, 1)
            self.put_obj(RuleProperty('is_win'), 3, 1)

        # Place Objects
        if self.randomize:
            # TODO: create randomized version of this environment (change the static implementation below)
            win_obj_pos = (width-2, height-2)
            self.win_obj_pos = win_obj_pos
            self.put_obj(make_obj(self.win_obj), *self.win_obj_pos)
            dist_obj_pos = (width-2, 1)
            self.dist_obj_pos = dist_obj_pos
            self.put_obj(make_obj(self.distract_obj), *self.dist_obj_pos)
        else:
            win_obj_pos = (width - 2, height - 2)
            self.win_obj_pos = win_obj_pos
            self.put_obj(make_obj(self.win_obj), *self.win_obj_pos)
            dist_obj_pos = (width - 2, 1)
            self.dist_obj_pos = dist_obj_pos
            self.put_obj(make_obj(self.distract_obj), *self.dist_obj_pos)

        # Additional stuff to add and play around with ----------------
        self.put_obj(RuleColor("white"), 1, 4)


        # -------------------------------------

        # Place agent - this may be wrong
        self.place_obj(Baba())
        self.place_agent()

    def reward(self):
        return super().reward()


class Experiment4(BabaIsYouEnv):
    def __init__(self, agent_objs=[], agent_prop=None, exp_num=None, static=True,
                 randomize=False, size=8, **kwargs):

        if len(agent_objs) == 0 or exp_num is None:
            raise Exception("Provide info on agent objects and experiment type")
        self.agent_objs = agent_objs
        self.agent_prop = agent_prop
        self.exp_num = exp_num
        self.task = "open_shut" if self.exp_num == 2 else "goto_win"
        self.static = static
        self.randomize = randomize
        self.size = size
        # add default ruleset based on exp number (baseline rules)
        # could also add them to the grid too not sure what's best

        super().__init__(grid_size=self.size, max_steps=4 * self.size * self.size, default_ruleset={},
                         **kwargs)

    def _gen_grid(self, width, height):
        self.grid = BabaIsYouGrid(width, height)
        self.grid.wall_rect(0, 0, width, height)

        # put in base rules, iterate through baba and props to add rules

        # if self.exp_num in [1, 4, 5, 6, 7]:
        #     self.put_obj(RuleObject('fdoor'), 1, 1)
        #     self.put_obj(RuleIs(), 2, 1)
        #     self.put_obj(RuleProperty('is_goal'), 3, 1)






    def reward(self):
        # if self.task == "open_shut":
        #     assert self._shut_obj_pos is not None
        #     # check if the shut obj is destroyed
        #     if self.grid.get(*self._shut_obj_pos) is None:
        #         return self.get_reward(), True
        #     else:
        #         return 0, False
        #
        # elif self.task == "goto_win":
        #     return super().reward()
        pass


        # agent object list
        # task = "goto_win", "open_shut"


# class GoToObjEnv(BaseGridEnv):
#     # OBJECT_TO_IDX = {
#     #     "empty": 0,
#     #     "wall": 1,
#     #     "fball": 2,
#     #     "baba": 3
#     # }
#     # unencoded_object = {
#     #     "rule_object": 1,
#     #     "rule_is": 1,
#     #     "rule_property": 1
#     # }
#     # COLOR_TO_IDX = {}
#     # STATE_TO_IDX = {}
#
#     def __init__(self, size=8, agent_start_dir=0, rdm_rule_pos=False, rdm_ball_pos=False, rdm_agent_pos=False,
#                  push_rule_block=False, n_balls=1, show_rules=True, **kwargs):
#         self.size = size
#         self.agent_start_dir = agent_start_dir
#         self.rdm_rule_pos = rdm_rule_pos
#         self.rdm_ball_pos = rdm_ball_pos
#         self.rdm_agent_pos = rdm_agent_pos
#         self.push_rule_block = push_rule_block
#         self.n_balls = n_balls
#         self.show_rules = show_rules
#         if not self.show_rules:
#             ruleset = {
#                 "is_goal": {"fball": True},
#                 "is_agent": {"baba": True}
#             }
#         else:
#             ruleset = {}
#         super().__init__(size=size, default_ruleset=ruleset, **kwargs)
#
#     def _gen_grid(self, width, height):
#         # rule blocks position
#         if self.rdm_rule_pos:
#             # self.rule_pos = random_position(self.size, n_samples=3, margin=3)
#             self.rule_pos = random_rule_pos(self.size, margin=2)
#         else:
#             # self.rule_pos = [(2, 2), (3, 2), (4, 2)]
#             self.rule_pos = [(1, 2), (2, 2), (3, 2)]
#
#         # agent and ball positions
#         agent_start_pos, self.ball_pos = grid_random_position(self.size, n_samples=2, margin=1)
#         while agent_start_pos in self.rule_pos or self.ball_pos in self.rule_pos:
#             agent_start_pos, self.ball_pos = grid_random_position(self.size, n_samples=2, margin=1)
#
#         self.agent_start_pos = agent_start_pos
#
#         # Create an empty grid
#         self.grid = BabaIsYouGrid(width, height)
#
#         # Generate the surrounding walls
#         self.grid.wall_rect(0, 0, width, height)
#
#         # self.put_obj(FBall(), *self.ball_pos)
#
#         if self.show_rules:
#             self.put_rule(obj='baba', property='is_agent', positions=[(1, 1), (2, 1), (3, 1)])
#             self.put_rule(obj='fball', property='is_goal', positions=self.rule_pos, is_push=self.push_rule_block)
#
#         if self.rdm_ball_pos:
#             for i in range(self.n_balls):
#                 self.place_obj(FBall())
#         else:
#             self.put_obj(FBall(), 4, 4)
#
#         if self.rdm_agent_pos:
#             self.place_obj(Baba())
#         else:
#             self.put_obj(Baba(), 2, 5)
#         self.place_agent()
#
#     # def gen_obs(self):
#     #     array = np.zeros((self.grid.width, self.grid.height, 3), dtype="uint8")
#     #
#     #     for i in range(self.grid.width):
#     #         for j in range(self.grid.height):
#     #             v = self.grid.get(i, j)
#     #
#     #             if v is None:
#     #                 array[i, j, 0] = self.OBJECT_TO_IDX["empty"]
#     #                 array[i, j, 1] = 0
#     #                 array[i, j, 2] = 0
#     #
#     #             else:
#     #                 if v.type in self.OBJECT_TO_IDX:
#     #                     idx = self.OBJECT_TO_IDX[v.type]
#     #                 else:
#     #                     idx = self.unencoded_object[v.type]
#     #                 array[i, j, :] = [idx, 0, 0]
#     #
#     #     return array
#
#
# class GoToWinObjEnv(BaseGridEnv):
#     def __init__(self, size=6, rdm_pos=False, n_walls=1, n_balls=1, rules=None, show_rules=True, **kwargs):
#         self.rdm_pos = rdm_pos
#         self.n_balls = n_balls
#         self.n_walls = n_walls
#         if rules is None:
#             self.rules = [
#                 {'fball': 'is_defeat', 'fwall': 'is_goal'},
#                 {'fball': 'is_goal', 'fwall': 'is_defeat'},
#                 {'fball': 'is_goal', 'fwall': 'is_goal'},
#                 {'fball': 'is_defeat', 'fwall': 'is_defeat'}
#             ]
#         else:
#             self.rules = rules
#
#         self.show_rules = show_rules
#         if not self.show_rules:
#             # only for constant rules
#             assert len(self.rules) == 1
#             ruleset = defaultdict(dict)
#             ruleset["is_agent"]["baba"] = True
#             for k, v in self.rules[0].items():
#                 ruleset[v][k] = True
#         else:
#             ruleset = {}
#         super().__init__(size=size, default_ruleset=ruleset,  **kwargs)
#
#     def encode_rules(self, mode='matrix'):
#         ruleset = self.get_ruleset()
#         objects = {'fball': 0, 'fwall': 1, 'baba': 2}
#         properties = {'is_goal': 0, 'is_defeat': 1, 'is_agent': 2}
#
#         rule_encoding = np.zeros((len(objects), len(properties)))
#         rules = []
#         for property in ruleset.keys():
#             for obj in ruleset[property]:
#                 if ruleset[property][obj]:
#                     rule_encoding[objects[obj], properties[property]] = 1
#                     rules.append((objects[obj], properties[property]))
#
#         if mode == 'matrix':
#             return rule_encoding
#         elif mode == 'list':
#             return rules
#         elif mode == 'dict':
#             return ruleset
#         else:
#             raise ValueError
#
#     def _gen_grid(self, width, height):
#         self.grid = BabaIsYouGrid(width, height)
#         self.grid.wall_rect(0, 0, width, height)
#
#         self.rule1_pos = [(1, 1), (2, 1), (3, 1)]
#         self.rule2_pos = [(1, 2), (2, 2), (3, 2)]
#
#         # randomly sample the rules
#         rule_idx = np.random.choice(len(self.rules))
#         ball_property = self.rules[rule_idx]['fball']
#         wall_property = self.rules[rule_idx]['fwall']
#
#         if self.show_rules:
#             self.put_rule('fball', ball_property, self.rule1_pos)
#             self.put_rule('fwall', wall_property, self.rule2_pos)
#             self.put_rule(obj='baba', property='is_agent', positions=[(1, 3), (2, 3), (3, 3)])
#
#         # wall_pos, ball_pos = grid_random_position(self.size, n_samples=2, margin=1,
#         #                                           exclude_pos=[*self.rule1_pos, *self.rule2_pos])
#
#         n_walls = np.random.choice(self.n_walls) if isinstance(self.n_walls, list) else self.n_walls
#         n_balls = np.random.choice(self.n_balls) if isinstance(self.n_balls, list) else self.n_balls
#
#         if not self.rdm_pos:
#             wall_pos = (1, 4)
#             ball_pos = (3, 4)
#             baba_pos = (2, 4)
#             self.put_obj(FWall(), *wall_pos)
#             self.put_obj(FBall(), *ball_pos)
#             self.put_obj(Baba(), *baba_pos)
#         else:
#             for _ in range(n_walls):
#                 self.place_obj(FWall())
#             for _ in range(n_balls):
#                 self.place_obj(FBall())
#             self.place_obj(Baba())
#
#         # self.agent_pos = (2, 4)
#         # self.agent_dir = 0
#         self.place_agent()
