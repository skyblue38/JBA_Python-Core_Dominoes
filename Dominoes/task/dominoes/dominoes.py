# JBA Python Core
# Project: Dominoes - https://hyperskill.org/projects/146
# submitted by Chris Freeman - Stage 5/5 - The AI

import random


stock = []          # pool of unallocated domino pieces
computer = []       # the computer's dominoes
player = []         # the player's dominoes
snake = [[]]        # the start of the placed dominoes
status = ''         # who plays next: player or computer
ai_plays = []       # descending list of positions for popular dominos in computer's hand
ai_score = {}       # dictionary of piece values with frequencies of each


def stock_generate(dominoes: list) -> list:
    """ create list of all domino pieces in stock list """
    for i in range(7):
        for j in range(i, 7):
            dominoes.append([i, j])
    return dominoes


def l_sum(lx: list) -> int:
    """ return the sum of elements in a two element list """
    return len(lx) == 2 and lx[0] + lx[1]


def is_double(dx: list) -> bool:
    """ returns True if dx is a 2 element list and both elements are the same value """
    return len(dx) == 2 and dx[0] == dx[1]


def get_starting_piece(cx: list, px: list) -> list:
    """ Finds and returns the domino to use as starting piece.
    The starting piece is the highest sum of piece values.
    Double pieces are higher than other non-doubles with the same sum value.
    After finding the highest domino, it is removed from the respective list,
    and the other player then goes first. If both candidates have equal non-double
    pieces, return and empty list, which should trigger a reshuffle and redraw. """
    c_list = [(l_sum(c), c) for c in cx]
    c_ordered = sorted(c_list)
    p_list = [(l_sum(p), p) for p in px]
    p_ordered = sorted(p_list)
    if c_ordered[-1][0] > p_ordered[-1][0]:
        ind = cx.index(c_ordered[-1][1])    # computer has high piece
        return cx.pop(ind)                  # remove it from computer's pieces and return it
    elif p_ordered[-1][0] > c_ordered[-1][0]:
        ind = px.index(p_ordered[-1][1])    # player has high piece
        return px.pop(ind)                  # remove it from player's pieces and return it
    else:
        c_domino = c_ordered[-1][1]         # computer and player have equal highest pieces
        p_domino = p_ordered[-1][1]         # get each piece
        if is_double(c_domino):
            ind = cx.index(c_domino)        # computer has double piece - player goes first
            return cx.pop(ind)              # remove it from computer's pieces and return it
        elif is_double(p_domino):
            ind = px.index(p_domino)        # player has double piece - computer goes first
            return px.pop(ind)              # remove it from player's pieces and return it
        else:
            return []   # empty list as player and computer have same value and neither is a double


def win_state(cx: list, px: list, sx: list) -> bool:
    """ Checks the game state for Win or Draw.
    The first player to run out of pieces wins.
    A draw is when no player can play a legal move and also
    cannot pass as the stock of space dominoes is empty. """
    if len(cx) == 0:            # computer exhausted all pieces
        print('Status: The game is over. The computer won!')
        return True
    elif len(px) == 0:          # player exhausted all pieces
        print('Status: The game is over. You won!')
        return True
    else:                       # is it a draw?
        left_val = sx[0][0]
        right_val = sx[-1][1]
        if left_val == right_val:   # are both ends of snake the same value?
            val_count = 0           # if so, count how many times this value appears
            for ni in range(len(sx)):
                if sx[ni][0] == left_val:
                    val_count += 1
                if sx[ni][1] == right_val:
                    val_count += 1
            if val_count == 8:      # if the same value appears 8 times, DRAW
                print("Status: The game is over. It's a draw!")
                return True
    return False                    # otherwise, keep playing...


def place_domino(xx: list, xi: int, sx: list, st: list):
    """ Add the indicated domino to the snake.
     The selected domino is specified using the list position number
     which is negative for left-hand placement and positive for right-hand placement.
     An indicator value of Zero is a Pass, so a domino is transferred from the stock
     list and appended to the candidate's list. """
    if xi < 0:          # add piece ix to head (left-hand end) of snake
        sx.insert(0, xx.pop(abs(xi)-1))
    elif xi > 0:        # add piece ix to tail (right-hand end) of snake
        sx.append(xx.pop(xi-1))
    else:               # get a piece from stock (if available)
        if len(st) > 0:
            xx.append(st.pop())


def rotate_domino(d: list):
    """ Switch the values of a given domino. """
    d[1], d[0] = d[0], d[1]  # swap places of domino values


def valid_move(vx: list, xi: int, sx: list) -> bool:
    """ Check that the nominated move is allowed.
    A value on the nominated domino must be the same as the outer value of
    the domino at the indicated end of the snake list.
    This may include rotating the nominated domino, so that matching values abutt. """
    if xi < 0:          # check for valid placement on left-hand end of snake
        sd = sx[0][0]   # snake-left end value
        vd = vx[abs(xi)-1]  # candidate domino
        if vd[0] == sd:
            rotate_domino(vx[abs(xi)-1])
            return True
        elif vd[1] == sd:
            return True
    elif xi > 0:        # check for valid placement on right-had end of snake
        sd = sx[-1][1]  # snake-right end value
        vd = vx[xi-1]   # candidate domino
        if vd[0] == sd:
            return True
        elif vd[1] == sd:
            rotate_domino(vx[xi-1])
            return True
    else:
        return True
    return False


def value_frequency(cx: list, sx: list) -> dict:
    freq_dict = {}
    for c in cx:
        freq_dict.setdefault(c[0], 0)
        freq_dict[c[0]] += 1
        freq_dict.setdefault(c[1], 0)
        freq_dict[c[1]] += 1
    for s in sx:
        freq_dict.setdefault(s[0], 0)
        freq_dict[s[0]] += 1
        freq_dict.setdefault(s[1], 0)
        freq_dict[s[1]] += 1
    return freq_dict


def rank_hand(sc: dict, cx: list) -> list:
    rank = []
    for ci in range(len(cx)):
        rank.append((sc[cx[ci][0]] + sc[cx[ci][1]], ci+1))
    rank.sort(reverse=True)
    return [i[1] for i in rank]


# Start here:
while snake == [[]]:
    computer = []               # clear the lists
    player = []
    stock = stock_generate([])  # create list of dominoes
    random.shuffle(stock)       # shuffle them
    for n in range(7):          # transfer 7 dominoes to each player
        computer.append(stock.pop())
        player.append(stock.pop())
    snake = [(get_starting_piece(computer, player))]  # repeat until starting piece found
if len(computer) == 7:          # set game status - who plays next
    status = 'computer'
else:
    status = 'player'
while True:
    print('=' * 70)
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(computer)}')
    print()
    if len(snake) > 6:      # print board pieces, truncated if too many...
        print(f'{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}')
    else:
        for n in range(len(snake)):
            print(f'{snake[n]}', end='')
    print()
    print('Your pieces')
    n = 0
    for pl in player:
        n += 1
        print(f'{n}:{pl}')
    print()
    if win_state(computer, player, snake):
        break
    if status == 'computer':
        print('Status: Computer is about to make a move. Press Enter to continue...')
        input()
        ai_score = value_frequency(computer, snake)
        ai_plays = rank_hand(ai_score, computer)
        c_move = 0
        for dom in ai_plays:
            if valid_move(computer, -dom, snake):
                c_move = -dom
                break
            elif valid_move(computer, dom, snake):
                c_move = dom
                break
        place_domino(computer, c_move, snake, stock)
    else:
        print("Status: It's your turn to make a move. Enter your command.")
        while True:
            try:
                p_move = int(input())
            except ValueError:      # non-numeric input
                print('Invalid input. Please try again.')
                continue
            p_size = len(player)
            if -p_size <= p_move <= p_size:
                if valid_move(player, p_move, snake):
                    place_domino(player, p_move, snake, stock)
                    break
                else:
                    print('Illegal move. Please try again.')
            else:
                print('Invalid input. Please try again.')
    if status == 'computer':
        status = 'player'
    else:
        status = 'computer'
