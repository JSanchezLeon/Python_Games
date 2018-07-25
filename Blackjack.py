# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
Busted = False



# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):

        self.hand = []

    def __str__(self):
        ans = ''
        for i in range(len(self.hand)):
            ans += str(self.hand[i])

        return 'Hand contains ' + ans

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        hand_value = 0
        for i in range(len(self.hand)):
            hand_value += VALUES[self.hand[i].rank]
        for j in range(len(self.hand)):
            if self.hand[i].rank != 'A':
                return hand_value
            else:
                if (hand_value + 10) <= 21:
                    return hand_value + 10
                else:
                    return hand_value
        if hand_value == 0:
            return 0

    def draw(self, canvas, pos):

        for i in range(len(self.hand)):
            self.hand[i].draw(canvas, pos)
            pos[0] += 100








# define deck class
class Deck:
    def __init__(self):
        deck = []
        self.deck = deck
        for i in SUITS:
            for j in RANKS:
                card = Card(i , j)
                deck.append(card)


    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
            c1 = random.choice(self.deck)
            self.deck.remove(c1)
            return c1

    def __str__(self):
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i])

        return "Deck contains " + str(ans)



#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, Dealer_hand, game_deck, Busted,score
    game_deck = Deck()
    game_deck.shuffle()
    #player
    player_hand = Hand()
    player_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    #dealer
    Dealer_hand = Hand()
    Dealer_hand.add_card(game_deck.deal_card())
    Dealer_hand.add_card(game_deck.deal_card())
    #GlobalVariableUpdates
    outcome = ""
    Busted = False

    if in_play == False:
        in_play = True
    else:
        score -= 1


def hit():
    global player_hand, in_play, game_deck, Busted, outcome, score
    if in_play == True:
        if player_hand.get_value() <= 21:
            player_hand.add_card(game_deck.deal_card())

            if player_hand.get_value() > 21:
                Busted = True
                score -= 1
                outcome = 'You have busted'
                in_play = False






def stand():
    global  Dealer_hand, player_hand, in_play, game_deck, Busted, outcome, score
    if in_play == True:
        if Busted == True:
            outcome = 'You Booosted!'
        elif Busted == False:
            while Dealer_hand.get_value() <= 17:
                   Dealer_hand.add_card(game_deck.deal_card())

            if Dealer_hand.get_value() > 21:
                outcome = 'Dealer busted'
                score += 1
                in_play = False

            else:
                #value of hands
                if player_hand.get_value() < Dealer_hand.get_value():
                    outcome = "Dealer wins"
                    score -= 1
                    in_play = False
                else:
                    outcome = "Player wins"
                    score += 1
                    in_play = False



    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score


def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, Dealer_hand, outcome, in_play, score
    canvas.draw_text('Blackjack', [370, 50], 50, 'Yellow', 'serif')
    canvas.draw_text('Dealer Hand', [100, 190], 20, "Black")
    canvas.draw_text('Player Hand', [100, 390], 20, 'Black')
    canvas.draw_text(outcome, [370, 150], 30, 'White')
    canvas.draw_text('score is: ' + str(score), [370, 75], 20, 'White')
    player_hand.draw(canvas, [100, 400])

    if in_play == True:
        canvas.draw_text('Hit or Stand?', [150, 350], 25, 'White')
        Dealer_hand.draw(canvas, [100, 200])
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,[100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

    else:
        canvas.draw_text('New Deal?', [150, 350], 25, 'White')
        Dealer_hand.draw(canvas, [100, 200])




# initialization frame
frame = simplegui.create_frame("", 800, 800)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
