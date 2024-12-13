
import poker_game
import poker_functions

if __name__ == "__main__":

    TEST_ROUNDS = 1000000

    hand_one_wins = 0
    hand_two_wins = 0
    split_pot     = 0

    for rounds in range(TEST_ROUNDS):
        hands        = poker_game.start_new_game()

        static_hand  = hands[0]
        bot_hand     = hands[1]

        bot_hand     = poker_game.modify_bot_hand(bot_hand)

        winner       = poker_functions.compare_hands(static_hand, bot_hand)

        hand_one_wins += 1 if winner == 'ONE'   else 0
        hand_two_wins += 1 if winner == 'TWO'   else 0
        split_pot     += 1 if winner == 'SPLIT' else 0

    print('No Discard:        {}'.format(hand_one_wins))
    print('Strategic Discard: {}'.format(hand_two_wins))
    print('Split Pot:         {}'.format(split_pot))

