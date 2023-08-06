import re
import math
import numpy as np

def quadratic(equation):
  equation = equation.replace(" ", "")

  pattern = r'([-+]?\d*)x\^2([-+]?\d*)x([-+]?\d*)'
  matches = re.match(pattern, equation)

  a_str, b_str, c_str = matches.groups()
  
  a = int(a_str) if a_str and a_str not in ['+', '-'] else (1 if a_str == '' else -1)
  b = int(b_str) if b_str and b_str not in ['+', '-'] else (1 if b_str == '' else -1)
  c = int(c_str) if c_str else 0

  try:

    pos = (-b+math.sqrt(b**2-4*a*c))/(2*a)
    neg = (-b-math.sqrt(b**2-4*a*c))/(2*a)
    
  except:

    pos, neg = None, None

  if pos == neg:
    return np.array([pos])
    
  return np.array([pos, neg])