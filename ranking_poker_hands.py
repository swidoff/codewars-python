from collections import Counter
from typing import List


class PokerHand(object):
    RESULT = ["Loss", "Tie", "Win"]
    FACES = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def __init__(self, hand):
        self.cards = hand.split(" ")
        self.ranks = sorted([PokerHand.FACES[c[0]] if c[0] in PokerHand.FACES else int(c[0]) for c in self.cards],
                            reverse=True)
        self.suits = {c[1] for c in self.cards}

    def compare_with(self, other):
        self_rank, self_remainder = self.rank()
        other_rank, other_remainder = other.rank()
        if self_rank > other_rank:
            return PokerHand.RESULT[2]
        elif self_rank < other_rank:
            return PokerHand.RESULT[0]
        else:
            return self.compare_remainders(self_remainder, other_remainder)

    @staticmethod
    def compare_remainders(self_remainder: List[int], other_remainder: List[int]):
        for c1, c2 in zip(self_remainder, other_remainder):
            if c1 > c2:
                return PokerHand.RESULT[2]
            elif c2 > c1:
                return PokerHand.RESULT[0]
        return PokerHand.RESULT[1]

    def rank(self) -> (int, List[int]):
        flush = len(self.suits) == 1
        straight = all(self.ranks[i - 1] - self.ranks[i] == 1 for i in range(1, 5))
        (kind1_rank, kind1_count), (kind2_rank, kind2_count) = Counter(self.ranks).most_common(2)

        if straight and flush:
            hand = 9
            high_card = max(self.ranks)
            remainder = []
        elif kind1_count == 4:
            hand = 8
            high_card = kind1_rank
            remainder = [r for r in self.ranks if r != kind1_rank]
        elif kind1_count == 3 and kind2_count == 2:
            hand = 7
            high_card = kind1_rank
            remainder = [kind2_rank]
        elif flush:
            hand = 6
            high_card = max(self.ranks)
            remainder = self.ranks
        elif straight:
            hand = 5
            high_card = max(self.ranks)
            remainder = []
        elif kind1_count == 3:
            hand = 4
            high_card = kind1_rank
            remainder = [r for r in self.ranks if r != kind1_rank]
        elif kind1_count == 2 and kind2_count == 2:
            hand = 3
            high_card = max(kind1_rank, kind2_rank)
            remainder = [r for r in self.ranks if r != kind1_rank and r != kind2_rank]
        elif kind1_count == 2:
            hand = 2
            high_card = kind1_rank
            remainder = [r for r in self.ranks if r != kind1_rank]
        else:
            hand = 1
            high_card = max(self.ranks)
            remainder = self.ranks

        return hand * 100 + high_card, remainder


if __name__ == '__main__':
    def runTest(msg, expected, hand, other):
        player, opponent = PokerHand(hand), PokerHand(other)
        assert player.compare_with(opponent) == expected, "{}: '{}' against '{}'".format(msg, hand, other)


    runTest("Highest straight flush wins", "Loss", "2H 3H 4H 5H 6H", "KS AS TS QS JS")
    runTest("Straight flush wins of 4 of a kind", "Win", "2H 3H 4H 5H 6H", "AS AD AC AH JD")
    runTest("Highest 4 of a kind wins", "Win", "AS AH 2H AD AC", "JS JD JC JH 3D")
    runTest("4 Of a kind wins of full house", "Loss", "2S AH 2H AS AC", "JS JD JC JH AD")
    runTest("Full house wins of flush", "Win", "2S AH 2H AS AC", "2H 3H 5H 6H 7H")
    runTest("Highest flush wins", "Win", "AS 3S 4S 8S 2S", "2H 3H 5H 6H 7H")
    runTest("Flush wins of straight", "Win", "2H 3H 5H 6H 7H", "2S 3H 4H 5S 6C")
    runTest("Equal straight is tie", "Tie", "2S 3H 4H 5S 6C", "3D 4C 5H 6H 2S")
    runTest("Straight wins of three of a kind", "Win", "2S 3H 4H 5S 6C", "AH AC 5H 6H AS")
    runTest("3 Of a kind wins of two pair", "Loss", "2S 2H 4H 5S 4C", "AH AC 5H 6H AS")
    runTest("2 Pair wins of pair", "Win", "2S 2H 4H 5S 4C", "AH AC 5H 6H 7S")
    runTest("Highest pair wins", "Loss", "6S AD 7H 4S AS", "AH AC 5H 6H 7S")
    runTest("Pair wins of nothing", "Loss", "2S AH 4H 5S KC", "AH AC 5H 6H 7S")
    runTest("Highest card loses", "Loss", "2S 3H 6H 7S 9C", "7H 3C TH 6H 9S")
    runTest("Highest card wins", "Win", "4S 5H 6H TS AC", "3S 5H 6H TS AC")
    runTest("Equal cards is tie", "Tie", "2S AH 4H 5S 6C", "AD 4C 5H 6H 2C")
    runTest("", "Loss", "3S 8S 9S 5S KS", "4C 5C 9C 8C KC")
    runTest("", "Loss", "2H 2C 3S 3H 3D", "KH KC 3S 3H 3D")
    runTest("", "Win", "3C KH 5D 5S KH", "3H 4C 4H 3S 2H")
    runTest("", "Win", "KH KC 3S 3H 3D", "2H 2C 3S 3H 3D")
    runTest("", "Win", "2H 2C 3S 3H 3D", "3D 2H 3H 2C 2D")
