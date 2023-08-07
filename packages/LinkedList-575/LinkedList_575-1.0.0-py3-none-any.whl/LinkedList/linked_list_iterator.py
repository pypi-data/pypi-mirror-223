class LinkedListIterator :
    """
    An iterator class for iterating over the elements of a linked list.

    This iterator is designed to work with a linked list represented by nodes,
    where each node has a `data` attribute representing the value of the element,
    and a `_next` attribute pointing to the next node in the linked list.

    Attributes:
        current (Node): The current node being iterated over.

    Methods:
        __init__(self, head):
            Constructor method to initialize the iterator with the head node of the linked list.
            
        __iter__(self):
            Returns the iterator object itself. This method is required for the object to be
            considered an iterator, and it enables the iterator to be used in a `for` loop.
            In this case, it simply returns `self`.
            
        __next__(self):
            Retrieves the next element in the linked list as the iterator is moved forward.
            It returns the value of the `data` attribute of the current node and then updates
            the `current` attribute to point to the next node in the linked list.
            
            Raises:
                StopIteration: When the end of the linked list is reached, and there are no
                               more elements to iterate over. This is the signal to stop
                               iterating and is used to terminate the `for` loop or other
                               iterable operations.
    """

    def __init__(self , head) :
        """
        Initialize the iterator with the head node of the linked list.

        Parameters:
            head (Node): The head node of the linked list.
        """

        # Initialize the iterator with the head node of the linked list.
        self.current = head

    def __iter__(self) :
        """
        Returns the iterator object itself.

        Returns:
            LinkedListIterator: The iterator object itself.
        """

        # Return the iterator object itself (required for iteration using 'for' loop).
        return self

    def __next__(self) :
        """
        Retrieves the next element in the linked list as the iterator is moved forward.

        Returns:
            Any: The value of the `data` attribute of the current node.

        Raises:
            StopIteration: When the end of the linked list is reached, and there are no
                           more elements to iterate over. This is the signal to stop
                           iterating and is used to terminate the `for` loop or other
                           iterable operations.
        """

        # If we reach to the end of the linked list, stop the iteration
        if self.current == None :
            raise StopIteration

        # Get the next element in the linked list and update the 'current' attribute.
        data = self.current.data
        self.current = self.current._next

        # Get the data at the node
        return data