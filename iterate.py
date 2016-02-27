import math

def iterate(fn, seed, iterations=1000000):
    val = seed
    for i in range(iterations):
        val = fn(val)
        print val

if __name__ == '__main__':
    iterate(math.cos, 1.57)
    # iterate(lambda x:4*x*(1-x), 0.8)

        
    
