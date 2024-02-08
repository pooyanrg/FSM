import numpy as np
import random


CAPACITY_CHOICES = [5, 11, 23, 47, 97, 197, 397, 797, 1597, 3203, 6421, 12853, 25717, 51437, 102877, 205759, 411527, 823117, 1646237, 3292489, 6584983, 13169977, 26339969, 52679969, 105359939]

class Node: 
	def __init__(self, key, value): 
		self.key = key 
		self.value = value 
		self.next = None


class HashTable: 
	def __init__(self, capacity): 
		self.capacity = capacity 
		self.size = 0
		self.table = [None] * capacity 

	def _hash(self, key): 
		return hash(key) % self.capacity 

	def insert(self, key, value): 
		index = self._hash(key) 

		if self.table[index] is None: 
			self.table[index] = Node(key, value) 
			self.size += 1
		else: 
			current = self.table[index] 
			while current: 
				if current.key == key: 
					current.value = value 
					return
				current = current.next
			new_node = Node(key, value) 
			new_node.next = self.table[index] 
			self.table[index] = new_node 
			self.size += 1
		
	def search(self, key): 
		index = self._hash(key) 

		current = self.table[index] 
		while current: 
			if current.key == key: 
				return current.value 
			current = current.next

		return False 

	def remove(self, key): 
		index = self._hash(key) 

		previous = None
		current = self.table[index] 

		while current: 
			if current.key == key: 
				if previous: 
					previous.next = current.next
				else: 
					self.table[index] = current.next
				self.size -= 1
				return
			previous = current 
			current = current.next

		raise KeyError(key) 

	def __len__(self): 
		return self.size 

	def __contains__(self, key): 
		try: 
			self.search(key) 
			return True
		except KeyError: 
			return False
		
	def factor(self): 
		return self.size / self.capacity
	
    
def resize(H, cap):
	old_cap = H.capacity
	old_table = H.table
	ht = HashTable(cap)
	for i in range(old_cap):
		current = old_table[i]
		if current:
		    while(current.next):
				ht.insert(current.next.key, current.next.value)
	return ht
	



# # Driver code 
# if __name__ == '__main__': 

# 	# Create a hash table with 
# 	# a capacity of 5 
# 	ht = HashTable(CAPACITY_CHOICES[0]) 

# 	# Add some key-value pairs 
# 	# to the hash table 
# 	ht.insert("apple", 3) 
# 	ht.insert("banana", 2) 
# 	ht.insert("cherry", 5) 

# 	# Check if the hash table 
# 	# contains a key 
# 	print("apple" in ht) # True 
# 	print("durian" in ht) # False 

# 	# Get the value for a key 
# 	print(ht.search("banana")) # 2 

# 	# Update the value for a key 
# 	ht.insert("banana", 4) 
# 	print(ht.search("banana")) # 4 

# 	ht.remove("apple") 
# 	# Check the size of the hash table 
# 	print(len(ht)) # 3 
