import random
import os
from assets import cards, values, colours

colourString = ""
for i in range(len(colours)):
    colourString += f"{i+1}={colours[i]}   "

info = {
    "human": [[], [], 1000, 0, 0, 0, 0, "", ""],
    "computer": [[], [], 400, "", ""],
}


def clear():
    """Clears the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def repeat():
    """Checks players' balances and if possible, asks user if they want to play another round."""
    # print("Rounds won: {0}. Rounds tied: {1}. Rounds lost: {2}".
    #       format(info["human"][3],info["human"][4],info["human"][5]))
    
    if info["human"][2] <= 0:
        print("\n💀  You've run out of money! Game over. 💀\n")
        print("Rounds won: {0}. Rounds tied: {1}. Rounds lost: {2}\n".
              format(info["human"][3], info["human"][4], info["human"][5]))
    elif info["computer"][2] <= 0:
        print("\n💰  The computer has run out of money, congratulations! 💰\n")
        print("Rounds won: {0}. Rounds tied: {1}. Rounds lost: {2}\n".
              format(info["human"][3], info["human"][4], info["human"][5]))
    else:
        print("\nYour new balance is £{0}. Computer has £{1}.\n".
              format(info["human"][2], info["computer"][2]))
        response = input("Press [Enter] to play again. Type anything else to quit.\n > ")
        if len(response) == 0:
            blackjack()
        else:
            clear()
            print("Thanks for playing!\n")


def card_picker(player):
    """Generates a new card for a given player and appends it to their card/value lists"""
    index = random.randint(0, 12)  # change this to 12
    info[player][0].append(cards[index])
    info[player][1].append(values[index])
    if sum(info[player][1]) > 21:
        if 11 in info[player][1]:
            info[player][1][info[player][1].index(11)] = 1
        else:
            return "end"
    if sum(info[player][1]) == 21:
        return "end"
    else:
        return "continue"


def colour_picker():
    while True:
        colour_index = input("\n{0}\n\nChoose your player colour:\n > ".format(colourString))
        try:
            colour_index = int(colour_index)-1
            if colour_index in range(len(colours)):
                info["human"][7] = colours[colour_index]
                if colour_index == 0 or colour_index == 4:
                    info["human"][8] = " "
                    print("Human triggered")
                while True:
                    info["computer"][3] = random.choice(colours)
                    if info["computer"][3] != info["human"][7]:
                        if colours.index(info["computer"][3]) == 0 or colours.index(info["computer"][3]) == 4:
                            info["computer"][4] = " "
                            print("Computer triggered")
                        break
                break
            else:
                clear()
                print("Invalid entry. Please try again...")
        except:
            clear()
            print("Invalid entry. Please try again...")


def balance_setter():
    while True:
        balance = input("\nSet a starting balance:\n > £")
        try:
            balance = int(balance)
        except:
            print("Invalid amount - please try again...")
            continue
        if balance > 0:
            info["human"][2] = balance
            info["computer"][2] = 4*balance
            break


def setup():
    """Resets player cards and generates two new cards for each player"""
    clear()   
    for player in ["human", "computer"]:
        for i in range(2):
            info[player][i] = []
        for _ in range(2):
            card_picker(player)


def bet():
    """Returns a bet amount from the user"""
    while True:
        bet = input("You have £{0}. Computer has £{1}.\n\nPlace your bet:\n > £".
                    format(info["human"][2], info["computer"][2]))
        try:
            bet = int(bet)
        except:
            clear()
            print("Invalid bet, please enter a whole amount up to £{0}...\n".
                  format(min(info["human"][2], info["computer"][2])))
            continue
        if bet in range(1, min(info["human"][2], info["computer"][2])+1):
            return bet
        else:
            clear()
            print("Your bet must be between £1 and £{0}!\n".
                  format(min(info["human"][2], info["computer"][2])))


def blackjack():
    """Starts game and runs until user has completed their hand"""
    setup()
    info["human"][6] = bet()
    
    if sum(info["human"][1]) == 21:
        results(True)
    
    while True:
        clear()

        if sum(info["human"][1]) >= 21:
            break

        print("{0}  Your score = {1}\t{2}{3}".
              format(info["human"][7], sum(info["human"][1]), info["human"][8], " ".join(info["human"][0])))
        print("{0}  AI's score = ??\t{2}{1}".
              format(info["computer"][3], info["computer"][0][0], info["computer"][4]))

        while True:
            new_card = input("\nType 'y' to draw another card, type 'n' to pass:\n > ").lower()
            if new_card not in ["y", "n"]:
                print("\nInvalid response, please try again...")
            else:
                break
        
        if new_card == "n":
            break
        elif card_picker("human") == "end":
            break

    results(False)


def results(blackjack_outcome):
    """Compares user's hand against computer's and determines outcome"""
    clear()

    print("{0}  Your score = {1}\t{2}{3}".
          format(info["human"][7], sum(info["human"][1]), info["human"][8], " ".
                 join(info["human"][0])))

    if sum(info["human"][1]) > 21:
        print("{0}  AI's score = {1}\t{2}{3}".
              format(info["computer"][3], sum(info["computer"][1]), info["computer"][4], " ".
                     join(info["computer"][0])))
        print("\n❌  You lost £{0} - you went over 21!\n".format(info["human"][6]))
        info["human"][2] -= info["human"][6]
        info["computer"][2] += info["human"][6]
        info["human"][5] += 1

    else:
        while sum(info["computer"][1]) < 17 and sum(info["computer"][1]) != 21:
            if card_picker("computer") == "end":
                break

        print("{0}  AI's score = {1}\t{2}{3}".
              format(info["computer"][3], sum(info["computer"][1]), info["computer"][4], " ".
                     join(info["computer"][0])))

        if blackjack_outcome:
            if sum(info["computer"][1]) == 21:
                print("\nIt's a draw!\n")
                info["human"][4] += 1
            else:
                print("\n✅  You won £{0} - BLACKJACK!\n".format(2*info["human"][6]))
                info["human"][2] += 2*info["human"][6]
                info["computer"][2] -= 2*info["human"][6]
                info["human"][3] += 1

        elif sum(info["computer"][1]) > 21:
            print("\n✅  You won £{0} - computer went over 21!\n".format(info["human"][6]))
            info["human"][2] += info["human"][6]
            info["computer"][2] -= info["human"][6]
            info["human"][3] += 1

        elif sum(info["computer"][1]) > sum(info["human"][1]):
            print("\n❌  You lost £{0} - computer scored higher!\n".format(info["human"][6]))
            info["human"][2] -= info["human"][6]
            info["computer"][2] += info["human"][6]
            info["human"][5] += 1

        elif sum(info["computer"][1]) == sum(info["human"][1]):
            print("\nIt's a draw!\n")
            info["human"][4] += 1

        elif sum(info["computer"][1]) < sum(info["human"][1]):
            print("\n✅  You won £{0} - you scored higher!\n".format(info["human"][6]))
            info["human"][2] += info["human"][6]
            info["computer"][2] -= info["human"][6]
            info["human"][3] += 1
    
    repeat()


clear()
input("Welcome to Blackjack! Press [Enter] to start...")
clear()
# balance_setter()  # <- enable this to set your own starting balance
print("You have £{0}, computer has £{1}. Win by bankrupting the computer.".
      format(info["human"][2], info["computer"][2]))
colour_picker()
blackjack()
