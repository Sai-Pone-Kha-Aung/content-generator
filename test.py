
"""Can you implement a binary search algorithm in Python to find an element in a sorted array?
Show both the pseudocode and working code, and explain how it achieves O(log n) time complexity!"""

#pseudocode:
"""
BinarySearch(array, target, low, high):
    IF LOW > HIGH: ဖြစ်ရင်
        RETURN -1 

    အလည်ကိန်းကိုရှာမယ်ဆိုရင်
    mid = (low + high) / 2
    
    အလည်ကိန်းက target နဲ့တူရင်
    IF array[mid] == target:
        RETURN mid 
    IF array[mid] < target:
        recursive call လုပ်မယ်
        BinarySearch(array, target, mid + 1, high)
    IF array[mid] > target:
        recursive call လုပ်မယ်
        BinarySearch(array, target, low, mid - 1)
"""

def binary_search(array, target, low, high):
    if low > high:
        return -1
    
    mid = (low + high) // 2
    
    if array[mid] == target:
        return mid
    if array[mid] < target:
        return binary_search(array, target, mid + 1, high)
    if array[mid] > target:
        return binary_search(array, target, low, mid - 1)
    
# Test Case
# question က sorted array ဖြစ်ရမယ်ပြောထားတဲ့အတွက်ကြောင့်
arr = [2,3,4,10,40,50,60,70]
target = 10
result = binary_search(arr, target, 0, len(arr) - 1)
print(f"Element found at index: {result}" if result != -1 else "Element not found")