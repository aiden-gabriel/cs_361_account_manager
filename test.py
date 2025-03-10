import os
import time

FILE = "am_comm.txt"

response = []

# Test 1
with open(FILE, "w") as file:
    file.write("1, user1, pass1")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 1 Response: {response}")

# Test 2
with open(FILE, "w") as file:
    file.write("1, user1, pass2")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 2 Response: {response}")

# Test 3
with open(FILE, "w") as file:
    file.write("0, user1, pass1")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 3 Response: {response}")

# Test 4
with open(FILE, "w") as file:
    file.write("0, user1, pass2")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 4 Response: {response}")

# Test 5
with open(FILE, "w") as file:
    file.write("0, user2, pass2")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 5 Response: {response}")

# Test 6
with open(FILE, "w") as file:
    file.write("2, user2, pass2")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 6 Response: {response}")

# Test 7
with open(FILE, "w") as file:
    file.write("2, user1, pass1")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 7 Response: {response}")

# Test 8
with open(FILE, "w") as file:
    file.write("1, user2, pass2")
time.sleep(5)

with open(FILE, "r") as file:
    response = file.read()
print(f"Test 8 Response: {response}")
