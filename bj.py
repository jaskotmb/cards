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
    def __init__(self, cards, owner, status=''):
        self.cards = cards
        self.owner = owner
        self.softTotal = sum(c.number for c in cards)
        self.hardTotal = sum(c.numbermax for c in cards)
        if self.softTotal > 21:
            self.bestTotal = self.softTotal
        else:
            self.bestTotal = self.hardTotal
        self.action = ''
        self.status = status

class Player:
    def __init__(self, name, bankroll, wins, losses):
        self.name = name
        self.bankroll = bankroll
        self.wins = wins
        self.losses = losses

def PrintShoe(shoe):
    for card in shoe:
        print(card.value,card.suit,sep='')

def DealerHand(shoe):
    dealer1 = shoe.pop(0)
    dealer2 = shoe.pop(0)
    return Hand([dealer1, dealer2],'dealer')

def InitialHand(shoe):
    card1 = shoe.pop(0)
    card2 = shoe.pop(0)
    return [card1, card2]

def PrintDealerHand(hand):
    print("Dealer: ",hand.cards[0].value,hand.cards[0].suit,sep='')

def PrintPlayerHand(hand, playerList):
    h = hand.cards
    player = int(hand.owner.name)
    print('Player ',hand.owner.name,' (bankroll: ',str(playerList[player].bankroll),' )',sep='')
    vals = [card.value for card in h]
    suits = [card.suit for card in h]
    for i in range(len(h)):
        print(vals[i],suits[i],' ',sep='',end='')
    if hand.softTotal < hand.hardTotal:
        print(' (',hand.softTotal,'/',hand.hardTotal,')',sep='')
    else:
        print(' (',hand.hardTotal,')',sep='')

def UpdateHandTotal(hand):
    hardTotal = 0
    softTotal = 0
    bestTotal = 0
    for i in range(len(hand.cards)):
        hardTotal = hand.cards[i].number + hardTotal
        softTotal = hand.cards[i].numbermax + softTotal
    if softTotal > 21:
        bestTotal = hardTotal
    else:
        bestTotal = softTotal
    hand.softTotal = softTotal
    hand.hardTotal = hardTotal
    hand.bestTotal = bestTotal
    return hand

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

def InitializePlayers(players, deck, bankrolls):
    playerList = []
    handList = []
    for i in range(players):
        playerList.append(Player(i,bankrolls[i],0,0))
        handList.append(Hand(InitialHand(deck),playerList[i]))
        PrintPlayerHand(handList[i],playerList)
    return [playerList, handList]

def DealPlayerCard(hand, deck):
    hand.cards.append(deck.pop(0))
    return [hand, deck]

suits = ['\u2665','\u2663','\u2660','\u25C6']
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

# create single deck
deck = [Card(value, suit) for value in values for suit in suits]
# create shoe of multiple decks
shoe = deck*6
print(len(shoe),' cards in shoe')
# query how many players
players = int(input('How many players? '))

# initialize players with bankrolls
playerList = []
for i in range(players):
    playerList.append(Player(i,1000,0,0))

# shuffle shoe
random.shuffle(shoe)

# cut shoe
cutPos = random.randrange(0,52,1)
print(cutPos)
del shoe[len(shoe)-cutPos:len(shoe)]
print(len(shoe),' cards in shoe')

# ask for bets this hand
betList = []
bankrollList = []
for i in range(len(playerList)):
    print('Player ',str(i),' (bankroll: ',str(playerList[i].bankroll),'), ',sep='',end='')
    betTemp = int(input('bet: '))
    # remove bet amount from player bankroll
    playerList[i].bankroll = playerList[i].bankroll - betTemp
    betList.append(betTemp)
    bankrollList.append(playerList[i].bankroll)

# deal hand to dealer and players
dealerHand = DealerHand(shoe)

# artificially set dealer hand first card to A
dealerHand.cards[0].value = 'A'
dealerHand.cards[1].value = '4'
dealerHand.cards[1].number = 4
PrintDealerHand(dealerHand)
[playerList, handList] = InitializePlayers(players,shoe,bankrollList)

def DetermineOutcomesDealerBJ(playerList, handList, dealerHand, betList):
    outcomeList = []
    for i in range(len(handList)):
        if handList[i].bestTotal == 21:
            playerList[i].bankroll = playerList[i].bankroll + betList[i]
            print('Player ',str(i),' push, (bankroll: ',str(playerList[i].bankroll),')')
        if handList[i].bestTotal != 21:
            print('Player ',str(i),' loses, (bankroll: ',str(playerList[i].bankroll),')')

# if dealer ace ask for insurance
if dealerHand.cards[0].value == 'A':
    print('Dealer ace')
    for i in range(len(playerList)):
        print('Player ',str(i),sep='',end='')
        insTemp = input(' insurance? (y/n): ')
        if insTemp == 'y' and dealerHand.cards[1].number != 10:
            playerList[i].bankroll = playerList[i].bankroll - int(betList[i]/2)
        if insTemp == 'y' and dealerHand.cards[1].number == 10:
            playerList[i].bankroll = playerList[i].bankroll + betList[i]
    # reveal if dealer blackjack
    if dealerHand.cards[1].number == 10:
        PrintFullDealerHand(dealerHand)
        print('Dealer Blackjack')
        outcomeList = DetermineOutcomesDealerBJ(playerList,handList,dealerHand,betList)

# if dealer blackjack, determine outcomes
# move to first hand, test for split condition
# if split condition, ask for split
# if split yes, create 2 new hands from original hand and remove another bet from bankroll
# assign these hands to the same original player
# while loop to continue splitting if allowed
# ask in first move for double/hit/stand
# if double yes, deal next card and double bet, removing from bankroll
# if hit yes, deal next card
# if stand yes, break loop
# after all players done, dealer hand plays out
# determine winners and losers
# pay out bets and add to bankroll

