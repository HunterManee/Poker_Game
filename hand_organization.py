import poker_functions

def create_card_list(hand:dict) -> list:
    '''
    Create a card list from all the cards in a given hand

    Parameters:
        hand: a dictionary of cards sorted by suit

    Return:
        card_list: unorganized list of tuples

    Examples/Doctests:
    >>> create_card_list({0:[(2, 0), (5,0)], 1:[(3,1)], 2:[(13,2)], 3:[(6,3)]})
    [(2, 0), (5, 0), (3, 1), (13, 2), (6, 3)]
    '''
    card_list = list()
    for suit_list in hand.values():
        card_list += suit_list

    return card_list

def create_hand_dict(card_list:list) -> dict:
    '''
    From the given card list create a dictionary that discribes that card list
    
    Parameters:
        card_list: unorganized list of tuples
    
    Returns:
        hand: a dictionary of cards sorted by suit

    Examples/Doctest:
    >>> create_hand_dict({0:[(2,0), (5,0)], 1:[(3,1)], 2:[(13,2)], 3:[(6,3)]})
    [(2, 0), (5, 0), (3, 1), (13, 2), (6, 3)]
    '''
    hand = {0:[], 1:[], 2:[], 3:[]}
    for card in card_list:
        card_suit = card[1]
        hand[card_suit].append(card)

    return hand

#####################################################################################

def organize_hand(hand:dict) -> list:
    '''
    Organize hand based of the best possible score made from hand

    Parameters:
        hand: a dictionary of cards sorted by suit

    Return:
        organized_card_list: The list of cards in a hand based of the score of the hand

    Examples/Doctests:
    #High Card
    >>> organize_hand({0:[(2, 0), (5,0)], 1:[(3,1)], 2:[(13,2)], 3:[(6,3)]})
    [(13, 2), (2, 0), (5, 0), (3, 1), (6, 3)]

    #One Pair
    >>> organize_hand({0:[(2,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(6,3)]})
    [(13, 1), (13, 2), (2, 0), (5, 0), (6, 3)]

    #Two Pair
    >>> organize_hand({0:[(2,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(5,3)]})
    [(13, 1), (13, 2), (5, 0), (5, 3), (2, 0)]

    #Three of a Kind
    >>> organize_hand({0:[(13,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(6,3)]})
    [(13, 0), (13, 1), (13, 2), (5, 0), (6, 3)]

    #Straight
    >>> organize_hand({0:[(10,0), (9,0)], 1:[(13,1)], 2:[(12,2)], 3:[(11,3)]})
    [(13, 1), (12, 2), (11, 3), (10, 0), (9, 0)]

    #Flush
    >>> organize_hand({0:[(10,0), (9,0), (1,0), (7,0), (12,0)], 1:[], 2:[], 3:[]})
    [(12, 0), (10, 0), (9, 0), (7, 0), (1, 0)]

    #Full House
    >>> organize_hand({0:[(10,0), (9,0), (1,0), (7,0), (12,0)], 1:[], 2:[], 3:[]})
    [(12, 0), (10, 0), (9, 0), (7, 0), (1, 0)]

    #Four of a Kind
    >>> organize_hand({0:[(13,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(13,3)]})
    [(13, 0), (13, 1), (13, 2), (13, 3), (5, 0)]

    #Straight Flush
    >>> organize_hand({0:[(10,0), (9,0), (8,0), (7,0), (11,0)], 1:[], 2:[], 3:[]})
    [(11, 0), (10, 0), (9, 0), (8, 0), (7, 0)]
    '''
    score = poker_functions.score_hand(hand)
    
    #dictionary whose keys are all possible score values for a given hand
    #dictionary values are the function that would best organize the hand for 
    #  the associated score
    organization_station = {
        0: organize_high_card,
        1: organize_one_pair,
        2: organize_two_pair,
        3: organize_three_of_a_kind,
        4: organize_straight,
        5: organize_flush,
        6: organize_full_house,
        7: organize_four_of_a_kind,
        8: organize_straight_flush
    }

    #Pass the hand dictionary into whichever function will best organize 
    # the hand into an organized card list based of the current 
    # score of the hand
    organized_card_list = organization_station[score](hand)
    return organized_card_list

def organize_high_card(hand:dict) -> list:
    '''
    Organzed list of cards with the highest card at index 0

    Parameters:
        hand: a dictionary of cards sorted by suit
    
    Return:
        organized_card_list: organized list of tuples

    Examples/Doctests:
    >>> organize_high_card({0:[(2, 0), (5,0)], 1:[(3,1)], 2:[(13,2)], 3:[(6,3)]})
    [(13, 2), (2, 0), (5, 0), (3, 1), (6, 3)]

    >>> organize_high_card({0:[(2, 0), (6,0)], 1:[(3,1)], 2:[(5,2)], 3:[(12,3)]})
    [(12, 3), (2, 0), (6, 0), (3, 1), (5, 2)]

    >>> organize_high_card({0:[(13, 0), (5,0)], 1:[(3,1)], 2:[(1,2)], 3:[(6,3)]})
    [(13, 0), (5, 0), (3, 1), (1, 2), (6, 3)]
    '''
    #Determine what card has the highest rank
    card_list = create_card_list(hand)
    high_card = card_list[0]
    for card_index in range(len(card_list)-1, 0, -1):
        current_card_rank = card_list[card_index][0]
        high_card_rank    = high_card[0]
        high_card         = card_list[card_index] if current_card_rank > high_card_rank else high_card

    #Set the card with the highest rank to the top of the list
    organized_list = list()
    organized_list.append(high_card)
    for card in card_list:
        if card != high_card:
            organized_list.append(card)

    return organized_list

def organize_one_pair(hand:dict) -> list:
    '''
    Organize list of cards so that a pair takes index 0-1

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples
    
    Examples/Doctests:
    >>> organize_one_pair({0:[(2,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(6,3)]})
    [(13, 1), (13, 2), (2, 0), (5, 0), (6, 3)]

    >>> organize_one_pair({0:[(2,0), (5,0)], 1:[(3,1)], 2:[(13,2)], 3:[(5,3)]})
    [(5, 0), (5, 3), (2, 0), (3, 1), (13, 2)]

    >>> organize_one_pair({0:[(2,0), (5,0)], 1:[(3,1)], 2:[(2,2)], 3:[(6,3)]})
    [(2, 0), (2, 2), (5, 0), (3, 1), (6, 3)]

    '''
    return organize_n_of_a_kind(hand, 2)

def organize_two_pair(hand:dict) -> list:
    '''
    Organize list of cards so that the largest ranked pair takes index 0-1 and
        the smallest ranked pair takes index 2-3

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples

    Examples/Doctests:
    >>> organize_two_pair({0:[(2,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(5,3)]})
    [(13, 1), (13, 2), (5, 0), (5, 3), (2, 0)]

    >>> organize_two_pair({0:[(12,0), (5,0)], 1:[(3,1)], 2:[(12,2)], 3:[(5,3)]})
    [(12, 0), (12, 2), (5, 0), (5, 3), (3, 1)]

    >>> organize_two_pair({0:[(2,0), (5,0)], 1:[(6,1)], 2:[(2,2)], 3:[(6,3)]})
    [(6, 1), (6, 3), (2, 0), (2, 2), (5, 0)]
    '''
    rank_list = poker_functions.hand_ranks(hand)

    #Look for paired ranks
    pair_rank_list = list()
    for index, rank_frequence in enumerate(rank_list):
        rank = index + 1
        if rank_frequence == 2:
            pair_rank_list.append(rank)

            if len(pair_rank_list) == 2:
                break

    #Determine the largest and smallest rank pair
    max_rank  = max(pair_rank_list)
    min_rank  = min(pair_rank_list)
    
    #Set lists variables
    card_list = create_card_list(hand)
    max_pair  = list()
    min_pair  = list()

    #Sort the different pairs into the cooresponding list
    for card in list(card_list):
        card_rank = card[0]
        if card_rank == max_rank:
            max_pair.append(card)
            card_list.remove(card)
        elif card_rank == min_rank:
            min_pair.append(card)
            card_list.remove(card)

    return max_pair + min_pair + card_list
            
def organize_three_of_a_kind(hand:dict) -> list:
    '''
    Organize list of cards so that a pair takes index 0-2

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples
    
    Examples/Doctests:
    >>> organize_three_of_a_kind({0:[(13,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(6,3)]})
    [(13, 0), (13, 1), (13, 2), (5, 0), (6, 3)]

    >>> organize_three_of_a_kind({0:[(2,0), (5,0)], 1:[(5,1)], 2:[(13,2)], 3:[(5,3)]})
    [(5, 0), (5, 1), (5, 3), (2, 0), (13, 2)]

    >>> organize_three_of_a_kind({0:[(2,0), (5,0)], 1:[(3,1)], 2:[(2,2)], 3:[(2,3)]})
    [(2, 0), (2, 2), (2, 3), (5, 0), (3, 1)]
    '''
    
    return organize_n_of_a_kind(hand, 3)

def organize_straight(hand:dict) -> list:
    '''
    Organize list of cards from largest rank to smallest rank

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples

    Examples/Doctests:
    >>> organize_straight({0:[(10,0), (9,0)], 1:[(13,1)], 2:[(12,2)], 3:[(11,3)]})
    [(13, 1), (12, 2), (11, 3), (10, 0), (9, 0)]

    >>> organize_straight({0:[(1,0), (5,0)], 1:[(3,1)], 2:[(2,2)], 3:[(4,3)]})
    [(5, 0), (4, 3), (3, 1), (2, 2), (1, 0)]

    >>> organize_straight({0:[(7,0), (5,0)], 1:[(8,1)], 2:[(9,2)], 3:[(6,3)]})
    [(9, 2), (8, 1), (7, 0), (6, 3), (5, 0)]
    '''
    card_list = create_card_list(hand)

    card_list.sort(reverse=True)

    return card_list

def organize_flush(hand:dict) -> list:
    '''
    Organize list of cards from largest rank to smallest rank

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples

    Examples/Doctests:
    >>> organize_straight({0:[(10,0), (9,0), (1,0), (7,0), (12,0)], 1:[], 2:[], 3:[]})
    [(12, 0), (10, 0), (9, 0), (7, 0), (1, 0)]

    >>> organize_straight({0:[], 1:[(10,1), (9,1), (1,1), (7,1), (12,1)], 2:[], 3:[]})
    [(12, 1), (10, 1), (9, 1), (7, 1), (1, 1)]

    >>> organize_straight({0:[], 1:[], 2:[], 3:[(10,3), (9,3), (1,3), (7,3), (12,3)]})
    [(12, 3), (10, 3), (9, 3), (7, 3), (1, 3)]
    '''
    return organize_straight(hand)

def organize_full_house(hand:dict) -> list:
    '''
    Organize list of cards from largest rank to smallest rank

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples

    Examples/Doctests:
    >>> organize_straight({0:[(10,0), (9,0), (1,0), (7,0), (12,0)], 1:[], 2:[], 3:[]})
    [(12, 0), (10, 0), (9, 0), (7, 0), (1, 0)]

    >>> organize_straight({0:[], 1:[(10,1), (9,1), (1,1), (7,1), (12,1)], 2:[], 3:[]})
    [(12, 1), (10, 1), (9, 1), (7, 1), (1, 1)]

    >>> organize_straight({0:[], 1:[], 2:[], 3:[(10,3), (9,3), (1,3), (7,3), (12,3)]})
    [(12, 3), (10, 3), (9, 3), (7, 3), (1, 3)]
    '''
    pair_list = organize_n_of_a_kind(hand, 2)
    three_of_a_kind_list = organize_n_of_a_kind(hand, 3)

    pair_rank = pair_list[0][0]
    three_of_a_kind_rank = three_of_a_kind_list[0][0]

    #Return the pair version of the list or the three of a kin version of the list depending on which rank is larger
    return three_of_a_kind_list if three_of_a_kind_rank > pair_rank else pair_list

def organize_four_of_a_kind(hand:dict) -> list:
    '''
    Organize list of cards so that a pair takes index 0-3

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples
    
    Examples/Doctests:
    >>> organize_four_of_a_kind({0:[(13,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(13,3)]})
    [(13, 0), (13, 1), (13, 2), (13, 3), (5, 0)]

    >>> organize_four_of_a_kind({0:[(5,0), (5,0)], 1:[(5,1)], 2:[(13,2)], 3:[(5,3)]})
    [(5, 0), (5, 0), (5, 1), (5, 3), (13, 2)]

    >>> organize_four_of_a_kind({0:[(12,0), (5,0)], 1:[(12,1)], 2:[(12,2)], 3:[(12,3)]})
    [(12, 0), (12, 1), (12, 2), (12, 3), (5, 0)]

    '''
    return organize_n_of_a_kind(hand, 4)

def organize_straight_flush(hand:dict) -> list:
    '''
    Organize list of cards from largest rank to smallest rank

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples

    Examples/Doctests:
    >>> organize_straight_flush({0:[(10,0), (9,0), (8,0), (7,0), (11,0)], 1:[], 2:[], 3:[]})
    [(11, 0), (10, 0), (9, 0), (8, 0), (7, 0)]

    >>> organize_straight_flush({0:[], 1:[(10,1), (9,1), (11,1), (13,1), (12,1)], 2:[], 3:[]})
    [(13, 1), (12, 1), (11, 1), (10, 1), (9, 1)]

    >>> organize_straight_flush({0:[], 1:[], 2:[], 3:[(3,3), (4,3), (5,3), (7,3), (6,3)]})
    [(7, 3), (6, 3), (5, 3), (4, 3), (3, 3)]
    '''
    return organize_straight(hand)

def organize_n_of_a_kind(hand:dict, n_of_a_kind:int) -> list:
    '''
    Organize list of cards so that a pair takes index 0-n

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        organized_card_list: organized list of tuples
    
    Examples/Doctests:
    >>> organize_n_of_a_kind({0:[(2,0), (5,0)], 1:[(13,1)], 2:[(13,2)], 3:[(6,3)]}, 2)
    [(13, 1), (13, 2), (2, 0), (5, 0), (6, 3)]

    >>> organize_n_of_a_kind({0:[(2,0), (5,0)], 1:[(5,1)], 2:[(13,2)], 3:[(5,3)]}, 3)
    [(5, 0), (5, 1), (5, 3), (2, 0), (13, 2)]

    >>> organize_n_of_a_kind({0:[(12,0), (5,0)], 1:[(12,1)], 2:[(12,2)], 3:[(12,3)]}, 4)
    [(12, 0), (12, 1), (12, 2), (12, 3), (5, 0)]

    '''
    rank_list = poker_functions.hand_ranks(hand)
    n_rank = -1

    #Get the rank whose frequence is equivlant to n
    for index, rank_frequency in enumerate(rank_list):
        n_rank = index + 1
        if rank_frequency == n_of_a_kind:
            break
    
    card_list          = create_card_list(hand)
    of_a_kind_list     = list()
    not_of_a_kind_list = list()

    for card in card_list:
        card_rank = card[0]
        if card_rank == n_rank:
            of_a_kind_list.append(card)
            continue
        
        not_of_a_kind_list.append(card)

    return of_a_kind_list + not_of_a_kind_list



    


