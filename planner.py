from flight import Flight
from myqueue import Queue
from myheap import Heap

def merge(left,right):
    i=0
    j=0
    ans=[]
    while i<len(left) and j<len(right) :
        if left[i].departure_time<right[j].departure_time:
            ans.append(left[i])
            i+=1
        else:
            ans.append(right[j])
            j+=1
    while i<len(left):
        ans.append(left[i])
        i+=1
    while j<len(right):
        ans.append(right[j])
        j+=1
    return ans

def mergeSort(low,high,arr):
    if low==high:
        return [arr[low]]
    else:
        mid=(low+high)//2
        left=mergeSort(low,mid,arr)
        right=mergeSort(mid+1,high,arr)
        return merge(left,right)

def sort_comparator(travel1):
    return travel1.departure_time

def travel_comparison1(travel1,travel2):
    if travel1.fare<travel2.fare:
        return True
    elif travel1.fare>travel2.fare:
        return False
    else:
        return travel1.flight.arrival_time<travel2.flight.arrival_time

def travel_comparison2(travel1,travel2):
    if travel1.flights<travel2.flights:
        return True
    elif travel1.flights>travel2.flights:
        return False
    elif travel1.fare<travel2.fare:
        return True
    elif travel1.fare>travel2.fare:
        return False
    else:
        return travel1.flight.arrival_time<travel2.flight.arrival_time

class Travel:
    def __init__(self,flight,prev,fare=0,flights=0):
        self.flight:Flight=flight
        self.prev:Travel=prev
        self.fare=fare
        self.flights=flights

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.m=0
        for i in flights:
            if i.start_city>self.m:self.m=i.start_city
            if i.end_city>self.m:self.m=i.end_city
        self.flights1=[None]*(self.m+1)
        for i in flights:
            if self.flights1[i.start_city]==None:
                self.flights1[i.start_city]=[i]
            else:
                self.flights1[i.start_city].append(i)
        for index in range(len(self.flights1)):
            if self.flights1[index]:
                self.flights1[index] = sorted(self.flights1[index], key=sort_comparator)
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if start_city==end_city:
            return []
        q=Queue()
        min=float('inf')
        n=float('inf')
        route=None
        visited=[0]*(self.m+1)
        for i in range(self.m+1):
            if self.flights1[i]:visited[i]=len(self.flights1[i])
        visited2=[None]*(self.m+1)
        q.enque((start_city,None,t1-20,0))
        while not q.is_empty():
            city,prev,arr,flights=q.dequeu()
            if flights>n:
                break
            if city==end_city and arr<=t2:
                if arr<min:
                    min=arr
                    route=prev
                    n=flights
                continue
            temp=visited[city]
            for i in range(temp):
                flight=self.flights1[city][i]
                if visited2[flight.end_city]==None or visited2[flight.end_city]>flight.arrival_time:
                    if flight.departure_time>=arr+20 and flight.arrival_time<=t2:
                        visited2[flight.end_city]=flight.arrival_time
                        travel=Travel(flight,prev)
                        q.enque((flight.end_city,travel,flight.arrival_time,flights+1))
                        if i<visited[city]:visited[city]=i
        if not route or route.flight.end_city!=end_city or route.flight.arrival_time>t2:
            return []
        ans=[route.flight]
        while not route.prev==None:
            route=route.prev
            ans.append(route.flight)
        ans.reverse()
        return ans
        
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        if start_city==end_city or not self.flights1[start_city]:
            return []
        temp=[]
        for j in self.flights1[start_city]:
            if j.departure_time>=t1:
                temp.append(Travel(j,None,j.fare))
        heap=Heap(travel_comparison1,temp)
        best_travel=heap.extract()
        n=0
        visited=[0]*(self.m+1)
        for i in range(self.m+1):
            if self.flights1[i]:visited[i]=len(self.flights1[i])
        while best_travel and not (best_travel.flight.end_city==end_city and best_travel.flight.arrival_time<=t2):
            temp=visited[best_travel.flight.end_city]
            for j in range(temp):
                i=self.flights1[best_travel.flight.end_city][j]
                if i.departure_time-20>=best_travel.flight.arrival_time and i.arrival_time<=t2:
                    heap.insert(Travel(i,best_travel,best_travel.fare+i.fare))
                    if j<temp:visited[best_travel.flight.end_city]=j
            best_travel=heap.extract()
        if not best_travel or best_travel.flight.arrival_time>t2:
            return []
        ans=[best_travel.flight]
        while best_travel.prev!=None:
            best_travel=best_travel.prev
            ans.append(best_travel.flight)
        ans.reverse()
        return ans            

    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if start_city==end_city or not self.flights1[start_city]:
            return []
        temp=[]
        for j in self.flights1[start_city]:
            if j.departure_time>=t1:
                temp.append(Travel(j,None,j.fare,1))
        heap=Heap(travel_comparison2,temp)
        best_travel=heap.extract()
        n=0
        visited=[0]*(self.m+1)
        for i in range(self.m+1):
            if self.flights1[i]:visited[i]=len(self.flights1[i])
        while best_travel and not (best_travel.flight.end_city==end_city and best_travel.flight.arrival_time<=t2):
            temp=visited[best_travel.flight.end_city]
            for j in range(temp):
                i=self.flights1[best_travel.flight.end_city][j]
                if i.departure_time-20>=best_travel.flight.arrival_time and i.arrival_time<=t2:
                    heap.insert(Travel(i,best_travel,best_travel.fare+i.fare,best_travel.flights+1))
                    if j<temp:visited[best_travel.flight.end_city]=j
            best_travel=heap.extract()
        if not best_travel or best_travel.flight.arrival_time>t2:
            return []
        ans=[best_travel.flight]
        while best_travel.prev!=None:
            best_travel=best_travel.prev
            ans.append(best_travel.flight)
        ans.reverse()
        return ans