import random

class Card:
    def __init__(self, value, suit, number, numbermax):
        self.value = value
        self.suit = suit
        numDict = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
        num2Dict = {'A':10,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
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

hitOrStand = ''
while hitOrStand != 's':
    if sum(c.number for c in playerHand) >= 21:
        break
    else:
        hitOrStand = input("(h)it or (s)tand?: ")
        if hitOrStand == 'h':
            playerHand.append(deck.pop(0))
            PrintDealerHand(dealerHand)
            PrintPlayerHand(playerHand)
print('Player Stands')
print('')
PrintDealerFullHand(dealerHand)
# dealer hits soft 17
while sum(c.number for c in dealerHand) < 17 and (sum(c.numbermax for c in dealerHand) <= 17):
    print('Dealer hits')
    dealerHand.append(deck.pop(0))
    PrintDealerFullHand(dealerHand)
    PrintPlayerHand(playerHand)
