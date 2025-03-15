from practice.BankAccount import BankAccount  
"""
Write a Python program that can do the following:

- You have $50

- You buy an item that is $15, that has a 3% tax

- Using the print()  Print how much money you have left, after purchasing the item.

"""

"""
String Assignment. (This can be tricky so feel free to watch solution so we can do it together)

- Ask the user how many days until their birthday

- Using the print()function. Print an approx. number of weeks until their birthday

- 1 week is = to 7 days.

"""


# String Assignment solution 1
money = 50
expense = 15
tax = 0.03
totalExpenses = expense + (expense * tax)
balance  = money - totalExpenses
print(balance)


"""
Lists Assignment
- Create a list of 5 animals called zoo

- Delete the animal at the 3rd index.

- Append a new animal at the end of the list

- Delete the animal at the beginning of the list.

- Print all the animals

- Print only the first 3 animals
"""
# Lists Assignment solution
zoo = ["Cat", "Dog", "Cow", "Sheep", "Chickens" ]
zoo.remove('Sheep')
zoo.pop(3)
zoo.append("Goat")
zoo.pop(0)


"""
If Else Assignment
- Create a variable grade holding an integer between 0 - 100

- Code if, elif, else statements to print the letter grade of the number grade variable

Grades:

A = 90 - 100

B = 80 - 89

C = 70-79

D = 60 - 69

F = 0 - 59

"""

# If Else Assignment solution
grade = 49
if grade  >= 90:
    print("A")
elif grade >= 80:
    print("B")
elif grade >= 70:
    print("C")
elif grade >= 60:
    print("D")
else:
    print("F")

# For Loop Assignment
"""
Given: my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

- Create a while loop that prints all elements of the my_list variable 3 times.

- When printing the elements, use a for loop to print the elements

- However, if the element of the for loop is equal to Monday, continue without printing
"""

# For Loop Assignment solution
my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
i = 0
while i < 3:
    for day in my_list:
        if day == "Monday":
            continue
        # print(day)
    i += 1

#Dictionary Assignment
"""
Based on the dictionary:
* 		my_vehicle = {
* 		"model": "Ford",
* 		"make": "Explorer",
* 		"year": 2018,
* 		"mileage": 40000
* 		}
- Create a for loop to print all keys and values
- Create a new variable vehicle2, which is a copy of my_vehicle
- Add a new key 'number_of_tires' to the vehicle2 variable that is equal to 4
- Delete the mileage key and value from vehicle2
- Print just the keys from vehicle2
"""

# Dictionary Assignment solution
my_vehicle = {
    "model": "Ford",
    "make": "Explorer",
    "year": 2018,
    "mileage": 40000
}

for key, value in my_vehicle.items():
    # print(key, value)
    pass

vehicle2 = my_vehicle.copy()
vehicle2["number_of_tires"] = 4
del vehicle2["mileage"]
# print(vehicle2.keys())



bankAccount = BankAccount('Aminat', 1000)
bankAccount.deposit(500)
accHol = bankAccount.account_holder
bal = bankAccount.get_balance()
print(f"Account Holder: {accHol}  Balance: {bal}")