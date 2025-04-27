# def cube(x):
#     return x*x*x

cube = lambda x: x*x*x
print(cube(22))





def sum(fs):
    def mx(*args, **kwargs):
        fs(*args, **kwargs)
    return mx  

@sum
def mysum(a,b):
    return a+b  

mysum(10,20)


import threading
import time

def second(x):
    print(f"sleeping for {x} seconf")
    time.sleep(x)
time1 = time.perf_counter()
'''second(3)
second(6)    
second(9)    
'''


t1 = threading.Thread(target=second,args=[2])
t2 = threading.Thread(target=second,args=[4])
t3 = threading.Thread(target=second,args=[5])
t4 = threading.Thread(target=second,args=[7])
t1.start()
t2.start()
t3.start()
t4.start()
time2 = time.perf_counter()
print(time2-time1)
