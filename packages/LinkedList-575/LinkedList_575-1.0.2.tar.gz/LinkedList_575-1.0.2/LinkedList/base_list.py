from LinkedList.node import Node
from typing import Union
from typing import Tuple
from typing import List
from copy import copy

class BaseList :
    """
    A custom implementation of a singly LinkedList.

    Attributes:
        __len (int): Private attribute to store the length of the LinkedList
        head (Node or None): Reference to the first node (head) of the LinkedList.

    Methods:
        __init__(): Initializes an empty LinkedList with head set to None.
        show(): Prints the elements of the LinkedList in a human-readable format.

    Example:
        # Create a new LinkedList
        linked_list = BaseList()

        # Add elements to the LinkedList
        linked_list.head = Node(1)
        second_node = Node(2)
        third_node = Node(3)

        linked_list.head.next = second_node
        second_node.next = third_node
    """
    # Set initial length of LinkedList as 0
    __len = 0
    __index = 0
    __index_ptr = None

    def __init__(self) -> None:
        """
        Initializes an empty LinkedList with head set to None.

        Parameters :
            None

        Returns:
            None
        """
        self.__head = None

    @property
    def head(self) -> Union['Node' , None] :
        """
        Get the reference to the first node (head) of the LinkedList.

        Returns:
            Node or None: The head node of the LinkedList or None if the list is empty.
        """
        return self.__head

    @property
    def len(self) -> int:
        """
        Get the length of the LinkedList.

        Returns:
            int: The number of nodes in the LinkedList.
        """
        return self.__len

    def _show(self) -> str:
        """
        Prints the elements of the LinkedList in a human-readable format.

        Returns:
            str: A string representation of the LinkedList.

        Example:
            # Create a new LinkedList
            linked_list = LinkedList()

            # Add elements to the LinkedList
            linked_list.head = Node(1)
            second_node = Node(2)
            third_node = Node(3)

            linked_list.head.next = second_node
            second_node.next = third_node

            # Show the LinkedList
            print(linked_list)
            # Output: 1 --> 2 --> 3 --> None

        Note:
            If Lopp is Detected then it will print the last two printed elements will represents the loop. In this case end of Node will not be None.
        """

        # If the LinkedList is empty, return an appropriate message
        if self.__head == None :
            return "LinkedList is Empty"

        # Print each node's data with an arrow separator
        temp = self.__head

        # Set variable to print all the value 
        count , n = 0 , len(self)
        while count < n :
            print(temp.data , end = ' --> ')
            temp = temp._next
            count += 1

        # If Lopp is Detected then 
        if temp :
            print(temp.data , end = ' ')
            return '(<<<<<<   Loop is Detected   >>>>> )'

        # Print 'None' to indicate the end of the LinkedList
        return 'None'
        
    def insert(self , 
        data : Union[int , List[int] , Tuple[int]] = None , 
        index : int = None
        ) -> None :

        """
        Insert an element at the specified index in the LinkedList.

        Parameters:
            data (int or list or tuple): The element or iterable containing elements to be inserted into the LinkedList.
                - If 'data' is a single integer, it will be inserted as a single node.
                - If 'data' is a list or tuple, each element in the iterable will be inserted as individual nodes.
                The order of insertion will be maintained from left to right.

            index (int, optional): Index at which the element(s) will be added. If not provided (default is None),
                                   the element(s) will be appended at the end of the LinkedList. Negative indexing 
                                   can be used just like in normal lists.

        Returns:
            None

        Notes:
            - If the index is not provided (None), the element(s) will be appended at the end of the LinkedList.
            - Negative indexing can be used, similar to normal lists in Python.
            - The indexing should be in the range of [-len(LinkedList), len(LinkedList)].
            Otherwise, this function will raise an IndexError.

        Example:
            # Create a LinkedList and insert elements at different indices
            linked_list = BaseList()

            # Single element insertion
            linked_list.insert(10)      # Appends 10 at the end
            linked_list.insert(20, 0)   # Inserts 20 at the beginning
            linked_list.insert(30, 2)   # Inserts 30 at index 2
            linked_list.insert(40, -1)  # Inserts 40 at index -1 (last position)

            # Multiple elements insertion using a list or tuple
            linked_list.insert([50, 60, 70], 3)  # Inserts [50, 60, 70] starting from index 3
            linked_list.insert((80, 90), -2)     # Inserts [80, 90] starting from second-to-last index
        """

        # Make last index as default index if index is not Provided.
        if index == None :
            index = self.__len                       

        # Support negative indexing
        if index < 0 :

            # Convert negative index into equivalent positive index.
            index = self.__len + index + 1             
        
        # If index is out of range then raise IndexError Exception
        if index < 0 or index > self.__len :
            raise IndexError('Index Out Of Range')

        # If multiple elements needs to be added using list or tuple, call __insert_many method.
        if type(data) == list or type(data) == tuple :
            return self.__insert_many(data, index)
        
        # If index is 0 or LinkedList is empty, add element at the first position.
        if self.__head == None or index == 0 :
            new_node = Node(data)
            new_node._next , self.__head = self.__head , new_node

            # Update the current length of LinkedList by 1 as element was successfully added
            self.__len += 1
            return 

        # Create a new node for the data which is to be inserted      
        new_node = Node(data)

        # Keep track of prev node and curr node until reach to the required index
        prev , curr , count = None , self.__head , 0
        while count < index :
            prev , curr = curr , curr._next
            count += 1       

        # Now add the new node to the specified index
        prev._next , new_node._next = new_node , curr
        
        # Update the current length of LinkedList by 1 as element was successfully added
        self.__len += 1

    def __insert_many(self ,
        data : Union[List[int] , Tuple[int]] , 
        index : int
        ) -> None :

        """
        Insert multiple elements at the specified index in the LinkedList.

        Parameters:
            data (list or tuple): The list or tuple containing elements to be inserted into the LinkedList.
            index (int): Index at which the elements will be added.

        Returns:
            None

        Notes:
            - The 'data' parameter should be a list or tuple containing integers.
            - The elements in the 'data' list/tuple will be inserted as individual nodes in the LinkedList.
            - The order of insertion will be maintained from left to right, i.e., the first element in 'data' will be the first node inserted.
            - If the LinkedList is empty or 'index' is 0, the elements will be inserted at the beginning of the LinkedList.
            - If 'index' is out of range, the elements will be appended at the end of the LinkedList.
            - Negative indexing can be used for 'index', similar to normal lists in Python.
            - The indexing should be in the range of [-len(LinkedList), len(LinkedList)].

        Example:
            # Create a LinkedList and insert multiple elements at different indices
            linked_list = BaseList()

            linked_list.insert(10)      # Appends 10 at the end
            linked_list.insert(20, 0)   # Inserts 20 at the beginning
            linked_list.insert(30, 2)   # Inserts 30 at index 2
            linked_list.insert(40, -1)  # Inserts 40 at index -1 (last position)

            # Insert multiple elements using a list or tuple
            linked_list.__insert_many([50, 60, 70], 3)  # Inserts [50, 60, 70] starting from index 3
            linked_list.__insert_many((80, 90), -2)     # Inserts [80, 90] starting from second-to-last index
        """

        # Create the first node and the last node for the elements in 'data'
        first_node = Node(data[0])
        last_node = first_node

        # Iterate through 'data' to create individual nodes and link them
        for ele in data[1 : ] :
            last_node._next = Node(ele)
            last_node = last_node._next

        # If LinkedList is empty or 'index' is 0, insert elements at the beginning
        if self.__head == None or index == 0 :
            last_node._next , self.__head = self.__head , first_node

            # Update the current length of LinkedList as elements was successfully added
            self.__len += len(data)
            return

        # Find the previous and current nodes at the specified 'index'
        prev , curr , count = None , self.__head , 0
        while count < index :
            prev , curr = curr , curr._next
            count += 1

        # Insert the elements after the 'prev' node and before the 'curr' node
        prev._next , last_node._next = first_node , curr

        # Update the current length of LinkedList as elements was successfully added
        self.__len += len(data)

    def _getitem(self , index : int ) -> Union['Node' , None] :
        """
        Retrieve the element at the specified index in the LinkedList.

        Parameters:
            index (int): The index of the element to be retrieved. Negative indexing can be used just like in normal lists.

        Returns:
            Node or None: The node at the specified index in the LinkedList.
                          Returns None if the index is out of range or the LinkedList is empty.

        Raises:
            IndexError: If the index is out of range (less than -len(LinkedList) or greater/equal to len(LinkedList)).

        Notes:
            - Negative indexing can be used, similar to normal lists in Python.
            - The indexing should be in the range of [-len(LinkedList), len(LinkedList)).
            - The function keeps track of the last accessed node and optimizes the search for elements in increasing index order.
            This can improve performance when accessing consecutive elements in the LinkedList.

        Example:
            # Create a LinkedList and access elements at different indices
            linked_list = BaseList()

            linked_list.insert(10)      # Appends 10 at the end
            linked_list.insert(20, 0)   # Inserts 20 at the beginning
            linked_list.insert(30, 2)   # Inserts 30 at index 2
            linked_list.insert(40, -1)  # Inserts 40 at index -1 (last position)

            # Retrieve elements using positive and negative indices
            print(linked_list._getitem(0))   # Output: Node(20) (Element at index 0, i.e., first element)
            print(linked_list._getitem(2))   # Output: Node(30) (Element at index 2)
            print(linked_list._getitem(-1))  # Output: Node(40) (Last element)
            print(linked_list._getitem(-4))  # Output: Node(20) (Element at index -4, i.e., first element)

            # Access elements using consecutive indices (optimized access)
            print(linked_list._getitem(1))   # Output: Node(10) (Element at index 1, accessed using optimization)
            print(linked_list._getitem(3))   # Output: Node(40) (Element at index 3, accessed using optimization)
        """

        # Optimization: Keep track of last accessed node for consecutive access
        if self.__index == 0 :
            self.__index_ptr = self.__head

        # Support negative indexing
        if index < 0 :
            index += self.__len

        # Check if index is out of range
        if self.__len <= index or index < 0 :

            # Raise IndexError
            raise IndexError('Index Out Of Range')

        # Reset index_ptr if index is smaller than last accessed index
        if index < self.__index :
            self.__index = 0
            self.__index_ptr = self.__head

        # Optimization: Return the last accessed node directly
        if self.__index == index :
            return self.__index_ptr

        # Traverse the LinkedList to find the requested inde
        if self.__index < index :
            while self.__index_ptr and self.__index < index :
                self.__index_ptr = self.__index_ptr._next
                self.__index += 1
            return self.__index_ptr

    def _delete(self , index : int ) -> None :
        """
        Remove the element at the specified index from the LinkedList.

        Parameters:
            index (int): The index of the element to be removed. Negative indexing can be used just like in normal lists.

        Returns:
            None

        Raises:
            IndexError: If the index is out of range (less than -len(LinkedList) or greater/equal to len(LinkedList)).

        Notes:
            - If the index is 0, the first node (head) will be removed, and the head pointer will be updated.
            - Negative indexing can be used, similar to normal lists in Python.
            - The indexing should be in the range of [-len(LinkedList), len(LinkedList)).
            - The function finds the node before the one to be deleted (prev) and the node to be deleted (curr).
            - It then updates the 'next' reference of the previous node to skip the node to be deleted.
            - The node to be deleted is deleted by setting its reference to None.
            - After a successful deletion, the length of the LinkedList is decreased by 1.

        Example:
            # Create a LinkedList and remove elements at different indices
            linked_list = BaseList()

            linked_list.insert(10)      # Appends 10 at the end
            linked_list.insert(20, 0)   # Inserts 20 at the beginning
            linked_list.insert(30, 2)   # Inserts 30 at index 2
            linked_list.insert(40, -1)  # Inserts 40 at index -1 (last position)

            print(linked_list)  # Output: 20 --> 10 --> 30 --> 40 --> None

            linked_list._delete(0)     # Remove the first element (index 0)
            print(linked_list)  # Output: 10 --> 30 --> 40 --> None

            linked_list._delete(2)     # Remove the element at index 2
            print(linked_list)  # Output: 10 --> 30 --> None

            linked_list._delete(-1)    # Remove the last element (index -1)
            print(linked_list)  # Output: 10 --> None
        """

        # If index is 0, remove the first node (head) and update the head pointer
        if index == 0 :
            curr = self.__head
            self.__head = curr._next
            curr = None
            self.__len -= 1
            return 

        # Find the node before the one to be deleted (prev)
        prev = self._getitem(index - 1)

        # Find the node to be deleted (curr)
        curr = self._getitem(index)

        # Update the 'next' reference of the previous node to skip the node to be deleted
        prev._next = curr._next

        # Delete the node by setting its reference to None
        curr = None

        # Update length of LinkedList by 1 as an element was successfully deleted
        self.__len -= 1

    def _delete_all_nodes(self) -> None:
        """
        Delete all nodes in the LinkedList and reset the head and length.

        This method removes all the nodes in the LinkedList and resets the head to None
        and the length of the LinkedList to zero.

        Parameters:
            None

        Returns:
            None

        Example:
            # Create a LinkedList and add elements
            linked_list = BaseList()
            linked_list.insert(10)
            linked_list.insert(20)
            linked_list.insert(30)

            # Display the LinkedList before deletion
            print(linked_list)  # Output: 10 --> 20 --> 30 --> None

            # Delete all nodes
            linked_list.delete_all_nodes()

            # Display the LinkedList after deletion
            print(linked_list)  # Output: LinkedList is Empty
        """

        # Initialize the current node to the head of the LinkedList
        curr = self.__head
        while curr:
            # Store the reference to the current node in 'prev'
            prev = curr

            # Move 'curr' to the next node
            curr = curr._next

            # Ensure there are no dangling references
            prev._next = None

            # Delete the current node
            prev = None

        # Set the head of the LinkedList to None, effectively deleting all nodes
        self.__head = None

        # Update the current length of LinkedList as 0
        self.__len = 0

    def _add(self , ll : 'LinkedList', result : 'LinkedList') -> 'LinkedList':
        """
        Adds two LinkedLists together by concatenating them.
        
        This method combines the elements of the current LinkedList (self) and another
        LinkedList (ll) and stores the result in the 'result' LinkedList. It assumes
        that all three LinkedLists have at least one element

        Parameters:
            ll (LinkedList): The LinkedList to be added to the current LinkedList.
            result (LinkedList): The LinkedList to store the result of addition.

        Returns:
            LinkedList: The 'result' LinkedList containing the elements from both
            input LinkedLists concatenated together.

        Raises:
            ValueError: If both LinkedLists are empty.

        Example:
            # Create two LinkedLists
            linked_list1 = LinkedList()
            linked_list1.insert(1)
            linked_list1.insert(2)
            linked_list1.insert(3)

            linked_list2 = LinkedList()
            linked_list2.insert(4)
            linked_list2.insert(5)

            # Add the two LinkedLists
            result = linked_list1._add(linked_list2)

            # Show the resulting LinkedList
            print(result._show())
            # Output: 1 --> 2 --> 3 --> 4 --> 5 --> None

        Note:
        This method performs concatenation of the two input LinkedLists.
        It does not modify the original LinkedLists, and the order of the elements
        remains unchanged in the 'result' LinkedList.
        """

        # If both the LinkedList are empty, raise a ValueError
        if self.__head == None and ll.__head == None :
            raise ValueError("Can't add empty LinkedList")

        # if either of LinkedList is empty, return the other one
        if self.__head == None :
            return ll
        if ll.head == None :
            return self

        # Insert the head data of self into the result LinkedList
        result.insert(self.__head.data)

        # Store the head node of the result LinkedList
        start_node = result.__head
        last_node = start_node

        # Copy the elements of self (excluding the head) into the result LinkedList
        for i in range(1 , len(self)) :
            last_node._next = Node(self[i])
            last_node = last_node._next

        # Copy the elements of ll into the result LinkedList
        for j in range(len(ll)) :
            last_node._next = Node(ll[j])
            last_node = last_node._next

        # Adjust the 'next' pointer of the last node to create the loop in the result LinkedList
        result._next = start_node._next

        # Update the length of the result LinkedList
        result.__len = len(self) + len(ll)

        # Return the 'result' LinkedList containing the addition
        return result

    def _mul(self , value : int ) -> 'LinkedList' :
        """
        Multiply each element of the LinkedList by the given value.

        This method multiplies the data of each node in the LinkedList by the
        specified integer value. It modifies the current LinkedList in-place and
        returns a reference to the modified LinkedList.

        Parameters:
            value (int): The integer value to multiply each element with.

        Returns:
            LinkedList: A reference to the modified LinkedList.

        Example:
            # Create a new LinkedList
            linked_list = LinkedList()

            # Add elements to the LinkedList
            linked_list.insert(1)
            linked_list.insert(2)
            linked_list.insert(3)

            # Multiply all elements in the LinkedList by 5
            linked_list._mul(5)

            # Show the modified LinkedList
            print(linked_list)
            # Output: 5 --> 10 --> 15 --> None

        Note:
            This method modifies the current LinkedList and does not create a new one.
            It changes the data of each node in the LinkedList in-place.
        """
        # Multiply each element of the LinkedList by the given value
        for i in range(len(self)) :
            self._getitem(i).data *= value

        # Return a reference to the modified LinkedList
        return self

    def _div(self , value : Union[int , float]) -> 'LinkedList' :
        """
        Divide each element of the LinkedList by the given value.

        This method divides each element in the current LinkedList by the given
        numeric value. The operation is performed in-place, meaning the original
        LinkedList is modified.

        Parameters:
            value (int or float): The value to divide each element of the LinkedList by.

        Returns:
            LinkedList: The modified LinkedList after the division.

        Example:
            # Create a new LinkedList
            linked_list = LinkedList()

            # Add elements to the LinkedList
            linked_list.insert(10)
            linked_list.insert(20)
            linked_list.insert(30)

            # Divide each element by 2
            linked_list._div(2)

            # Show the modified LinkedList
            print(linked_list)
            # Output: 5.0 --> 10.0 --> 15.0 --> None

        Note:
            This method modifies the original LinkedList and returns a reference
            to the same modified LinkedList. If you want to keep the original
            LinkedList unchanged and get a new modified LinkedList, consider
            making a copy before using this method.
        """
        # Divide each element of the LinkedList by the given value
        for i in range(len(self)):
            try :
                self._getitem(i).data /= value
            except Exception as e :
                raise e

        # Return the modified LinkedList
        return self

    def _reversed(self) -> 'LinkedList' :
        """
        Reverse the elements of the LinkedList in-place.

        This method reverses the order of elements in the current LinkedList and modifies
        the LinkedList in-place. The head node of the LinkedList will become the new tail
        node, and the tail node will become the new head node.

        Returns:
            LinkedList: The reversed LinkedList.

        Example:
            # Create a new LinkedList
            linked_list = LinkedList()

            # Add elements to the LinkedList
            linked_list.insert(1)
            linked_list.insert(2)
            linked_list.insert(3)

            # Reverse the LinkedList in-place
            linked_list._reversed()

            # Show the reversed LinkedList
            print(linked_list)
            # Output: 3 --> 2 --> 1 --> None

        Note:
            This method modifies the original LinkedList and returns a reference
            to the same modified LinkedList. If you want to keep the original
            LinkedList unchanged and get a new modified LinkedList, consider
            making a copy before using this method.
        """
        # Set current and previous pointer
        prev , curr = None , self.__head

        # Reversing the nodes
        while curr :
            next_ptr , curr._next = curr._next , prev
            prev , curr = curr , next_ptr

        # Set the last pointer as head pointer
        self.__head = prev

        # Return modified reversed LinkedList
        return self

    def _sort(self , reverse : bool ) -> None :
        """
        Sorts the elements of the linked list in ascending or descending order using merge sort.

        Parameters:
            reverse (bool): If True, sorts the elements in descending order.
                            If False, sorts the elements in ascending order.

        Notes:
            - This method modifies the linked list in place by rearranging the node connections.
            - If the linked list is empty or contains a single element, it remains unchanged.

        Example:
            Suppose we have a linked list with the following elements: 5 -> 2 -> 8 -> 1 -> 6
            Calling `_sort(reverse=False)` will sort the list in ascending order: 1 -> 2 -> 5 -> 6 -> 8
            Calling `_sort(reverse=True)` will sort the list in descending order: 8 -> 6 -> 5 -> 2 -> 1
        """
        self.__head = self.__merge_sort(self.__head , reverse)

    def __merge_sort(self, head , reverse : bool) -> 'Node' :
        """
        Sorts the linked list in ascending or descending order using the merge sort algorithm.

        Parameters:
            head (Node): The head node of the linked list to be sorted.
            reverse (bool, optional): If True, sorts the list in descending order; otherwise, in ascending order.
                                      Default is False, i.e., ascending order.

        Returns:
            Node: The head node of the sorted linked list.

        Algorithm Steps:
        1. Check if the linked list is empty or contains only one node. If so, it is already sorted, and we return the head.
        2. Find the middle node of the linked list using the find_middle() method.
        3. Set the next pointer of the middle node to None, effectively dividing the list into two halves.
        4. Recursively apply the merge_sort() function on the left half and right half of the linked list.
        5. Merge the sorted left and right halves using the merge() method to create a single sorted linked list.
        6. Return the head of the sorted linked list.

        Note: The find_middle() and merge() methods are assumed to be implemented in the LinkedList class.
        """

        # Base case: If the linked list is empty or has only one node, it is already sorted.
        if head == None or head._next == None:
            return head

        # Find the middle of the linked list.
        mid = self.__find_middle(head)

        # Find the head node of left and right parts of LinkedList
        left_head  = mid 
        right_head = mid._next

        # Get the node next to the middle node to split the linked list into two parts
        mid._next = None
        
        # Recursively sort the left half of the linked list
        left = self.__merge_sort(head , reverse)

        # Recursively sort the right half of the linked list.
        right = self.__merge_sort(right_head , reverse)

        # Merge the sorted left and right halves into a single sorted linked list.
        sorted_list = self.__merge(left, right , reverse)

        # Return the head of the sorted linked list
        return sorted_list

    def __find_middle(self, head : 'Node') -> 'Node' :
        """
        Find the middle node of a given linked list using the two-pointer technique.

        Parameters:
        head (Node): The head node of the linked list.

        Returns:
        Node: The middle node of the linked list. If the linked list contains an even number of nodes,
              it returns the second middle node.

        Description:
        The function uses two pointers, slow and fast, to traverse the linked list. The slow pointer
        moves one step at a time, while the fast pointer moves two steps at a time. When the fast
        pointer reaches the end of the linked list, the slow pointer will be at the middle node.

        This method has a time complexity of O(n) since both pointers traverse the list once.
        """

        # Initialize both slow and fast pointers to the head node
        slow = head
        fast = head

        # Traverse the linked list with two pointers until the end is reached
        while fast._next and fast._next._next:

            # Move the slow pointer one step forward
            slow = slow._next

            # Move the fast pointer two steps forward
            fast = fast._next._next

        # Return the middle node (second middle if even number of nodes)
        return slow

    def __merge(self, left, right , reverse : bool) -> 'Node':
        """
        Merges two sorted linked lists 'left' and 'right' into a single sorted linked list.
        The 'reverse' parameter determines whether the merge should be in ascending or descending order.

        Parameters:
            - left: The head node of the first linked list.
            - right: The head node of the second linked list.
            - reverse: A boolean flag indicating whether to merge in descending order (True) or ascending order (False).

        Returns:
            The head node of the merged linked list.

        Steps:
            1. Check if 'left' is None. If so, the merging process is complete, return 'right'.
            2. Check if 'right' is None. If so, the merging process is complete, return 'left'.
            3. If 'reverse' is False:
                a. Compare the data of 'left' and 'right' nodes.
                b. If the data of 'left' is less than or equal to the data of 'right':
                    - Set 'result' to 'left'.
                    - Recursively call 'merge' with the next node in 'left' and 'right'.
                    - Set 'result._next' to the result of the recursive merge operation.
                c. If the data of 'right' is less than the data of 'left':
                    - Set 'result' to 'right'.
                    - Recursively call 'merge' with 'left' and the next node in 'right'.
                    - Set 'result._next' to the result of the recursive merge operation.
            4. If 'reverse' is True:
                a. Compare the data of 'left' and 'right' nodes.
                b. If the data of 'right' is less than or equal to the data of 'left':
                    - Set 'result' to 'left'.
                    - Recursively call 'merge' with the next node in 'left' and 'right'.
                    - Set 'result._next' to the result of the recursive merge operation.
                c. If the data of 'left' is less than the data of 'right':
                    - Set 'result' to 'right'.
                    - Recursively call 'merge' with 'left' and the next node in 'right'.
                    - Set 'result._next' to the result of the recursive merge operation.

            5. Return the 'result' node as the head of the merged linked list.

        """

        result = None

        # Base: If one of the lists is empty, return the other list as the result.
        if left == None:
            return right
        if right == None:
            return left

        # If reverse is False, perform regular merge (ascending order).
        if reverse == False :

            # Compare data of the current nodes in both lists.
            if left.data <= right.data:

                # Set result to the current node from the left list.
                result = left

                # Recursively merge the next node from left with right.
                result._next = self.__merge(left._next, right , reverse)
            else:

                # Set result to the current node from the right list.
                result = right

                # Recursively merge the next node from right with left.
                result._next = self.__merge(left, right._next , reverse)
        
         # If reverse is True, perform merge in descending order.
        else :

            # Compare data of the current nodes in both lists (opposite to regular merge).
            if right.data <= left.data:

                # Set result to the current node from the left list.
                result = left

                # Recursively merge the next node from left with right.
                result._next = self.__merge(left._next, right , reverse)
            else:

                # Set result to the current node from the right list.
                result = right

                # Recursively merge the next node from right with left.
                result._next = self.__merge(left, right._next , reverse)

        # Return the merged linked list.
        return result
        