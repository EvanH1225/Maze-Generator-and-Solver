import random

import numpy as np
import pprint


class Hashtable:

    def __init__(self, max_len):
        self.MAX_LENGTH = max_len
        self.table = np.empty(self.MAX_LENGTH, dtype=object)
        self.length = 0
        self.last_inserted = None
        self.first_inserted = None
        self.used_indices = []

    def add(self, entry):
        element, direction = entry
        # checks to make sure the element isn't already in the list
        if self.table[element.hashcode()] is None:

            # adds the new element to the hashtable
            self.table[element.hashcode()] = (element, direction, self.last_inserted, None)

            if self.last_inserted is not None:
                # edits the last element to update its next index
                print(self.last_inserted)
                print(self.table[self.last_inserted])
                last_element, prev_direction,  prev_index, _ = self.table[self.last_inserted]  # gets the last element
                self.last_inserted = element.hashcode()  # updates last_inserted to the new element added
                self.table[last_element.hashcode()] = (last_element, prev_direction, prev_index, self.last_inserted)  # stores index in the last element
            else:
                self.last_inserted = element.hashcode()
                self.first_inserted = element.hashcode()

            # updates the length
            self.length += 1
            self.used_indices.append(element.hashcode())

        else:
            element, direction, prev_index, next_index = self.table[element.hashcode()]

            # update previous element
            if prev_index is not None:
                prev_element, direction, temp_index, _ = self.table[prev_index]
                self.table[prev_index] = prev_element, direction, temp_index, next_index

            # update next element
            if next_index is not None:
                next_element, direction, _, temp_index = self.table[next_index]
                self.table[next_index] = next_element, direction, prev_index, temp_index

            # remove from current spot and add new element
            self.delete(element.hashcode())
            if element.hashcode() == self.last_inserted:
                self.last_inserted = prev_index
            self.add(entry)

    def delete(self, index):
        element, direction, prev_index, next_index = self.table[index]
        self.table[index] = None
        self.length -= 1
        self.used_indices.remove(index)
        return element, direction, prev_index, next_index

    def pop(self):
        element, direction, prev_index, next_index = self.delete(self.last_inserted)
        self.last_inserted = prev_index

        if prev_index is not None:
            prev_element, prev_direction, prev_prev_index, prev_next_index = self.table[prev_index]
            self.table[prev_index] = prev_element, prev_direction, prev_prev_index, None

        if self.length == 0:
            self.first_inserted = None
        return element, direction

    def popleft(self):
        element, direction, prev_index, next_index = self.delete(self.first_inserted)
        self.first_inserted = next_index

        if self.length == 0:
            self.last_inserted = None
        return element, direction

    def size(self):
        return self.length

    def contains(self, other_element):
        if self.table[other_element.hashcode()] is not None:

            element, _, _ = self.table[other_element.hashcode()]
            if element.equals(other_element):
                return True

        return False

    def clear(self):
        self.table = np.empty(self.MAX_LENGTH, dtype=object)

    def random_pop(self):
        random_index = random.choice(self.used_indices)

        if random_index == self.last_inserted:
            return self.pop()
        elif random_index == self.first_inserted:
            return self.popleft()

        element, direction, prev_index, next_index = self.table[random_index]

        # update previous element
        if prev_index is not None:
            prev_element, direction, temp_index, _ = self.table[prev_index]
            self.table[prev_index] = prev_element, direction, temp_index, next_index

        # update next element
        if next_index is not None:
            next_element, direction, _, temp_index = self.table[next_index]
            self.table[next_index] = next_element, direction, prev_index, temp_index

        # remove from current spot and add new element
        self.delete(random_index)
        return element, direction

    def pretty(self):
        result = "\n"
        for i in self.table:
            if i is not None:
                element, _, _, _ = i
                result += str(element.get_pos()) + ", " + str(element.hashcode()) + "\n"
            else:
                result += "None\n"
        return result
