# implementation of card game - Memory

import simplegui
import random
CARD_DECK = range(0,8)*2
state = 0
exposed = [False] * 16
random.shuffle(CARD_DECK)

# helper function to initialize globals
def new_game():
    global state, exposed, CARD_DECK, turns
    random.shuffle(CARD_DECK)
    state = 0
    exposed = [False] * 16
    turns = 0
    label.set_text('Turns = ' + str(turns))


# define event handlers
def mouseclick(pos):
    global state, exposed, index1, index2, turns

    #States alternation for logical test
    if exposed[pos[0] // 50] == False:
        if state == 0:
            index1 = pos[0] // 50
            state = 1
        elif state == 1:
            index2 = pos[0] // 50
            state = 2
            turns += 1
        else:
            if CARD_DECK[index1] != CARD_DECK[index2]:
                exposed[index1] = False
                exposed[index2] = False
            state = 1
            index1 = pos[0] // 50
            label.set_text("Turns = "+ str(turns))

    exposed[pos[0] // 50] = True

# cards are logically 50x100 pixels in size
def draw(canvas):
    global exposed

    for card in range(len(CARD_DECK)):
        card_pos = 50 * card
        if exposed[card] == True:
            canvas.draw_text(str(CARD_DECK[card]),[13+card_pos,70], 50, 'White')

        else:
             canvas.draw_polygon([[card_pos, 0],[50+card_pos, 0], [50+card_pos, 100],
                                 [card_pos, 100]], 3, 'Red', 'Green')



# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()



# Always remember to review the grading rubric
