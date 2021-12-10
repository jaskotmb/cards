import random

class Card:
    def __init__(self, value, suit, number, numbermax):
        self.value = value
        self.suit = suit
        numDict = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
        num2Dict = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
        self.number = numDict[value]
        self.numbermax = num2Dict[value]

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
    if sum(c.number for c in hand) <= 21:
        if hand[0].value != 'A' and hand[1].value != 'A':
            print("Player: ",[h.value + ' ' + h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),sep='')
        elif hand[0].value == 'A' or hand[1].value == 'A':
            print("Player: ",[h.value + ' '+ h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),' or ',sum(c.number for c in hand) + 10,sep='')
    else:
        print("Player: ",[h.value + ' ' + h.suit for h in hand],' ','Total: ',sum(c.number for c in hand),' Player busts!',sep='')

def DealPlayerHand(shoe):
    player1 = shoe.pop(0)
    player2 = shoe.pop(0)
    return [player1, player2]


random.shuffle(deck)
# inital dealer hand
dealerHand = DealerHand(deck)
PrintDealerHand(dealerHand)
# initial player hand
playerHand = DealPlayerHand(deck)
PrintPlayerHand(playerHand)
bj = 0
# test if player has blackjack
if sum(c.numbermax for c in playerHand) == 21:
    print('Player Blackjack!')
    bj = 1

hitOrStand = ''
insur = ''
# test if dealer is showing an ace
if dealerHand[0].value == 'A':
    if bj == 0:
        print('fuckin dealer ace bud')
        insur = input('insurance? (y or n): ')
    if dealerHand[1].number == 10:
        print('Dealer Blackjack')
        hitOrStand = 's'
    else:
        print('No Dealer Blackjack')

while hitOrStand != 's':
    # double down condition
    if len(playerHand) == 2:
        hitOrStand = input('(h)it or (s)tand or (d)ouble?: ')
        if hitOrStand == 'h':
            playerHand.append(deck.pop(0))
            PrintDealerHand(dealerHand)
            PrintPlayerHand(playerHand)
        if hitOrStand == 'd':
            print('Double Down')
            playerHand.append(deck.pop(0))
            PrintDealerHand(dealerHand)
            PrintPlayerHand(playerHand)
            hitOrStand = 's'
    elif sum(c.number for c in playerHand) >= 21:
        break
    else:
        hitOrStand = input("(h)it or (s)tand?: ")
        if hitOrStand == 'h':
            playerHand.append(deck.pop(0))
            PrintDealerHand(dealerHand)
            PrintPlayerHand(playerHand)
            print(' ')
print('Player Stands')
print('')
PrintDealerFullHand(dealerHand)
PrintPlayerHand(playerHand)
# dealer hits soft 17
dealerAction = ''

while dealerAction != 's' and dealerAction != 'b':
    if sum(c.number for c in dealerHand) > 21:
        dealerAction = 'b'
    # hard 16 or less:
    if (sum(c.number for c in dealerHand) < 17) and ('A' not in [c.value for c in dealerHand]):
        dealerAction = 'h'
    # soft 17 or less:
    elif ('A' in [c.value for c in dealerHand]) and sum(c.numbermax for c in dealerHand) <= 17:
        dealerAction = 'h'
    # hard 17 to 21:
    elif (17 <= sum(c.number for c in dealerHand)) and (sum(c.number for c in dealerHand) <= 21) and ('A' not in [c.value for c in dealerHand]):
        dealerAction = 's'
    # soft 18 to 21:
    elif (17 <= sum(c.numbermax for c in dealerHand)) and (sum(c.numbermax for c in dealerHand) <= 21) and ('A' in [c.value for c in dealerHand]):
        dealerAction = 's'

    if dealerAction == 'h':
        dealerHand.append(deck.pop(0))
        print('Dealer hits')
        PrintDealerFullHand(dealerHand)
        PrintPlayerHand(playerHand)
    if dealerAction == 's':
        print('Dealer stands')

# determine number value of standing hand:
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

#print(finalTotal(dealerHand))
#print(finalTotal(playerHand))
if finalTotal(dealerHand) > finalTotal(playerHand):
    print('Dealer wins')
elif finalTotal(playerHand) > finalTotal(dealerHand):
    print('Player wins')
elif finalTotal(dealerHand) == finalTotal(playerHand):
    print('Push')