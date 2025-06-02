nums = [1,2,3,4,5]
i=0
while i != len(nums):
    i += i
    popprint = nums.pop(i)
    print(popprint)

print("Lista:",nums)