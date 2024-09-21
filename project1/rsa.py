import random
import sys

import fermat
# This may come in handy...
from fermat import miller_rabin

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return (1, 0, a) # a SHOULD be one for extended cases, if a isn't one then we try again
    (x1, y1, d) = ext_euclid(b, a % b) # magic
    return (y1, (x1 - ((a//b)*y1)), d) # d is the GCD so we want that



# Implement this function
def generate_large_prime(bits=512) -> int:
    myPrime = 6
    k = 20
    while fermat.miller_rabin(myPrime, k) != "prime":
        myPrime = random.getrandbits(bits)

    return myPrime # Guaranteed random prime number obtained through fair dice roll


# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:

    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    N = p * q

    pq = (p-1) * (q-1) # just to save space and make it easier to read

    d = 0
    index = 0
    while d != 1:
        (y1, x1, d) = ext_euclid((p-1) * (q-1), primes[index])
        index += 1

    e = primes[index-1]  # yeah its funky don't worry about it

    # find D

    (r1, d, r3) = ext_euclid((p-1) * (q-1), e)

    d = d % ((p-1) * (q-1))  # this is VERY imporant, he NEEDS to be positive lol otherwise he will recurse into the floor


    print("This is what we are returning ", N, " ", e, " ", d)
    return (N, e, d)


# WRITE UP: SPACE AND TIME COMPLEXITIES OF RELATED FUNCTIONS
# if you would like to see this in a better format, here's the drive page:
# https://docs.google.com/document/d/15ysNv9G759zuxsQsH30g152rZIbs5SVbS4m-p-GV5tQ/edit?usp=sharing
#
#
#Ext_euclid: This one has some magic going on, but the biggest thing is its recursive call
#We know that when we take our a % b, we can’t be any larger than ½ of the size, so we are taking a log of b.
#We are going to say that a and b are similarly sized inputs, and as such we can say that the big o of this function is O(log(n))
#In terms of space complexity, the only thing that is happening here is once again, the recursive call. So, our space complexity is going to be the same as our time complexity, which is to say, O(log(n))
#
#
#Generate_Large_Prime: This one has two things going on in it. First, is that I call miller_rabin (I tried both) and based on my last assumption we can say that miller_rabbin is O(n^4).
#We call this until we get a random number. This is going to require us to use the prime number theorem. Given a random integer from 0-N, the probability of being a prime is approx 1 / ln(N).
#If we assume that our N is a constant 512 bits, then this reduces to O(1) time. If, however, we assume that this is NOT the case, then we can see that we will need to run 1 / ln(N) times.
#This means that we take O(n^4) * 1/ln(n), which still simplifies out to O(n^4) runtime.
#
#
#
# Generate_Key_Pairs: this one generates a large prime, which is O(n^4) and does this twice.
# We then store pq, which is n^2 given p and q, (much slower than checking if its prime)
# We then calculate d, and if we assume euclid's extent is never larger than Olog(n), we can add that in. This gets us e and we store it. We run ext_euclids again for another O(log(n)) and then make sure d is positive, (O(1)) and then return those pairs.
# So our big O looks like
# O(n^4) + n^2 + Olog(n) + O(log(n)) + O(1)
# So our time complexity is O(n^4), almost entirely just from checking to make sure that our numbers are prime. The rest is easy potatoes.
# In terms of space complexity, there’s not a lot going on here.
# The only thing to watch out for here is once again, generating random primes, it can be O(n) when using get_rand_bits(where we have to randomize each bit in N size).
# Miller rabin test for primality is also O(n) in terms of input size, which is what I use. Ext_euclid is only going to be O(log(n))
# Space complexity: O(n)