print("=============")
print("Welcome here")
print("My first post!")
print("=============")

username = "cool blogger"
bio = "Fun Blogger"
followers = 100

username = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("=================")
print("Username: ", username)
print("Bio: ", bio)
print("Category: ", category)

if age>40 and category == "fun":
    print("You are old what is fun for you??")

followers += 50
print("Day 1: ", followers)

followers += 20
print("Day 2: ", followers)

followers -= 10
print("Day 3: ", followers)

print("Followers: ", followers)