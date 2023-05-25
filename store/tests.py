# from django.test import TestCase

# Create your tests here.

oscar =  {'6': {'title': 'T-Shirt', 'qty': 2}, '1': {'title': 'Headphones', 'qty': '1'}, '5': {'title': 'Shoes', 'qty': 7}}


# Dictionary Methods
# marks = {}.fromkeys(['Math', 'English', 'Science'], 0)

# Output: {'English': 0, 'Math': 0, 'Science': 0}
# print(marks)
number_final = 0
for item in oscar.values():
    final = int(item['qty'])
    number_final += final
print(number_final)

# Output: ['English', 'Math', 'Science']
# print(list(sorted(marks.keys())))
