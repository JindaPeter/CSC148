"""
The Skill classes for A2.

See a2_characters.py for how these are used.
For any skills you make, you're responsible for making sure their style adheres
to PythonTA and that you include all documentation for it.
"""


class Skill:
    """
    An abstract superclass for all Skills.
    """

    def __init__(self, cost: int, damage: int) -> None:
        """
        Initialize this Skill such that it costs cost SP and deals damage
        damage.
        """
        self._cost = cost
        self._damage = damage

    def get_sp_cost(self) -> int:
        """
        Return the SP cost of this Skill.
        """
        return self._cost

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.
        """
        raise NotImplementedError

    def _deal_damage(self, caster: 'Character', target: 'Character') -> None:
        """
        Reduces the SP of caster and inflicts damage on target.
        """
        caster.reduce_sp(self._cost)
        target.apply_damage(self._damage)


class NormalAttack(Skill):
    """
    A class representing a NormalAttack.
    Not to be instantiated.
    """

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(caster)


class SorcererAttack(Skill):
    """
    A class representing a Sorcerer's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this SorcererAttack.

        >>> S = SorcererAttack()
        >>> S.get_sp_cost()
        15
        """
        super().__init__(15, 0)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Sorcerer's Attack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Sorcerer
        >>> from a2_skill_decision_tree import create_default_tree
        >>> bq = BattleQueue()
        >>> s1 = Sorcerer("s1", bq, ManualPlaystyle(bq))
        >>> s2 = Sorcerer("s2", bq, ManualPlaystyle(bq))
        >>> s1.enemy = s2
        >>> s2.enemy = s1
        >>> s1.set_skill_decision_tree(create_default_tree())
        >>> s2.set_skill_decision_tree(create_default_tree())
        >>> s1.attack()
        >>> s1.get_sp()
        85
        >>> s2.get_hp()
        90
        """
        tree = caster.skill_decision_tree
        skill_use = tree.pick_skill(caster, target)
        caster.reduce_sp(self._cost)
        if type(skill_use) == MageAttack:
            target.apply_damage(20)
            caster.battle_queue.add(caster)
        elif type(skill_use) == RogueAttack:
            target.apply_damage(15)
            caster.battle_queue.add(caster)
        elif type(skill_use) == MageSpecial:
            target.apply_damage(40)
            caster.battle_queue.add(target)
            caster.battle_queue.add(caster)
        elif type(skill_use) == RogueSpecial:
            target.apply_damage(20)
            caster.battle_queue.add(caster)
            caster.battle_queue.add(caster)


class SorcererSpecial(Skill):
    """
    A class representing a Sorcerer's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this SorcererAttack.

        >>> s = SorcererSpecial()
        >>> s.get_sp_cost()
        20
        """
        super().__init__(20, 25)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Sorcerer's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Sorcerer
        >>> bq = BattleQueue()
        >>> s1 = Sorcerer("s1", bq, ManualPlaystyle(bq))
        >>> s2 = Sorcerer("s2", bq, ManualPlaystyle(bq))
        >>> s1.enemy = s2
        >>> s2.enemy = s1
        >>> s1.special_attack()
        >>> s1.get_sp()
        80
        >>> s2.get_hp()
        85
        """
        self._deal_damage(caster, target)
        while caster.battle_queue.is_empty() is False:
            caster.battle_queue.remove()
        caster.battle_queue.add(caster)
        caster.battle_queue.add(target)
        caster.battle_queue.add(caster)


class VampireAttack(Skill):
    """
    A class representing a Vampire's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this VampireAttack.

        >>> v = VampireAttack()
        >>> v.get_sp_cost()
        15
        """
        super().__init__(15, 20)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Vampire
        >>> bq = BattleQueue()
        >>> v1 = Vampire("v1", bq, ManualPlaystyle(bq))
        >>> v2 = Vampire("v2", bq, ManualPlaystyle(bq))
        >>> v1.enemy = v2
        >>> v2.enemy = v1
        >>> v1.attack()
        >>> v1.get_sp()
        85
        >>> v1.get_hp()
        117
        >>> v2.get_hp()
        83
        """
        hp_original = target.get_hp()
        self._deal_damage(caster, target)
        hp_now = target.get_hp()
        damage_take = hp_original - hp_now
        caster.restore_hp(damage_take)
        caster.battle_queue.add(caster)


class VampireSpecial(Skill):
    """
    A class representing a Vampire's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this VampireAttack.

        >>> v = VampireSpecial()
        >>> v.get_sp_cost()
        20
        """
        super().__init__(20, 30)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Vampire's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Vampire
        >>> bq = BattleQueue()
        >>> v1 = Vampire("v1", bq, ManualPlaystyle(bq))
        >>> v2 = Vampire("v2", bq, ManualPlaystyle(bq))
        >>> v1.enemy = v2
        >>> v2.enemy = v1
        >>> v1.special_attack()
        >>> v1.get_sp()
        80
        >>> v1.get_hp()
        127
        >>> v2.get_hp()
        73
        """
        hp_original = target.get_hp()
        self._deal_damage(caster, target)
        hp_now = target.get_hp()
        damage_take = hp_original - hp_now
        caster.restore_hp(damage_take)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(target)


class MageAttack(NormalAttack):
    """
    A class representing a Mage's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this MageAttack.

        >>> m = MageAttack()
        >>> m.get_sp_cost()
        5
        """
        super().__init__(5, 20)


class MageSpecial(Skill):
    """
    A class representing a Mage's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this MageAttack.

        >>> m = MageSpecial()
        >>> m.get_sp_cost()
        30
        """
        super().__init__(30, 40)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Mage's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> m.special_attack()
        >>> m.get_sp()
        70
        >>> r.get_hp()
        70
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(target)
        caster.battle_queue.add(caster)


class RogueAttack(NormalAttack):
    """
    A class representing a Rogue's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this RogueAttack.

        >>> r = RogueAttack()
        >>> r.get_sp_cost()
        3
        """
        super().__init__(3, 15)


class RogueSpecial(Skill):
    """
    A class representing a Rogue's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this RogueSpecial.

        >>> r = RogueSpecial()
        >>> r.get_sp_cost()
        10
        """
        super().__init__(10, 20)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Rogue's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> r.special_attack()
        >>> r.get_sp()
        90
        >>> m.get_hp()
        88
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(caster)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
