""" CSCI 204, Stack lab """
""" Tongyu Yang CSCI204 Lab06 """

class MyStack:
    """ Implement this Stack ADT using a Python list to hold elements.
         
        Do NOT use the len() feature of lists.
    """
    CAPACITY = 10
    def __init__( self ):
        """ Initialize an empty stack. """
        self._capacity = MyStack.CAPACITY
        self._size = 0
        self._array = [None] * self._capacity

    def isEmpty( self ):
        """ Is the stack empty? 
        Returns True if the stack is empty; False otherwise. """
        if self._size == 0:
            return True
        else:
            return False

    def push( self, item ):
        """ Push the item onto the top of the stack. """
        if self._size == 0:
            self._array[0] = item
        else:
            if self._size == self._capacity:
                new_array = [None] * (2 * self._capacity)
                self._capacity *= 2
            else:
                new_array = [None] * self._capacity

            new_array[0] = item
            for index in range(self._capacity - 1):
                new_array[index + 1] = self._array[index]
            self._array = new_array
        self._size += 1

    def pop( self ):
        """ Pop the top item off the stack and return it. """
        if self._size == 0:
            return None
        else:
            popped_item = self._array[0]
            for index in range(self._capacity - 1):
                self._array[index] = self._array[index + 1]
            self._size -= 1
            return popped_item

    def peek( self ):
        """ Return the top item on the stack (does not change the stack). """
        return self._array[0]

    def __repr__ (self):
        return str(self._array)
    
# stack=MyStack()
# print(stack.isEmpty())
# stack.push(1)
# print(stack)
# stack.push(2)
# stack.push(3)
# print(stack)
# stack.pop()
# print(stack)
# stack.pop()
# print(stack)
# stack.pop()
# print(stack)
# print(stack.peek())


