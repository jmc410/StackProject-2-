class Stack:

    def __init__(self):
        """Create an empty stack."""
        self.__items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.__items.append(item)

    def pop(self):
        """
        Remove and return the top item.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")

        return self.__items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")

        return self.__items[-1]

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self.__items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self.__items)


# Tests for the Stack class
if __name__ == "__main__":

    print("Testing Stack Class")

    stack = Stack()

    assert stack.is_empty()
    assert stack.size() == 0

    stack.push(10)
    assert stack.size() == 1
    assert stack.peek() == 10

    assert stack.size() == 1

    stack.push(20)
    stack.push(30)

    assert stack.size() == 3
    assert stack.pop() == 30
    assert stack.pop() == 20
    assert stack.pop() == 10

    assert stack.is_empty()

    try:
        stack.pop()
    except IndexError:
        print("Empty pop test has passed.")

    try:
        stack.peek()
    except IndexError:
        print("Empty peek test has passed.")

    print("All Stack tests passed! :)")