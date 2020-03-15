import random
import numpy as np

suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
counter = np.zeros(9)


class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)


class Deck(object):
    def __init__(self):
        self.cards = []
        for s in suits:
            for r in ranks:
                self.cards.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        deck = ""
        for i in range(0, 52):
            deck += str(self.cards[i]) + " "
        return deck

    def take_one(self):
        return self.cards.pop(0)


class Hand(object):
    def __init__(self, deck):
        self.cards = []
        self.ranks_in_hand = []
        for i in range(5):
            self.cards.append(deck.take_one())
        for i in range(5):
            ind = ranks.index(self.cards[i].get_rank())
            self.ranks_in_hand.append(ind)
        # Automatically counts which hand it is
        self.get_hand()

    def __str__(self):
        hand = ""
        for i in range(5):
            hand += str(self.cards[i]) + " "
        return hand

    def is_pair(self):
        for i in range(5):
            for j in range(i + 1, 5):
                if self.cards[i].get_rank() == self.cards[j].get_rank():
                    return True
        return False

    def is_pair_new(self):
        _, counts = np.unique(self.ranks_in_hand, return_counts=True)
        if len(counts) == 4:
            return True
        return False

    def is_two_pairs(self):
        _, counts = np.unique(self.ranks_in_hand, return_counts=True)
        if (2 in counts) and len(counts) == 3:
            return True
        return False

    def is_three_of_kind(self):
        _, counts = np.unique(self.ranks_in_hand, return_counts=True)
        if (3 in counts) and len(counts) == 3:
            return True

        return False

    def is_straight(self):
        # The element-wise addition of the ordered and reverse ranks is equal : [3, 4, 5] + [5, 4, 3] = [8, 8, 8]
        additions = [sum(x) for x in zip(self.ranks_in_hand, self.ranks_in_hand[::-1])]
        if len(set(additions)) == 1:
            return True
        return False

    def is_flush(self):
        suits_in_hand = []
        for i in range(5):
            suits_in_hand.append(self.cards[i].get_suit())
        if len(set(suits_in_hand)) == 1:
            return True
        return False

    def is_full_house(self):
        # Numpy.unique returns unique elements and their counts. The counts for full house should always be a 2 and 3
        _, counts = np.unique(self.ranks_in_hand, return_counts=True)
        if set(counts) == {2, 3}:
            return True
        return False

    def is_four_of_kind(self):
        # Same logic as full house. The counts for four of a kind should always be a 1 and 4
        _, counts = np.unique(self.ranks_in_hand, return_counts=True)
        if set(counts) == {1, 4}:
            return True
        return False

    def is_straight_flush(self):
        if self.is_straight() and self.is_flush():
            return True
        return False

    def is_royal_flush(self):
        if set(self.cards) == {"10", "J", "Q", "K", "A"} and self.is_flush():
            return True
        return False

    def get_hand(self):
        if self.is_pair_new():
            counter[0] += 1
        elif self.is_two_pairs():
            counter[1] += 1
        elif self.is_flush() :
            counter[4] += 1
        elif self.is_full_house():
            counter[5] += 1
        elif self.is_four_of_kind():
            counter[6] += 1
        elif self.is_straight_flush():
            counter[7] += 1
        elif self.is_straight():
            counter[3] += 1
        elif self.is_three_of_kind():
            counter[2] += 1
        elif self.is_royal_flush():
            counter[8] += 1


# Super quick-and-dirty implementations.. But the idea is here, and it's Sunday 11PM !

for i in range(5000):
    new_deck = Deck()
    new_deck.shuffle()
    hand = Hand(new_deck)

names = ["Pair", "Two Pair","Three of a kind", "Straight", "Flush",
         "Full House", "Four of a kind", "Straight Flush", "Royal Flush"]
print("----- 50000 Iterations ------")
for n,c in zip(names, counter):
    print("{} : {} ({}%)".format(n,int(c), (round(c/5000 * 100, 2))))
