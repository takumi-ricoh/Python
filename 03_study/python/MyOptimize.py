import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def f(x):
    return x**2 + 10*np.sin(x)

x = np.arange(-10, 10, 0.1)
plt.plot(x, f(x))

a=optimize.fmin_bfgs(f,0,disp=0)
b=optimize.fmin_bfgs(f,3,disp=0)
c=optimize.basinhopping(f,0)
d=optimize.fsolve(f,1)

#print(a)

#print(b)

#print(c)

print(d

)