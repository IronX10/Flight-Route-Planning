'''
Python Code to implement a heap with general comparison function
'''

class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array):
        self.init_array = init_array
        self.comparison_function = comparison_function
        self.build_heap(self.init_array)
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        
    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.init_array.append(value)
        self.up_heap(self.init_array, len(self.init_array)-1)
        return
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        if len(self.init_array)==0:
            return None
        temp=self.init_array[0]
        self.init_array[0]=self.init_array[-1]
        self.init_array.pop()
        self.down_heap(self.init_array, len(self.init_array), 0)
        return temp
    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        # Write your code here
        if len(self.init_array)==0:
            return None
        return self.init_array[0]
    
    # You can add more functions if you want to

    def build_heap(self,arr):
        n = len(arr)
        for i in range(n//2 - 1, -1, -1):
            self.down_heap(arr, n, i)
        return

    def down_heap(self,arr, n, i):
        temp=i
        while temp<n:
            left = 2*i+1
            right = 2*i+2
            if left<n and self.comparison_function(arr[left],arr[temp]):
                temp=left
            if right<n and self.comparison_function(arr[right],arr[temp]):
                temp=right
            if temp==i:
                break
            arr[i],arr[temp]=arr[temp],arr[i]
            i=temp
        return

    def up_heap(self,arr, i):
        temp=i
        while temp>=0:
            parent = (i-1)//2
            if parent>=0 and self.comparison_function(arr[temp],arr[parent]):
                temp=parent
            if temp==i:
                break
            arr[i],arr[temp]=arr[temp],arr[i]
            i=temp
        return

    def is_empty(self):
        return len(self.init_array)==0