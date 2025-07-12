class Queue:
    def __init__(self):
        self.start=0
        self.size=0
        self.items=[]

    def is_empty(self):
        return self.size==0

    def enque(self,x):
        if self.size==len(self.items):
            self.resize(2*len(self.items)+1)
        temp=(self.size+self.start)%len(self.items)
        self.items[temp]=x
        self.size+=1
    
    def dequeu(self):
        if self.size==0:
            return None
        ans=self.items[self.start]
        self.items[self.start]=None
        self.start=(self.start+1)%len(self.items)
        self.size-=1
        return ans

    def resize(self,size):
        temp=self.items
        self.items=[None]*size
        front=self.start
        for i in range(self.size):
            self.items[i]=temp[front]
            front=(front+1)%len(temp)
        self.start=0
        temp.clear()
        return
