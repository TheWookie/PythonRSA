import math  # for the squareroot in isPrime
from itertools import zip_longest  # for the RSA padding function
import string
import sys

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# alphabet = string.ascii_uppercase

def baseExp(n, b):  # page 249
    q = n
    a = []
    while (q != 0):
        a.append(q % b)
        q = q // b
        pass
    return a

def modularExp(b, n, m):  # page 254
    a = baseExp(n, 2)
    x = 1
    power = b % m
    for i in range(0, len(a)):
        if (a[i] == 1):
            x = (x * power) % m
            pass
        power = (power ** 2) % m
        pass
    return x

def gcd(x, y):  # page 269
    while(y != 0):
        r = x % y   
        x = y
        y = r
    return x

def lcm(x, y):  # http://en.wikipedia.org/wiki/Least_common_multiple
    return int(abs(x * y) / gcd(x, y))

def isPrime(x):  # as describe in lecture video
    sqr = math.sqrt(x)
    for i in range(2, int(sqr) + 1):
        if ((x % i) == 0):
            return False
    return True

def coprime(a, b):
    return gcd(a, b) == 1

'''
def totient(p, q):
    if (not isPrime(p)):
        raise Exception("P is not prime!")
    if (not isPrime(q)):
        raise Exception("Q is not prime!")
    return (p - 1) * (q - 1)
'''
# # ^^ that implementaion is WRONG, it was based on my misreading of wikipedia on the assignment page.

# http://www.usna.edu/Users/math/wdj/_files/documents/book/node15.html
# this is based of this guy's algorithm, but his doens't actually work without slight modification:
# http://forums.codeguru.com/showthread.php?485848-Euler-Totient-Function-Algorithm
def totient(p):
    t = 0
    for i in range(p, 0, -1):
        if (coprime(p, i) == 1):
            t += 1
    return t
''' #totient test.
tne = []
for i in range(1, 11):
    tne.append(totient(i))
print(tne)
#cool, it works.
# '''

# http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
'''
The extended Euclidean algorithm is particularly useful when a and b are coprime,
since x is the modular multiplicative inverse of a modulo b, and y is the modular
multiplicative inverse of b modulo a. This has value in a key calculation of the RSA
public-key encryption algorithm; finding an integer decryption exponent d that is
the modular multiplicative inverse of the chosen encryption exponent e modulo φ(n),
where e and φ(n) are coprime.
'''
def egcd(a, b):
    x, lastX = 0, 1
    y, lastY = 1, 0
    while (b != 0):
        q = a // b
        a, b = b, a % b
        x, lastX = lastX - q * x, x
        y, lastY = lastY - q * y, y
    return (lastX, lastY)

def __chrToNumStr__(letter):
    # print(letter)
    return "{0:02d}".format(alphabet.index(letter))

def __determineSize__(message, n):
    if (n < len(alphabet) - 1):
        raise Exception("n is not sufficiently large")
    tf = ""
    for i in range(0, n, 2):  # for i in range(0, n, 2):
        # Resorting to dirty concatination because I can't get string formatting to work
        tf += str(len(alphabet) - 1)  # default is 25, however this is because it's the zero indexed length of our alphabet.
        # tf += str(25)
        if (int(tf) > int(n)):
            groupSize = len(tf) - 2
            return groupSize

def __rsaEncPadding__(message, n):
    groupSize = __determineSize__(message, n)
    # rslt = zip_longest(*[iter(message)] * groupSize, fillvalue=__chrToNumStr__("Z")) #this isn't working?
    # http://docs.python.org/3/library/itertools.html#itertools-recipes -> grouper
    # Can't get it to work. I must resort to a dirty for-loop.
    rslt = []
    for i in range(0, len(message), groupSize):
        rslt.append("")
        for j in range(0, groupSize):
            if (i + j >= len(message)):
                break  # attempting to "try/except" index out of bounds an extra Z added to the end of the last cell. Why? WHO KNOWS.
            rslt[len(rslt) - 1] += message[i + j]
    while len(rslt[0]) != len(rslt[len(rslt) - 1]):  # DIRTY GROSS ICKY HAAAAAACK
        # rslt[len(rslt) - 1] += __chrToNumStr__("Z")
        rslt[len(rslt) - 1] += __chrToNumStr__(alphabet[len(alphabet) - 1])  # The instructions call for adding a "Z" to the end as padding. I am going to just pad it with the last char instead. This will let me choose a space in my own implementation instead.
    return rslt

def rsaEncrypt(message, n, e):
    if (not coprime(n, e)):
        raise Exception("n and e are not coprime!")
    newMessage = ""
    for i in range(0, len(message)):
        newMessage += __chrToNumStr__(message[i])  # "{0:02d}".format(alphabet.index(message[i]));
    newMessage = __rsaEncPadding__(newMessage, n)
    for i in range(0, len(newMessage)):
        newMessage[i] = "{0:0{lnth}d}".format(modularExp(int(newMessage[i]), e, n), lnth=len(newMessage[i]))  # modularExp(int(newMessage[i]), e, n)
    return "".join(newMessage)    

def rsaDecrypt(message, n, e):
    groupedCells = __rsaEncPadding__(message, n)
    for i in range(0, len(groupedCells)):
        # print(groupedCells[i])
        groupedCells[i] = "{0:0{lnth}d}".format(modularExp(int(groupedCells[i]), e, n), lnth=len(groupedCells[i]))
    msg = "".join(groupedCells)
    decryptedMsg = ""
    for i in range(0, len(msg), 2):
        decryptedMsg += alphabet[int(str(msg[i] + msg[i + 1]))]
    return decryptedMsg

''' #This was a dirty hack. Please do not use these methods ever. 
def __cleanString__(message):
    result = ""
    for i in range(0, len(message)):
        if (message[i].upper() == message[i]):
            result += "_"
        result += message[i].upper()
    return result

def __parseString__(message):
    result = ""
    caps = False
    for i in range(0, len(message)):
        if (message[i] == "_"):
            caps = True
            continue
        if caps == True:
            caps = False
            result += message[i].upper()
        else:
            result += message[i].lower()
    return result
'''

def demoRSA(p, q, e, message):
    n = p * q
    totientN = totient(n)
    if (not 1 < e < totientN):
        raise Exception("Your exponent (e={0}) is larger than or equal to (phi(n)={1}).".format(e, totientN))
    de = (egcd(e, totientN)[0]) % totientN
    print("p={0},q={1},n={2},e={3},phi(n)={4},e & phi(n) coprime?={5},de={6}".format(p, q, n, e, totientN, coprime(e, totientN), de))
    encryptedMessage = rsaEncrypt(message, n, e)
    print("The message \"{0}\"\n\tencrypts to \"{1}\"".format(message, encryptedMessage))
    decryptedMessage = rsaDecrypt(encryptedMessage, n, de)
    print("The cyphertext \"{0}\"\n\tdecrypts to \"{1}\"\n".format(encryptedMessage, decryptedMessage))
    return

# demoRSA(43, 59, 13, "STOP")
alphabet += ".?_'"
alphabet += " "
#we have to make the messages uppercase to compensate for the artificially small p and q values.
msg = "The Queen Can't Roll When Sand is in the Jar".upper()  # The Queen Can't Roll When Sand is in the Jar
demoRSA(61, 53, 17, msg)
demoRSA(61, 53, 17, "Well Hello There. How are you?".upper())
