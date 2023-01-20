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
    assert len(block_list) == 3
    for e in block_list:
        if e is None:
            return None

    def _is_valid_rule(blocks, template):
        is_valid = True
        for i, block in enumerate(blocks):
            is_valid = is_valid and block.type == template[i]
        return is_valid

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


def add_rule(block_list, ruleset):
    """
    If the blocks form a valid rule, add it to the ruleset
    Args:
        block_list: list of 3 blocks
        ruleset: dict with the active rules
    """
    rule = extract_rule(block_list)
    if rule is not None:
        if 'property' in rule and 'object' in rule:
            ruleset[rule['property']][rule['object']] = True
        elif 'object1' in rule and 'object2' in rule:
            replace_list = ruleset.get('replace', [])
            replace_list.append((rule['object1'], rule['object2']))
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

            # check for horizontal rules
            if inside_grid(grid, (i-1, j)) and inside_grid(grid, (i+1, j)):
                left_cell = grid.get(i-1, j)
                right_cell = grid.get(i+1, j)
                add_rule([left_cell, e, right_cell], ruleset)

            # check for vertical rules
            if inside_grid(grid, (i, j-1)) and inside_grid(grid, (i, j+1)):
                up_cell = grid.get(i, j-1)
                down_cell = grid.get(i, j+1)
                add_rule([up_cell, e, down_cell], ruleset)

    return ruleset
