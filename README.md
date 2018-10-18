# Ruba Mazetto

## Overview
A computerized version (in Python) of this Italian card game (2-4 players) in which I used a shuffling function to shuffle a Neapolitan (40-card) deck In each turn, players play a single card to “capture” one or more face-up cards from the table if and only if they sum to the card played. A player can steal another’s stash by matching others’ top card with one of their own, or from the table. Once players run out of cards, they are dealt three more cards until all cards have been used up. A computer player makes a move against the human players by recursively constructing a game tree of all possible legal moves, and then choosing the move that maximizes the number of cards gained from other players’ stashes.
