
def calculate_code(n):
    code = 20151125
    for i in range(1, n):
        code = (code*252533)%33554393
    return code



def calculate_number(n, m):
    return ((n+m-2)*(n+m-1))//2 + m


# Test the function
import time 
start_time = time.time()
print(calculate_number(2978, 3083))  # Output: 19                     
print(calculate_code(18361853))
endTime = time.time()
print("Time taken: ",endTime  - start_time)
print("Time taken in ms: ", (endTime - start_time) * 1000)

