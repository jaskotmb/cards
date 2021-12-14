import random
import operator

def finalTotal(hand):
    softTotal = sum(c.numbermax for c in hand)
    hardTotal = sum(c.number for c in hand)
    if softTotal > 21:
        total = hardTotal
    else:
        total = softTotal
    if total > 21:
        total = 0
    return(total)

class Card:
    def __init__(self, value, suit, number, numbermax):
        self.value = value
        self.suit = suit
        numDict = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
        num2Dict = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
        self.number = numDict[value]
        self.numbermax = num2Dict[value]

class Player:
    def __init__(self, hand, bestTotal, action, name):
        self.hand = hand
        self.action = action
        self.bestTotal = finalTotal(hand)
        self.name = name

suits = ['\u2665','\u2663','\u2660','\u25C6']
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

deck = [Card(value, suit, 0, 0) for value in values for suit in suits]
for i in range(len(deck)):
    deck[i].number

for i in range(len(deck)):
    print(deck[i].value,deck[i].suit,deck[i].number)


def DealerHand(shoe):
    dealer1 = shoe.pop(0)
    dealer2 = shoe.pop(0)
    return [dealer1, dealer2]

def InitialHand(shoe):
    card1 = shoe.pop(0)
    card2 = shoe.pop(0)
    return [card1, card2]

def PrintDealerHand(hand):
    print("Dealer: ",hand[0].value,hand[0].suit,sep='')

def PrintDealerFullHand(hand):
    if sum(c.number for c in hand) <= 21:
        if hand[0].value != 'A' and hand[1].value != 'A':
            print("Dealer: ",[h.value + ' ' + h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),sep='')
        elif hand[0].value == 'A' or hand[1].value == 'A':
            print("Dealer: ",[h.value + ' '+ h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),' or ',sum(c.number for c in hand) + 10,sep='')
    else:
        print("Dealer: ",[h.value + ' ' + h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),' Dealer busts!',sep='')

def PrintPlayerHand(hand):
    if sum(c.number for c in hand) <= 21 and len(hand) > 1:
        if hand[0].value != 'A' and hand[1].value != 'A':
            print("",[h.value + ' ' + h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),sep='')
        elif hand[0].value == 'A' or hand[1].value == 'A':
            print("",[h.value + ' '+ h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),' or ',sum(c.number for c in hand) + 10,sep='')
    elif len(hand) > 1:
        print("",[h.value + ' ' + h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),' Player busts!',sep='')
    else:
        print("",[h.value + ' ' + h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),sep='')

# shuffle deck
random.shuffle(deck)
# create player objects and deal hands
rawPlayers = input('Number of Players: ')
players = int(rawPlayers)
print(''+str(players)+' players selected')
playerList = [Player(InitialHand(deck),0,'','') for i in range(players)]
# deal initial dealer hand
gameStatus = 'playing'
dealerHand = InitialHand(deck)
# show dealer hand
PrintDealerHand(dealerHand)
# name players
for i in range(len(playerList)):
    playerList[i].name = str(i+1)
# show player hands
for i in range(players):
    print('Player '+str(i+1)+':')
    PrintPlayerHand(playerList[i].hand)
    if sum(c.numbermax for c in playerList[i].hand) == 21:
        print('Player '+playerList[i].name+' Blackjack!')
        playerList[i].action = 'b'
# ask for insurance on dealer ace
if dealerHand[0].value == 'A':
    print('fuckin dealer ace bud')
    for i in range(players):
        insur = input('Player '+playerList[i].name+' insurance? (y or n): ')
        if insur == 'y':
            playerList[i].action = 'i'
        insur = ''
# test for dealer blackjack
if dealerHand[0].numbermax == 21:
    print('Dealer blackjack')
    for i in range(players):
        if playerList[i].action == 'i':
            print('Player '+playerList[i].name+' had insurance')
    gameStatus = 'over'
# pay out blackjacks if dealer doesn't have one
for i in range(players):
    if playerList[i].action == 'b':
        print('Player '+playerList[i].name+' wins 3:2')
# test for splits
areThereSplits = ''
splitPlayers = []
splitHands1 = []
splitHands2 = []
split = ''
splitCount = 0
while areThereSplits != 'n':
    for i in range(len(playerList)):
        if len(playerList[i].hand) > 1:
            if playerList[i].hand[0].number == playerList[i].hand[1].number:
                split = input('Player '+playerList[i].name+' split hand? (y or n): ')
                if split == 'y':
                    areThereSplits = 'y'
                    tempHand = playerList[i].hand
                    splitPlayers.append(i)
                    # create single card hands
                    hand1 = [playerList[i].hand[0]]
                    hand2 = [playerList[i].hand[1]]
                    print(Player(hand1,0,'',''))
                    splitHands1.append(Player(hand1,0,'',''))
                    splitHands2.append(Player(hand2,0,'',''))
                    splitCount = splitCount + 1
            if splitCount == 0:
                areThereSplits = 'n'
    if split == 'y' and areThereSplits != 'n':
        splitPlayers.reverse()
        print(splitPlayers)
        print(playerList)
        print('here')
        for i in splitPlayers:
            playerList.pop(i)
        splitPlayers.reverse()
        for i in range(len(splitPlayers)):
            playerList.insert(i,splitHands1[i])
            playerList.insert(i+1,splitHands2[i])
            print(playerList)
            playerList[i].name = str(splitPlayers[i]+1)+'s'
            playerList[i+1].name = str(splitPlayers[i]+1)+'s'
        # sort list
        playerList.sort(key=operator.attrgetter('name'))
        print('playerlist:')
        print(playerList)
        for i in range(len(playerList)):
            print('Player '+playerList[i].name+':')
            PrintPlayerHand(playerList[i].hand)
    print(splitCount)
    print(areThereSplits)
    # deal new cards to those with splits
    for i in range(len(playerList)):
        if len(playerList[i].hand) < 2:
            playerList[i].hand.append(deck.pop())
    if areThereSplits != 'n':
        for i in range(len(playerList)):
            print('Player '+playerList[i].name+':')
            PrintPlayerHand(playerList[i].hand)
# check for new splits
    splitCount = 0
    for i in range(len(playerList)):
        if playerList[i].hand[0].number == playerList[i].hand[1].number:
            areThereSplits = 'y'
            splitCount = splitCount + 1
            print('yo theres a new split')
        if splitCount == 0:
            areThereSplits = 'n'


# go to each player in turn and ask hit/stand (double) until done
# reveal dealer hand
# hit dealer hand until done
# mark winners/losers



# insur = ''
# # test if dealer is showing an ace
# if dealerHand[0].value == 'A':
#     if bj == 0:
#         print('fuckin dealer ace bud')
#         insur = input('insurance? (y or n): ')
#     if dealerHand[1].number == 10:
#         print('Dealer Blackjack')
#         hitOrStand = 's'
#     else:
#         print('No Dealer Blackjack')
#
# while hitOrStand != 's':
#     # double down condition
#     if len(playerHand) == 2:
#         hitOrStand = input('(h)it or (s)tand or (d)ouble?: ')
#         if hitOrStand == 'h':
#             playerHand.append(deck.pop(0))
#             PrintDealerHand(dealerHand)
#             PrintPlayerHand(playerHand)
#         if hitOrStand == 'd':
#             print('Double Down')
#             playerHand.append(deck.pop(0))
#             PrintDealerHand(dealerHand)
#             PrintPlayerHand(playerHand)
#             hitOrStand = 's'
#     elif sum(c.number for c in playerHand) >= 21:
#         break
#     else:
#         hitOrStand = input("(h)it or (s)tand?: ")
#         if hitOrStand == 'h':
#             playerHand.append(deck.pop(0))
#             PrintDealerHand(dealerHand)
#             PrintPlayerHand(playerHand)
#             print(' ')
# print('Player Stands')
# print('')
# PrintDealerFullHand(dealerHand)
# PrintPlayerHand(playerHand)
# # dealer hits soft 17
# dealerAction = ''
#
# while dealerAction != 's' and dealerAction != 'b':
#     if sum(c.number for c in dealerHand) > 21:
#         dealerAction = 'b'
#     # hard 16 or less:
#     if (sum(c.number for c in dealerHand) < 17) and ('A' not in [c.value for c in dealerHand]):
#         dealerAction = 'h'
#     # soft 17 or less:
#     elif ('A' in [c.value for c in dealerHand]) and sum(c.numbermax for c in dealerHand) <= 17:
#         dealerAction = 'h'
#     # hard 17 to 21:
#     elif (17 <= sum(c.number for c in dealerHand)) and (sum(c.number for c in dealerHand) <= 21) and ('A' not in [c.value for c in dealerHand]):
#         dealerAction = 's'
#     # soft 18 to 21:
#     elif (17 <= sum(c.numbermax for c in dealerHand)) and (sum(c.numbermax for c in dealerHand) <= 21) and ('A' in [c.value for c in dealerHand]):
#         dealerAction = 's'
#
#     if dealerAction == 'h':
#         dealerHand.append(deck.pop(0))
#         print('Dealer hits')
#         PrintDealerFullHand(dealerHand)
#         PrintPlayerHand(playerHand)
#     if dealerAction == 's':
#         print('Dealer stands')
#
# # determine number value of standing hand:
#
# #print(finalTotal(dealerHand))
# #print(finalTotal(playerHand))
# if finalTotal(playerHand) == 0:
#     print('Dealer wins')
# elif finalTotal(dealerHand) > finalTotal(playerHand):
#     print('Dealer wins')
# elif finalTotal(playerHand) > finalTotal(dealerHand):
#     print('Player wins')
# elif finalTotal(dealerHand) == finalTotal(playerHand):
#    print('Push')