import random

logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

card_values = {
    "A": [1, 11],
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}

'''
We assume an infinite deck. 
In order to limit that, we can get the random card and then remove it from the deck. 
Deck can be list(card_values) appended n times.
'''


def deal_card():
    """Returns a random card from the deck"""
    return random.choice(list(card_values.keys()))


def calculate_final_sum(sum1, sum2):
    final_sum = 0
    if sum1 == 21:
        return sum1
    elif sum2 == 21:
        return sum2
    elif sum1 > 21:
        final_sum = sum2
    elif sum2 > 21:
        final_sum = sum1
    else:
        final_sum = min(sum1, sum2)
    return final_sum


def calculate_sum_for_ace_hand(current_hand):
    if "A" not in current_hand:
        calculate_current_hand_sum(current_hand)

    sum1 = 0
    sum2 = 0

    # Min calculation
    for i in current_hand:
        if i == "A":
            value = card_values[i][0]
            sum1 += value
        else:
            sum1 += card_values[i]

    # Max calculation
    for i in current_hand:
        if i == "A":
            value = card_values[i][1]
            sum2 += value
        else:
            sum2 += card_values[i]

    return calculate_final_sum(sum1, sum2)


def calculate_current_hand_sum(current_hand):
    """Take a list of cards and return the sum calculated for it"""
    final_sum = 0
    if "A" in current_hand:
        final_sum = calculate_sum_for_ace_hand(current_hand)
    else:
        for i in current_hand:
            final_sum += card_values[i]

    return final_sum


def should_computer_continue(current_hand):
    return True if calculate_current_hand_sum(current_hand) < 17 else False


def populate_initial_hands(computer, user):
    for _ in range(2):
        computer.append(deal_card())
        user.append(deal_card())


def get_hand_as_string(hand):
    res = "["
    for i in hand:
        res = res + i + ","
    res = res[:-1]  # To remove the final comma
    res += "]"
    return res


def print_hands(computer_str, computer, user_str, user):
    print(f"{user_str}: {get_hand_as_string(user)}, sum is {calculate_current_hand_sum(user)}")
    res = ""
    if isinstance(computer, list):
        res = f", sum is {calculate_current_hand_sum(computer)}"
    print(f"{computer_str}: {get_hand_as_string(computer)}" + res)


def print_final_hand(computer, user):
    print_hands("Computer's final hand", computer, "Your final hand", user)


def find_over_status_and_blackjack(loser, loser_sum, winner_cards):
    res = []
    res1 = ""
    res2 = ""
    if loser_sum > 21:
        res1 = loser + " went over. "
    if (len(winner_cards) == 2 and
            "A" in winner_cards and
            (
                    "J" in winner_cards or
                    "Q" in winner_cards or
                    "K" in winner_cards
            )):
        res2 = " with a blackjack"
    res.append(res1)
    res.append(res2)
    return res


def find_winner(user_cards, computer_cards, should_check_for_winner):
    stop_game = False
    user_sum_value = calculate_current_hand_sum(user_cards)
    computer_sum_value = calculate_current_hand_sum(computer_cards)

    if user_sum_value > 21 and computer_sum_value > 21:

        print_final_hand(computer_cards, user_cards)

        if user_sum_value == computer_sum_value:
            print("It's a draw!")
        else:
            print("You both went over. You lose!")

        stop_game = True

    elif (user_sum_value == 21 or
          computer_sum_value > 21 or
          (should_check_for_winner and user_sum_value > computer_sum_value)):

        print_final_hand(computer_cards, user_cards)

        res = find_over_status_and_blackjack("Computer", computer_sum_value, user_cards)
        res1 = res[0]
        res2 = res[1]
        print(res1 + "You win" + res2 + "!")

        stop_game = True

    elif (computer_sum_value == 21 or
          user_sum_value > 21
          or (should_check_for_winner and computer_sum_value > user_sum_value)):

        print_final_hand(computer_cards, user_cards)

        res = find_over_status_and_blackjack("You", user_sum_value, computer_cards)
        res1 = res[0]
        res2 = res[1]
        print(res1 + "The computer wins" + res2 + "!")

        stop_game = True

    elif should_check_for_winner and user_sum_value == computer_sum_value:
        print_final_hand(computer_cards, user_cards)
        print("It's a draw!")
        stop_game = True

    return stop_game


continue_playing = True
while continue_playing:
    user_choice = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower()
    if user_choice == "n":
        continue_playing = False
        break
    print("\n" * 10)
    print(logo)

    computer_hand = []
    user_hand = []
    computer_sum = -1
    user_sum = -1

    populate_initial_hands(computer_hand, user_hand)
    # Check if someone has already achieved blackjack
    game_over = find_winner(user_hand, computer_hand, False)

    if game_over:
        continue

    print_hands("Computer's first card", computer_hand[0], "Your cards", user_hand)
    game_over = False

    while not game_over:
        user_choice = input("Type 'y' to get another card, type 'n' to pass: ").lower()

        user_continued = False
        if user_choice == "y":
            user_hand.append(deal_card())
            user_continued = True
        # If user has decided to stop, then let the computer keep playing until it reaches its natural end point

        while should_computer_continue(computer_hand):
            computer_hand.append(deal_card())

        check_for_winner = False  # Additional variable simply for better understanding
        if not user_continued:
            check_for_winner = True
            # game_over = True

        game_over = find_winner(user_hand, computer_hand, check_for_winner)

        if not game_over:
            print_hands("Computer's first card", computer_hand[0], "Your hand", user_hand)
