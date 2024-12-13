import poker_functions
import hand_organization

############################### Bot Discard Strategy ###############################
def get_junk_index(hand:dict) -> int:
    '''
    Get the index of the first card after any points have been determined for hand

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        index: integer value of where the first card not associated with points lies
    '''
    score = poker_functions.score_hand(hand)

    #score(int) : index(int)                     Round 1
    junk_index = {#                               01234
#############################################################
        0  :  1,  #Highest Card    : Junk Index:  K0000
        1  :  2,  #One Pair        : Junk Index:  KK000
        2  :  4,  #Two Pair        : Junk Index:  KKQQ0
        3  :  3,  #Three of a Kind : Junk Index:  KKK00
        4  :  5,  #Straight        : Junk Index:  5
        5  :  5,  #Flush           : Junk Index:  5
        6  :  5,  #Full House      : Junk Index:  5
        7  :  4,  #Four of a Kind  : Junk Index:  QQQQK
        8  :  5   #Straight Flush  : Junk Index:  5
    }

    return junk_index[score]

def calculate_keep(bot_hand:dict) -> list:
    '''
    Create a string of integers describing what cards to replace

    Parameters:
        bot_hand: a dictionary of cards sorted by suit

    Returns:
        keep_list: the string of card numbers 1-5 with a max len of 4.
    '''

    
    card_list  = hand_organization.organize_hand(bot_hand)
    junk_index = get_junk_index(bot_hand)

    
    if junk_index == 5: #Bot hand is a: Straight, Flush, Full House, xor Straight Flush
        return card_list            #Don't replace any cards
    
    #if the current score of the hands is 0 check for potential flush and straight
    if poker_functions.score_hand(bot_hand) == 0:
        #Check for flush first (worth more points)
        suited_replacement_list = check_n_suited(bot_hand, 4)
        if suited_replacement_list != card_list:
            return suited_replacement_list
        
        #Check straight nexts
        sequence_replacement_list = check_4_sequenced(bot_hand)
        if sequence_replacement_list != card_list:
            return sequence_replacement_list

    #If you have a 4 of a kind with a 12 or 13 kicker don't get rid of the kicker
    keep_list = card_list[:] if poker_functions.score_hand(bot_hand) == 7 and card_list[junk_index][0] >= 12 else card_list[:junk_index]
    
    return keep_list

def check_4_sequenced(bot_hand:dict) -> list:
    '''
    Given a hand check if there is a possible sequence given hand already has n cards within a sequence

         sequence     |  Parts
    [X] [5 6 7 8]     |    2
    [X] [5 6 7] + [9] |    3
    [X] [5 6] + [8 9] |    3
    [X] [5] + [7 8 9] |    3
    [X]     [6 7 8 9] |    2

    Parameters:
        bot_hand: a dictionary of cards sorted by suit

    Return:
        sequence_keep_list: list of cards that make up 4 sequence

        organized_card_list: default list to be returned if there is not possiblle sequence
    '''
    rank_list = poker_functions.hand_ranks(bot_hand)

    #Create initial data structure
    list_of_lists = [[]]
    for index, rank_frequency in enumerate(rank_list):
        if rank_frequency > 0:
            rank = index + 1
            list_of_lists[len(list_of_lists) - 1].append(rank)
            continue

        if len(list_of_lists[len(list_of_lists) - 1]) > 0:
            list_of_lists.append(list())

    #Trim all empty lists
    for count in range(list_of_lists.count(list())):
        list_of_lists.remove(list())

    card_list = hand_organization.organize_hand(bot_hand)
    
    #If there are more than 3 sublists exit function
    if len(list_of_lists) > 3:
        return card_list
    
    
    #If there are only 2 list in the list of lists
    if len(list_of_lists) == 2:
        sequence_list = list_of_lists[0] if len(list_of_lists[0]) == 4 else list_of_lists[1]
        return construct_card_list(bot_hand, sequence_list)
 
    
    #Assume the list of lists has a length of 3
    #If the center list has a length of 3 then return card_list
    if len(list_of_lists[1]) == 3:
        return card_list
    
    #Remove whichever end that has a list of length 1
    removed = list_of_lists.pop(0) if len(list_of_lists[0]) == 1 else list_of_lists.pop()
    
    #Return the combination of what's left inside the list of lists
    sequence_list = list_of_lists[0] + list_of_lists[1]

    return construct_card_list(bot_hand, sequence_list)


def construct_card_list(bot_hand:dict, sequence_list) -> list:
    '''
    Up to this point is is fair to assume the bot_hand has no
        points associated with it. Search through the card list
        and remove any card who's rank is not in the sequence list

    Parameters:
        bot_hand: a dictionary of cards sorted by suit

        sequence_list: a list of card ranks in the hand that make a sequence of 4 cards

    Returns:
        card_list: list of tuples whose ranks are in the sequence_list
    '''
    card_list = hand_organization.create_card_list(bot_hand)
    for card in card_list:
        if card[0] not in sequence_list:
            card_list.remove(card)
            return card_list

    

def check_n_suited(bot_hand:dict, n_suited:int) -> list:
    '''
    Given a hand check if there is a possible sequence given hand already has n cards within a sequence

    Parameters:
        bot_hand: a dictionary of cards sorted by suit

    Return:
        suited_keep_list: the string of card numbers 1->n with a max len of (5-n).

        organized_card_list: default list to be returned if there is not possiblle flush
    '''
    for suit_list in bot_hand.values():
        if len(suit_list) >= n_suited:
            return suit_list

    return hand_organization.organize_hand(bot_hand)

    


    
####################################################################################


if __name__ == "__main__":
    calculate_keep({0:[(1,0), (2,0)], 1:[(3,1)], 2:[(5,2)], 3:[(11,3)]})
