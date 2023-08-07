from LinkedList.linked_list_iterator import LinkedListIterator
from LinkedList.base_list import BaseList
from typing import Union

class LinkedList(BaseList) :
    def __init__(self) -> None :
        """
        Initializes a new LinkedList object.

        Parameters:
            None

        Returns:
            None

        Example:
            linked_list = LinkedList()
        """
        super().__init__()

    def __str__(self) -> None :
        """
        String representation of the LinkedList.

        Parameters:
            None

        Returns:
            str: A string representation of the LinkedList.

        Example:
            print(linked_list)
            # output : 1 --> 2 --> 3 --> None
        """

        # String representation of the LinkedList.
        return self._show()

    def __len__(self) -> None :
        """
        Get the current length of the LinkedList.

        Parameters:
            None

        Returns:
            int: The length of the LinkedList.

        Example:
            length = len(linked_list)
            # output : 3
        """

        # Get the current length of the LinkedList.
        return self.len

    def __iter__(self) :
        """
        Return an iterator object for the LinkedList.

        This method allows the LinkedList class to be iterable, enabling the use of Python's built-in
        iteration features, such as for loops and iterable functions.

        Returns
        -------
        LinkedListIterator :
            An iterator object that provides access to the elements in the linked list.

        Notes
        -----
        The iterator object returned by this method will start iteration from the head (first node) of
        the linked list and continue until it reaches the end of the linked list.

        Example
        -------
        ll = LinkedList()
        ll.insert(10)
        ll.insert(20)
        ll.insert(30)

        # Using the linked list in a for loop
        for item in ll:
            print(item)

        # Output:
        # 10
        # 20
        # 30

        # Using the built-in sum function to get the sum of elements
        total = sum(ll)
        print(total)

        # Output:
        # 60

        # Converting the linked list to a list
        ll_list = list(ll)
        print(ll_list)

        # Output:
        # [10, 20, 30]

        The __iter__ method enables the LinkedList class to be used in iteration and other iterable
        operations, providing more flexibility and integration with Python's standard library.
        """

        return LinkedListIterator(self.head)

    def __getitem__(self , index : int) -> int :
        """
        Retrieve the value of the element at the specified index in the LinkedList.

        Parameters:
            index (int): The index of the element to be retrieved. Negative indexing can be used just like in normal lists.

        Returns:
            int: The value of the element at the specified index in the LinkedList.

        Raises:
            IndexError: If the index is out of range (less than -len(LinkedList) or greater/equal to len(LinkedList)).
            AttributeError: If the element at the specified index does not have the 'data' attribute.

        Notes:
            - Negative indexing can be used, similar to normal lists in Python.
            - The indexing should be in the range of [-len(LinkedList), len(LinkedList)).
            - This method provides a convenient way to access the value of a node at a specific index using the '[]' syntax.

        Example:
            # Create a LinkedList and access elements at different indices
            linked_list = BaseList()

            linked_list.insert(10)      # Appends 10 at the end
            linked_list.insert(20, 0)   # Inserts 20 at the beginning
            linked_list.insert(30, 2)   # Inserts 30 at index 2
            linked_list.insert(40, -1)  # Inserts 40 at index -1 (last position)

            # Retrieve values using positive and negative indices
            print(linked_list[0])   # Output: 20 (Value at index 0, i.e., value of the first element)
            print(linked_list[2])   # Output: 30 (Value at index 2)
            print(linked_list[-1])  # Output: 40 (Value of the last element)
            print(linked_list[-4])  # Output: 20 (Value at index -4, i.e., value of the first element)
        """

        # Check if the LinkedList is empty
        if self.head == None :

            # Raise IndexError
            raise IndexError("Can't access an element from empty LinkedList")

        # Get the required data at the Node
        return self._getitem(index).data
    
    def __setitem__(self , index : int , value : int) -> None :
        """
        Update the value of the element at the specified index in the LinkedList.

        Parameters:
            index (int): The index of the element to be updated. Negative indexing can be used just like in normal lists.
            value (int): The new value to be assigned to the element.

        Raises:
            IndexError: If the index is out of range (less than -len(LinkedList) or greater/equal to len(LinkedList)).
            AttributeError: If the element at the specified index does not have the 'data' attribute.

        Notes:
            - Negative indexing can be used, similar to normal lists in Python.
            - The indexing should be in the range of [-len(LinkedList), len(LinkedList)).
            - This method provides a convenient way to update the value of a node at a specific index using the '[]' syntax.

        Example:
            # Create a LinkedList and update elements at different indices
            linked_list = BaseList()

            linked_list.insert(10)      # Appends 10 at the end
            linked_list.insert(20, 0)   # Inserts 20 at the beginning
            linked_list.insert(30, 2)   # Inserts 30 at index 2
            linked_list.insert(40, -1)  # Inserts 40 at index -1 (last position)

            # Update values using positive and negative indices
            linked_list[0]  = 50    # Update the value at index 0 to 50
            linked_list[2]  = 60    # Update the value at index 2 to 60
            linked_list[-1] = 70    # Update the value of the last element to 70
            linked_list[-4] = 80    # Update the value at index -4 to 80
        """

        # Check if the LinkedList is empty
        if self.head == None :

            # Raise IndexError
            raise IndexError("LinkedList assignment index out of range")

        # Set the given value at the Node
        self._getitem(index).data = value

    def __delitem__(self , index : int ) -> None :
        """
        Delete a node at the specified index from the LinkedList.

        Parameters:
            index (int): The index of the node to delete.

        Returns:
            None

        Raises:
            IndexError: If the index is out of range or if the LinkedList is empty.

        Example:
            # Create a LinkedList
            linked_list = LinkedList()
            linked_list.insert(10)
            linked_list.insert(20)
            linked_list.insert(30)

            # Delete the second node (index 1)
            del linked_list[1]
            # Now, the LinkedList becomes: 10 --> 30 --> None

            # Trying to delete from an empty LinkedList will raise an IndexError
            empty_list = LinkedList()
            try:
                del empty_list[0]
            except IndexError as e:
                print(f"Error: {e}")
                # Output: Error: can't delete from an empty LinkedList
        """

        # Check if the LinkedList is empty
        if self.head == None :

            # Raise IndexError
            raise IndexError("can't delete from an empty LinkedList")

        return self._delete(index)

    def __del__(self) -> None :
        """
        Destructor for the LinkedList.

        This method is automatically called when the LinkedList object is no longer referenced and is being deleted from memory.
        It deletes all nodes of the LinkedList, freeing up the memory occupied by each node.

        Parameters:
            None

        Returns:
            None

        Notes:
            - This method should not be called directly by the user; it is automatically invoked when the LinkedList object is destroyed.
            - It is responsible for properly cleaning up the memory used by the LinkedList nodes.

        Example:
            # Create a LinkedList
            linked_list = BaseList()

            # Add elements to the LinkedList
            linked_list.insert(10)      # Appends 10 at the end
            linked_list.insert(20, 0)   # Inserts 20 at the beginning
            linked_list.insert(30, 2)   # Inserts 30 at index 2

            # Delete the LinkedList object
            del linked_list
            # The destructor (__del__) is automatically called, and all nodes of the LinkedList are deleted.
            # The memory occupied by each node is freed.
        """

        # Destructor - deletes all nodes in the LinkedList when the object is destroyed.
        self._delete_all_nodes()

    # def _add(self , ll) :
    #     ans = self
    #     last_node = self._getitem(-1)
    #     last_node._next = ll.head
    #     return self

    def __add__(self , ll : 'LinkedList') -> 'LinkedList' :
        """
        Perform addition on two LinkedList objects.

        This method adds the elements of the current LinkedList with another
        LinkedList provided as input. It returns a new LinkedList containing
        the elements from both LinkedLists concatenated together.

        Parameters:
            ll (LinkedList): The LinkedList to be added to the current LinkedList.

        Returns:
            LinkedList: A new LinkedList containing the concatenated elements
            from both LinkedLists.

        Example:
            # Create two LinkedLists
            linked_list1 = LinkedList()
            linked_list2 = LinkedList()

            # Add elements to the first LinkedList
            linked_list1.insert(1)
            linked_list1.insert(2)
            linked_list1.insert(3)

            # Add elements to the second LinkedList
            linked_list2.insert(4)
            linked_list2.insert(5)

            # Add the LinkedLists and store the result in a new LinkedList
            result = linked_list1 + linked_list2

            # Show the result
            print(result)
            # Output: 1 --> 2 --> 3 --> 4 --> 5 --> None

        Note:
            This method allows you to use the '+' operator between two LinkedList
            objects to concatenate their elements and create a new LinkedList.
            It does not modify the original LinkedLists, and the order of the
            elements remains unchanged in the new LinkedList.
        """

        # Create a LinkedList to store concatenated LinkedList separately
        result = LinkedList()

        # Return the concatenated LinkedList
        return self._add(ll , result)

    def __mul__(self , value : int) -> 'LinkedList' :
        """
        Perform element-wise multiplication of the LinkedList with a numeric value.

        This method performs element-wise multiplication of the elements in the
        LinkedList with a numeric value and returns a modified LinkedList with the
        multiplied elements.

        Parameters:
            value (int or float): The numeric value to multiply the elements with.

        Returns:
            LinkedList: The modified LinkedList containing the elements after multiplication.

        Raises:
            ValueError: If the LinkedList is empty or if the 'value' parameter is not numeric.

        Example:
            # Create a new LinkedList
            linked_list = LinkedList()

            # Add elements to the LinkedList
            linked_list.insert(1)
            linked_list.insert(2)
            linked_list.insert(3)

            # Perform multiplication with value 2
            result = linked_list.__mul__(2)

            # Show the result
            print(result)
            # Output: 2 --> 4 --> 6 --> None

        Note:
            This method modifies the current LinkedList and does not create a new one.
            It changes the data of each node in the LinkedList in-place.
        """

        # Check if the LinkedList is empty
        if self.head == None :
            raise ValueError("Can't multiply with Empty LinkedList")

        # Check if the value is a numeric type (int or float)
        if not isinstance(value, (int , float)):
            raise ValueError("Numeric value is required for multiplication")

        # Return the modified LinkedList with the multiplication result
        return self._mul(value)

    
    def __truediv__(self , value : Union[int , float]) -> 'LinkedList' :
        """
        Divide each element of the LinkedList by the given numeric value.

        This method performs division on each element of the LinkedList by the provided
        numeric value and returns a modeified LinkedList containing the results.

        Parameters:
            value (int or float): The numeric value to divide each element of the LinkedList by.

        Returns:
            LinkedList: A modified LinkedList containing the results of the division.

        Raises:
            ValueError: If the LinkedList is empty or the provided value is not a numeric type.

        Example:
            # Create a new LinkedList
            linked_list = LinkedList()

            # Add elements to the LinkedList
            linked_list.insert(10)
            linked_list.insert(20)
            linked_list.insert(30)

            # Divide each element by 2 and store the result in a new LinkedList
            result = linked_list.__div__(2)

            # Show the result
            print(result)
            # Output: 5.0 --> 10.0 --> 15.0 --> None

        Note:
            This method modifies the original LinkedList and returns a reference
            to the same modified LinkedList. If you want to keep the original
            LinkedList unchanged and get a new modified LinkedList, consider
            making a copy before using this method.
        """
         # Check if the LinkedList is empty
        if self.head == None :
            raise ValueError("Can't multiply with Empty LinkedList")

        # Check if the value is a numeric type (int or float)
        if not isinstance(value, (int , float)):

            # Raise Valueerror if value is not numeric
            raise ValueError("Numeric value is required for multiplication")

        # Return the modified LinkedList with the division result
        return self._div(value)

    def __reversed__(self) -> 'LinkedList':
        """
        Return a new reversed LinkedList.

        This method creates and returns the modified LinkedList containing the elements
        of the current LinkedList (self) in reversed order. The original LinkedList
        will changed.

        Returns:
            LinkedList: The modified LinkedList with elements in reversed order.

        Example:
            # Create a new LinkedList
            linked_list = LinkedList()

            # Add elements to the LinkedList
            linked_list.insert(1)
            linked_list.insert(2)
            linked_list.insert(3)

            # Get the reversed LinkedList
            reversed_list = reversed(linked_list)

            # Show the original and reversed LinkedLists
            print(linked_list)
            # Output: 1 --> 2 --> 3 --> None

            print(reversed_list)
            # Output: 3 --> 2 --> 1 --> None

        Note :
            This method modifies the original LinkedList and returns a reference
            to the same modified LinkedList. If you want to keep the original
            LinkedList unchanged and get a new modified LinkedList, consider
            making a copy before using this method.
        """

        # If LinkedList is empty or it has only one element, return it without any modification
        if self.head == None or self.head.next == None :
            return self

        # Return the modified LinkedList with elements in reverse order
        return self._reversed()

    def sort(self , reverse = False) -> None :
        """
        Sorts the elements of the LinkedList in ascending order by default, or in descending order if reverse is set to True.

        Parameters:
            reverse (bool, optional): If True, the list will be sorted in descending order. If False (default), the list will be sorted in ascending order.

        Returns:
            None: This method does not return any value. It sorts the elements of the LinkedList in place.

        Note:
            - The elements of the LinkedList must be comparable (i.e., support comparison operations such as '<', '>', '==', etc.) for sorting to work correctly.
            - If the LinkedList contains elements of different data types, the sorting behavior may not be as expected.

        Example:
            # Create a LinkedList
            linked_list = LinkedList()
            linked_list.insert(5)
            linked_list.insert(2)
            linked_list.insert(8)

            # print(linked_list)      output: 5 --> 2 --> 8 --> None

            # Sort the LinkedList in ascending order
            linked_list.sort()
            # After sorting: 2 --> 5 --> 8 --> None

            # Sort the LinkedList in descending order
            linked_list.sort(reverse=True)
            # After sorting: 8 --> 5 --> 2 --> None
        """
        return self._sort(reverse)
    
