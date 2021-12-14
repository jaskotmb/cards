import random
import operator

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        numDict = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
        num2Dict = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
        self.number = numDict[value]
        self.numbermax = num2Dict[value]

class Hand:
    def __init__(self, cards, owner):
        self.cards = cards
        self.owner = owner
        self.softTotal = sum(c.number for c in cards)
        self.hardTotal = sum(c.numbermax for c in cards)
        if self.softTotal > 21:
            self.bestTotal = self.softTotal
        else:
            self.bestTotal = self.hardTotal
        self.action = ''

class Player:
    def __init__(self, name, bankroll, wins, losses):
        self.name = name
        self.bankroll = bankroll
        self.wins = wins
        self.losses = losses

def DealerHand(shoe):
    dealer1 = shoe.pop(0)
    dealer2 = shoe.pop(0)
    return [dealer1, dealer2]

def InitialHand(shoe):
    card1 = shoe.pop(0)
    card2 = shoe.pop(0)
    return [card1, card2]

def PrintDealerHand(hand):
    print("Dealer: ",hand.cards[0].value,hand.cards[0].suit,sep='')

def PrintPlayerHand(hand):
    h = hand.cards
    hand.hardTotal = 0
    hand.softTotal = 0
    for i in range(len(hand.cards)):
        hand.hardTotal = hand.hardTotal + hand.cards[i].number
        hand.softTotal = hand.softTotal + hand.cards[i].number
        if hand.softTotal > 21:
            hand.bestTotal = hand.hardTotal
        else:
            hand.bestTotal = hand.softTotal
    print('Player ',hand.owner.name,':',sep='')
    vals = [card.value for card in h]
    suits = [card.suit for card in h]
    for i in range(len(h)):
        print(vals[i],suits[i],' ',sep='',end='')
    if hand.softTotal < hand.hardTotal:
        print(' (',hand.softTotal,'/',hand.hardTotal,')',sep='')
    else:
        print(' (',hand.hardTotal,')',sep='')

def PrintFullDealerHand(hand,quiet='n'):
    h = hand.cards
    hand.hardTotal = 0
    hand.softTotal = 0
    for i in range(len(hand.cards)):
        hand.hardTotal = hand.hardTotal + hand.cards[i].number
        hand.softTotal = hand.softTotal + hand.cards[i].number
        if hand.softTotal > 21:
            hand.bestTotal = hand.hardTotal
        else:
            hand.bestTotal = hand.softTotal
    if quiet != 'q':
        print('Dealer :')
        vals = [card.value for card in h]
        suits = [card.suit for card in h]
        for i in range(len(h)):
            print(vals[i],suits[i],' ',sep='',end='')
        if hand.softTotal < hand.hardTotal:
            print(' (',hand.softTotal,'/',hand.hardTotal,')',sep='')
        else:
            print(' (',hand.hardTotal,')',sep='')

def InitializePlayers(players,deck):
    playerList = []
    handList = []
    for i in range(players):
        playerList.append(Player(i,0,0,0))
        handList.append(Hand(InitialHand(deck),playerList[i]))
        PrintPlayerHand(handList[i])
    return [playerList, handList]

def DealPlayerCard(hand, deck):
    hand.cards.append(deck.pop(0))
    return [hand, deck]

suits = ['\u2665','\u2663','\u2660','\u25C6']
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

deck = [Card(value, suit) for value in values for suit in suits]
players = int(input('How many players? '))
random.shuffle(deck)

dealerHand = Hand(DealerHand(deck),'dealer')
PrintDealerHand(dealerHand)
playerList = []
handList = []
[playerList, handList] = InitializePlayers(players,deck)
print('')
for i in range(players):
    PrintPlayerHand(handList[i])
    action = 'h'
    while action == 'h':
        print('Player ',str(i),', ',sep='',end='')
        action = input('(h)it or (s)tand? ')
        if action == 's':
            break
        [handList[i], deck] = DealPlayerCard(handList[i], deck)
        PrintPlayerHand(handList[i])
        if handList[i].hardTotal > 21:
            print('Player ',str(i),'busts!')
            print('')
            break
print('All players done, time for dealer hand')
for i in range(players):
    PrintPlayerHand(handList[i])
PrintFullDealerHand(dealerHand)
dealerAction = ''
while dealerAction != 'f':
    PrintFullDealerHand(dealerHand,'q')
    if dealerHand.hardTotal <= 17:
        [dealerHand, deck] = DealPlayerCard(dealerHand, deck)
    if 21 > dealerHand.softTotal and dealerHand.softTotal > 17:
        dealerAction = 'f'
        print('Dealer stands')
    if dealerHand.bestTotal > 21:
        dealerAction = 'f'
        print('Dealer busts')


