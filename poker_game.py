import poker_functions
import hand_organization
import bot_functions

####################################### Base Game ######################################
def greet_player() -> None:
    '''
    Display rules for game
    '''
    print('Welcome to the Poker Championship')
    print('=================================\n')
    for point in range(8,0, -1):
        print('{:>2}:{:>17}'.format(point, poker_functions.get_hand_type(point)))

    print('\n*** King is the Highest Rank ***')
    print('================================')
    input('press enter to continue...')
    print('--------------------------------')

def start_new_game() -> list:
    '''
    Create a new deck and shuffle. Deal 2 hands

    Returns:
        hands: a list of each player hands
    '''

    poker_functions.create_deck()
    poker_functions.shuffle()

    hands = poker_functions.deal_hands(2)
    return hands

###################################### Modify Hand ########################################
def modify_hand(card_list:list) -> dict:
    '''
    Deal card list back up to 5 cards

    Parameters:
        card_list: list of cards remaining in hand

    Return:
        modify_hand: a dictionary of cards sorted by suit
    '''
    while len(card_list) < 5:
        card_list.append(poker_functions.deal())
    
    
    hand = hand_organization.create_hand_dict(card_list)

    return hand

def modify_player_hand(player_hand:dict) -> dict:
    '''
    Display hand to user, take input from user, discard cards from hand

    Parameters:
        player_hand: a dictionary of cards sorted by suit

    Return:
        modify_hand: a dictionary of cards sorted by suit
    '''
    print('Your Hand:')
    poker_functions.print_hand(player_hand)

    print('invalid input will result in no replacement')
    replacement_string = input('what Card(s) would you like to keep Ex.351: ')

    keep_list = list()
    card_list = hand_organization.organize_hand(player_hand)
    for i, card in enumerate(card_list):
        if str(i + 1) in replacement_string:
            keep_list.append(card)

    return modify_hand(keep_list)


def modify_bot_hand(bot_hand:dict) -> dict:
    '''
    Parameters:
        bot_hand: a dictionary of cards sorted by suit

    Returns:
        modify_hand a dictionary of cards sorted by suit
    '''

    keep_list = bot_functions.calculate_keep(bot_hand)

    return modify_hand(keep_list)
    


if __name__ == "__main__":
    greet_player()

    repeat_string = 'y'

    while repeat_string == 'y':
        hands        = start_new_game()

        player_hand  = hands[0]
        bot_hand     = hands[1]

        player_hand  = modify_player_hand(player_hand)
        bot_hand     = modify_bot_hand(bot_hand)

        winner       = poker_functions.compare_hands(player_hand, bot_hand)

        repeat_string = input('Would you like to play again (y/n):').lower()


