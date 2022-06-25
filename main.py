# Blackjack House Rules:
#
# The deck is unlimited in size.
# There are no jokers.
# The Jack/Queen/King all count as 10.
# The the Ace can count as 11 or 1.
# Cards are not removed from the deck as they are drawn.
# http://listmoz.com/view/6h34DJpvJBFVRlZfJvxF

import random
import os
import time
import msvcrt  # Windows OS only
from gfx import *
DECKS = {
    'ace': 11,
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'j': 10, 'q': 10, 'k': 10
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    print('Press any key to continue . . .', end='', flush=True)
    msvcrt.getch()


def get_input_char(valid_chars: set):
    user_input = ''
    while user_input not in valid_chars:
        user_input = msvcrt.getwch().lower()

    return user_input


def draw_card(player):
    key = random.choice(list(DECKS.keys()))
    player['cards'].append(key)
    player['scores'] += DECKS[key]

    # Adjust ace value
    if player['scores'] > 21 and 'ace' in player['cards']:
        player['scores'] -= 10
        ace_pos = player['cards'].index('ace')
        player['cards'][ace_pos] = 'ace_'


def display_cards(cards):
    cards_list = [cards_art[card].split('\n') for card in cards]
    for j in range(len(cards_list[0])):
        print(' '.join(card[j] for card in cards_list))


def screen_display(player_cards, dealer_cards, show_cards=True):
    clear()
    print(logo)

    print("\033[35mDealer's hand:")
    if show_cards:
        display_cards(dealer_cards)
    else:
        display_cards([dealer_cards[0], '0'])

    print("\033[94m\nPlayer's hand:")
    display_cards(player_cards)

    print('\033[0m', end='')


def game_over(is_win=False, is_draw=False):
    if is_draw:
        print(f'\033[38;2;{255};{160};{122}m{draw_text}\033[0m')

    else:
        if is_win:
            print(f'\033[38;2;{255};{215};{0}m{win_text}\033[0m')
        else:
            print(f'\033[38;2;{102};{51};{0}m{lose_text}\033[0m')

    pause()


def compare_scores(player_scores, dealer_scores):
    # Blackjack
    if dealer_scores == 0:
        game_over(False)
    elif player_scores == 0:
        game_over(True)

    elif dealer_scores > 21:
        game_over(True)
    elif player_scores > 21 or dealer_scores > player_scores:
        game_over(False)
    elif dealer_scores < player_scores:
        game_over(True)

    # Draw
    else:
        game_over(is_draw=True)


def play_game():
    player = {'cards': [], 'scores': 0}
    dealer = {'cards': [], 'scores': 0}

    # Each person draws two cards at the beginning
    for _ in range(2):
        draw_card(player)
        draw_card(dealer)

    # Blackjack
    if dealer['scores'] == 21:
        dealer['scores'] = 0
    elif player['scores'] == 21:
        player['scores'] = 0

    else:
        dealer_turn = False

        while True:
            screen_display(player['cards'], dealer['cards'], dealer_turn)
            # For testing
            # print("Dealer's scores:", dealer['scores'])
            # print("Player's scores:", player['scores'])

            if not dealer_turn:
                print('\n1. Hit (draw a card)\n2. Stand (end turn)\n0. Surrender')
                print('Choose an action: ', end='', flush=True)

                # Avoid invalid input
                action = get_input_char({'0', '1', '2'})

                if action == '1':
                    draw_card(player)
                    if player['scores'] > 21:
                        break
                    elif player['scores'] == 21:
                        dealer_turn = True

                elif action == '2':
                    dealer_turn = True

                elif action == '0':
                    player['scores'] = 100
                    break

            elif dealer['scores'] < 17:
                # The dealer keep drawing cards until going over 16 scores.
                draw_card(dealer)
                time.sleep(1)

            else:
                break

    screen_display(player['cards'], dealer['cards'], True)
    # Compare player's and dealer's scores
    compare_scores(player['scores'], dealer['scores'])


if __name__ == '__main__':
    while True:
        play_game()

        clear()
        print(logo)
        print('Do you want to continue?')
        print("Type \033[32my\033[0m or \033[31mn\033[0m: ", end='', flush=True)

        choice = get_input_char({'y', 'n'})
        if choice == 'n':
            break
