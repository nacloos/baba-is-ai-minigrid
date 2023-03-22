from collections import defaultdict
from typing import Iterable

# ruleset = defaultdict(dict)
#
# def get_ruleset():
#     return ruleset
#
# def set_ruleset(_ruleset):
#     global ruleset
#     ruleset = _ruleset



def extract_rule(block_list):
    """
    Take a list of 3 blocks and return the rule object and property if these blocks form a valid rule, otherwise
    return None. Valid rule: 'object', 'is', 'property'
    """
    assert len(block_list) == 3 or len(block_list) == 4
    for e in block_list:
        if e is None:
            return None

    def _is_valid_rule(blocks, template):
        is_valid = True
        for i, block in enumerate(blocks):
            is_valid = is_valid and block.type == template[i]
        return is_valid
    
    if len(block_list) == 3:

        if _is_valid_rule(block_list, ["rule_object", "rule_is", "rule_property"]):
            return {
                'object': block_list[0].object,
                'property': block_list[2].property
            }
        elif _is_valid_rule(block_list, ["rule_object", "rule_is", "rule_object"]):
            return {
                'object1': block_list[0].object,
                'object2': block_list[2].object
            }
        else:
            return None
    else:
        if _is_valid_rule(block_list, ["rule_color", "rule_object", "rule_is", "rule_property"]):
            return {
                'obj_color': block_list[0].obj_color,
                'object': block_list[1].object,
                'property': block_list[3].property
            }
        elif _is_valid_rule(block_list, ["rule_color", "rule_object", "rule_is", "rule_object"]):
            return{
                'obj_color1': block_list[0].obj_color,
                'object1': block_list[1].object,
                'object2': block_list[3].object
            }
        elif _is_valid_rule(block_list, ["rule_object", "rule_is", "rule_color", "rule_object"]):
            return{
                'object1': block_list[0].object,
                'obj_color2': block_list[2].obj_color,
                'object2': block_list[3].object
            }
        else:
            return None


def add_rule(block_list, ruleset):
    """
    If the blocks form a valid rule, add it to the ruleset
    Args:
        block_list: list of 3 or 4 blocks
        ruleset: dict with the active rules
    """
    rule = extract_rule(block_list)
    if rule is not None:
        if len(rule) == 2:  # corresponds to block_list of length 3
            if 'property' in rule and 'object' in rule:
                ruleset[rule['property']][rule['object']] = True
            elif 'object1' in rule and 'object2' in rule:
                replace_list = ruleset.get('replace', [])
                replace_list.append((rule['object1'], rule['object2'], None, True))
                ruleset['replace'] = replace_list
        else:  # correponds to block_list of length 4 (includes color)
            if 'property' in rule and 'obj_color' in rule and 'object' in rule:
                color_key = rule['object'] + "_color"

                ruleset[rule['property']][rule['object']] = True # add property
                replace_list = ruleset[rule['property']].get(color_key, set())
                replace_list.add(rule['obj_color']) #add color in string form
                ruleset[rule['property']][color_key] = replace_list

                # if color_key in ruleset[rule['property']]:
                #     ruleset[rule['property']][color_key].append(color_id)
                # else:
                #     ruleset[rule['property']][color_key] = [color_id]
            elif 'object_color1' in rule and 'object1' in rule and 'object2' in rule:
                replace_list = ruleset.get('replace', set())
                # True in the tuple indicates that the color corresponds to the first obj
                replace_list.add((rule['object1'], rule['object2'], rule['object_color1'], True))
                ruleset['replace'] = replace_list

            elif 'object_color2' in rule and 'object1' in rule and 'object2' in rule:
                replace_list = ruleset.get('replace', set())
                # False in the tuple indicates that the color correponds to the second obj
                replace_list.add((rule['object1'], rule['object2'], rule['object_color2'], False))
                ruleset['replace'] = replace_list
                

def inside_grid(grid, pos):
    """
    Return true if pos is inside the boundaries of the grid
    """
    i, j = pos
    inside_grid = (i >= 0 and i < grid.width) and (j >= 0 and j < grid.height)
    return inside_grid


def extract_ruleset(grid, default_ruleset=None):
    """
    Construct the ruleset from the grid. Called every time a RuleBlock is pushed.
    """
    ruleset = defaultdict(dict)
    ruleset.update(default_ruleset) if default_ruleset is not None else None

    if not isinstance(grid, Iterable):
        grid = grid.grid

    # loop through all 'is' blocks
    for k, e in enumerate(grid):
        if e is not None and e.type == 'rule_is':
            i, j = k % grid.width, k // grid.width
            assert k == j * grid.width + i
            add_horizontal = True # set to Flase when add horizontal rule
            add_vertical = True # set to False when add vertical rule

            # check for horizontal rules 
            if add_horizontal and inside_grid(grid, (i-2, j)) and inside_grid(grid, (i-1, j)) and inside_grid(grid, (i+1, j)):
                first_left_cell = grid.get(i-2, j)
                second_left_cell = grid.get(i-1, j)
                right_cell = grid.get(i+1, j)
                if isinstance(extract_rule([first_left_cell, second_left_cell, e, right_cell]), dict):
                    add_horizontal = False
                    add_rule([first_left_cell, second_left_cell, e, right_cell], ruleset)
            if add_horizontal and inside_grid(grid, (i-1, j)) and inside_grid(grid, (i+1, j)) and inside_grid(grid, (i+2, j)):
                left_cell = grid.get(i-1, j)
                first_right_cell = grid.get(i+1, j)
                second_right_cell = grid.get(i+2, j)
                if isinstance(extract_rule([left_cell, e, first_right_cell, second_right_cell]), dict):
                    add_horizontal = False
                    add_rule([left_cell, e, first_right_cell, second_right_cell], ruleset)
            if add_horizontal and inside_grid(grid, (i-1, j)) and inside_grid(grid, (i+1, j)):
                left_cell = grid.get(i-1, j)
                right_cell = grid.get(i+1, j)
                add_rule([left_cell, e, right_cell], ruleset)

            # check for vertical rules
            if add_vertical and inside_grid(grid, (i, j-2)) and inside_grid(grid, (i, j-1)) and inside_grid(grid, (i, j+1)):
                first_up_cell = grid.get(i, j-2)
                second_up_cell = grid.get(i, j-1)
                down_cell = grid.get(i, j+1)
                if isinstance(extract_rule([first_up_cell, second_up_cell, e, down_cell]), dict):
                    add_vertical = False
                    add_rule([first_up_cell, second_up_cell, e, down_cell], ruleset)
            if add_vertical and inside_grid(grid, (i, j-1)) and inside_grid(grid, (i, j+1)) and inside_grid(grid, (i, j+2)):
                up_cell = grid.get(i, j-1)
                first_down_cell = grid.get(i, j+1)
                second_down_cell = grid.get(i, j+2)
                if isinstance(extract_rule([up_cell, e, first_down_cell, second_down_cell]), dict):
                    add_vertical = False
                    add_rule([up_cell, e, first_down_cell, second_down_cell], ruleset)
            if add_vertical and inside_grid(grid, (i, j-1)) and inside_grid(grid, (i, j+1)):
                up_cell = grid.get(i, j-1)
                down_cell = grid.get(i, j+1)
                add_rule([up_cell, e, down_cell], ruleset)
            
            # # check for horizontal rules
            # if inside_grid(grid, (i-1, j)) and inside_grid(grid, (i+1, j)):
            #     left_cell = grid.get(i-1, j)
            #     right_cell = grid.get(i+1, j)
            #     add_rule([left_cell, e, right_cell], ruleset)

            # # check for vertical rules
            # if inside_grid(grid, (i, j-1)) and inside_grid(grid, (i, j+1)):
            #     up_cell = grid.get(i, j-1)
            #     down_cell = grid.get(i, j+1)
            #     add_rule([up_cell, e, down_cell], ruleset)

    return ruleset
