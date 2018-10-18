# CS1210 HW5
# Basil Chatha and Tuo Wu

# I certify that the entirety of this file contains only my own work
# and/or that of my assigned partner. I also certify that my partner
# and I have not shared the contents of this file with anyone in any form.
from random import randint

######################################################################
# createDeck() produces a new, cannonically ordered, 40 card deck.
# Uses a nested comprehension; deviates a bit from the specification
# because it allows one to specify a different size deck. In other
# words, createDeck(13) would create a standard 52-card deck (with J,
# Q, K denoted 11, 12, 13).
def createDeck(N=10, S=('spades', 'hearts', 'clubs', 'diamonds')):
    return([ (v, s) for s in S for v in range(1, N+1) ])

# Fisher-Yates-Knuth fair shuffle. Faster and fairer than riffle(), so
# we may as well use this one! Corrected so as not to create a default
# deck D, which would otherwise be built once and then consumed,
# making it unavailable for subsequent games.
def shuffle(D):
    i = len(D)-1
    while i > 0:
        j = randint(0, i)
        D[i], D[j] = D[j], D[i]
        i = i-1
    return(D)

######################################################################
# Construct the representation of a given card using special unicode
# characters for hearts, diamonds, clubs, and spades.
def displayCard(c):
    suits = {'spades':'\u2660', 'hearts':'\u2661', 'diamonds':'\u2662', 'clubs':'\u2663'}
    return(''.join( [ str(c[0]), suits[c[1]] ] ))

######################################################################
# Print out an indexed list of the cards in input list H, representing
# a hand.
def showHand(H):
    print('\nMy hand: {}'.format(', '.join([ "[{}] {}".format(i, displayCard(H[i])) for i in range(len(H)) ] )))

# Print out an indexed representation of the state of the table,
# including any player stashes and the cards laid on the table. Uses a
# nested set of string format expressions, with the outer one joining
# individual sets of format expressions.
def showTable(N, T, P):
    print('Stash: {}\nTable: {}'.format(', '.join([ "[Player {}] {} (*{})".format(j, displayCard(P[j][-1]), len(P[j])) for j in sorted(P.keys()) ] ),
                                        ', '.join([ "[{}] {}".format(j+N, displayCard(T[j])) for j in range(len(T)) ] )))

######################################################################
# Deal 3 cards, or as many as you can, to each of the N players from
# the deck. Also, update the table so that it has 4 cards if it
# currently has fewer. We'll use try/except to catch the condition
# when we try to pop from an empty deck so we can exit gracefully.
def deal(N, D, T, H):
    try:
        # Three cards...
        for j in range(3):
            # ...to each player...
            for i in range(N):
                H[i].append(D.pop())
        # ...plus a few more to the table, as necessary.
        while len(T) < 4:
            T.append(D.pop())
    except:
        print("Ooops! ran out of cards.")
    return (D, T, H)

######################################################################
# Return (c, M) where c is an index into H[i] and M is either [] (in
# which case we discard c to table), or a list of indexes in range(0,
# N+len(T)) except for i.
def getMove(i, N, H, T, P):
    # Recursive helper function that explores the combinatorial space
    # of possible moves. Let c be the card you are seeking to match,
    # and v represent the remaining value you need to match
    # (initially, the value on card c), j represent the index (into
    # stashes and/or table) of the card you are currently considering
    # adding to the move, M represent the move under construction, and
    # L the collection of legal moves found so far.
    x = []
    for b in P:
        if b != i:
            x.append((P[b][-1][0], b))
    for t in range(len(T)):
        x.append((T[t][0], N+t))

    def helper(c, v, j, M, L):
        #print("Helper: {}, {}, {}, {}".format(i, M, v, j))
        #TODO complete the recursive helper function.
        if(v == 0):
            L += [(c, M)]
            return L
        elif(j > len(x)-1):
            return(L)
        # the two base cases that exit the recursion
        # if the cards picked sum to the picked card,
        # or if  you reach the last card, terminate
        #recursion
        else:
            L = helper(c, v, j+1, M, L)
            # search combinations of cards with values <= card picked
            if(x[j][0] <= v and x[j][1] not in M):
                nL = M + [x[j][1]]
                L = helper(c, (v - x[j][0]), j+1, nL, L)
            # if the cards in the stash or table's values are less than
            # what's left to add to get to the value of c and it's not
            # already in M, construct the list of lists which is a list of
            # possible legal moves. recursively call helper and make it =
            # to L so it will keep being filled with possible legal moves


        # Done. Return legal moves found so far.
        return(L)

    # Human player; solicit move interactively.
    if i == 0:
        return(pickMove(i, N, H, T, P))

    # Autplayer for player i. Search combinations for legal moves for
    # every card c in H[i].
    L = []
    for c in range(len(H[i])):
        L = helper(c, H[i][c][0], 0, [], L)
    # No legal moves?
    if not L:
        # L is still [] (no matches); discard a random card.
        return((randint(1, len(H[i]))-1, []))

    # print("Legal moves: {}".format(L))
    # Return the "largest" match. There could better heuristics here
    # that depend on, e.g., the sizes of the constituent piles.
    return( max(L, key=lambda x: len(x[1])) )

######################################################################
# Return (c, M) where c is an index into H[i] and M is either [] (in
# which case we discard c to table), or a list of indexes in range(0,
# N+len(T)) except for i.
def pickMove(i, N, H, T, P):
    # Human player gets to see his/her hand.
    showHand(H[i])
    # Prompt player i for card to play from H[i].
    while True:
        # Capture any errors from non-integer inputs.
        try:
            #TODO complete
            c = int(input("Play which card? "))
            if(H[i][c]):
                break
        except:
            pass
    # Prompt player i for list of indeces to match.
    while True:
        # Capture any errors from non-integer inputs.
        try:
            #TODO complete
            M = []
            temp = input("Select matching indeces separated by spaces (blank to discard): ").split()
            # get input from user
            if(temp == []):
                break
            # if nothing is inputed, break out of loop and discard card
            M += [int(x) for x in temp]
            # make a list of the converted strings
            nM = []
            for a in M:
                #for every number in M
                if a < N and a != i:
                    nM.append(P[a][-1][0])
                # if the number < N and its not = the player's index append
                # the top stash card to the new list nM
                elif a >= N and a < N + len(T) and a != i:
                    nM.append(T[a-N][0])
                # if the number is >= to N and < N + len(T) and its not =
                # the player's index append that table card to nM
            if(len(nM) == len(M) and sum(nM) == H[i][c][0]):
                break
                # if the inputed cards add to the picked hand, break out of the loop
            else:
                M = []
        except:
            pass
    # Done.
    return((c, M))

######################################################################
# Governs game play for N players (2 by default) using an K-card deck
# (40 by default). Refactored for simplicity from version of HW4.
def play(N=2, K=10):
    # Corrected so that we can play multiple games without resetting
    # the Python session. As originally written, shuffle() creates a
    # default deck as its argument which is consumed (and not reset)
    # the first time you play.
    D = shuffle(createDeck(K))     # Create a deck
    T = []                         # Table top
    H = [ [] for i in range(N) ]   # Player hands
    P = { }                        # Player piles i:(c, n)
    # Record last player to steal a stash or take a card from T
    last = None			   # Used at end of game.

    # Play a game.
    while D:
        # Deal cards and (re)populate the table.
        print("\n=========\nDealing...")
        D, T, H = deal(N, D, T, H)

        # While the first player has any cards...
        while H[0]:
            # For each player.
            for i in range(0, N):
                # We need to check to make sure player i has something
                # left to play in case there was an funny distribution
                # of cards. Because of how we dealt the card, as soon
                # as player i runs out of cards, the remaining players
                # >i will have done so as well.
                if not H[i]:
                    break

                # Good to go. Show the state of the game from player 0 perspective
                # (i.e., do not reveal player i's hand, because player 0 is watching).
                print("\n=========\nPlayer {}:".format(i))
                showTable(N, T, P)

                # Manage move selection.
                (c, M) = getMove(i, N, H, T, P)

                # Execute the move (c, M).
                if not M:
                    # M is []: discard card c.
                    print("Player {} adds {} to table".format(i, displayCard(H[i][c])))
                    T.append(H[i].pop(c))
                else:
                    # M is a list of indexes describing a combination
                    # of cards on table or other player's
                    # stashes.
                    print("Player {} plays {} and...".format(i, displayCard(H[i][c])))

                    # Player i is last to take a trick (for distribution
                    # of remaining table cards at end of game).
                    last = i

                    # Execute the move.
                    while M:
                        j = M.pop()
                        if j < N:
                            # Stealing player j's stash.
                            print("...steals Player {} stash {}".format(j, displayCard(P[j][-1])))
                            if i in P:
                                P[i].extend(P[j])
                            else:
                                P[i] = P[j]
                            # Clear player j's stash.
                            del P[j]
                        else:
                            # Add table card t to player i stash if it exists (else create it).
                            print("...takes {} from table".format(displayCard(T[j - N])))
                            if i in P:
                                P[i].append(T.pop(j - N))
                            else:
                                P[i] = [ T.pop(j - N) ]
                    # Append matching card from player i hand to top of stash.
                    P[i].append(H[i].pop(c))

    # Game over. Assign remaining cards from table to player who took
    # the last trick (= last).
    if ( T ):
        print("Done: awarding {} from table to Player {}".format(', '.join([ displayCard(c) for c in T ]), last))
        if last in P:
            P[last].extend(T)
        else:
            P[last] = T

    # Return player scores as dictionary.
    return({ p:sum( [ c[0] for c in P[p] ] ) for p in P })
