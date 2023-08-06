def rebuildKey(plainText, key):
  targetLength = len(plainText)
  keyBoundary = (len(key) - 1)

  newKey = []

  keyPosition = 0
  for i in range(0, targetLength):
    if plainText[i] == " ":
      keyToAdd = " "
    else:
      keyToAdd = key[keyPosition]
      if keyPosition == keyBoundary:
        keyPosition = 0
      else:
        keyPosition += 1
    newKey.append(keyToAdd)
  return "".join(newKey)

def stringToNumbers(string):
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  numberList = []
  for letter in string.lower():
    if letter == " ":
      number = 1000
    else:
      number = alphabet.find(letter)
    numberList.append(number)
  return numberList

def numbersToString(numbers):
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  letterList = []
  for number in numbers:
    if number == 1000:
      letter = " "
    else:
      letter = alphabet[int(number)]
    letterList.append(letter)
  return "".join(letterList)

def vigenereCipher(plainText, key, encrypt = True):
  plainTextLength = len(plainText)
  key = rebuildKey(plainText, key)

  numberList = stringToNumbers(plainText)
  numericKey = stringToNumbers(key)
  cipherNumbers = []
  
  for i in range(0, plainTextLength):
    plainNumber = numberList[i]
    shift = numericKey[i]

    if plainNumber == 1000:
      cipherNumbers.append(1000)
    else:
      if encrypt == True:
        shiftedNumber = (plainNumber + shift) % 26
      else:
        shiftedNumber = (plainNumber - shift) % 26
      cipherNumbers.append(shiftedNumber)

  cipherText = numbersToString(cipherNumbers)
  return cipherText