import FreeSimpleGUI as sg
import time


"""
=== SPACE ADVENTURE GAME ===

Basic project running a choose your own adventure game
GUI implementation using FreeSimpleGUI
"""


CHAR_DELAY = 0.020    # s between chars

sg.change_look_and_feel('Dark Blue 3')

# === TEXT POPUP ===

def slow_output_popup(text, choices):

    """'
    Displays pop up window with buttons for the players to click

    :param text: (str) Full text to display
    :param choices: (tuple[str]) Button labels
    :return: (str) the label of the button the player clicked
    """

    #defines content of window
    #FreeSimpleGUI breaks char-by-char updates when widget is diabled. Enabled fixes spacing issues
    #write only makes multiline behave like text output box
    #autoscroll makes sure the text scrolls properly, avoids formatting issues
    layout = [  [sg.Multiline(size=(60,18), key='-OUTPUT-', disabled=False, autoscroll=True, write_only=True, enable_events=True)],
                [sg.Button(choice) for choice in choices]  ]

    #makes window
    window = sg.Window('Space Game', layout, keep_on_top=True, finalize=True)

    output = window['-OUTPUT-']

    #print text into multiline box
    #text printed without spaces, instead of +c, replaced with end=""
    for c in text:
        output.print(c, end="")
        window.refresh()
        time.sleep(CHAR_DELAY)

    #after printing, wait for button click
           # user hasn't clicked anything yet so wait for something to happen
    event, values = window.read()
    window.close()
    return event


# === ROOMS ===
#Each room shows text and offers a binary choice (+quit button)
#Player goes into another room, or triggers an ending

def space_room():

    text = (
        "You walk into a room with a large window.\n"
        "You're in outer space!\n"
        "There's a door to your right, next to a big red button.\n\n"
        "How would you like to proceed?\n"
        "[1] Press the button\n"
        "[2] Walk through the door"
    )

    choice = slow_output_popup(text, ("1", "2", "Quit")) #button mapping

    if choice == "1":
        game_over("The escape hatch opens. You're sucked into space.")
    elif choice == "2":
        slow_output_popup("You walk through the door unharmed", ("Continue",))
        bear_room()
    else:
        game_over("You died of boredom in the room.")

def spaceship_room():

    text = (
        "You walk into the corridor of a spaceship.\n"
        "The computer scans for alien technology.\n"
        "It detects traces of an alien onboard.\n\n"
        "How would you like to proceed?\n"
        "[1] Follow the alien\n"
        "[2] Ignore the scan and wander around"
    )

    choice = slow_output_popup(text, ("1", "2", "Quit"))

    if choice == "1":
        alien_room()
    elif choice == "2":
        game_over("You wander aimlessly around the ship.")
    else:
        game_over("Make up your mind, man.")

def teleport_room():

    text = (
        "You walk into another room.\n"
        "On the floor is a large blue circular platform.\n"
        "Next to it is a door.\n\n"
        "How would you like to proceed?\n"
        "[1] Step onto the platform\n"
        "[2] Step through the door"
    )

    choice = slow_output_popup(text, ("1", "2", "Quit"))

    if choice == "1":
        slow_output_popup("The platform teleports you back to the start!", ("OK",))
        start_room()
    elif choice == "2":
        credits_room()
    else:
        game_over("You just stand there doing nothing.")

def bear_room():

    text = (
        "There's a bear in here.\n"
        "What's a bear doing on a spaceship?\n"
        "Behind the bear is another door.\n"
        "The bear is eating honey.\n\n"
        "How would you like to proceed?\n"
        "[1] Take the honey\n"
        "[2] Distract the bear"
    )

    choice = slow_output_popup(text, ("1", "2", "Quit"))

    if choice == "1":
        game_over("The bear eats you instead...")
    elif choice == "2":
        slow_output_popup("The bear moves out of the way.", ("OK",))
        teleport_room()
    else:
        game_over("1 or 2, man, just pick one.")

def alien_room():
    text = (
        "There's an alien in here.\n"
        "It's looking at you with a curious expression.\n\n"
        "How would you like to proceed?\n"
        "[1] Move towards the door\n"
        "[2] Attack the alien!"
    )

    choice = slow_output_popup(text, ("1", "2", "Quit"))

    if choice == "1":
        teleport_room()
    elif choice == "2":
        game_over("You're no match for an extraterrestrial.")
    else:
        game_over("I said press 1 or 2...")

def credits_room():


    text = (
        "You made it to the final room!\n"
        "It's full of intergalactic credits and treasure.\n\n"
        "How do you proceed?\n"
        "[1] Leave without taking anything\n"
        "[2] Take some money"
    )

    choice = slow_output_popup(text, ("1", "2", "Quit"))

    if choice == "1":
        won_game()
        return

    if choice == "2":
        amount = slow_output_popup(
            "How many credits do you take?",
            ("10", "20", "30", "40", "50", "75", "100")
        )

        try:
            credits_taken = int(amount)
        except:
            game_over("You hesitate too long and starve in the treasure room.")
            return

        if credits_taken < 50:
            slow_output_popup(
                "The aliens are annoyed, but let you pass anyway.",
                ("OK",)
            )
            won_game()
        else:
            game_over("You're a greedy bastard!")

def title_screen():
    """
    Title screen, start button. Appears once before game loop
    """
    layout = [
        [sg.Text("SPACE ADVENTURE", font=("Any", 24), justification="center")],
        [sg.Text("A tiny space adventure", font=("Any", 12), justification="center")],
        [sg.Button("Start"), sg.Button("Quit")]
    ]

    window = sg.Window("Welcome to Space Adventure!", layout, element_justification="center", keep_on_top=True)
    event, values = window.read()
    window.close()

    return event


#START ROOM
#left = space room, right = spaceship room

def start_room():
    text = (
        "You're in a dark room.\n"
        "There's a door to your LEFT and one to your RIGHT.\n\n"
        "Which door do you choose?"
    )

    choice = slow_output_popup(text, ("Left", "Right", "Quit"))

    if choice == "Left":
        space_room()
    elif choice == "Right":
        spaceship_room()
    else:
        game_over("Can't make up your mind?")

# === GAME ENDINGS ===

def game_over(cause_of_death):
    #message based on the room they're in when game ends
    slow_output_popup(cause_of_death + "\n\nYou suck at this game...", ("Ok",))

def won_game():
    #victory msg
    slow_output_popup(
        "You've made it out! Well done!\n"
        "Good luck finding a ride back to Earth.",
        ("OK",)
    )

#MAIN LOOP

#title screen once before loop, quits if you press quit (obviously)
choice = title_screen()
if choice != "Start":
    exit()

while True:
    start_room()
    again = slow_output_popup("Try again?", ("Yes", "No"))
    if again != "Yes":
        slow_output_popup("Thanks for playing!", ("Bye",))
        break

