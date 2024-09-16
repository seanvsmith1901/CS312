import argparse
import random
import math


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)


# You will need to implement this function and change the return value.
# Takes in x and N, and an integer component y, and returns x^y mod N
def mod_exp(x: int, y: int, N: int) -> int:  # time complexity is O(n^3)
    if y == 0: # constant time
        return 1
    z = mod_exp(x, (y//2), N) # recursive call   # USE INTEGER DIVISION NOT FLOOR
    if (y % 2) == 0: # constant time # if even
        return (z*z) % N # assuming modulo is constant time
    else:  # if odd
        return (x * (z*z)) % N #


# You will need to implement this function and change the return value.
def fprobability(k: int) -> float: # never tested but pretty sure
    return (1/(pow(2, k)))  # constant time


# You will need to implement this function and change the return value.
def mprobability(k: int) -> float:  # never tested but pretty sure
    return (3/pow(4, k))  # constant time, if pow is considered O(1)


# fermats test for primes, given prime number N, and the number of iterations run (K)
def fermat(N: int, k: int) -> str: # time complexity is kO(N-1)^2
    for i in range(k): # repeat K times
        a = random.randint(1, N-1) # pick a rand int (constant time)
        if (mod_exp(a, N-1, N)) != 1: # however long modular exponentiation takes
            return "composite"
    return "prime"


# miller rabbin test for primes given a number N and the number of iterations to run K
def miller_rabin(N: int, k: int) -> str: # woohoo! I am a genius! I got it working!
    for i in range(k): # run K times # best case is O(1), worst case is O((n-1)^2)
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
    result = mod_exp(a, exp, mod) # calculate the result
    if result == mod-1:  # mod -1, we can break cause its prime
        return "probably prime"
    if result == 1:  # continue the chain for as long as we can
        if (exp//2) > 1:  # make sure we can still go down and sqrt the exponent
            miller_rabin_help(a, exp//2, mod)
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
