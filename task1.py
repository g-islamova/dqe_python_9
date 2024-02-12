import random

# create list of 100 random numbers from 0 to 1000:
random_nums = [random.randint(0, 1000) for i in range(100)]


# sort list from min to max (without using sort()):
def my_bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # last elements put in place
        for j in range(0, n - i - 1):
            # go through the array from 0 to n-i-1 and
            # swap if the element found is greater than the next one
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# sort list of random numbers
my_bubble_sort(random_nums)

# calculate average for even and odd numbers, print both results in console

# declare variables to store result:
even_sum = 0
even_count = 0
odd_sum = 0
odd_count = 0

# Iterate through the list to calculate sum and count for even and odd numbers
for num in random_nums:
    if num % 2 == 0:  # Check if the number is even
        even_sum += num
        even_count += 1
    else:
        odd_sum += num
        odd_count += 1

# Calculate average for even and odd numbers using try-except block to handle division by zero:
try:
    avg_even = even_sum / even_count
except ZeroDivisionError:
    avg_even = 0

try:
    avg_odd = odd_sum / odd_count
except ZeroDivisionError:
    avg_odd = 0

# Print the averages
print("Average for even numbers:", avg_even)
print("Average for odd numbers:", avg_odd)
