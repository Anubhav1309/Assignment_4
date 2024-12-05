from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        self.z1 = params[0]
        self.table_size = params[-1]

        if collision_type == "Double":
            self.z2 = params[1] 
            self.c2 = params[2] 
            
        self.table = [None] * self.table_size
        self.count = 0
    
    def polynomial_hash(self, key, z, mod):
        h = 0
        for i, char in enumerate(key):
            if char.islower():
                p = ord(char) - ord('a')
            elif char.isupper():
                p = ord(char) - ord('A') + 26
            else:
                continue

            h = (h + p * pow(z, i, mod)) % mod
        return h
    
    
    def get_slot(self, key):
        h1 = self.polynomial_hash(key, self.z1, self.table_size)
        slots = []
        if self.collision_type == "Chain":
            slots.append(h1)
        elif self.collision_type == "Linear":
            for i in range(self.table_size):
                slots.append((h1 + i) % self.table_size)
        elif self.collision_type == "Double":
            h2 = self.c2 - (self.polynomial_hash(key, self.z2, self.c2) % self.c2)
            if h2 == 0:
                h2 = 1
            for i in range(self.table_size):
                slots.append((h1 + i * h2) % self.table_size)
        return slots
    
    def __str__(self):
        result = []
        for slot in self.table:
            if self.collision_type == "Chain":
                result.append(" ; ".join(str(x) for x in slot) if slot else "<EMPTY>")
            else:
                result.append(str(slot) if slot else "<EMPTY>")
        return " | ".join(result)
    
    def find(self, key):
        pass

    def insert(self, key):
        pass

    def get_load(self):
        return self.count / self.table_size

    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE

class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        self.keys = []
    
    def insert(self, key):
        if self.find(key):
            return
        probe_seq = self.get_slot(key)
        if self.collision_type == "Chain":
            slot = probe_seq[0]
            if self.table[slot] is None:
                self.table[slot] = []
            self.table[slot].append(key)
        else:
            for slot in probe_seq:
                if self.table[slot] is None:
                    self.table[slot] = key
                    break
            else:
                raise Exception("Hash table is full")
        self.keys.append(key)
        self.count += 1
    
    def find(self, key):
        probe_seq = self.get_slot(key)
        if self.collision_type == "Chain":
            slot = probe_seq[0]
            if self.table[slot]:
                return key in self.table[slot]
            else:
                return False
        else:
            for slot in probe_seq:
                if self.table[slot] is None:
                    return False
                elif self.table[slot] == key:
                    return True
            return False
    
    def get_load(self):
        return self.count / self.table_size
    
    def __str__(self):
        return super().__str__()
    
    def get_slot(self, key):
        return super().get_slot(key)
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, x):
        key, value = x
        probe_seq = self.get_slot(key)
        if self.collision_type == "Chain":
            slot = probe_seq[0]
            if self.table[slot] is None:
                self.table[slot] = []
            
            for i, item in enumerate(self.table[slot]):
                if item[0] == key:
                    self.table[slot][i] = (key, value)
                    return
            
            self.table[slot].append((key, value))
            self.count += 1
        else:
            for slot in probe_seq:
                if self.table[slot] is None:
                    self.table[slot] = (key, value)
                    self.count += 1
                    return
                elif self.table[slot][0] == key:
                    self.table[slot] = (key, value)
                    return

            raise Exception("Hash table is full")
    
    def find(self, key):
        probe_seq = self.get_slot(key)
        if self.collision_type == "Chain":
            slot = probe_seq[0]
            if self.table[slot]:
                for item in self.table[slot]:
                    if item[0] == key:
                        return item[1]
            return None
        else:
            for slot in probe_seq:
                if self.table[slot] is None:
                    return None
                elif self.table[slot][0] == key:
                    return self.table[slot][1]
            return None
    
    def get_load(self):
        return self.count / self.table_size
    
    def __str__(self):
        return super().__str__()
    
    def get_slot(self, key):
        return super().get_slot(key)
