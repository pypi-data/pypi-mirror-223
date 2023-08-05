'''
    ######################################
    # HASH TABLE IMPLEMENTATION [PYTHON] #
    ######################################

    NOTES   
        * main source: programiz.com (modified implementation)
        * requires singly linked-list (same project)
		* printable / narrow width 

    API  
        HashTable   
            Properties
                - size 
                - resolution_mode 
                - quadratic_probe_c1 
                - quadratic_probe_c2 
                - multiplication_hash-a 
                - hash_function_a 
                - hash_function_b 
                - threshold_mode 
                - threshold_factor  
                - load_factor 
                - table 

            Static Methods 
                - init_cap(n)
            
            Utility Methods 
                - map_hash_fn(idx) 
                - setup_hash_fns() 
                - make_container() 
                - make_table(capacity)
            
            General Methods 
                - threshold() 
                - capacity()
                - rehash()
                - expand() 
                - shrink() 
                - size()
                - is_empty()

            Open Addressing Fnctions 
                - linear_probe(k, i) 
                - quadratic_probe(k, i) 
                - double_hashing(k, i) 

            Hash Functions 
                - division_hash(k) 
                - multiplication_hash(k) 
            
            Main Operations 
                - set_item(key, val)
                - insert_item(key, val)
                - update_item(key, val) 
                - remove_item(key) 
                - has_item(key)
                - get_item(key)
                - search(key)
                - clear()

            Utility Methods
                - iterate(cb)
                - report_container_frequencies()
                - report_container_items() 
                - display() 
                - size()

            Key/Value/Items Accessors 
                - items() 
                - keys() 
                - values() 
 ''' 

from dsap.linked_lists.structs.sll import SLL
import math 

#############
# CONSTANTS #
#############

# --- COLLISION RESOLUTION --- # 
CHAINING_RESOLUTION = 1 
LINEAR_PROBING_RESOLUTION = 2 
QUADRATIC_PROBING_RESOLUTION = 3 

OPEN_ADDRESSING_MODES = [
    LINEAR_PROBING_RESOLUTION,
    QUADRATIC_PROBING_RESOLUTION 
]

# --- HASH FUNCTIONS --- # 
DIVISION_METHOD = 4
MULTIPLICATION_METHOD = 5

#####################
# UTILITY FUNCTIONS #
##################### 

def log2(x):
    return x.bit_length() + 2

class HashTable: 
    def __init__(self, init_cap = 2, **kwargs):
        
        # meta config
        self.count = 0
        self.resolution_mode = \
            kwargs.get("resolution_mode", CHAINING_RESOLUTION) 

        #
        # Source: https://en.wikipedia.org/wiki/Quadratic_probing
        #    * 1/2 is a good c1 and c2 val for 2^n
        #
        self.quadratic_probe_c1 = 1/2
        self.quadratic_probe_c2 = 1/2 

        #
        # Source: https://www.programiz.com/dsa/hash-table
        #    * (sqrt(5) - 1) / 2 is a good val for A
        # 
        self.multiplication_hash_a = ((5 ** 1/2) - 1) / 2
         
        # 
        # Hash Function Configuration
        # 

        self.hash_function_a = \
            kwargs.get("hash_fn_a", DIVISION_METHOD) 
        self.hash_function_b = \
            kwargs.get("hash_fn_b", MULTIPLICATION_METHOD)

        self.hash_fn_a = None 
        self.hash_fn_b = None 
        
        self.setup_hash_fns()

        #
        # Threshold Configuration (for Chaining)
        # 
        self.threshold_mode = "constant"
        self.threshold_factor = 10

        #
        # Load Factor Configuration (for Open Addressing)
        # 
        self.load_factor = 0.8

        # main table 
        self.table = [self.make_container() for i in range(init_cap)]

    #
    # STATIC METHODS 
    # 

    def init_cap(n): 
        x = math.ceil(log2(n))
        return 2 ** (x + 2)

    #
    # UTILITY METHODS 
    # 

    def map_hash_fn(self, idx): 
        if idx == DIVISION_METHOD: 
            return self.division_hash
        elif idx == MULTIPLICATION_METHOD:
            return self.multiplication_hash 
        
    def setup_hash_fns(self):      
        self.hash_fn_a = self.map_hash_fn(self.hash_function_a)
        self.hash_fn_b = self.map_hash_fn(self.hash_function_b)

    def make_container(self): 
        if self.resolution_mode == CHAINING_RESOLUTION: 
            return SLL() 
        elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
            return None
 
    def make_table(self, capacity): 
        table = [] 
        for i in range(capacity): 
            table.append(self.make_container())
        return table

    # 
    #  GENERAL METHODS
    #
    def threshold(self):
        tf = self.threshold_factor  
        tm = self.threshold_mode 
        if tm == "log":
            return int(tf * log2(self.capacity()))
        elif tm == "constant": 
            return tf

    def capacity(self):
        return len(self.table)

    
    def rehash(self, aux): 
        # handle chaining resolution mode
        if self.resolution_mode == CHAINING_RESOLUTION:     
            for container in self.table: 
                current = container.head 
                while current is not None: 
                    aux.set_item(current.value[0], current.value[1])
                    current = current.next 

        # handle open addressing mode
        elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
            for container in self.table:
                if container is not None:
                    aux.set_item(container[0], container[1])

        self.table = aux.table

    def expand(self): 
        # make an auxiliary hash table 
        aux = HashTable(
            self.capacity() * 2, 
            resolution_mode = self.resolution_mode,
            hash_fn_a=self.hash_function_a, 
            hash_fn_b=self.hash_function_b
        )

        self.rehash(aux)

    def shrink(self): 
        # make an auxiliary hash table 
        aux = HashTable(
            self.capacity() // 2, 
            resolution_mode=self.resolution_mode,
            hash_fn_a=self.hash_function_a, 
            hash_fn_b=self.hash_function_b
        )

        self.rehash(aux)

    def resolver(self): 
        if self.resolution_mode == LINEAR_PROBING_RESOLUTION: 
            return self.linear_probe 
        elif self.resolution_mode == QUADRATIC_PROBING_RESOLUTION:
            return self.quadratic_probe 
        elif self.resolution_mode == DOUBLE_HASHING_RESOLUTION: 
            return self.double_hashing 
        
    # --- Open Addressing Functions --- # 
    def linear_probe(self, k, i): 
        m = self.capacity()
        hf = self.hash_fn_a
        return int((hf(k) + i) % m)

    def quadratic_probe(self, k, i): 
        m = self.capacity()
        hf = self.hash_fn_a
        c1 = self.quadratic_probe_c1 
        c2 = self.quadratic_probe_c2
        return int((hf(k) + (c1 * i) + (c2 * (i << 1))) % m)

    # --- Hash Functions --- # 
    def division_hash(self, k):
        k = int(k)
        m = self.capacity()
        return k % m

    def multiplication_hash(self, k):
        k = int(k)
        m = self.capacity()
        A = self.multiplication_hash_a  
        return int(m * ((k * A) % 1))

    # 
    # MAIN OPERATIONS 
    # 
    def set_item(self, key, val):   
        if self.has_item(key): 
            self.update_item(key, val)
        else: 
            self.insert_item(key, val)

    def insert_item(self, key, val):
        if self.resolution_mode == CHAINING_RESOLUTION: 
            index = self.hash_fn_a(key)  
            container = self.table[index] 
            container.append([key, val])

            self.count += 1

            # expand when container size reach threshold
            if container.count >= self.threshold(): 
                self.expand()

        elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
            i = 0 

            resolver = self.resolver()
            index = None 
            
            while True: 
                index = resolver(key, i)
                if self.table[index] is None: 
                    break 
                i += 1

            self.table[index] = [key, val] 
            self.count += 1 

            # expand when list reaches maximum capacity
            if self.count >= self.capacity() * self.load_factor:
                self.expand()  

        else: 
            error = "Unknown resolution mode when inserting item."
            raise Exception(error)
    
    def update_item(self, key, val): 
        if not self.has_item(key):
            raise Exception("Item not in hash table.") 
        else: 
            search = self.search(key) 
            if self.resolution_mode == CHAINING_RESOLUTION: 
                self.table[search[1]].at(search[2]).value[1] = val
            elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
                self.table[search[1]][1] = val 

    def remove_item(self, key):
        if not self.has_item(key): 
            raise Exception("Item not in hash table.") 
        else: 
            # remove item from hash table
            search = self.search(key)
            
            if self.resolution_mode == CHAINING_RESOLUTION: 
                self.table[search[1]].delete(search[2])
            elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
                self.table[search[1]] = None
            
            
            self.count -= 1

            # attempt to shrink  hash table
            threshold = None

            if self.resolution_mode == CHAINING_RESOLUTION: 
                threshold = (self.capacity() * self.threshold()) // 2
            elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
                threshold = self.capacity() * self.load_factor 

            if self.count < self.threshold(): 
                self.shrink()


    def has_item(self, key): 
        if self.search(key): 
            return True 
        else: 
            return False 

    def get_item(self, key): 
        s = self.search(key)
        if s == None: 
            return None 
        else: 
            return s[0][1]

    def search(self, key): 
        if self.resolution_mode == CHAINING_RESOLUTION: 
            index = self.hash_fn_a(key)  
            container = self.table[index] 
            current = container.head 
            i = 0 
            while current is not None: 
                if current.value[0] == key: 
                    return current.value, index, i
                current = current.next
                i += 1
            return None  

        elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
            i = 0 

            resolver = self.resolver()
            index = None 

            while i < self.capacity(): 
                index = resolver(key, i)
                
                if self.table[index] is not None and \
                   self.table[index][0] == key: 
                    return self.table[index], index 

                i += 1

            return None 

    def clear(self):
        self.table = self.make_table(self.capacity()) 
        self.count = 0

    def iterate(self, cb): 
        if self.resolution_mode == CHAINING_RESOLUTION: 
            i = 0 
            idx = 0
            for container in self.table: 
                current = container.head
                j = 0
                while current is not None: 
                    yield current.value, i, j, idx
                    current = current.next 
                    j += 1
                    idx += 1 
                i += 1
            return None

        elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
            i = 0
            idx = 0
            j = None
            for item in self.table: 
                if item != None:
                    yield item, i, j, idx
                    idx += 1
                i += 1

  
    def report_container_frequencies(self): 
        containers = [None] * self.capacity()   
        for i in range(len(self.table)): 
            containers[i] = self.table[i].size
        return containers

    def report_container_items(self): 
        for item in self.table: 
            print(item)

    def display(self): 
        self.traverse(
            lambda item, i, j, idx: 
                print(str(item).ljust(20), i, j, idx)
        )
            
    def size(self): 
        return self.count

    def is_empty(self): 
        return self.size() == 0

    # --- KEY/VALUE/ITEM ACCESSORS --- # 

    def items(self): 
        if self.resolution_mode == CHAINING_RESOLUTION: 
            for container in self.table: 
                current = container.head
                while current is not None: 
                    item = current.value
                    yield item
                    current = current.next
            return None

        elif self.resolution_mode in OPEN_ADDRESSING_MODES: 
            for item in self.table: 
                if item != None:
                    yield item

    def keys(self): 
        for item in self.items(): 
            yield item[0]

    def values(self):
        for item in self.items(): 
            yield item[1]
