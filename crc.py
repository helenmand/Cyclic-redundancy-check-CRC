import random
import numpy as np

N = 10000

# digits: binary message size.
def binaryMessageGenerator(digits):
    # filling the array with 0s and 1s.
    # the size of the array is equal to "digits".
    # the probability to get 1 and 0 is 50-50.
    arr = np.random.choice([0, 1], size=digits, p=[1/2, 1/2])

    message = ''
    for element in arr:
        message += str(element)

    return message

# message: the message that needs to be checked if it contains an error.
# polynomial: the polynomial used to create the crc.
def CRCcheck(message, polynomial):
    divResult = mod2div(message, polynomial)
    for bit in divResult:
        if bit == '1': # if there is 1 in the result of the division
            return 1   # it means that there is an error.
    return 0 # if there are no 1s, the is no remainder so there is no error.

# xor without carries between 
# a & b: binary numbers
def xor(a, b):
    result = []
    for i in range(0, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return result

# perform modulo-2 division -> divident/divisor
def mod2div(divident, divisor):
    index = len(divisor) # indicates the end of the divident that is xored so it can match the size of the divisor.
    divident += '0'*(index-1)
    temp = divident[0 : index] # adding the number to a temporary variable.
    temp = xor(divisor, temp) # performing xor.

    # loop ends if it reaches the end of the divident
    # or when the remainder is smaller in size than the divisor 
    # which means that it has at least a digit at the beginning that is 0.
    while index < len(divident) or temp[0] == '1':
        # if the 1st digit of the temporary divident is 0, we need to use the rest
        # digits of the original divident.
        if temp[0] == '0': 
            temp = temp[1:index] 
            temp += divident[index]
            index += 1
        else:   
            # when the temporary divident can still be xored we perform xor.
            temp = xor(divisor, temp)
    result = ''.join(temp[1:index]) 
    return result

# simulation of a noise canal.
# message: the binary message that goes through the canal.
# BER: the probability of a bit having an error (bit error rate).
def noiseCanal(message, BER):
    temp = '' # the message that is going to be returned. 
    isMutated = 0 # is 0 if the message is not mutated, and 1 if it is.
    for bit in message:
        probability = random.uniform(0.0, 1.0) # getting a number between 0 and 1.
        if probability < BER: # if the number is less than the bit error rate, the message gets mutated.
            isMutated = 1
            if bit == '0':
                temp += '1'
            else: 
                temp += '0'
        else:
            temp += bit
    return str(temp), isMutated
   
digits = int(input("Digits: "))
polynomial = str(input("Polynomial: "))
BERex = int(input("bit error rate, please type an negative number (exponent): "))
BER = 10**(BERex)

# MESSAGE CREATION
messages = []
for i in range(N):
    messages.append(binaryMessageGenerator(digits))

# sender's side
sentMessages = [message + mod2div(message, polynomial) for message in messages]

# noise canal
mutatedMessages = 0 # affected messages
noisedMessages = [] # messages to be sent
for message in sentMessages:
    noisedMessage, isMutated = noiseCanal(message, BER)
    mutatedMessages += isMutated
    noisedMessages.append(noisedMessage)

# receiver's side
CRCDetectedMutatedMessages = 0
for message in noisedMessages:
    isMutated = CRCcheck(message, polynomial)
    CRCDetectedMutatedMessages += isMutated

# output
if mutatedMessages == 0:
    print("zero mutated")
else:
    print("percentage of mutated messages: " 
            + str(100*mutatedMessages/N))
    print("percentage of detected mutated messages: " 
            + str(100*CRCDetectedMutatedMessages/mutatedMessages))
    print("percentage of non detected mutated messages: " 
            + str(100*(mutatedMessages - CRCDetectedMutatedMessages)/mutatedMessages))
