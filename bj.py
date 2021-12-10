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
        self.softTotal = 0
        self.hardTotal = 0
        self.bestTotal = 0
        self.action = ''

class Player:
    def __init__(self, name, bankroll, wins, losses):
        self.name = name
        self.bankroll = bankroll
        self.wins = wins
        self.losses = losses

suits = ['\u2665','\u2663','\u2660','\u25C6']
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

deck = [Card(value, suit) for value in values for suit in suits]

