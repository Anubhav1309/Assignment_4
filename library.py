import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]: 
            result.append(left[i])
            i +=1
        else:
            result.append(right[j])
            j +=1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        self.books = {title: merge_sort(self.unique_words(text)) for title, text in zip(book_titles, texts)}
    
    def distinct_words(self, book_title):
        return merge_sort(self.books[book_title])
    
    def unique_words(self, words):
        unique_list = []
        for word in words:
            if word not in unique_list:
                unique_list.append(word)
        return unique_list
    
    def count_distinct_words(self, book_title):
        return len(self.distinct_words(book_title))
    
    def search_keyword(self, keyword):
        list_of_books = []
        for title, words in self.books.items():
            if keyword in words:
                list_of_books.append(title)
        
        list_of_books = merge_sort(list_of_books)
        return list_of_books
    
    def print_books(self):
        for title in merge_sort(list(self.books.keys())):
            words = self.books[title]
            print(f"{title}: {' | '.join(words)}")

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''

        self.name = name
        self.books = {}
        
        if name == "Jobs":
            self.hash_table = ht.HashTable(collision_type="Chain", params=params)
        elif name == "Gates":
            self.hash_table = ht.HashTable(collision_type="Linear", params=params)
        elif name == "Bezos":
            self.hash_table = ht.HashTable(collision_type="Double", params=params)
    
    def add_book(self, book_title, text):
        unique_words = self.unique_words(text)
        if self.name == "Bezos":
            params = [self.hash_table.z1, self.hash_table.z2, self.hash_table.c2, self.hash_table.table_size]
        else:
            params = [self.hash_table.z1, self.hash_table.table_size]
        self.books[book_title] = ht.HashSet(self.hash_table.collision_type, params)
        for word in unique_words:
            self.books[book_title].insert(word)
    
    def unique_words(self, words):
        unique_list = []
        for word in words:
            if word not in unique_list:
                unique_list.append(word)
        return unique_list
    
    def distinct_words(self, book_title):
        if book_title in self.books:
            hash_set = self.books[book_title]
            if self.hash_table.collision_type == "Chain":
                words = []
                for slot in hash_set.table:
                    if slot:
                        words.extend(slot)
                return words
            else:
                list_ans =  [word for word in hash_set.table if word is not None]  
                return list_ans
        return []
    
    def count_distinct_words(self, book_title):
        if book_title in self.books:
            return self.books[book_title].count
        return 0
    
    def search_keyword(self, keyword):
        found_books = []
        for book_title, hash_set in self.books.items():
            if hash_set.find(keyword):
                found_books.append(book_title)
        return merge_sort(found_books)
    
    def print_books(self):
        for book_title, hash_set in self.books.items():
            print(f"{book_title}: {hash_set}")
