"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill',
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None):
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []

    def pick_skill(self, caster: 'Character', target: 'Character') -> 'Skill':
        """
        Return a skill.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Mage
        >>> bq = BattleQueue()
        >>> c = Mage("m", bq, ManualPlaystyle(bq))
        >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> t = create_default_tree()
        >>> t.pick_skill(c, c2).get_sp_cost()
        10
        """
        skill_list = self.skill_list(caster, target)
        priori = skill_list[0]
        for item in skill_list:
            if item.priority < priori.priority:
                priori = item
        return priori.value

    def skill_list(self, caster: 'Character', target: 'Character') -> list:
        """
        Return a list of nodes that satisfy the condition
        (don't care about the prioriy).

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Mage
        >>> bq = BattleQueue()
        >>> c = Mage("m", bq, ManualPlaystyle(bq))
        >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> t = create_default_tree()
        >>> t.skill_list(c, c2)[0].priority
        4
        >>> t.skill_list(c, c2)[1].value.get_sp_cost()
        3
        """
        if self.children == []:
            return [self]
        else:
            if self.condition(caster, target):
                skill_lst = sum([child.skill_list(caster, target)
                                 for child in self.children], [])
            else:
                return [self]
        return skill_lst


def f1(caster, _):
    """
    Return True if the caster's hp is higher than 90.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Mage
    >>> bq = BattleQueue()
    >>> c = Mage("m", bq, ManualPlaystyle(bq))
    >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
    >>> f1(c, c2)
    True
    """
    return caster.get_hp() > 90


def f2(_, target):
    """
    Return True if the target's sp is higher than 40.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Mage
    >>> bq = BattleQueue()
    >>> c = Mage("m", bq, ManualPlaystyle(bq))
    >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
    >>> f2(c, c2)
    True
    """
    return target.get_sp() > 40


def f3(caster, _):
    """
    Return True if the caster's sp is higher than 20.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Mage
    >>> bq = BattleQueue()
    >>> c = Mage("m", bq, ManualPlaystyle(bq))
    >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
    >>> f3(c, c2)
    True
    """
    return caster.get_sp() > 20


def f4(_, target):
    """
    Return True if the target's hp is lower than 30.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Mage
    >>> bq = BattleQueue()
    >>> c = Mage("m", bq, ManualPlaystyle(bq))
    >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
    >>> f4(c, c2)
    False
    """
    return target.get_hp() < 30


def f5(caster, _):
    """
    Return True if the caster's hp is higher than 50.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Mage
    >>> bq = BattleQueue()
    >>> c = Mage("m", bq, ManualPlaystyle(bq))
    >>> c2 = Mage("m2", bq, ManualPlaystyle(bq))
    >>> f5(c, c2)
    True
    """
    return caster.get_hp() > 50


def create_default_tree() -> 'SkillDecisionTree':
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    >>> t = create_default_tree()
    >>> t.value.get_sp_cost()
    5
    >>> t.priority
    5
    >>> t.children[0].priority
    3
    """
    from a2_skills import RogueAttack, RogueSpecial, MageAttack, MageSpecial
    t4 = SkillDecisionTree(RogueSpecial(), f4, 4,
                           [SkillDecisionTree(RogueAttack(), f1, priority=6)])
    t3 = SkillDecisionTree(MageAttack(), f3, 3, [t4])
    t2 = SkillDecisionTree(MageSpecial(), f2, 2,
                           [SkillDecisionTree(RogueAttack(), f1, priority=8)])
    t1 = SkillDecisionTree(RogueAttack(), f1, 1,
                           [SkillDecisionTree(RogueSpecial(), f1, priority=7)])
    root = SkillDecisionTree(MageAttack(), f5, 5, [t3, t2, t1])
    return root


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
