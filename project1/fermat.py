import argparse
import random
import math


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)

# add a commment to see if this is working

# You will need to implement this function and change the return value.
# Takes in x and N, and an integer component y, and returns x^y mod N
def mod_exp(x: int, y: int, N: int) -> int:  # time complexity is O(n^2* m) (see slide 84, lecture 3 notes)
                                            # If we assume that y length is similar to x and N then complexity is O(n^3)
    if y == 0: # constant time              # space complexity is O(log(n)), cause each recursion adds a call onto the stack. 
        return 1
    z = mod_exp(x, (y//2), N) # recursive call   # USE INTEGER DIVISION NOT FLOOR
    if (y % 2) == 0: # constant time # if even
        return (z*z) % N # assuming modulo is constant time
    else:  # if odd
        return (x * (z*z)) % N #


def fprobability(k: int) -> float: # look at the textbook for this one
    return (1/(2 ** k)) 


def mprobability(k: int) -> float: # even works for carmicheal numbers
    return (3/ (3 ** k))  # look at the text book. 


# fermats test for primes, given prime number N, and the number of iterations run (K)
def fermat(N: int, k: int) -> str: # we have K recursion calls
    for i in range(k): # repeat K times
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

# pretty sure that this fucntion is Olog(n)^2, becuase mod_exp is Olog(n) and this functino is also Olog(N)
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
