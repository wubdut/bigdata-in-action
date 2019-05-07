from multiprocessing import Process    
import os    
import numpy as np    
    
class F:    
    def __init__(self, len):    
        self.W = np.random.randn(len)    
    
    def function(self, x):    
        return np.dot(self.W, x)    
    
    
def eval_numerical_gradient(f, x):    
    """  
    a naive implementation of numerical gradient of f at x  
    - f should be a function that takes a single argument  
    - x is the point (numpy array) to evaluate the gradient at  
    """    
    fx = f.function(x) # evaluate function value at original point    
    grad = np.zeros(x.shape)    
    h = 0.00001    
    # iterate over all indexes in x    
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])    
    while not it.finished:    
        # evaluate function at x+h    
        ix = it.multi_index    
        old_value = x[ix]    
        x[ix] = old_value + h # increment by h    
        fxh = f.function(x) # evaluate f(x + h)    
        x[ix] = old_value # restore to previous value (very important!)    
        # compute the partial derivative    
        grad[ix] = (fxh - fx) / h # the slope    
        it.iternext() # step to next dimension    
    return grad 
