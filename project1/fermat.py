import argparse
import random
import math


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)

# add a commment to see if this is working

# You will need to implement this function and change the return value.
# Takes in x and N, and an integer component y, and returns x^y mod N
def mod_exp(x: int, y: int, N: int) -> int:  # time complexity is O(n^3) in terms of bits and
    if y == 0: # constant time
        return 1
    z = mod_exp(x, (y//2), N)  # USE INTEGER DIVISION NOT FLOOR
    if (y % 2) == 0:  # if even
        return (z*z) % N
    else:  # if odd
        return (x * (z*z)) % N


def fprobability(k: int) -> float: # look at the textbook for this one
    return (1/(2 ** k)) 


def mprobability(k: int) -> float: # even works for carmicheal numbers
    return (3/ (4 ** k))  # look at the text book.


# fermats test for primes, given prime number N, and the number of iterations run (K)
def fermat(N: int, k: int) -> str: # we have K recursion calls
    for i in range(k):  # repeat K times
        a = random.randint(1, N-1) # pick a rand int (constant time)
        if (mod_exp(a, N-1, N)) != 1: # O(n^3) here
            return "composite"
    return "prime"
                                    # given K recursion calls * O(n^3), assuming they are of similar length, 
                                    # our total time is O(n^4)


# miller rabbin test for primes given a number N and the number of iterations to run K
def miller_rabin(N: int, k: int) -> str: # woohoo! I am a genius! I got it working!
    for i in range(k): # run K times 
        a = random.randint(1, N-1)  # pick a random number
        result = mod_exp(a, N-1, N)  # calculate the result with modular exponentiation
        if result == 1:  # if we start with a 1 we have to keep checking down the list
            if (miller_rabin_help(a, (N-1)//2, N)) == "composite":  # if we ever return composite break
                return "composite"   # we can only prove its composite
        else:  # forgot to include this little else statement and almost game myself a heart attack. we all good now.
            return "composite"
    return "prime"  # if we never return composite its prolly prime


def miller_rabin_help(a, exp, mod): # a is our term, N is our exponent and mod is our %
    result = mod_exp(a, exp, mod) # calculate the result (O(n^3))
    if result == mod-1:  # mod -1, we can break cause its prime
        return "probably prime"
    if result == 1:  # continue the chain for as long as we can
        if (exp//2) > 1:  # make sure we can still go down and sqrt the exponent
            miller_rabin_help(a, exp//2, mod) # calls itself log(exp) times
        else:  # we can't prove its prime but we gotta return something anyway
            return "probably prime"  # sequence consisted of all ones, break
    else:
        return "composite"



def main(number: int, k: int):
    fermat_call, miller_rabin_call = prime_test(number, k)
    fermat_prob = fprobability(k)
    mr_prob = mprobability(k)

    print(f'Is {number} prime?')
    print(f'Fermat: {fermat_call} (prob={fermat_prob})')
    print(f'Miller-Rabin: {miller_rabin_call} (prob={mr_prob})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('k', type=int)
    args = parser.parse_args()
    main(args.number, args.k)



# WRITE UP: SPACE AND TIME COMPLEXITIES OF RELATED FUNCTIONS
# if you would like to see this in a better format, here's the drive page:
# https://docs.google.com/document/d/15ysNv9G759zuxsQsH30g152rZIbs5SVbS4m-p-GV5tQ/edit?usp=sharing
#
#
# mod_exp: We are sort of making the assumption that n = log(2)x = log(2)y = log(2)N.
# The rest is fairly simple - we have a constant for the return statement, we have a recursive call that goes off log(N) times, and then we have 2 return statements, which are both n2 return time.
# Given our n * n * log(2)N (we can simplify log(2)N to n) for space complexity we have n * n * n or O(n3)
# For our space complexity, we aren’t creating any lists or anything, so the only non-constant affecting memory is our recursive call, which we do log(2)N times, or n.
# So our space complexity is O(n)
#
#
# Fermat: we first have to do this K times, so K will be in there somewhere.
# So we will have K times picking our randINt, we can assume to be constant time.
# We already know that our mod_exp has a time of O(n3), so our total time complexity will be
# O(n3*k), and if we can assume that K and N are similar sizes, then we can say that we are dealing with kO(n3) (this can either be rewritten as O(n^3) assuming K is a constant, or we can rewrite it as O(n^4) if we assume that K is similar to N. for the duration of this paper, I will be assuming that K is constant and be using O(n^3)
# For space complexity, we are storing the var a but then deleting it, and we don’t appear to do anything else with it. We just call K times on our mod_exp, but everytime we call K we overwrite the old var. Therefore, I am pretty sure this has the same space complexity as mod_exp, which is to say, O(n)
#
#
# Miller Rabbin: so we once again have to do this K times, so K will be in there somewhere.
# We pick a randit, which is constant time, and then we do mod_exp. Mod_exp is O(n^3).
# If it's not prime (assume worst case) we then have to run the help function on top of that.
# We then get to this helper function.
# And under miller rabbin help, we run mod_exp again, which has a time of O(n3), we then check, if it fails (assume worst case) then we run it within itself and we run it a max of log(exp) times, which simplifies out to n, so its total time is n(n^3) or n^4.
# n^3 + n^4 or n^4 complexity, where n^3 represents the mod_exp call outside helper
# n^4 represents the n^3 mod_exp call inside the helper, and we call the helper log(N) or n. Because K is a constant we can multiply it.
# Total time complexity: kO(n4) (I am going to assume K is constant and use O(n^4) for the rest of this paper)
# Space complexity:  the only thing here that takes space is the recursive call to its help function, as well as the call to mod_exp. Miller rabbin will call itself log(exp) times or O(n) times, and mod_exp calls itself log(y) or n times. Either way, we are dealing with O(n) space, where n is either log(y) or log(exp).
#
#
# probability: The space complexity on this is O(1) lets get that right out the way.
# The time complexity is a little harder to grasp - given that division has a call time of O(n^2), we have O(n^2) multiplied by 2^n. Given my old rules, I do believe that an dominates over na, so we can have this as  O(n^2)
#
#
# mpProbability: This one is very similar to fProbability, where
# Time complexity: O(n3) (see the process above but replace 2 with 3). We can simplify out the 3 as it is a constant and we want the shortest order possible.
# Space complexity: O(1)