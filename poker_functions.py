import hand_organization

############################## Deck Functions #################################
deck = list()

suits = {
    0: 'H',
    1: 'D',
    2: 'C',
    3: 'S',
}

#A-K -> 1-13
ranks = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

def create_deck() -> None:
    '''
    Using the suits dictionary and the ranks tuple create a
        single list of 52 cards
    '''
    
    #Create an instance of a new list
    global deck
    deck = list()
     
    #For each suit in suits
    for suit in suits.keys():
        #For each rank in ranks
        for rank in ranks:
            #Create a card tuple and add to deck list
            deck.append((rank, suit))

def print_card(card:tuple) -> None:
    '''
    Given the card tuple data structure (rank, suit), print 
        out "{rank} of {suit}"

    Parameters:
        Card: (rank(int), suit(int)) tuple that represents one card

    Returns:
        The funtion itself returns None, however the 
            function print "{rank} of {suit}" to console    
    '''

    faces = {
        1  : "A",
        11 : "J",
        12 : "Q",
        13 : "K"
    }
    #if the integer is inside the faces dictionary then use the name in 
    #dictionary otherwise use the given number
    rank = faces[card[0]] if card[0] in faces.keys() else card[0]

    #Use the suit associated with the given number
    suit = suits[card[1]]

    print("{:>2} of {}".format(rank, suit))

def shuffle() -> None:
    '''
    Remove all cards from deck into temp_deck, 1 randomly chosen card
        at a time until the deck has no more cards and temp_deck holds
        all the cards. Set deck to temp_deck
    '''
    import random


    global deck
    temp_deck = list()

    while len(deck) > 0:
        random_card_index = random.randint(0, len(deck)-1) #
        temp_deck.append(deck[random_card_index][:])
        deck.remove(deck[random_card_index])

    deck = temp_deck[:]

def deal() -> tuple:
    '''
    Remove the top card of the global deck list and return the card

    Returns:
        card: Tuple (rank, suit)
    '''
    global deck

    card = deck.pop(0)

    return card

############################### Hand Functions ##################################
def deal_hands(number_of_hands:int) -> list:
    '''
    Deal five cards by alternating dealing a single card to each hand

    Parameters:
        number_of_hands: integer

    Returns:
        hands: list of hand dictionaries
    '''
    hands = list()
    
    #each player gets a hand data structure
    for hand_count in range(0, number_of_hands):
        
        hand = { 0:[], 1:[], 2:[], 3:[]}
        
        hands.append(hand)

    #deal cards around as if at a poker table
    cards_per_hand = 5
    for card_count in range(0, number_of_hands * cards_per_hand):
        
        hand_index   = card_count % number_of_hands
        card         = deal()
        suit_of_card = card[1]

        hands[hand_index][suit_of_card].append(card)

    return hands

def print_hand(hand:dict) -> None:
    '''
    Print cards from a new card list structure

    Parameters:
        hand: a dictionary of cards sorted by suit
    '''
    card_list = hand_organization.organize_hand(hand)

    for index, card in enumerate(card_list):
        print(f'   C{index + 1}:', end=" ")
        print_card(card)
    
########################### Ranking ############################################
def hand_ranks(hand:dict) -> list:
    '''
    create a list that holds how many of each rank is in a given hand

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        rank_list: list

    Examples/Doctests:
    >>> hand_ranks({0:[(1,0),(2,0)], 1:[(1,1)], 2:[(1,2)], 3:[(1,3)]})
    [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    >>> hand_ranks({ 0:[], 1:[(1,1), (2,1), (3,1), (4,1), (5,1)], 2:[], 3:[]})
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

    >>> hand_ranks({0:[(1,1),(10,0)], 1:[(2,1)], 2:[(2,2)], 3:[(11,3)]})
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]

    '''
    rank_list = [0] * 13
    card_list = hand_organization.create_card_list(hand)

    for card in card_list:
        rank = card[0]
        rank_list[rank - 1] += 1

    return rank_list

def straight_flush(hand:dict) -> int: #8 points
    '''
    Return points for a hand that has all cards of the same suit and 
        ranks are incrementing by 1

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        points: int

    Examples/Doctests:
    >>> straight_flush({0:[(1,0), (2,0), (3,0), (4,0), (5,0)], 1:[], 2:[], 3:[]})
    8
    >>> straight_flush({ 0:[], 1:[(1,1), (2,1), (3,1), (4,1), (5,1)], 2:[], 3:[]})
    8
    >>> straight_flush({ 0:[], 1:[], 2:[], 3:[]})
    0
    '''
    rank_list = hand_ranks(hand)
    stright_points = straight(rank_list)

    flush_points = flush(hand)

    return 8 if stright_points != 0 and flush_points != 0 else 0
    
def four_of_a_kind(rank_list:list) -> int: #7 points
    '''
    Return points for a hand that has all 4 ranks of a given suit

    Parameters:
        rank_list: a list that holds how many of each rank is in a given hand

    Returns:
        points: int

    Examples/Doctests:
    >>> four_of_a_kind([4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    7
    >>> four_of_a_kind([0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0])
    7
    >>> four_of_a_kind([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    0
    '''

    for rank in rank_list:
        if rank == 4:
            return 7
    
    return 0

def full_house(rank_list:list) -> int: #6 points
    '''
    Return points for a hand that has 2 ranks of 1 suit and 3 ranks of different suit

    Parameters:
        rank_list: a list that holds how many of each rank is in a given hand

    Returns:
        points: int

    Examples/Doctests:
    >>> full_house([3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    6
    >>> full_house([0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0])
    6
    >>> full_house([1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    0
    '''
    one_pair_points = one_pair(rank_list)
    three_of_a_kind_points = three_of_a_kind(rank_list)

    return 6 if one_pair_points != 0 and three_of_a_kind_points != 0 else 0

def flush(hand:dict) -> int: #5 points
    '''
    Return points for a hand that has all cards of the same suit

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        points: int

    Examples/Doctests:
    >>> flush({0:[(1,0), (2,0), (3,0), (4,0), (5,0)], 1:[], 2:[], 3:[]})
    5
    >>> flush({ 0:[], 1:[(1,1), (2,1), (3,1), (4,1), (5,1)], 2:[], 3:[]})
    5
    >>> flush({ 0:[], 1:[], 2:[], 3:[]})
    0
    '''
    for suit_list in hand.values():
        if len(suit_list) == 5:
            return 5
        
    return 0

def straight(rank_list:dict) -> int: #4 points
    '''
    Return points for a hand that has ranks are incrementing by 1

    Parameters:
        rank_list: a list that holds how many of each rank is in a given hand

    Returns:
        points: int

    Examples/Doctests:
    >>> straight([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    4
    >>> straight([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    4
    >>> straight([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    0
    '''
    sequence_counter = 0

    for rank in rank_list:
        if rank == 0:
            sequence_counter = 0
            continue
            
        sequence_counter += 1

        if sequence_counter == 5:
            return 4
        
    return 0
        
def three_of_a_kind(rank_list:dict) -> int: #3 points
    '''
    Return points for a hand that has 3 ranks of 1 suit

    Parameters:
        rank_list: a list that holds how many of each rank is in a given hand

    Returns:
        points: int

    Examples/Doctests:
    >>> three_of_a_kind([3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    3
    >>> three_of_a_kind([0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0])
    3
    >>> three_of_a_kind([1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    0
    '''

    for rank in rank_list:
        if rank == 3:
            return 3
        
    return 0

def two_pair(rank_list:dict) -> int: #2 points
    '''
    Return points for a hand that has 2 ranks of 1 suit and 2 ranks of another suit

    Parameters:
        rank_list: a list that holds how many of each rank is in a given hand

    Returns:
        points: int

    Examples/Doctests:
    >>> two_pair([2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    2
    >>> two_pair([0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0])
    2
    >>> two_pair([1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    0
    '''
    
    pair_counter = 0
    for rank in rank_list:
        if rank == 2:
            pair_counter += 1

        if pair_counter == 2:
            return 2
        
    return 0

def one_pair(rank_list:dict) -> int: #1 point
    '''
    Return a point for a hand that has 2 ranks of 1 suit

    Parameters:
        rank_list: a list that holds how many of each rank is in a given hand

    Returns:
        points: int

    Examples/Doctests:
    >>> one_pair([2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    1
    >>> one_pair([0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    1
    >>> one_pair([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    0
    '''
    for rank in rank_list:
        if rank == 2:
            return 1
        
    return 0

#No Combination: 0 points

#Tie Breaker
def highest_card(rank_list:list) -> int:
    '''
    Return the highest rank card among cards in hand based off of the rank list

    Parameters:
        rank_list: a list that holds how many of each rank is in a given hand

    Returns:
        card_rank: int

    Examples/Doctests:
    >>> highest_card([2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    2
    >>> highest_card([0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    11
    >>> highest_card([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    13
    '''
    
    for index in range(12, -1, -1):
        if rank_list[index] > 0:
            return index + 1

################################### Hand Scoring ###############################################
def score_hand(hand:dict) -> int:
    '''
    Scores a given hand

    Parameters:
        hand: a dictionary of cards sorted by suit

    Returns:
        score: an integer value represent the amount of points a hand is worth

    >>> score_hand({0:[(1,0), (2,0), (3,0), (4,0), (5,0)], 1:[], 2:[], 3:[]})
    8

    >>> score_hand({0:[(1,0), (2,0)], 1:[(1,1)], 2:[(1,2)], 3:[(1,3)]})
    7

    >>> score_hand({0:[(5,0), (9,0)], 1:[(5,1), (9,1)], 2:[(5,2)], 3:[]})
    6

    >>> score_hand({0:[(1,0), (2,0), (3,0), (5,0), (11,0)], 1:[], 2:[], 3:[]})
    5
     
    >>> score_hand({0:[(1,0), (3,0)], 1:[(2,1)], 2:[(5,2)], 3:[(4,3)]})
    4
      
    >>> score_hand({0:[(1,0), (2,0)], 1:[(1,1)], 2:[(1,2)], 3:[(4,3)]})
    3
       
    >>> score_hand({0:[(1,0), (2,0)], 1:[(1,1), (2,1)], 2:[], 3:[(11,3)]})
    2
        
    >>> score_hand({0:[(1,0)], 1:[(1,1)], 2:[(11,2),(2,2)], 3:[(13,3)]})
    1
         
    >>> score_hand({0:[], 1:[], 2:[], 3:[]})
    0

    '''
    points = 0

    rank_list = hand_ranks(hand)
    points = points if one_pair(rank_list)        == 0 else 1
    points = points if two_pair(rank_list)        == 0 else 2
    points = points if three_of_a_kind(rank_list) == 0 else 3
    points = points if straight(rank_list)        == 0 else 4
    points = points if flush(hand)                == 0 else 5
    points = points if full_house(rank_list)      == 0 else 6
    points = points if four_of_a_kind(rank_list)  == 0 else 7
    points = points if straight_flush(hand)       == 0 else 8

    return points

def get_hand_type(hand_score) -> str:
    '''
    Return hand type based off the give score for hand

    Parameters:
        hand_score: integer between 0-8

    Returns:
        hand_type: str Ex. Straight Flush
    '''
    score_to_type = {
        8: 'Straight Flush',
        7: 'Four of a Kind',
        6: 'Full House',
        5: 'Flush',
        4: 'Straight',
        3: 'Three of a Kind',
        2: 'Two Pair',
        1: 'One Pair'
    }

    return score_to_type[hand_score]

def compare_hands(hand_one:dict, hand_two:dict) -> str:
    '''
    Print content of hand one and two to the console along with the result

    Parameters:
        hand_one: a dictionary of cards sorted by suit

        hand_two: a dictionary of cards sorted by suit

    Returns:
        outcome_indicator: ONE, TWO, SPLIT
    '''
    #Print Hand One
    print('YOUR HAND')
    print('==============')
    print_hand(hand_one)
    print('\n')

    #Print Hand Two
    print('CPU HAND')
    print('==============')
    print_hand(hand_two)
    print('\n')

    #Score each hand
    score_one = score_hand(hand_one)
    score_two = score_hand(hand_two)

    #If one has a higher score hand one wins
    if score_one > score_two:
        print('HAND ONE WINS WITH: {}'.format(get_hand_type(score_one)))
        return 'ONE'
    
    #If two has a higher score hand two wins
    elif score_one < score_two:
        print('HAND TWO WINS WITH: {}'.format(get_hand_type(score_two)))
        return 'TWO'
    
    #Each hand has the same base score Ex. 0:0, 5:5, 4:4, 8:8
    else:
        #Find high card for hand one
        high_rank_card_one = hand_organization.organize_hand(hand_one)[0]

        #Find high card for hand two
        high_rank_card_two = hand_organization.organize_hand(hand_two)[0]

        #If one has the higher rank within their hand
        if high_rank_card_one > high_rank_card_two:
            print('HAND ONE WINS WITH: Highest Card')
            return 'ONE'
        
        #If two has the higher rank within their hand
        elif high_rank_card_one < high_rank_card_two:
            print('HAND TWO WINS WITH: Highest Card')
            return 'TWO'
        
        #If one and two have the same score and the same high ranking card
        else:
            print('SPLIT POT')
            return 'SPLIT'
    