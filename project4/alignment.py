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
    E = [[point() for j in range(seq2_length+1)] for i in range(seq1_length+1)] # creates my lsit

    E[0][0] = point(0,0,0,None)
    # establishes our base cases including the 0 edge case.
    for i in range(1,seq1_length+1):
        new_point = point(i, 0, indel_penalty * i, E[i-1][0])
        E[i][0] = new_point


    for j in range(1,seq2_length+1):
        new_point = point(0, j, indel_penalty * j, E[j-1][0])
        E[0][j] = new_point

    for i in range(1, seq1_length+1):
        for j in range(1, seq2_length+1):                       # this represents the actual letters maybe.
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
    total_cost = E[seq1_length][seq2_length].return_cost()
    print("this is the total cost! ", total_cost)




def calc_cost(a,b, sub_penalty, match_award):
    if a == b:
        return match_award
    else:
        return sub_penalty