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

    # creates our blank array (we will have to refactor this for k bands
    seq1_length, seq2_length = len(seq1), len(seq2)

    if banded_width != -1: # there is no band with, n * m size array and initalize base cases
        E = [[point() for j in range((2 * banded_width) + 1)] for i in range(seq1_length + 1)]  # creates an N by k table
        for i in range(1, banded_width + 1):
            new_point = point(i, 0, indel_penalty * i, E[i - 1][0])
            E[i][0] = new_point

        for j in range(1, banded_width + 1):
            new_point = point(0, j, indel_penalty * j, E[j - 1][0])
            E[0][j] = new_point

    else: # we create an n * k size array. and initalize base cases all the way down.
        E = [[point() for j in range(seq1_length + 2)] for i in range(seq1_length + 1)]  # creates n by k
        for i in range(1, seq1_length):
            new_point = point(i, 0, indel_penalty * i, E[i - 1][0])
            E[i][0] = new_point

        for j in range(1, seq2_length):
            new_point = point(0, j, indel_penalty * j, E[j - 1][0])
            E[0][j] = new_point

    # will always be the same :)
    E[0][0] = point(0,0,0,None)
    # establishes our base cases including the 0 edge case.


    for i in range(1, seq1_length+1):
        #for j in range(1, seq2_length+1): # this represents the actual letters maybe.
        # this is where we need to modify
            cost1 = (E[i-1][j-1]).return_cost() + calc_cost(seq1[i-1], seq2[j-1], sub_penalty, match_award)
            cost2 = (E[i][j-1]).return_cost() + indel_penalty
            cost3 = (E[i-1][j]).return_cost() + indel_penalty

            if cost1 <= cost2 and cost1 <= cost3:
                prev = E[i-1][j-1]
                cost = cost1
            elif cost2 < cost1 and cost2 <= cost3:
                prev = E[i][j-1]
                cost = cost2
            else:
                prev = E[i-1][j]
                cost = cost3

            E[i][j] = point(i, j, cost, prev)

    # need to reconstruct the previous tree
    final_node = E[seq1_length][seq2_length]
    total_cost = final_node.return_cost()
    print("this is the total cost! ", total_cost, seq1, seq2, gap)

    word1, word2 = make_prev(final_node, seq1, seq2, gap)
    return total_cost, word1, word2




def calc_cost(a,b, sub_penalty, match_award):
    if a == b:
        return match_award
    else:
        return sub_penalty

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
