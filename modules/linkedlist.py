#!python
from bin.utils import time_it

class LinkedListIterator():
    def __init__(self, head):
        self.current_node = head

    def __next__(self):
        output_node = self.current_node

        if self.current_node is not None:
            self.current_node = self.current_node.next
        else:
            raise StopIteration

        return output_node


class Node(object):

    def __init__(self, data):
        """Initialize this node with the given data."""
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        """Return a string representation of this node."""
        return 'Node({!r})'.format(self.data)


class LinkedList(object):
    def __init__(self, items=None):
        """Initialize this linked list and append the given items, if any."""

        self.head = None  # First node
        self.tail = None  # Last node
        self.size = 0  # Size of Linked List

        # Append given items
        if items is not None:
            for item in items:
                self.append(item)

    def __str__(self):
        """Return a formatted string representation of this linked list."""

        items = ['({!r})'.format(item) for item in self.items()]
        return '[{}]'.format(' -> '.join(items))

    def __repr__(self):
        """Return a string representation of this linked list."""

        return 'LinkedList({!r})'.format(self.items())

    def __iter__(self):
        return LinkedListIterator(self.head)

#    @time_it
    def items(self):
        """Return a list (dynamic array) of all items in this linked list.

        Best Case: O(n)
        Worst Case: O(n)

        """

        items = []
        node = self.head

        while node is not None:
            items.append(node.data)
            node = node.next

        return items

    #@time_it
    def is_empty(self):
        """Return a boolean indicating whether this linked list is empty.

        Best/Worst Case: O(1)

        """
        return self.head is None

    #@time_it
    def length(self):
        return self.size

    @time_it
    def length_(self):
        """Return the length of this linked list by traversing its nodes.

        Best Case: O(n)
        Worst Case: O(n)

        We have to iterate through the whole linked list, which is size n, so best and worst case
        runtime would be on the order of O(n) operations

        """

        count = 0
        current_node = self.head

        while(current_node is not None):
            count += 1
            current_node = current_node.next

        return count

    #@time_it
    def replace(self, item_to_replace, value_to_replace_with):
        """Find and replace "item_to_replace" with the value_to_replace_with.

        Best Case: O(1) -> If the Node to replace is in the beginning
        Worst Case: O(n) -> If the Node is at the tail or doesnt exist

        """

        if self.is_empty():
            raise ValueError("List is empty")

        current_node = self.head

        while current_node is not None:
            # Check for matching item
            if current_node.data == item_to_replace:
                # Replace with input data
                current_node.data = value_to_replace_with
                return

            current_node = current_node.next

        # If did not return, item was not found
        raise ValueError("Node with value {} not found!".format(item_to_replace))

    #@time_it
    def append(self, item):
        """Insert the given item at the tail of this linked list.

        Best Case: O(1)
        Worst Case: O(1)

        Inserting at the end, so there is no need to iterate over the linked list because we have
        a tail pointer

        """

        new_node = Node(item)
        self.add_last(new_node)

    #@time_it
    def prepend(self, item):
        """Insert the given item at the head of this linked list.

        Best Case: O(1)
        Worst Case: O(1)

        Inserting at the beginning of the list, so no need to iterate over it because we have
        a head pointer

        """

        new_node = Node(item)
        self.add_first(new_node)

    #@time_it
    def find(self, quality):
        """Return an item from this linked list satisfying the given quality.

        Best Case: O(1) -> If the first node matches!
        Worst Case: O(n) -> If the last node matches, or if there is no match at all

        """

        current_node = self.head

        while current_node is not None:
            if quality(current_node.data):
                return current_node.data

            current_node = current_node.next

        # Return None if no nodes match quality
        return None

    #@time_it
    def delete(self, item):
        """Delete the given item from this linked list, or raise ValueError.

        Best Case: O(1) -> If the item to delete is the head of linked list
        Worst Case: O(n) -> If the item to delete is the tail of the linked list or does not exist at all

        """

        if self.is_empty():
            raise ValueError("List is empty")

        prev_node = None
        current_node = self.head

        while current_node is not None:
            # Check for matching item
            if current_node.data == item:
                # Check if current_node is head
                if prev_node is None:
                    self.remove_first()
                    return

                # Check if current_node is tail
                if current_node.next is None:
                    self.remove_last()
                    return

                # Current node is somewhere in the middle
                prev_node.next = current_node.next
                current_node.next.prev = prev_node
                self.size -= 1
                return

            prev_node = current_node
            current_node = current_node.next

        # If did not return, item was not found
        raise ValueError("Item not found: {}".format(item))

    # HELPER FUNCTIONS

    #@time_it
    def add_last(self, new_node):
        """Add to the end of linked list -> O(1)."""

        # If linked list is empty
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.head
            self.size += 1
            return

        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node
        self.size += 1

    #@time_it
    def add_first(self, new_node):
        """Add to beginning of linked list -> O(1)."""

        # If linked list is empty
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.head
            self.size += 1
            return

        new_node.next = self.head
        self.head = new_node
        new_node.prev = self.head
        self.size += 1

    #@time_it
    def remove_first(self):
        """Remove first node in the linked list -> O(1)."""

        print("Removing first! ")
        print("Next of: {} is {}".format(self.head.data, self.head.next))
        print("Prev of: {} is {}".format(self.head.data, self.head.prev))

        # If linked list is empty
        if self.head is None:
            raise ValueError("Can't delete, linked list is empty")

        # If only one remaining
        if self.size == 1:
            self.head = None
            self.tail = None
            self.size -= 1
            return

        self.head = self.head.next
        self.head.prev = self.head
        self.size -= 1

    #@time_it
    def remove_last(self):

        print("Removing last! ")
        print("Next of: {} is {}".format(self.tail.data, self.tail.next))
        print("Prev of: {} is {}".format(self.tail.data, self.tail.prev))

        # If linked list is empty
        if self.head is None:
            raise ValueError("Can't delete, linked list is empty")

        # If only one remaining:
        if self.size == 1:
            self.head = None
            self.tail = None
            self.size -= 1
            return

        self.tail = self.tail.prev
        self.tail.next = None
        self.size -= 1


def test_linked_list():
    ll = LinkedList()

    print('\nTesting append:')
    for item in ['A', 'B', 'C']:
        print('append({!r})'.format(item))
        ll.append(item)
        print('list: {}'.format(ll))
        print("Next of: {} is {}".format(item, ll.tail.next))
        print("Prev of: {} is {}".format(item, ll.tail.prev))

    print('head: {}'.format(ll.head))
    print('tail: {}'.format(ll.tail))
    print('length: {}'.format(ll.length()))

    print("\n\n Testing iterator:")
    for node in ll:
        print("Item: {}".format(node.data))


    # Enable this after implementing delete method
    delete_implemented = True
    if delete_implemented:
        print('\nTesting delete:')
        for item in ['B', 'C', 'A']:
            print('delete({!r})'.format(item))
            ll.delete(item)
            print('list: {}'.format(ll))


        print('head: {}'.format(ll.head))
        print('tail: {}'.format(ll.tail))
        print('length: {}'.format(ll.length()))


if __name__ == '__main__':
    test_linked_list()
