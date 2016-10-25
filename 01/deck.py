from __future__ import division
import pydealer
import time

TRIALS = 1000000    # ~3 mins for a million trials
FORMAT = '{0:.5f}'

atLeast1Ace3Cards = 0
allEquals3Cards = 0
exactly1Ace5Cards = 0
allDiamonds5Cards = 0
full5Cards = 0

def at_least_1_ace_3_cards(hand):
    return any(c.value == 'Ace' for c in hand[:3])

def all_equals_3_cards(hand):
    return hand[0].value == hand[1].value and hand[1].value == hand[2].value\
            and hand[0].value == hand[2].value

def exactly_1_ace_5_cards(hand):
    aceFound = False
    for c in hand:
        if c.value == 'Ace' and not aceFound:
            aceFound = True
        elif c.value == 'Ace' and aceFound:
            return False
    return aceFound

def all_diamonds_5_cards(hand):
    for c in hand:
        if c.suit != 'Diamonds':
            return False
    return True

def full_5_cards(hand):
    # NOTE: hand is passed by reference, sort() update original
    hand.sort()
    return (hand[0].value == hand[1].value == hand[2].value and hand[3].value == hand[4].value\
                and hand[0].value != hand[3].value)\
            or (hand[0].value == hand[1].value and hand[2].value == hand[3].value == hand[4].value\
                and hand[0].value != hand[2].value)

def print_results():
    print '##### Frequencies report on %d trials #####\n' % (TRIALS) 
    print 'At least 1 Ace in first 3 cards:\t' + FORMAT.format(atLeast1Ace3Cards / TRIALS)
    print 'First 3 cards all equals:\t\t' + FORMAT.format(allEquals3Cards / TRIALS)
    print 'Exactly 1 Ace in first 5 cards:\t\t' + FORMAT.format(exactly1Ace5Cards / TRIALS)
    print 'All Diamonds in first 5 cards:\t\t' + FORMAT.format(allDiamonds5Cards / TRIALS)
    print 'Full in first 5 cards:\t\t\t' + FORMAT.format(full5Cards / TRIALS)

if __name__ == "__main__":
    start_time = time.time()
    for i in range(0,TRIALS):
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

