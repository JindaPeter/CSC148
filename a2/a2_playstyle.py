"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
from typing import Any, List, Union
import random


class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError


class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)


class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    """
    cbq = battle_queue.copy()
    if cbq.is_over() is True:
        if cbq.is_empty() is True:
            if cbq.get_winner() is None:
                return 0
            current_player = cbq.peek()
            if cbq.get_winner() == current_player:
                return current_player.get_hp()
            return -1 * current_player.enemy.get_hp()
        current_player = cbq.peek()
        if cbq.get_winner() == current_player:
            return current_player.get_hp()
        return -1 * current_player.enemy.get_hp()
    action = cbq.peek().get_available_actions()
    score_list = []
    for a in action:
        if a == 'A':
            abq = battle_queue.copy()
            original_player = abq.peek()
            abq.peek().attack()
            if abq.peek().get_available_actions() != []:
                abq.remove()
            if original_player == abq.peek():
                score_list.append(get_state_score(abq))
            else:
                score_list.append(-1 * get_state_score(abq))
        if a == 'S':
            sbq = battle_queue.copy()
            original_player = sbq.peek()
            sbq.peek().special_attack()
            if sbq.peek().get_available_actions() != []:
                sbq.remove()
            if original_player == sbq.peek():
                score_list.append(get_state_score(sbq))
            else:
                score_list.append(-1 * get_state_score(sbq))
    return max(score_list)


class RecursiveMinimax(Playstyle):
    """
    The RecurviseMinimax playstyle. Inherits from Playstyle.
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RecursiveMinimax playstyle with BattleQueue as
        its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, RecursiveMinimax(bq))
        >>> m = Mage("m", bq, RecursiveMinimax(bq))
        >>> playstyle = m.playstyle
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> playstyle.select_attack()
        'A'
        >>> r.set_hp(40)
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq.add(r)
        >>> playstyle.select_attack()
        'S'
        """
        actions = self.battle_queue.peek().get_available_actions()
        if not actions:
            return 'X'
        if len(actions) == 1:
            return actions[0]
        score_dict = {}
        for a in actions:
            if a == 'A':
                abq = self.battle_queue.copy()
                original_player = abq.peek()
                abq.peek().attack()
                if abq.peek().get_available_actions() != []:
                    abq.remove()
                if original_player == abq.peek():
                    score_dict['A'] = get_state_score(abq)
                else:
                    score_dict['A'] = -1 * get_state_score(abq)
            if a == 'S':
                sbq = self.battle_queue.copy()
                original_player = sbq.peek()
                sbq.peek().special_attack()
                if sbq.peek().get_available_actions() != []:
                    sbq.remove()
                if original_player == sbq.peek():
                    score_dict['S'] = get_state_score(sbq)
                else:
                    score_dict['S'] = -1 * get_state_score(sbq)
        if score_dict['A'] < score_dict['S']:
            return 'S'
        return 'A'

    def copy(self, new_battle_queue: 'BattleQueue'):
        """
        Return a copy of this RecursiveMinimax Playstyle which uses the
        BattleQueue new_battle_queue.
        """
        return RecursiveMinimax(new_battle_queue)


class BattleTree:
    """
    A class representing a BattleTree.

    bq - The battlequeue of the BattleTree.
    children - The root nodes of the children of this BattleTree.
    highest_score - the highest score this BattleTree is guarantee to get.
    parent_peek - the player returned by calling battlequeue's peek() method
    of this BattleTree's parent.
    """
    bq: 'BattleQueue'
    children: List['BattleTree']
    highest_score: Union[int, None]
    parent_peek: 'Character'

    def __init__(self, battle_queue: 'BattleQueue', p: 'Character' = None,
                 children: List['BattleTree'] = None) -> None:
        """
        Initialize this BattleTree with the battle_queue and children.
        """
        self.bq = battle_queue
        self.children = children[:] if children else None
        self.highest_score = None
        self.parent_peek = p


class IterativeMinimax(Playstyle):
    """
    The IterativeMinimax playstyle. Inherits from Playstyle.
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this IterativeMinimax playstyle with BattleQueue as
        its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def over_state_score(self, bt: 'BattleTree') -> None:
        """
        Set the highest score for the bt when the its battlequeue is over.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> playstyle = m.playstyle
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(0)
        >>> bt = BattleTree(bq.copy())
        >>> playstyle.over_state_score(bt)
        >>> bt.highest_score
        100
        """
        if bt.bq.is_empty() is True:
            if bt.bq.get_winner() is None:
                bt.highest_score = 0
            else:
                current_player = bt.bq.peek()
                if bt.bq.get_winner() == current_player:
                    bt.highest_score = current_player.get_hp()
                else:
                    bt.bq.highest_score = -1 * current_player.enemy.get_hp()
        current_player = bt.bq.peek()
        if bt.bq.get_winner() == current_player:
            bt.highest_score = current_player.get_hp()
        else:
            bt.highest_score = -1 * current_player.enemy.get_hp()

    def none_children_state(self, bt: 'BattleTree', stack: List['BattleTree'])\
            -> None:
        """
        Set the children of bt and add bt and its children back to the stack.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> playstyle = m.playstyle
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> stack = []
        >>> bt = BattleTree(bq.copy())
        >>> playstyle.none_children_state(bt, stack)
        >>> len(stack)
        3
        >>> bt.children is None
        False
        """
        actions = bt.bq.peek().get_available_actions()
        children_list = []
        for a in actions:
            if a == 'A':
                abq = bt.bq.copy()
                parent_player = abq.peek()
                abq.peek().attack()
                if abq.peek().get_available_actions() != []:
                    abq.remove()
                children_list.append(BattleTree(abq, parent_player))
            if a == 'S':
                sbq = bt.bq.copy()
                parent_player = sbq.peek()
                sbq.peek().special_attack()
                if sbq.peek().get_available_actions() != []:
                    sbq.remove()
                children_list.append(BattleTree(sbq, parent_player))
        bt.children = children_list
        stack.append(bt)
        for child in bt.children:
            stack.append(child)

    def children_list_state(self, bt: 'BattleTree') -> None:
        """
        Set the bt's highest_score when the children of bt is a list.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> playstyle = m.playstyle
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> stack = []
        >>> bt = BattleTree(bq.copy())
        >>> playstyle.none_children_state(bt, stack)
        >>> bt.children[0].highest_score = 50
        >>> bt.children[1].highest_score = -50
        >>> playstyle.children_list_state(bt)
        >>> bt.highest_score
        50
        """
        score_list = []
        for child in bt.children:
            if child.parent_peek == child.bq.peek():
                score_list.append(child.highest_score)
            else:
                score_list.append(-1 * child.highest_score)
        bt.highest_score = max(score_list)

    def get_state_score_iterative(self, battle_queue: 'BattleQueue') -> int:
        """
        Return an int corresponding to the highest score that the next player in
        battle_queue can guarantee.(Iteratively)

        For a state that's over, the score is the HP of the character who still
        has HP if the next player who was supposed to act is the winner. If the
        next player who was supposed to act is the loser, then the score is -1 *
        the HP of the character who still has HP. If there is no winner (i.e.
        there's a tie) then the score is 0.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> playstyle = m.playstyle
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> playstyle.get_state_score_iterative(bq)
        100
        >>> r.set_hp(40)
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq.add(r)
        >>> playstyle.get_state_score_iterative(bq)
        -10
        """
        present_state = BattleTree(battle_queue.copy())
        stack = [present_state]
        while stack:
            above = stack.pop()
            if above.bq.is_over() is True:
                self.over_state_score(above)
            else:
                if above.children is None:
                    self.none_children_state(above, stack)
                elif isinstance(above.children, list) is True:
                    self.children_list_state(above)
        return present_state.highest_score

    def select_attack(self, parameter: Any = None):
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> playstyle = m.playstyle
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> playstyle.select_attack()
        'A'
        >>> r.set_hp(40)
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq.add(r)
        >>> playstyle.select_attack()
        'S'
        """
        actions = self.battle_queue.peek().get_available_actions()
        if not actions:
            return 'X'
        if len(actions) == 1:
            return actions[0]
        score_dict = {}
        for a in actions:
            if a == 'A':
                abq = self.battle_queue.copy()
                original_player = abq.peek()
                abq.peek().attack()
                if abq.peek().get_available_actions() != []:
                    abq.remove()
                if original_player == abq.peek():
                    score_dict['A'] = self.get_state_score_iterative(abq)
                else:
                    score_dict['A'] = -1 * self.get_state_score_iterative(abq)
            if a == 'S':
                sbq = self.battle_queue.copy()
                original_player = sbq.peek()
                sbq.peek().special_attack()
                if sbq.peek().get_available_actions() != []:
                    sbq.remove()
                if original_player == sbq.peek():
                    score_dict['S'] = self.get_state_score_iterative(sbq)
                else:
                    score_dict['S'] = -1 * self.get_state_score_iterative(sbq)
        if score_dict['A'] < score_dict['S']:
            return 'S'
        return 'A'

    def copy(self, new_battle_queue: 'BattleQueue'):
        """
        Return a copy of this IterativeMinimax Playstyle which uses the
        BattleQueue new_battle_queue.
        """
        return IterativeMinimax(new_battle_queue)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
