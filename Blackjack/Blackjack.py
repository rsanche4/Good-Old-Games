import random
import time
import sys

def main():
    deck_hearts = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    deck_diamonds = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    deck_spades = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    deck_clubs = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    deck = [deck_hearts, deck_diamonds, deck_spades, deck_clubs]
    game(deck)

def game(deck):
    print("Starting Blackjack...")
    time.sleep(3)
    deal(deck)

def deal(deck):
    player_hand = [draw_card(deck), draw_card(deck)]
    print("Your cards: ")
    print(player_hand)
    time.sleep(3)
    dealer_hand = ['X', draw_card(deck)]
    print("The Dealer: ")
    print(dealer_hand)
    time.sleep(3)
    turn(deck, player_hand, dealer_hand)
    
def turn(deck, player_hand, dealer_hand):   
    player_choice = input("Would you like to HIT or STAND? Type H or S: ")
    if player_choice == 'H' or player_choice == 'h':
        player_hand = player_hand + [draw_card(deck)]
        print("Your new hand is: ")
        time.sleep(3)
        print(player_hand)
        still_playing = check_21(player_hand)
        if still_playing:
            turn(deck, player_hand, dealer_hand)
        else:
            time.sleep(3)
            print("Oh no! You went above 21.")
            lose()
    elif player_choice == 'S' or player_choice == 's':
        dealer_hand[0] = draw_card(deck)
        dealer_turn(deck, player_hand, dealer_hand)
    else:
        print("You did not type a correct input.")
        turn(deck, player_hand, dealer_hand)

            
def dealer_turn(deck, player_hand, dealer_hand):
    time.sleep(3)
    print("The Dealer: ")
    print(dealer_hand)
    dealer_below_16 = check_16(dealer_hand)
    if dealer_below_16:
        dealer_hand = dealer_hand + [draw_card(deck)]
        dealer_turn(deck, player_hand, dealer_hand)
    else:
        compare_player_dealer(player_hand, dealer_hand)


def check_21(player_hand):
    addit = 0
    new_addit = 0
    there_is_A = 0
    for i in range(0, len(player_hand)):
        if player_hand[i] == 'K' or player_hand[i] == 'Q' or player_hand[i] == 'J':
            addit += 10
        elif player_hand[i] == 'A':
            there_is_A += 1
            continue   
        else:
            addit += player_hand[i]
    while there_is_A != 0:
        new_addit = addit
        new_addit += 11
        if new_addit > 21:
            addit += 1
        else:
            addit += 11
        there_is_A -= 1
    if addit <= 21:
        return True 

def check_16(dealer_hand):
    addit = 0
    new_addit = 0
    there_is_A = 0
    for i in range(0, len(dealer_hand)):
        if dealer_hand[i] == 'K' or dealer_hand[i] == 'Q' or dealer_hand[i] == 'J':
            addit += 10
        elif dealer_hand[i] == 'A':
            there_is_A += 1
            continue   
        else:
            addit += dealer_hand[i]
    while there_is_A != 0:
        new_addit = addit
        new_addit += 11
        if new_addit > 21:
            addit += 1
        else:
            addit += 11
        there_is_A -= 1
    if addit <= 16:
        return True 

def compare_player_dealer(player_hand, dealer_hand):
    addit = 0
    new_addit = 0
    player_addit = 0
    newplayer_addit = 0
    there_is_A_dealer = 0
    there_is_A_player = 0
    for i in range(0, len(dealer_hand)):
        if dealer_hand[i] == 'K' or dealer_hand[i] == 'Q' or dealer_hand[i] == 'J':
            addit += 10
        elif dealer_hand[i] == 'A':
            there_is_A_dealer += 1
            continue   
        else:
            addit += dealer_hand[i]
    while there_is_A_dealer != 0:
        new_addit = addit
        new_addit += 11
        if new_addit > 21:
            addit += 1
        else:
            addit += 11
        there_is_A_dealer -= 1

    for i in range(0, len(player_hand)):
        if player_hand[i] == 'K' or player_hand[i] == 'Q' or player_hand[i] == 'J':
            player_addit += 10
        elif player_hand[i] == 'A':
            there_is_A_player += 1
            continue   
        else:
            player_addit += player_hand[i]
    while there_is_A_player != 0:
        newplayer_addit = player_addit
        newplayer_addit += 11
        if newplayer_addit > 21:
            player_addit += 1
        else:
            player_addit += 11
        there_is_A_player -= 1

    if addit > 21 and player_addit <= 21:
        win()
    elif addit <= 21 and player_addit > 21:
        lose()
    elif addit <= 21 and player_addit <= 21:
        dealer_score = 21 - addit
        player_score = 21 - player_addit
        if dealer_score < player_score:
            lose()
        elif dealer_score == player_score:
            tie()
        else:
            win()
    else:
        lose()

def lose():
    print("You lost!")
    play_again()

def win():
    print("You won!")
    play_again()

def tie():
    print("There was a tie!")
    play_again()

def draw_card(deck):
    random_deck = random.randint(0, 3)
    random_card = random.randint(0, 12)
    return deck[random_deck][random_card]

def play_again():
    res = input("Would you like to play again? Press Y if yes, or N if no: ")
    if res == 'Y' or res == 'y':
        main()
    elif res == 'N' or res == 'n':
        print("Ok! Come back anytime.")
        time.sleep(3)
        sys.exit()
    else:
        print("You typed an incorrect input. Please try again.")
        play_again()
    

if __name__ == '__main__':
    main()
