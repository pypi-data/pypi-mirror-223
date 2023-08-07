## **LinkedList : Simple and efficient way to access LinkedList in python** <br>
[![PyPI version](https://badge.fury.io/py/singly-linkedlist.svg)](https://badge.fury.io/py/singly-linkedlist) 
[![PyPI](https://img.shields.io/pypi/v/singly_linkedlist)](https://pypi.org/project/singly_linkedlist/)
[![PyPI - License](https://img.shields.io/pypi/l/singly_linkedlist)](https://pypi.org/project/singly_linkedlist/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/singly_linkedlist)](https://pypi.org/project/singly_linkedlist/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/singly_linkedlist)](https://pypi.org/project/singly_linkedlist/)
[![PyPI - Status](https://img.shields.io/pypi/status/singly_linkedlist)](https://pypi.org/project/singly_linkedlist/)

![GitHub](https://img.shields.io/github/license/Saqibs575/example)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Saqibs575/example?label=Pull%20Requests)](https://github.com/Saqibs575/example/pulls)
[![GitHub issues](https://img.shields.io/github/issues/Saqibs575/example?label=GitHub%20Issues)](https://github.com/Saqibs575/example/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/Saqibs575/LinkedList)](https://github.com/Saqibs575/LinkedList/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub last commit](https://img.shields.io/github/last-commit/Saqibs575/example)](https://github.com/Saqibs575/example/commits/main)
[![GitHub contributors](https://img.shields.io/github/contributors/Saqibs575/LinkedList)](https://github.com/Saqibs575/LinkedList/graphs/contributors)
[![GitHub code size](https://img.shields.io/github/languages/code-size/Saqibs575/LinkedList)](https://github.com/Saqibs575/LinkedList)
[![GitHub stars](https://img.shields.io/github/stars/Saqibs575/LinkedList)](https://github.com/Saqibs575/LinkedList/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Saqibs575/LinkedList)](https://github.com/Saqibs575/LinkedList/network)
[![GitHub top language](https://img.shields.io/github/languages/top/Saqibs575/LinkedList)](https://github.com/Saqibs575/LinkedList)

-----------------------------
-----------------------------

## **What is it ?**

The **LinkedList** package offers a robust and efficient implementation of a singly linked list data structure in Python. Unlike raw linked lists, this package provides convenient access to elements using indices, allowing for seamless integration with Python's iterable features, such as for loops and other iterable functions. With this package, you can create linked lists and effortlessly access and modify their elements just like you would with lists or tuples.

The primary goal of this package is to bridge the gap between raw linked lists and Python's built-in data structures, making linked lists as user-friendly and versatile as possible. By using this package, you can harness the power of linked lists while enjoying the familiar functionalities offered by Python's native data structures.

---------------------------
---------------------------

## **Table of Contents**

- [Project Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
    + [Creating a linked list](#create-linkedlist)
    + [Inserting Elements](#insert-elements)
    + [Printing Liked List](#print-list)
    + [Accessing Elements](#access-elements)
        * [Access Using for Lopp](#access-elements1)
        * [Linked List as an Iterator](#access-elements2)
    + [Updating Elements](#update-elements)
    + [Concatenation of Linked List](#concate-list)
    + [Basic Operations](#basic-operations)
        * [Finding Length](#basic-operations0)
        * [Reversing Linked List](#basic-operations1)
        * [Multiplying and Dividing Linked List with numeric Value](#basic-operations2)
        * [Sorting Linked List](#basic-operations3)
- [Contributing](#contributing)
- [License](#license)

------------------------------
------------------------------


## **Project Architecture** <a name = 'architecture'></a>

```
WORKSPACE /
    |
    |--> LinkedList /
    |     |
    |     |--> __init__.py
    |     |
    |     |--> base_list.py
    |     |
    |     |--> node.py
    |     |
    |     |--> linked_list.py
    |
    |--> tests /
    |     |
    |     |--> linked_list_test.py
    |
    |--> .gitignore
    |
    |--> LICENSE
    |
    |--> logo.png
    |
    |--> README.md
    |
    |--> requirements.txt
    |
    |--> setup.py

```
---------------------------------
---------------------------------

## **Features** <a name = 'features'></a>
Here are some key features of LinkedList provided by this package :
- Create a new linked list.
- Setting element with indexing.
- Print linked list using print function.
- Insert element in an existing linked list.
- Get the length of the linked list and reverse it.
- Sort the linked list in ascending or descending order.
- Delete elements(Nodes) from the linked list (using index).
- Perform concatenation of two or more LinkedLists (using '+').
- Insert element in an existing linked list at any index of linked list.
- Access and update elements using index (Just like noraml list in python).
- Perform element-wise division with a numeric value (for numeric linked list).
- Perform element-wise multiplication with a numeric value (for numeric linked list).

-------------------------------
-------------------------------


## **Installation** <a name = 'installation'></a>

You can install LinkedList package using pip :
```python
pip install LinkedList

```

---------------------------------
---------------------------------


## **Usage** <a name = 'usage'></a>

The linked list is present in linked_list.py file of LinkedList package. To use linked list in your project, you needed to import. You can import it as follows ;

```python
from LinkedList.linked_list import LinkedList

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


---------------------------------
---------------------------------


## **Creating a linked list** <a name = 'create-linkedlist'></a>

Now , let's create an object of linked list using LinkedList module. It will create an empty linked list :

```python
linked_list = LinkedList()

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

---------------------------------
---------------------------------


## **Inserting Elements** <a name = 'insert-elements'></a>

We have created an empty linked list. Now , we can add elements using `insert()` method :

```python
linked_list.insert(10)         # Append  10 at the end
linked_list.insert(30, 1)      # Inserts 30 at index 1
linked_list.insert(20, 0)      # Inserts 20 at the beginning
linked_list.insert(40,-1)      # Inserts 40 at index -1 (last position)
linked_list.insert(-8,-2)      # Inserts -8 at index -2 (second last position)

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

------------------------------------
------------------------------------


## **Printing Linked List** <a name = 'print-list'></a>

Now we can print each node of linked_list just using print function :

```python
print(linked_list)          # output : 20 --> 10 --> 30 --> -8 --> 40 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

------------------------------------
------------------------------------


## **Accessing Elements** <a name = 'access-elements'></a>

Now we can access each elements of linked_list present at any node using its index(i.e writing index in square braces) as we are accessing in case of normal list in python :

```python
print(linked_list[2])       # Output: 30 (Value at index 2)
print(linked_list[-1])      # Output: 40 (Value of the last element)
print(linked_list[-2])      # Output: -8 (Value of the second last element)
print(linked_list[0])       # Output: 20 (Value at index 0, i.e value of the first element)
print(linked_list[-4])      # Output: 10 (Value at index -4, i.e., value of the fourth last element)
    
```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

------------------------------------
------------------------------------


### **Access Using for Loop** <a name = 'access-elements1'></a>

```python
n = len(linked_list)        # Getting length of linked_list

for i in range(n) :
    print(linked_list[i])

# output: 
# 20 
# 10 
# 30 
# -8 
# 40

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

----------------------------------
----------------------------------


### **Linked List as an Iterator** <a name = 'access-elements2'></a>


As we know that it is very convinient to use and access the element of data structure by using for loop. But in case of linked list we can not directly access elements(data present at the node) using for loop. To solve this problem, I have used `__iter__`  and `__next__` dunder method to make it irerable.


```python
for data in linked_list :
    print(data)

# Output:
# 20 
# 10
# 30
# -8
# 40

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

-----------------------------------
-----------------------------------


## **Updating Elements** <a name = 'update-elements'></a>
Now we can update each elements of linked_list present at any node using its index(i.e writing index in square braces) and assignment as we are updating in case of normal list in python :

```python
linked_list[-1] = 25        # Update element at index -1 (i.e last element) to 25
linked_list[2]  = 50        # Update element at index 2  (i.e third element) to 50
linked_list[0]  = 108       # Update element at index 0  (i.e fist element) to 108
linked_list[-2] = -9        # Update element at index -2 (i.e second last element) to -9
linked_list[-4] = 0         # Update element at index -4 (i.e value of the fourth last element) to 0

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)



Now , let's see the updated linked_list :

```python
print(linked_list)           # output: 108 --> 0 --> 50 --> -9 --> 25 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

------------------------------------
------------------------------------


## **Concatenation of Linked List** <a name = 'concate-list'></a>

We can perform concatenation operation of two or more linked lists by just using '+' operator between them, let's see the example ;

```python
linked_list1 = LinkedList()     # Create linked list
linked_list2 = LinkedList()     # Create linked list

# Let's add the elements to both the linked lists
for i in range(6) :
    linked_list1.insert(i , 0)
for i in range(5) :
    linked_list2.insert(-(i+1) , 0)

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
# Let's print both the linked lists
print('linked_list1 =' ,linked_list1)            # output: linked_list1 = 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> None
print('linked_list2 =' ,linked_list2)            # output: linked_list2 = -5 --> -4 --> -3 --> -2 --> -1 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
# Let's perform concatenation of two linked lists linked_list1 and linked_list2
result1 = linked_list1 + linked_list2
result2 = linked_list2 + linked_list1

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
# Now, let's print concatenated linked list
print('result1 =' , result1)                 # output: result1 = 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> -5 --> -4 --> -3 --> -2 --> -1 --> None
print('result2 =' , result2)                 # output: result2 = -5 --> -4 --> -3 --> -2 --> -1 --> 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
# Let's perform concatenation of more than two linked lists
result3 = linked_list1 + linked_list2 + linked_list

# Now, let's print result3
print('result3 =' , result3)                 # output: result3 = 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> -5 --> -4 --> -3 --> -2 --> -1 --> 108 --> 0 --> 50 --> -9 --> 25 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

------------------------------------
------------------------------------


## **Basic Operations** <a name = 'basic-operations'></a>

In this section, we will perform some basic operations in linked list like finding length , reversing the node and sorting etc.

## **Finding Length** <a name = 'basic-operations0'></a>

As in case of python list or tuple or any other iterable it is an important task to find the number of elements present in the data structure. As finding the number of elements can be very important insight of data structure like we can iterate over the length and so on. We can find the number of elements by using `len()` funtion and we can pass linked list as as argument. This function `len()` will return the number of elements present in the linked list or we can say that it is a length of linked list.

```python
# Finding length of linked lists
print(len(linked_list ))        # output: 5
print(len(linked_list1))        # output: 6
print(len(linked_list2))        # output: 5
print(len(result1))             # output: 11
print(len(result2))             # output: 11
print(len(result3))             # output: 16

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

----------------------------------
----------------------------------


## **Reversing Linked List** <a name = 'basic-operations1'></a>
We have performed reverse operations many time in case of python iterables like list or tuple. Similarly, we can use the same function that is `reversed()` to reverse node of linked list. In this function `reverse()` we need to pass linked list as an argument. 

```python
# Reversing nodes of linked lists
print('Before reversing : linked_list =' , linked_list)             # output: Before reversing : linked_list = 108 --> 0 --> 50 --> -9 --> 25 --> None
reversed(linked_list)
print('After reversing : linked_list ='  , linked_list)             # output: After reversing : linked_list = 25 --> -9 --> 50 --> 0 --> 108 --> None
```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
print('Before reversing : linked_list1 =' ,linked_list1)             # output: Before reversing : linked_list1 = 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> None
reversed(linked_list1)
print('After reversing : linked_list1 ='  ,linked_list1)             # output: After reversing : linked_list1 = 0 --> 1 --> 2 --> 3 --> 4 --> 5 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
print('Before reversing : linked_list2 =' ,linked_list2)             # output: Before reversing : linked_list2 = -5 --> -4 --> -3 --> -2 --> -1 --> None
reversed(linked_list2)
print('After reversing : linked_list2 ='  ,linked_list2)             # output: After reversing : linked_list2 = -1 --> -2 --> -3 --> -4 --> -5 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
print('Before reversing : result1 ='     , result1)                 # output: Before reversing : result1 = 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> -5 --> -4 --> -3 --> -2 --> -1 --> None
reversed(result1)
print('After reversing : result1 ='      , result1)                 # output: After reversing : result1 = -1 --> -2 --> -3 --> -4 --> -5 --> 0 --> 1 --> 2 --> 3 --> 4 --> 5 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
print('Before reversing : result2 ='     , result2)                 # output: Before reversing : result2 = -5 --> -4 --> -3 --> -2 --> -1 --> 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> None
reversed(result2)
print('After reversing : result2 ='      , result2)                 # output: After reversing : result2 = 0 --> 1 --> 2 --> 3 --> 4 --> 5 --> -1 --> -2 --> -3 --> -4 --> -5 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
print('Before reversing : result3 ='     , result3)                 # output: Before reversing : result3 = 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> -5 --> -4 --> -3 --> -2 --> -1 --> 108 --> 0 --> 50 --> -9 --> 25 --> None
reversed(result3)
print('After reversing : result3 ='      , result3)                 # output: After reversing : result3 = 25 --> -9 --> 50 --> 0 --> 108 --> -1 --> -2 --> -3 --> -4 --> -5 --> 0 --> 1 --> 2 --> 3 --> 4 --> 5 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

------------------------------------
------------------------------------


### **Multiplying and Dividing linked list with numeric value** <a name = 'basic-operations2'></a>
We know that in numpy we can multilpy or divide array(numeric) with any numeric value, as a result the we will get an array in which all the elements of numpy array will be multiplied or divided by the number we have provided. Same operation can be performed on this LinkedList 

```python
# Multiplying Linked List by any numeric value
print('Before multiplication : linked_list =' , linked_list)        # output: Before multiplication : linked_list = 25 --> -9 --> 50 --> 0 --> 108 --> None
linked_list*2
print('After multiplication : linked_list ='  , linked_list)        # output: After multiplication : linked_list = 50 --> -18 --> 100 --> 0 --> 216 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)


```python
# Dividing Linked List by any numeric value
print('Before division : linked_list =' , linked_list)              # output: After division : linked_list = 50 --> -18 --> 100 --> 0 --> 216 --> None
linked_list / 2
print('After division : linked_list ='  , linked_list)              # output: After division : linked_list = 25.0 --> -9.0 --> 50.0 --> 0.0 --> 108.0 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

--------------------------------------
--------------------------------------


### **Sorting Linked Lists**  <a name = 'basic-operations3'></a>
Sorting is one of the most important part in case of oterables. As we have many options to sort LinkedList. But, here we will use merge sort that will provide time complexity of nlog(n) and space complexity is constant.


#### **Sorting Linked Lists in ascending order**

```python
print('Before sorting : linked_list2 =' , linked_list2)              # output: After sorting : linked_list2 = -1 --> -2 --> -3 --> -4 --> -5 --> None
linked_list2.sort()
print('After sorting : linked_list2 ='  , linked_list2)              # output: After sorting : linked_list2 = -5 --> -4 --> -3 --> -2 --> -1 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)



#### **Sorting Linked Lists in descending order**

```python
print('Before sorting : linked_list1 =' , linked_list1)              # output: After sorting : linked_list1 = 0 --> 1 --> 2 --> 3 --> 4 --> 5 --> None
linked_list1.sort(reverse = True)
print('After sorting : linked_list1 ='  , linked_list1)              # output: After sorting : linked_list1 = 5 --> 4 --> 3 --> 2 --> 1 --> 0 --> None

```
[CLICK HERE FOR CODE'S OUTPUT](https://github.com/Saqibs575/LinkedList/blob/main/examples.ipynb)

-------------------------------------
-------------------------------------


## **Contributing** <a name = 'contributing'></a>

Contributions to the LinkedList package are welcome! If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request on GitHub.

-------------------------------------
-------------------------------------


## **License** <a name = 'license'></a>

© 2023 Saqib Shaikh

This package is distributed under the GNU General Public License v3.0 (GPLv3) License. See the [LICENSE](https://github.com/Saqibs575/LinkedList/blob/main/LICENSE) file for more details.
