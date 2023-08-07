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