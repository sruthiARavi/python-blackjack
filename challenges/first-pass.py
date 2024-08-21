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


def get_next_card():
    return random.choice(list(card_values.keys()))


def get_minimum_current_hand_sum(current_hand):
    final_sum = 0
    if "A" in current_hand:
        sum1 = 0
        sum2 = 0

        for i in current_hand:
            if i == "A":
                value = card_values[i][0]
                sum1 += value
            else:
                sum1 += card_values[i]

        for i in current_hand:
            if i == "A":
                value = card_values[i][1]
                sum2 += value
            else:
                sum2 += card_values[i]

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

    else:
        for i in current_hand:
            final_sum += card_values[i]

    return final_sum


def should_computer_continue(current_hand):
    return True if get_minimum_current_hand_sum(current_hand) < 17 else False


def get_hand_as_string(hand):
    hand = "["
    for i in hand:
        hand = hand + i + ","
    hand = hand[:-1] # To remove the final comma
    hand += "]"
    return hand


def populate_initial_hands(one_hand, two_hands):
    one_hand.append(get_next_card())
    two_hands.append(get_next_card())
    two_hands.append(get_next_card())


def print_hands(computer_str, computer, user_str, user):
    print(f"{user_str}: {get_hand_as_string(user)}")
    print(f"{computer_str}: {get_hand_as_string(computer)}")


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
    populate_initial_hands(computer_hand, user_hand)
    print_hands("Computer's first card", computer_hand, "Your cards", user_hand)
    game_over = False
    result = ""

    while not game_over:
        user_choice = input("Type 'y' to get another card, type 'n' to pass: ").lower()

        if user_choice == "y":
            user_hand.append(get_next_card())

        if should_computer_continue(computer_hand):
            computer_hand.append(get_next_card())

        user_sum = get_minimum_current_hand_sum(user_hand)
        computer_sum = get_minimum_current_hand_sum(computer_hand)

        if user_sum == 21 or computer_sum>21:
            print_hands("Computer's final hand", computer_hand, "Your final hand", user_hand)
            print("You win")
            game_over = True
        elif computer_sum == 21 or user_sum>21:
            print_hands("Computer's final hand", computer_hand, "Your final hand", user_hand)
            print("The computer wins")
            game_over = True
        else:
            print_hands("Computer's hand", computer_hand, "Your hand", user_hand)





