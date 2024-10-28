import random


def create_domino():
    a_domain = []
    for i in range(0, 7):
        for j in range(i, 7):
            a_domain.append([i, j])
    return a_domain


def create_group(dominos):
    random.shuffle(dominos)
    return dominos[:7], dominos[7:14], dominos[14:]


def computer_scores(domino_snake, computer_data):
    tmp_array = [*domino_snake, *computer_data]
    counter = [0, 0, 0, 0, 0, 0, 0]
    for i in tmp_array:
        counter[i[0]] += 1
        counter[i[1]] += 1
    score = {}
    for i, key in enumerate(computer_data):
        total_score = sum([counter[key[0]], counter[key[1]]])
        score[i] = total_score
    return sorted(score.items(), key=lambda x: x[1], reverse=True)


def search_max_domino(group):
    domain = None
    for i in group:
        if domain is None and i[0] == i[1]:
            domain = i
        elif domain is not None and i[0] == i[1] and domain[0] < i[0] and domain[1] < i[1]:
            domain = i
    return domain


def get_max_domino(domain1, domain2):
    if domain1 is None and domain2 is None:
        return None
    if domain1 is None:
        return domain2
    if domain2 is None:
        return domain1
    if domain1[0] < domain2[0]:
        return domain2
    return domain1


def init_domino_game():
    array = create_domino()
    while True:
        user_data, computer_data, stock_data = create_group(array)
        user_domino_max = search_max_domino(user_data)
        computer_domino_max = search_max_domino(computer_data)

        domino_max = get_max_domino(user_domino_max, computer_domino_max)
        if domino_max is not None and domino_max in user_data:
            index = user_data.index(domino_max)
            del user_data[index]
            return user_data, computer_data, stock_data, [domino_max], "computer"
        elif domino_max is not None and domino_max in computer_data:
            index = computer_data.index(domino_max)
            del computer_data[index]
            return user_data, computer_data, stock_data, [domino_max], "player"


def computer_choice(domino_snake, computer_data, stock_data):
    i = 0
    while True:
        try:
            computer_score_data = computer_scores(domino_snake, computer_data)
            if i >= len(computer_score_data):
                index_choice = 0
            else:
                max_score = computer_score_data[i]
                index_choice = max_score[0] + 1
            update_game(index_choice, computer_data, stock_data, domino_snake)
            break
        except ValueError:
            i += 1


def user_choice(length_domino):
    while True:
        try:
            choice_command = input()
            choice_command = int(choice_command)
            if -length_domino <= choice_command <= length_domino:
                return choice_command
            print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def print_user_pieces(user_date):
    print("Your pieces:")
    if len(user_date) > 0:
        for i, piece in enumerate(user_date):
            print(f"{i+1}: {piece}")


def print_command(is_computer):
    if is_computer:
        print("Status: Computer is about to make a move. Press Enter to continue...")
    else:
        print("Status: It's your turn to make a move. Enter your command.")


def update_game(choice, data, stock_data, domino_snake):
    if choice == 0:
        if len(stock_data) == 0:
            return
        element = stock_data[0]
        data.append(element)
        del stock_data[0]
        return
    if choice > 0:
        element = data[choice - 1]
        element = is_valid_domino(element, domino_snake)
        if element is None:
            raise ValueError("Piece not valid")
        domino_snake.append(element)
        del data[choice - 1]
    else:
        element = data[((-1)*choice)-1]
        element = is_valid_domino(element, domino_snake, is_last=False)
        if element is None:
            raise ValueError("Piece not valid")
        domino.insert(0, element)
        del data[((-1)*choice)-1]

        
def print_domino_snake(domino_snake):
    if len(domino_snake) <= 6:
        print(*domino_snake)
        return
    first_part = domino_snake[:3]
    second_part = domino_snake[-3:]
    print(*first_part, "...", *second_part, sep="")


def print_status_game(user, computer, stock, domino, player):
    print('='.join(('' for i in range(71))))
    print("Stock size: ", len(stock))
    print("Computer pieces: ", len(computer))
    print()
    print_domino_snake(domino)
    print()
    print_user_pieces(user)
    print_command(player == "computer")


def print_game_final_status(user_data, computer_data, draw):
    if draw:
        print("Status: The game is over. It's a draw!")
        return
    if len(user_data) == 0 and len(computer_data) == 0:
        print("Status: The game is over. It's a draw!")
    elif len(user_data) == 0:
        print("Status: The game is over. You won!")
    else:
        print("Status: The game is over. The computer won")


def is_valid_domino(piece, snake_domino, is_last=True):
    last_piece = snake_domino[(-1 if is_last else 0)]
    index_test = 1 if is_last else 0
    piece_index = 0 if is_last else 1
    switch_index = 1 if is_last else 0
    if last_piece[index_test] == piece[piece_index]:
        return piece
    if last_piece[index_test] == piece[switch_index]:
        return [piece[1], piece[0]]
    return None


def computer_action(computer_domino, stock_data, domino_snake):
    input()
    computer_choice(domino_snake, computer_domino, stock_data)


def user_action(user_domino, stock_data, domino_snake):
    while True:
        try:
            index_piece = user_choice(len(user_domino))
            update_game(index_piece, user_domino, stock_data, domino_snake)
            break
        except ValueError:
            print("Illegal move. Please try again.")


def is_draw(domino_snake):
    final_element = domino_snake[-1][1]
    a = sum(element == final_element for sublist in domino_snake for element in sublist)
    return a >= 8


user, computer, stock, domino, player = init_domino_game()
computer_scores(domino, computer)
game_is_draw = False
while len(user) > 0 and len(computer) > 0:
    game_is_draw = is_draw(domino)
    if game_is_draw:
        break
    print_status_game(user, computer, stock, domino, player)
    if player == "computer":
        computer_action(computer, stock, domino)
        player = "user"
    else:
        user_action(user, stock, domino)
        player = "computer"


print_status_game(user, computer, stock, domino, player)
print_game_final_status(user, computer, game_is_draw)

