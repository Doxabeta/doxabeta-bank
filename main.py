import os #os module used to clear the screen for aesthetic reasons
import random #used to generate random numbers for the bank details

global currentUser #sentry variable to prevent crashes
currentUser = ""

#RNG for generating account numbers, sort codes and security codes
def RNG(string, num):
  for _i in range(num):
    rand = random.randrange(1,10)
    string += str(rand)
  return string

#string length validation function
def lengthValidation(string,limit):
  valid = True
  if len(string) < limit:
    valid = False
  return valid

#list contains user accounts
applicationAccounts = ["benson","ilovecake","example@gmail.com",
"Joshua","helloworld","example@yahoo.com"]
#list containing bank accounts
bankAccounts = ["Joshua", "FlexOne", "012345678910","334653","567",1000, 
"Joshua", "SaverPlus","098765432109","112233","345",100,
"benson", "FlexOne","123409871235","336655","654",200]

#validation function for login function
def validateExistingUser(username, password):
  return username in applicationAccounts and password == applicationAccounts[applicationAccounts.index(username) + 1]

#main menu when the user starts the app
def mainMenu(): 
  os.system("clear") #clear the screen
  print("Welcome to Doxabeta Bank. Please select a menu option.") #welcome message
  print("1. Sign Up\n2. Log in\n3. Quit\n") #menu options
  userChoice = input(": ")
  while userChoice not in ("1","2","3"): #validation
    print("Invalid input. Please enter 1 to 3.")
    userChoice = input(": ")
  if userChoice == "1": #call sign up function 
    signUpPage()
  elif userChoice == "2": #call log in function
    logInPage()
  elif userChoice == "3": #log out user by terminating current function
    input("Goodbye! Thank you for choosing Doxabeta bank. Press the enter key to exit.")
    exit()
  else: #catch-all
    print("An unexpected error occured.")

#menu for logged in users
def userMenu():
  os.system("clear") #clear the screen
  print("Welcome to your account,",currentUser +"! Please select a menu option.") #menu system
  print("""
  1. View account balance
  2. Pay or move money
  3. Create new bank account
  4. Log out\n""")
  userChoice = input(": ")
  while userChoice not in ("1","2","3","4"): #validation
    print("Invalid input. Please enter 1, 2, 3 or 4.")
    userChoice = input(": ")
  if userChoice == "1": #find the user's account balance by calling function
    balance = findAccountBalance(currentUser)
    if balance is not False:
      print(f"Your current account balance is: £{balance}")
      input("Press enter to return to main menu.")
      userMenu()
    else: #error handling
      print("""Something went wrong. 
We can't seem to find your account balance. You may not have one. Directing you back to main menu.""")
      input("Press enter to return to main menu.")
      userMenu()
      exit()
  elif userChoice == "2": #pay money function
    moveMoney(currentUser)
  elif userChoice == "3": #create bank account function
    newAccount()
  elif userChoice == "4": #log out function
    input("Logging you out. Press enter key to continue.")
    mainMenu()
    exit()
  else: #catch-all
    input("An unexpected error occured. Press enter key to return to home page.")
    mainMenu()

#sign up page for new users
def signUpPage():
  os.system("clear") #clear the display for aesthetic reasons
  print("SIGN UP FOR AN ACCOUNT WITH US")
  username = input("Username: ")
  while lengthValidation(username, 2) is False: #validation
    print("Username invalid. Please try again.")
    username = input("Username: ")
  password = input("Password: ")
  while lengthValidation(password, 8) is False: #validation
    print("Password must be 8 characters or more. Please try again.")
    password = input("Password: ")
  #need to check whether the user already exists
  if validateExistingUser(username, password) is True:
    input("""
Looks like your account already exists.
Press the enter key to return to the main menu. 
Please select log in.""")
    mainMenu()
    exit()
  email = input("Email address: ")
  while "@" not in email: #validation
    print("Not a valid email")
    email = input("Email address: ")
  print("Details validated. Press enter to access your account.")
  input()
  #append these details to the database list
  applicationAccounts.extend([username, password, email])
  global currentUser
  currentUser = username
  userMenu()

#log in page for existing users
def logInPage():
  os.system("clear")
  print("LOG IN TO YOUR ACCOUNT")
  username = input("Username: ")
  password = input("Password: ")
  while validateExistingUser(username, password) is False: #validation
    print("Username or password is incorrect. Try again.")
    username = input("Username: ")
    password = input("Password: ")
  print(f"Login successful. Welcome, {username}! Press enter to access your account")
  input()
  global currentUser
  currentUser = username
  userMenu()

#searching algorithm for finding balance for a specific account
def findAccountBalance(currentUser):
  if currentUser in bankAccounts: #first check if the user actually has a bank account
    whichAccount = input("Which account do you want to view the balance for?: ")
    if whichAccount in bankAccounts: #this algorithm finds the specific account which the user wants to access and returns its balance.
      for i in range(len(bankAccounts)):
        if bankAccounts[i] == currentUser and bankAccounts[i+1] == whichAccount:
          return bankAccounts[i+5]
        else:
          continue
    return False
  else:
    return False

#move money from one account to either user's other bank accounts or another person or company
def moveMoney(currentUser):
  os.system("clear")
  print("PAY OR MOVE MONEY")
  senderAccountName = input("""Please enter which account you
would like to move money from: """)
  if senderAccountName in bankAccounts: #validation that selected account actually exists
      print("\nAccount validated.")
      senderAccountNo = bankAccounts[bankAccounts.index(senderAccountName) + 1]
      senderAccountSortCode = bankAccounts[bankAccounts.index(senderAccountName) + 2] 
  else:
    input("""\nSomething went wrong. We can't seem to find your 
account. It might not exist. Press enter to return to the main
menu.""")
    userMenu()
    exit()
  print("\nSelected account details:") #print out the account details
  print(f"Name: {senderAccountName}")
  print(f"Account number: {senderAccountNo}")
  print(f"SortCode: {senderAccountSortCode}")
  amount = input("\nPlease enter the amount you would like to pay in £")  #this algorithm allows user to enter amount and ensure they have entered a number so it can be processed.
  while True:
    try:
      amount = int(amount)
    except ValueError:
      print("\nSorry, your input is not valid. Try again.")
      amount = input("\nPlease enter the amount you would like to pay in £") 
    else:
      amount = int(amount)
      break
  #selection of where to transfer the money to 
  print("""\nWho would you like to pay money to? 
  1. One of your bank accounts
  2. A person or company""")
  userChoice = input(": ") #menu system
  while userChoice not in ("1","2"): #validation
    print("Invalid input. Please enter 1 or 2.")
    userChoice = input(": ")
  if userChoice == "1": #if the user chooses to move money between accounts
    recipientAccountName = input("""\nPlease enter which account 
you would like to send money to: """)
    if currentUser in bankAccounts and recipientAccountName in bankAccounts: #check if their input actually exists and retrieve number,sort code
        print("\nAccount validated.")
        recipientAccountNo = bankAccounts[bankAccounts.index(recipientAccountName) + 1]
        recipientAccountSortCode = bankAccounts[bankAccounts.index(recipientAccountName) + 2]
    else:
      input("""\nSomething went wrong.
We can't seem to find your account. It might not exist. 
Press enter to return to the main menu.""")
      userMenu()
      exit()
  elif userChoice == "2": #move money to another person
    recipientAccountName = input("\nPlease enter the recipient's account holder name in capitals: ")
    while recipientAccountName != recipientAccountName.upper(): #validation
      print("Invalid input. Input must be in upper case.")
      recipientAccountName = input(": ")
    #the following algorithm checks whether the entered account details are valid
    #it also checks whether the user has decided to spam the program by entering their own details 
    while True:
      recipientAccountNo = input("Please enter the recipient's account number: ")
      if lengthValidation(recipientAccountNo,12) is False or recipientAccountNo.isnumeric() is False:
        print("Invalid account number")
      else:
        flag = True
        for i in range(len(bankAccounts)):
          if bankAccounts[i] == currentUser and bankAccounts[i+2] == recipientAccountNo:
            print("You can't send money to your own account using this function. Please try again.")
            flag = False
            break
        if flag:
          break
        else:
          continue     
    while True: #do validation checks for sort code as well
      recipientAccountSortCode = input("Please enter the recipient's account sort code: ")
      if lengthValidation(recipientAccountSortCode,6) is False or recipientAccountSortCode.isnumeric() is False:
        print("Input not valid. Try again.")
        continue
      else:
        break
  else: #catch-all
    input("An unexpected error occurred. Press enter to return to main menu.")
    mainMenu()
    exit()
  print("\nRecipient account details:") #print out recipient account details
  print(f"Name: {recipientAccountName}")
  print(f"Account number: {recipientAccountNo}")
  print(f"SortCode: {recipientAccountSortCode}")
  #payment with validation
  if bankAccounts[bankAccounts.index(senderAccountName) + 4] - amount < 0:
    input("""\nSorry, your account balance is too low to complete this transaction. 
Press the enter key to return to the main menu.""")
    userMenu()
    exit()
  else:
    bankAccounts[bankAccounts.index(senderAccountName) + 4] -= amount
    if recipientAccountName in bankAccounts: #pay money
      bankAccounts[bankAccounts.index(recipientAccountName) + 4] += amount
    else:
      pass
  input("\nTransaction complete. Press the enter key to return the the main menu.")
  userMenu()

#create a new bank account
def newAccount():
  availableAccounts = ["FlexOne","SaverPlus","KeepitSafe"]
  print("CREATE A NEW BANK ACCOUNT")
  print("Please make a selection from the following list of account types.") #user has to select an account from the menu
  for i in availableAccounts:
    print(i)
  accountSelection = input(": ")
  while accountSelection not in availableAccounts:
    print("Sorry, seems that your selection is not available. Try again.")
    accountSelection = input(": ")
  newAccountNumber = RNG("",12) #initialise account details
  newAccountSortCode = RNG("",6)
  newAccountSecurityCode = RNG("",3)
  bankAccounts.extend([currentUser, accountSelection,
  newAccountNumber,newAccountSortCode,newAccountSecurityCode,0]) #add account details to the database list
  print("Your new account details:") #print out details
  print("Name:",accountSelection)
  print("Account number:",newAccountNumber)
  print("Sort code:",newAccountSortCode)
  print("Security code:",newAccountSecurityCode)
  print("Initial balance: £0")
  input("Thank you for choosing Doxabeta Bank. Press enter to return to the main menu.")
  userMenu()
  
#kick off the program by calling this function
mainMenu()
