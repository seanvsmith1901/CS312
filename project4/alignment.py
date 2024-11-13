import math
from typing import final

from point import *

def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """


    seq1_length, seq2_length = len(seq1), len(seq2) # need these constants elsewhere baby

    E = initialize_matrix(banded_width, seq1_length, seq2_length) #creates either nm or nk matrix

    E = set_base_case(E, seq1_length, seq2_length, banded_width, indel_penalty) # populates the graph with our base case

    E = populate_tree(E, seq1_length, seq2_length, seq1, seq2, banded_width, sub_penalty, match_award, indel_penalty) # fills out the tree

    final_node = get_final(E, banded_width, seq1_length, seq2_length) # gets the final node (depends on band)

    total_cost = final_node.return_cost() # gets the cost of that node

    word1, word2 = make_prev(final_node, seq1, seq2, gap) # reconstructs from pointers the word path and the word comparisons

    return total_cost, word1, word2 # returns in the order the code wants them.


def set_base_case(E, seq1_length, seq2_length, banded_width, indel_penalty): # not a good way to reconcile these
    if banded_width != -1:
        for i in range(0, banded_width + 1):
            for j in range(0, (2 * banded_width) + 1):
                if i == 0:
                    cost = (j - banded_width) * indel_penalty
                    if cost < 0:
                        cost = math.inf
                    if cost == 0:
                        E[i][j] = point(i, j, cost, None)
                    else:
                        E[i][j] = point(i, j, cost, E[i][j - 1])
                else:
                    if j == banded_width - i:
                        E[i][j] = point(i, j, indel_penalty * i, E[i - 1][j + 1])

    else:
        for i in range(1, seq1_length):
            new_point = point(i, 0, indel_penalty * i, E[i - 1][0])
            E[i][0] = new_point

        for j in range(1, seq2_length):
            new_point = point(0, j, indel_penalty * j, E[0][j - 1])
            E[0][j] = new_point

        # will always be the same :) check the indentation level.
        E[0][0] = point(0,0,0,None)

    return E


def calc_cost(a,b, sub_penalty, match_award):
    if a == b:
        return match_award
    else:
        return sub_penalty


def initialize_matrix(banded_width, seq1_length, seq2_length):
    first_range = seq2_length + 1
    if banded_width != -1:
        first_range = (2 * banded_width) + 1

    return [[point() for _ in range(first_range)] for _ in range(seq1_length + 1)]  # creates n by k



def populate_tree(E, seq1_length, seq2_length, seq1, seq2, banded_width, sub_penalty, match_award, indel_penalty):
    first_int = 1
    second_length = seq2_length + 1

    if banded_width != -1:
        second_length = (2*banded_width) + 1
        first_int = 0

    if banded_width == -1:
        for i in range(1, seq1_length+1):
            for j in range(first_int, second_length): # this represents the actual letters maybe.

                if 0 < j < seq2_length + 1:
                # this is where we need to modify
                    cost1 = (E[i-1][j-1]).return_cost() + calc_cost(seq1[i-1], seq2[j-1], sub_penalty, match_award)
                    cost2 = (E[i][j-1]).return_cost() + indel_penalty
                    cost3 = (E[i-1][j]).return_cost() + indel_penalty

                    if cost1 <= cost2 and cost1 <= cost3:
                        prev = E[i-1][j-1]
                        prev.j = j - 1  # look man IDK why I had to do this but it worked alright?
                        cost = cost1
                    elif cost2 < cost1 and cost2 <= cost3:
                        prev = E[i][j-1]
                        cost = cost2
                    else:
                        prev = E[i-1][j]
                        cost = cost3

                    E[i][j] = point(i, j, cost, prev)

    else:
        for i in range(1, seq1_length+1):
            for k in range(first_int, second_length):
                j = -banded_width + k + i
                if 0 < j < seq2_length+1:

                    # you can always check diagonal. it is always morally correct. https://www.reddit.com/r/MemeRestoration/comments/mqoiv7/its_morally_correct_requested_by_ujustvolted/
                    cost1 = (E[i - 1][k]).return_cost() + calc_cost(seq1[i - 1], seq2[j - 1], sub_penalty, match_award)

                    if k == 0:
                        cost2 = math.inf
                    else:
                        cost2 = (E[i][k - 1]).return_cost() + indel_penalty

                    if k == 2 * banded_width:
                        cost3 = math.inf
                    else:
                        cost3 = (E[i - 1][k + 1]).return_cost() + indel_penalty

                    if cost1 <= cost2 and cost1 <= cost3:
                        prev = E[i - 1][k]
                        prev.j = j-1 # look man IDK why I had to do this but it worked alright?
                        cost = cost1

                    elif cost2 < cost1 and cost2 <= cost3:
                        prev = E[i][k-1]
                        cost = cost2
                    else:
                        prev = E[i - 1][k + 1]
                        cost = cost3

                    E[i][k] = point(i, j, cost, prev) # remember to store it at value k, but we need it to have value j for retracing reasons

    return E

def get_final(E, banded_width, seq1_length, seq2_length):
    second_length = seq2_length
    if banded_width != -1:
        second_length = banded_width

    final_node = E[seq1_length][second_length]

    return final_node

def make_prev(final_node, seq1, seq2, gap):
    word1 = ""
    word2 = ""
    while final_node.previous != None:
        if final_node.i-1 == final_node.previous.i and final_node.j-1 == final_node.previous.j:
            word2 += str((seq2[final_node.j-1]))
            word1 += str((seq1[final_node.i-1]))

        elif final_node.i-1 != final_node.previous.i and final_node.j-1 == final_node.previous.j:
            word1 += str((gap))
            word2 += str((seq2[final_node.j - 1]))
        elif final_node.i-1 == final_node.previous.i and final_node.j-1 != final_node.previous.j:
            word2 += str((gap))
            word1 += str((seq1[final_node.i - 1]))
        else:
            print("You're not supposed to be here")

        final_node = final_node.previous

    result1 = ''.join(reversed(word1))
    result2 = ''.join(reversed(word2))
    return result1, result2

