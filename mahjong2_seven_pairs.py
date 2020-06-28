from collections import namedtuple, Counter
from typing import List, Tuple, Set

Card = namedtuple('Card', ['rank', 'suit'])
State = namedtuple('State', ['hand', 'melds', 'pairs', 'unmatched', 'deck'])


def solution(tiles):
    suits = ['p', 's', 'm', 'z']

    def sort_cards(cards):
        return sorted(cards, key=lambda c: suits.index(c.suit) * 10 + c.rank)

    deck = Counter({
        Card(rank, suit): 4
        for suit in suits
        for rank in range(1, 8 if suit == 'z' else 10)
    })

    hand = sort_cards([
        Card(int(card[0]), card[1])
        for card in tiles.split(' ')
    ])

    for c in hand:
        deck[c] -= 1
        if deck[c] <= 0:
            del deck[c]

    initial_state = State(hand, melds=0, pairs=0, unmatched=[], deck=deck)
    res = search(initial_state)
    return ' '.join(f"{c.rank}{c.suit}" for c in sort_cards(res))


def search(state: State) -> Set[Card]:
    if not state.hand:
        winning_cards = winning_cards_for(state)
        if winning_cards:
            return winning_cards
        else:
            return set()

    res = set()
    c = state.hand[0]
    new_hand = state.hand[1:]

    # Straight meld
    if c.suit != 'z' and Card(c.rank + 1, c.suit) in new_hand and Card(c.rank + 2, c.suit) in new_hand:
        meld_hand = list(new_hand)
        meld_hand.remove(Card(c.rank + 1, c.suit))
        meld_hand.remove(Card(c.rank + 2, c.suit))
        meld_state = state._replace(hand=meld_hand, melds=state.melds + 1)
        meld_res = search(meld_state)
        res.update(meld_res)

    # Pair
    if Card(c.rank, c.suit) in new_hand:
        pair_hand = list(new_hand)
        pair_hand.remove(Card(c.rank, c.suit))
        pair_state = state._replace(hand=pair_hand, pairs=state.pairs + 1)
        pair_res = search(pair_state)
        res.update(pair_res)

        # Triple meld
        if Card(c.rank, c.suit) in pair_hand:
            triple_hand = list(pair_hand)
            triple_hand.remove(Card(c.rank, c.suit))
            triple_state = state._replace(hand=triple_hand, melds=state.melds + 1)
            triple_res = search(triple_state)
            res.update(triple_res)

    # Unmatched
    unmatched_state = state._replace(hand=list(new_hand), unmatched=state.unmatched + [c])
    unmatched_res = search(unmatched_state)
    res.update(unmatched_res)
    return res


def winning_cards_for(state: State) -> Set[Card]:
    if (state.melds == 4 and state.pairs == 0) or state.pairs == 6:
        return {c for c in state.unmatched if c in state.deck}
    elif state.melds == 3 and state.pairs == 1:
        return {c for c in meld_cards_for(state.unmatched) if c in state.deck}
    else:
        return set()


def meld_cards_for(cards: Tuple[Card]) -> List[Card]:
    res = []
    if len(cards) == 2 and cards[0].suit == cards[1].suit:
        min_rank = min(cards[0].rank, cards[1].rank)
        max_rank = max(cards[0].rank, cards[1].rank)
        if max_rank - min_rank == 0:
            res.append(Card(min_rank, cards[0].suit))
        elif cards[0].suit != 'z' and max_rank - min_rank == 1:
            res.append(Card(min_rank - 1, cards[0].suit))
            res.append(Card(max_rank + 1, cards[0].suit))
        elif cards[0].suit != 'z' and max_rank - min_rank == 2:
            res.append(Card(min_rank + 1, cards[0].suit))
    return res


if __name__ == '__main__':
    from test import Test as test

    # You may add more custom tests here :)
    cases = [
        ('2p 2p 3p 3p 4p 4p 5p 5p 7m 7m 8m 8m 8m', '2p 5p 7m 8m'),
        ('1p 1p 3p 3p 4p 4p 5p 5p 6p 6p 7p 7p 9p', '9p'),
        ('2p 2p 3p 3p 4p 4p 5p 5p 5p 5p 7p 7p 9p', '9p'),
        ('2p 2p 2p 3p 3p 3p 4p 4p 4p 5p 5p 6p 8p', '7p'),
        ('2p 2p 2p 3p 3p 3p 4p 4p 4p 5p 5p 7p 8p', '6p 9p'),
        ('2p 2p 2p 3p 3p 3p 4p 4p 4p 5p 5p 6m 7m', '5m 8m'),
        ('2p 2p 2p 3p 3p 3p 4p 4p 4p 5p 5p 6p 7p', '2p 3p 4p 5p 6p 8p'),
    ]

    for hand, expected in cases:
        test.assert_equals(solution(hand), expected)
