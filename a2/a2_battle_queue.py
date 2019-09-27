"""
The BattleQueue classes for A2.

A BattleQueue is a queue that lets our game know in what order various
characters are going to attack.

BattleQueue has been completed for you, and the class header for
RestrictedBattleQueue has been provided. You must implement
RestrictedBattleQueue and document it accordingly.
"""
from typing import Union


class BattleQueue:
    """
    A class representing a BattleQueue.
    """

    def __init__(self) -> None:
        """
        Initialize this BattleQueue.

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._content = []
        self._p1 = None
        self._p2 = None

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq.is_empty()
        False
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)

    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_empty()
        False
        """
        self._content.append(character)

        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content.pop(0)

    def is_empty(self) -> bool:
        """
        Return whether this BattleQueue is empty (i.e. has no players or
        has no players that can perform any actions).

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content == []

    def peek(self) -> 'Character':
        """
        Return the character at the front of this BattleQueue but does not
        remove them.

        If this BattleQueue is empty, returns the first player who was added
        to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.peek()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        False
        """
        self._clean_queue()

        if self._content:
            return self._content[0]

        return self._p1

    def is_over(self) -> bool:
        """
        Return whether the game being carried out in this BattleQueue is over
        or not.

        A game is considered over if:
            - Both players have no skills that they can use.
            - One player has 0 HP
            or
            - The BattleQueue is empty.

        >>> bq = BattleQueue()
        >>> bq.is_over()
        True

        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_over()
        False
        """
        if self.is_empty():
            return True

        if self._p1.get_hp() == 0 or self._p2.get_hp() == 0:
            return True

        return False

    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. Otherwise, return None.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.get_winner()
        """
        if not self.is_over():
            return None

        if self._p1.get_hp() == 0:
            return self._p2
        elif self._p2.get_hp() == 0:
            return self._p1

        return None

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = BattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()

        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)

        return new_battle_queue

    def __repr__(self) -> str:
        """
        Return a representation of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        return " -> ".join([repr(character) for character in self._content])


class RestrictedBattleQueue(BattleQueue):
    """
    A class representing a RestrictedBattleQueue.

    Rules for a RestrictedBattleQueue:
    - The first time each character is added to the RestrictedBattleQueue,
      they're able to add.

    For the below, you may assume that the character at the front of the
    RestrictedBattleQueue is the one adding:
    - Characters that are added to the RestrictedBattleQueue by a character
      other than themselves cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> B
      Able to add:     Y    Y

      Then if A tried to add B to the RestrictedBattleQueue, it would look like:
      Character order: A -> B -> B
      Able to add:     Y    Y    N
    - Characters that have 2 copies of themselves in the RestrictedBattleQueue
      already that can add cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> A -> B
      Able to add:     Y    Y    Y

      Then if A tried to add themselves in, the RestrictedBattleQueue would
      look like:
      Character order: A -> A -> B -> A
      Able to add:     Y    Y    Y    N

      If we removed from the RestrictedBattleQueue and tried to add A in again,
      then it would look like:
      Character order: A -> B -> A -> A
      Able to add:     Y    Y    N    Y
    """

    def __init__(self) -> None:
        super().__init__()
        self.able_content = []
        self.count_able_p1 = 0
        self.count_able_p2 = 0

    def add(self, character: 'Character') -> None:
        """
        Add character to this RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.is_empty()
        False
        >>> rbq.able_content
        ['Y']
        >>> rbq.add(c2)
        >>> rbq.able_content
        ['Y', 'Y']
        >>> rbq.add(c2)
        >>> rbq.able_content
        ['Y', 'Y', 'N']
        >>> rbq.remove()
        Sophia (Rogue): 100/100
        >>> rbq.remove()
        Sophia (Rogue): 100/100
        >>> rbq.add(c)
        >>> rbq.able_content
        ['N']
        >>> rbq.add(c2)
        >>> rbq.able_content
        ['N']
        """
        if self.able_content != [] and self.able_content[0] == 'N':
            return
        first_time = False
        if character not in self._content:
            first_time = True
        self._content.append(character)
        if not self._p1:
            self._p1 = character
            self.able_content.append('Y')
            self.count_able_p1 += 1
            self._p2 = character.enemy
            return
        if first_time:
            if character == self._p2:
                self.able_content.append('Y')
                self.count_able_p2 += 1
            if character == self._p1:
                self.able_content.append('Y')
                self.count_able_p1 += 1
            return
        if character == self._p1:
            if self._content[0] is character.enemy:
                self.able_content.append('N')
            elif self.count_able_p1 >= 2:
                self.able_content.append('N')
            else:
                self.able_content.append('Y')
                self.count_able_p1 += 1
        if character == self._p2:
            if self._content[0] is character.enemy:
                self.able_content.append('N')
            elif self.count_able_p2 >= 2:
                self.able_content.append('N')
            else:
                self.able_content.append('Y')
                self.count_able_p2 += 1

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.add(c2)
        >>> rbq.is_empty()
        False
        """
        while self._content and self._content[0].get_available_actions() == []:
            r1 = self._content.pop(0)
            r2 = self.able_content.pop(0)
            if r1 == self._p1 and r2 == 'Y':
                if self.count_able_p1 > 0:
                    self.count_able_p1 -= 1
            if r1 == self._p2 and r2 == 'Y':
                if self.count_able_p2 > 0:
                    self.count_able_p2 -= 1

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this
        RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.able_content
        ['Y']
        >>> rbq.remove()
        Sophia (Rogue): 100/100
        >>> rbq.is_empty()
        True
        >>> rbq.able_content
        []
        """
        self._clean_queue()
        r = self.able_content.pop(0)
        character_remove = self._content.pop(0)
        if character_remove == self._p1 and r == 'Y':
            if self.count_able_p1 > 0:
                self.count_able_p1 -= 1
        if character_remove == self._p2 and r == 'Y':
            if self.count_able_p2 > 0:
                self.count_able_p2 -= 1
        return character_remove

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this RestrictedBattleQueue. The copy contains copies of
        the characters inside this RestrictedBattleQueue, so any changes that
        rely on the copy do not affect this RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("r2", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.add(c2)
        >>> new_rbq = rbq.copy()
        >>> new_rbq.peek().attack()
        >>> new_rbq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> rbq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        >>> new_rbq.able_content
        ['Y', 'Y', 'Y']
        >>> rbq.able_content
        ['Y', 'Y']
        """
        new_battle_queue = RestrictedBattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()

        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)

        return new_battle_queue


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
