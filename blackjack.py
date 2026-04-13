import random
import os

def clear_terminal():
    os.system("clear")

#cards
DECK = ["A","A","A","A","K","K","K","K","Q","Q","Q","Q","J","J","J","J",10,10,10,10,9,9,9,9,8,8,8,8,7,7,7,7,6,6,6,6,5,5,5,5,4,4,4,4,3,3,3,3,2,2,2,2]
PICTURES = ["K","Q","J"]
DEALER_NAME = "Dealer"
PLAYER_NAME = "Player"

#shuffle
def shuffle():
    cards = DECK.copy()
    random.shuffle(cards)
    return cards

#deal
def deal_card(person,person_name,cards):
    card = cards.pop(0)
    print(f"{person_name} draws {card}")
    person.append(card)
    return person,cards

#point eval
def eval_points(person,person_name):
    person_points = 0
    aces = 0
    for card in person:
        if card in PICTURES:
            person_points += 10
        elif card == "A":
            person_points += 11
            aces += 1
        else:
            person_points += card
    while person_points > 21 and aces:
        person_points -= 10
        aces -= 1
    print(f"{person_name}s current points: {person_points}")
    return person_points

#final point eval
def final_eval_points(person):
    person_points = 0
    aces = 0
    for card in person:
        if card in PICTURES:
            person_points += 10
        elif card == "A":
            person_points += 11
            aces += 1
        else:
            person_points += card
    while person_points > 21 and aces:
        person_points -= 10
        aces -= 1
    return person_points

#blackjack
def blackjack_check(player_points):
    if player_points == 21:
        print("BLACKJACK!")
        blackjack = True
    else:
        blackjack = False
    return blackjack

#bustcheck
def bust_check(person_name, person_points):
    if person_points > 21:
        bust = True
        print(f"{person_name} busted!")
    else:
        bust = False
    return bust
    
#first choice
def first_choice(player,player_points,cards):
    choice = ""
    while choice != "h" and choice != "s" and choice != "d":
        choice = input("Hit (h), Stand (s), or Double down (d)? ")
    if choice == "h":
        player,cards = deal_card(player,PLAYER_NAME,cards)
        player_points = eval_points(player,PLAYER_NAME)
        bust = bust_check(PLAYER_NAME,player_points)
    elif choice == "d":
        player,cards = deal_card(player,PLAYER_NAME,cards)
        print("You doubled down.")
        player_points = eval_points(player,PLAYER_NAME)
        bust = bust_check(PLAYER_NAME,player_points)
    else: 
        print(f"You stand with {player_points} points")
        bust = False
    return bust,choice,player_points

#player choices
def choices(player,player_points,cards):
    choice = ""
    while choice != "s" and choice != "h":
        choice = input("Hit (h) or Stand (s)? ")
    if choice == "h":
        player,cards = deal_card(player,PLAYER_NAME,cards)
        player_points = eval_points(player,PLAYER_NAME)
        bust = bust_check(PLAYER_NAME,player_points)
    else: 
        print(f"You stand with {player_points} points")
        bust = False
    return bust,choice,player_points

#dealer's turn
def dealers_turn(dealer,cards):
    dealer_points = eval_points(dealer,DEALER_NAME)
    while dealer_points < 17:
        dealer,cards = deal_card(dealer,DEALER_NAME,cards)
        dealer_points = eval_points(dealer,DEALER_NAME)
    bust = bust_check(DEALER_NAME,dealer_points)
    return bust
        
#bet
def bet(chips):
    while True:
        try:
            stakes = int(input("How much do you want to bet this round? "))
            if stakes > chips or stakes <= 0:
                stakes = int(input(f"You only have {chips} chips left. How much do you want to bet this round? "))
            else:
                return stakes
        except:
            print("Please enter a valid number.")

#winorlose
def determine_winner(dealer,player,chips,stakes):
    dealer_points = final_eval_points(dealer)
    player_points = final_eval_points(player)
    if dealer_points == player_points:
        print("It's a tie!")
    elif dealer_points > player_points:
        print(f"The dealer wins! {dealer_points} - {player_points}")
        chips -= stakes
    else:
        print(f"You win! {player_points} - {dealer_points}")
        chips += stakes
    return chips

def play_blackjack():
    clear_terminal()
    again = ""
    print("\n---------------------\nWelcome to the table!\n---------------------\n")
    while True:
        try:
            chips = int(input("How many chips do you want to play with? "))
            break
        except:
            print("Please enter a valid number.")
    while again != "n" and chips > 0:
        clear_terminal()
        print("---------------------\nLet's play blackjack!\n---------------------\n")
        #initial values
        dealer = []
        player = []
        player_points = 0
        cards = []
        cards = shuffle()

        #bet
        print(f"You currently have {chips} chips.")
        stakes = bet(chips)

        #first deal
        dealer,cards = deal_card(dealer,DEALER_NAME,cards)
        player,cards = deal_card(player,PLAYER_NAME,cards) 
        player,cards = deal_card(player,PLAYER_NAME,cards)
        player_points = eval_points(player,PLAYER_NAME)
        blackjack = blackjack_check(player_points)

        if blackjack == False:
            #choices
            bust,choice,player_points = first_choice(player,player_points,cards)
            if choice == "d":
                if bust == False:
                    #dealer's turn
                    bust = dealers_turn(dealer,cards)
                    if bust == False:
                        chips = determine_winner(dealer,player,chips,stakes)
                        chips = determine_winner(dealer,player,chips,stakes) # 2 times bc of double down
                    else:
                        chips += 2 * stakes
                        print("You win!")
                else:
                    chips -= 2 * stakes
                    print("You lost!")
            else:
                while choice == "h" and bust == False:
                    bust,choice,player_points = choices(player,player_points,cards)
                if bust == False:
                    #dealer's turn
                    bust = dealers_turn(dealer,cards)
                    if bust == False:
                        chips = determine_winner(dealer,player,chips,stakes)
                    else:
                        chips += stakes
                        print("You win!")
                else:
                    chips -= stakes
                    print("You lost!")
        else: 
            chips += (stakes * 2.5) 
            chips = int(round(chips))
        again = input("Wanna play again? (y/n) ")
    if again == "n":
        print(f"You leave the table with {chips} chips.")
        print("See you again soon!")
    else:
        print(f"You are broke. You have {chips} chips left. Leave the table now.")


play_blackjack()
