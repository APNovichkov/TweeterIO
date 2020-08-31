#!python

from linkedlist import LinkedList
from bin.utils import time_it


class HashTableIterator():
    def __init__(self, buckets):
        self.buckets = buckets
        self.current_node = None
        self.current_bucket_index = 0

        # Find first bucket that isnt empty
        for i in range(len(buckets)):
            if self.buckets[i].length() != 0:
                self.current_node = self.buckets[i].head
                self.current_bucket_index = i
                break

        print("In __init__")
        print("Current Node: {}".format(self.current_node.data))
        print("Current Bucket Index: {}".format(self.current_bucket_index))

    def __next__(self):
        output_node = self.current_node

        print("s_next__")
        print("Output node: {}".format(output_node))
        print("Are there more buckets? {}".format(self.is_there_more_buckets()))
        print("CurrentNode.next: {}".format(self.current_node.next))
        print("current Bucket Index: {}".format(self.current_bucket_index))

        # Check if there are buckets, if so, set output node to current node

        # If last node in the whole hashtable, stop the iteration
        if self.current_node.next is None and not self.is_there_more_buckets():
            print("I AM IN THE IFFFF")
            raise StopIteration

        # If there are no more buckets after this one but current node is in the middle
        # Set current node to point to the next node
        elif not self.is_there_more_buckets() and self.current_node.next is not None:
            self.current_node = self.current_node.next

        # If there are more buckets and node is not at the end of bucket linked list
        # Set current node to point to next node
        elif self.is_there_more_buckets() and self.current_node.next is not None:
            self.current_node = self.current_node.next

        # If there are still buckets but node is at the end of a bucket linked list
        # Find the next bucket and set current node to its head
        else:
            self.set_next_bucket_index()
            self.current_node = self.buckets[self.current_bucket_index].head

        return output_node

    def set_next_bucket_index(self):
        for i in range(self.current_bucket_index + 1, len(self.buckets)):
            if self.buckets[i].length() != 0:
                self.current_bucket_index = i
                break

    def is_there_more_buckets(self):
        for i in range(self.current_bucket_index + 1, len(self.buckets)):
            if self.buckets[i].length() != 0:
                return True

        return False


class HashTable(object):
    def __init__(self, init_size=8):
        """Initialize this hash table with the given initial size."""

        # Create a new list (used as fixed-size array) of empty linked lists
        self.buckets = [LinkedList() for _ in range(init_size)]
        self.size = 0

    def __str__(self):
        """Return a formatted string representation of this hash table."""

        items = ['{!r}: {!r}'.format(key, val) for key, val in self.items()]
        return '{' + ', '.join(items) + '}'

    def __repr__(self):
        """Return a string representation of this hash table."""

        return 'HashTable({!r})'.format(self.items())

    def _bucket_index(self, key):
        """Return the bucket index where the given key would be stored."""

        # Calculate the given key's hash code and transform into bucket index
        return hash(key) % len(self.buckets)

    def __iter__(self):
        return HashTableIterator(self.buckets)

#    @time_it
    def keys(self):
        """Return a list of all keys in this hash table.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(n). Have to run through all key/value pairs
        Average Case Running Time -> O(n). Same thing

        """

        # Collect all keys in each bucket
        all_keys = []
        for bucket in self.buckets:
            for node in bucket:
                all_keys.append(node.data[0])

        return all_keys

#    @time_it
    def values(self):
        """Return a list of all values in this hash table.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(n). Have to run through all key/value pairs
        Average Case Running Time -> O(n). Same thing

        """

        all_values = []
        for bucket in self.buckets:
            for node in bucket:
                all_values.append(node.data[1])
        return all_values

#    @time_it
    def items(self):
        """Return a list of all key-value pairs in this hash table.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(n). Have to run through all key/value pairs
        Average Case Running Time -> O(n). Same thing

        """

        # Collect all pairs of key-value entries in each bucket
        all_items = []
        for bucket in self.buckets:
            all_items.extend(bucket.items())
        return all_items

#    @time_it
    def length(self):
        """Return the number of key-value entries by traversing its buckets.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(1). Just need to return value of size variable
        Average Case Running Time -> O(1). Same thing

        """

        return self.size

    def length_(self):
        """Return the number of key-value entries by traversing its buckets.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(n). Have to run through all key/value pairs
        Average Case Running Time -> O(n). Same thing


        """

        count = 0
        for bucket in self.buckets:
            for node in bucket:
                count += 1
        return count

#    @time_it
    def contains(self, key):
        """Return True if this hash table contains the given key, or False.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(1). Bucket only has linked list of size one
        Average Case Running Time -> O(l). Buckets have linked lists with variable
        number of items in it.

        """

        # This will contain a linkedlist object
        bucket_at_index = self.buckets[self._bucket_index(key)]

        if bucket_at_index is not None:
            for node in bucket_at_index:
                if node.data[0] == key:
                    return True

        return False

#    @time_it
    def get(self, key):
        """Return the value associated with the given key, or raise KeyError.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(1). Bucket only has linked list of size one
        Average Case Running Time -> O(l). Buckets have linked lists with variable
        number of items in it.

        """

        bucket_at_index = self.buckets[self._bucket_index(key)]
        if bucket_at_index is not None:
            for node in bucket_at_index:
                if node.data[0] == key:
                    return node.data[1]

        raise KeyError("Key not found: {}".format(key))

#    @time_it
    def set(self, key, value):
        """Insert or update the given key with its associated value.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(1). Bucket only has linked list of size one
        Average Case Running Time -> O(l). Buckets have linked lists with variable
        number of items in it.

        """

        # Get linked list at bucket index
        bucket_at_index = self.buckets[self._bucket_index(key)]

        if bucket_at_index.length() != 0:
            for node in bucket_at_index:
                if node.data[0] == key:
                    node.data = ((key, value))
                    return

            bucket_at_index.append((key, value))
            self.size += 1
        else:
            bucket_at_index.append((key, value))
            self.size += 1

#    @time_it
    def delete(self, key):
        """Delete the given key from this hash table, or raise KeyError.

        n -> number of key,value pairs in the hashtable
        b -> number of buckets in the hashtable
        l -> n/b (load factor, average number of key/value pairs per bucket)

        Best Case Running Time -> O(1). Bucket only has linked list of size one
        Average Case Running Time -> O(l). Buckets have linked lists with variable
        number of items in it.

        """

        bucket_at_index = self.buckets[self._bucket_index(key)]
        if bucket_at_index is not None:
            for node in bucket_at_index:
                if node.data[0] == key:
                    bucket_at_index.delete(node.data)
                    self.size -= 1
                    return

        raise KeyError("Key not found {}".format(key))

def test_hash_table_iterator():
    ht = HashTable()
    print('\nTesting set:')
    for key, value in [('I', 1), ('V', 5), ('X', 10)]:
        print('set({!r}, {!r})'.format(key, value))
        ht.set(key, value)
        print('hash table: {}'.format(ht))

    index = 0

    print("\nWe are going to run through this hashtable")
    for item in ht:
        if index == 5:
            break
        print("Key/Value: {} -> {}".format(item.data[0], item.data[1]))
        index += 1


def test_hash_table():
    ht = HashTable()
    print('hash table: {}'.format(ht))

    print('\nTesting set:')
    for key, value in [('I', 1), ('V', 5), ('X', 10)]:
        print('set({!r}, {!r})'.format(key, value))
        ht.set(key, value)
        print('hash table: {}'.format(ht))

    print("Testing update functionality of set method")
    ht.set('I', 10)
    print('hash table: {}'.format(ht))
    ht.set('V', 9)
    print('hash table: {}'.format(ht))

    print("Length of hash table: {}".format(ht.length()))

    print('\nTesting get:')
    for key in ['I', 'V', 'X']:
        value = ht.get(key)
        print('get({!r}): {!r}'.format(key, value))

    print('contains({!r}): {}'.format('X', ht.contains('X')))
    print('contains({!r}): {}'.format('W', ht.contains('W')))
    print('contains({!r}): {}'.format('I', ht.contains('I')))
    print('length: {}'.format(ht.length()))

    # Enable this after implementing delete method
    delete_implemented = True
    if delete_implemented:
        print('\nTesting delete:')
        for key in ['I', 'V', 'X']:
            print('delete({!r})'.format(key))
            ht.delete(key)
            print('hash table: {}'.format(ht))

        print('contains(X): {}'.format(ht.contains('X')))

        print('length: {}'.format(ht.length()))


if __name__ == '__main__':
    test_hash_table_iterator()
