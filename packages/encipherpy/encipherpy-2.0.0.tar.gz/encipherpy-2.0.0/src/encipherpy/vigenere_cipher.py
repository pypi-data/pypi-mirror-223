from .internal.string_number_convert import stringToNumbers, numbersToString
from encipherpy.internal.rebuild_key import rebuildKey

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