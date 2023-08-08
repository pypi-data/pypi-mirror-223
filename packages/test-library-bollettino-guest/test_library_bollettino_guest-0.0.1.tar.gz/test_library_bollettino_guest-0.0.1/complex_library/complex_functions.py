import math
import pandas as pd

def complex_function(a: float, b: float) -> float :
    """
    Takes 2 numbers as input, returns their sum times pi
    """
    result = (a + b) * math.pi
    return round(result, 3)
