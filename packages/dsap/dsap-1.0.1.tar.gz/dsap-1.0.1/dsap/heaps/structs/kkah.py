""" 
    ##################################################
    # KEYED D-ARY/K-ARY HEAP IMPLEMENTATION [PYTHON] #
    ##################################################

    NOTES 
        * array based 
		* does not require other files
		* printable / narrow width

    API 
        KBH_Item 
            Properties 
                - key 
                - value 
                - data 

        KBH 
            Properties 
                - items 
                - type 
                - key_no 
                - key_map
            
            Utility Methods 
                - comparator(a, b) 
                - bubble_up(arr, i)
                - bubble_down(arr, i)
                - keyfy(items) 
                - swap_key_map(i, j)
                - parent(i)
                - child(i, j) 
                - update_a(key, value)
                - update_b(key, value)
                - display()

            Main Operations
                - heapify_up(items, keyfy) 
                - heapify_down(items, keyfy) 
                - insert(key, value, data)
                - insert_node(node)
                - pop() 
                - delete(key)
                - clear()

            Accessors / Mutators  
                - update(key, new_value)
                - keys()
                - values()
                - top()
                - size()
                - is_empty()
                - get_data(key)
                - set_data(key, data) 
                - get_value(key) 
                - set_value(key, value)
                - get_item(key) 
                - set_item(key, data) 
                - display()
                - min() 
                - max() 
                - has_key(key)
""" 

class KKAH_Item: 
    def __init__(self, key, value, data): 
        self.key = key 
        self.value = value 
        self.data = data 
  

class KKAH: 
    def __init__(self, degree = 3, type_ = "min"): 
        self.items = [] 
        self.key_map = {}  
        self.degree = degree
        self.type = type_
        self.key_no = 0

    #
    # UTILITY METHODS
    # 

    def comparator(self, a, b): 
        if self.type == "min": 
            return a.value < b.value 
        elif self.type == "max": 
            return a.value > b.value 
        return None
    
    def bubble_down(self, arr, i): 
        n = len(arr) 
        d = self.degree

        while 2 * i + 1 < n: 
            m = i 
            for j in range(d): 
                c = self.child(i, j) 
                if c < n and self.comparator(arr[c], arr[m]): 
                    m = c 
            if m == i: 
                break  
            else: 
                self.swap_key_map(m, i) 
                arr[m], arr[i] = arr[i], arr[m] 
                i = m 

        return arr 

    def bubble_up(self, arr, i): 
        while i > 0: 
            p = self.parent(i)
            if self.comparator(arr[i], arr[p]):
                self.swap_key_map(i, p)
                arr[p], arr[i] = arr[i], arr[p] 
                i = p 
            else: 
                break 
        return arr 
    
    def keyfy(self, items): 
        if type(items) is list: 
            for i in range(len(items)): 
                items[i] = KKAH_Item(self.key_no, items[i], None)
                self.key_map[items[i].key] = i
                self.key_no += 1 
            return items
        elif type(items) is dict: 
            i = 0
            new_items = []
            for key in items: 
                value = items[key]
                new_items.append(KKAH_Item(key, value, None))
                self.key_map[key] = i
                self.key_no += 1 
                i += 1
            return new_items

    def swap_key_map(self, i, j): 
        arr = self.items
        self.key_map[arr[i].key] = j
        self.key_map[arr[j].key] = i
    
    def parent(self, i): 
        d = self.degree 
        return (i - 1) // d

    def child(self, i, j): 
        if j >= self.degree:
            error = f"Out of bounds for {j} when accessing children."
            raise Exception(error)
        return 2 * i + j 

    def update_a(self, key, value): 
        arr = self.items 
        i = self.key_map[key] 
        arr[i].value = value
        self.bubble_up(arr, i) 

    def update_b(self, key, value): 
        arr = self.items
        i = self.key_map[key] 
        arr[i].value = value
        n = len(arr)
        self.bubble_down(arr, i)

    def display(self): 
        text = [] 
        for item in self.items: 
            text.append(f"(k: {item.key}, v: {item.value}, " + \
                        f"d: {item.data})")
        print(", ".join(text))

    #
    # MAIN OPERATIONS
    #

    def heapify_up(self, arr, keyfy = True): 
        self.items = arr 
        
        if keyfy: 
            arr = self.keyfy(self.items) 
            self.items = arr 
        
        n = len(arr) 

        for i in range(n): 
            j = i 
            self.bubble_up(arr, j) 

    def heapify_down(self, arr, keyfy = True): 
        self.items = arr 
        
        if keyfy: 
            arr = self.keyfy(self.items) 
            self.items = arr 
    
        n = len(arr)
        d = self.degree

        for i in range(n // d - 1, -1, -1): 
            j = i 
            self.bubble_down(arr, j)   

    def insert(self, key, value, data = None): 
        item = KKAH_Item(key, value, data)

        arr = self.items 
        arr.append(item)
        
        i = len(arr) - 1 
        self.key_map[key] = i 

        self.bubble_up(arr, i)

    def pop(self): 
        if len(self.items) == 1: 
            self.items = [] 
            return 

        arr = self.items 
        n = len(arr)
        l = n - 1 

        item = arr[0]
        del self.key_map[arr[0].key]
        self.key_map[arr[l].key] = 0
        arr[0] = arr[l]

        arr.pop(l)
        n = len(arr)

        self.bubble_down(arr, 0) 

        return item 
    
    def delete(self, key):
        rem_val = float('-inf') if self.type == "min" else float("inf")
        self.update(key, rem_val) 
        self.pop()

    def clear(self): 
        self.items = []

    #
    # ACCESSORS / MUTATORS
    #

    def update(self, key, new_value): 
        arr = self.items 
        if key not in self.key_map: 
            raise Exception(f"{key} is not in list.")
        i = self.key_map[key] 

        aux = KKAH_Item(key, new_value, None)
        item = arr[i] 
    
        if self.comparator(aux, item):
            self.update_a(key, new_value)
        else:   
            self.update_b(key, new_value)

    def items(self): 
        for item in self.items: 
            yield item
            
    def keys(self): 
        for item in self.items: 
            yield item.key
    
    def values(self): 
        for item in self.items: 
            yield item.value

    def top(self): 
        if self.size() > 0: 
            return self.items[0]
        else: 
            return None

    def size(self): 
        return len(self.items)

    def is_empty(self): 
        return self.size() == 0

    def get_data(self, key): 
        return self.get_item(key).data

    def set_data(self, key, data): 
        self.get_item(key).data = data

    def get_value(self, key): 
        return self.get_item(key).value 

    def set_value(self, key, value): 
        self.get_item(key).value = value

    def get_item(self, key): 
        return self.items[self.key_map[key]]

    def set_item(self, key, item): 
        self.items[self.key_map[key]] = item

    def min(self): 
        if self.type != "min":
            raise Exception("Not a minimum heap.") 
        return self.top() 

    def max(self): 
        if self.type != "max": 
            raise Exception("Not a maximum heap.") 
        return self.top() 

    def min_key(self): 
        return self.min().key 
    
    def min_value(self): 
        return self.min().value 

    def max_key(self): 
        return self.max().key 

    def max_value(self) :
        return self.max().value

    def has_key(self, key): 
        return key in self.key_map

    def clear(self): 
        self.items = []
        self.key_no = 0
        self.key_map = {}