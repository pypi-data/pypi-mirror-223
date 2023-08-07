from typing import Union
from typing import Tuple
from typing import List
from copy import copy

class Node :
    """
    Class representing a Node in a singly LinkedList.

    Attributes:
        data (any): The data stored in the Node.
        next (Node or None): Reference to the next Node in the LinkedList. Default is None.

    Methods:
        __init__(self, data):
            Initialize a new Node instance with the given data.

    Example:
        # Create a Node with data value 10
        node = Node(10)
        # Now, 'node' represents a Node object with data = 10 and next = None.
    """
    def __init__(self , data : int) -> None :
        """
        Initialize a new Node instance with the given data.

        Parameters:
            data (any): The data to be stored in the Node.

        Returns:
            None
        """
        self.data : int = data
        self._next = None

    @property
    def next(self) -> Union['Node' , None] :
        """
        Get the reference to the next Node in the LinkedList.

        Returns:
            Node or None: The next Node in the LinkedList or None if it's the last Node.
        """
        return self._next