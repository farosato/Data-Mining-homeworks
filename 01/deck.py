from __future__ import division
import time
import pydealer

TRIALS = 1000000  # ~3 mins for a million trials
FORMAT = '{0:.5f}'

atLeast1Ace3Cards = 0
allEquals3Cards = 0
exactly1Ace5Cards = 0
allDiamonds5Cards = 0
full5Cards = 0


def at_least_1_ace_3_cards(cards):
    return any(c.value == 'Ace' for c in cards[:3])


def all_equals_3_cards(cards):
    return cards[0].value == cards[1].value == cards[2].value


def exactly_1_ace_5_cards(cards):
    ace_found = False
    for c in cards:
        if c.value == 'Ace' and not ace_found:
            ace_found = True
        elif c.value == 'Ace' and ace_found:
            return False
    return ace_found


def all_diamonds_5_cards(cards):
    return all(c.suit == 'Diamonds' for c in cards)


def full_5_cards(cards):
    # NOTE: hand is passed by reference, sort() updates original
    cards.sort()
    return (cards[0].value != cards[3].value and cards[0].value == cards[1].value == cards[2].value and cards[3].value == cards[4].value) \
           or (cards[0].value != cards[2].value and cards[0].value == cards[1].value and cards[2].value == cards[3].value == cards[4].value)


def print_results():
    print '##### Frequencies report on %d trials #####\n' % TRIALS
    print 'At least 1 Ace in first 3 cards:\t' + FORMAT.format(atLeast1Ace3Cards / TRIALS)
    print 'First 3 cards all equals:\t\t\t' + FORMAT.format(allEquals3Cards / TRIALS)
    print 'Exactly 1 Ace in first 5 cards:\t\t' + FORMAT.format(exactly1Ace5Cards / TRIALS)
    print 'All Diamonds in first 5 cards:\t\t' + FORMAT.format(allDiamonds5Cards / TRIALS)
    print 'Full in first 5 cards:\t\t\t\t' + FORMAT.format(full5Cards / TRIALS)


if __name__ == "__main__":
    start_time = time.time()
    for i in range(0, TRIALS):
        deck = pydealer.Deck()
        deck.shuffle()
        hand = deck.deal(5)
        if at_least_1_ace_3_cards(hand):
            atLeast1Ace3Cards += 1
        if all_equals_3_cards(hand):
            allEquals3Cards += 1
        if exactly_1_ace_5_cards(hand):
            exactly1Ace5Cards += 1
        if all_diamonds_5_cards(hand):
            allDiamonds5Cards += 1
        if full_5_cards(hand):
            full5Cards += 1
    print_results()
    print("\n--- %s seconds ---" % (time.time() - start_time))
