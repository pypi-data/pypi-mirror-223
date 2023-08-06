import numpy as np
import scipy


class eigenvector:

  def determinant(self, x):
    I = np.eye(self.A.shape[0])

    B = self.A - x * I

    return np.linalg.det(B)

  def eigval(self, tolerance=1e-8):
    eigenvalues = []
    for i in range(1, self.A.shape[0] + 1):
      x_solution = scipy.optimize.fsolve(self.determinant, x0=i)
      for val in x_solution:
        duplicate = False
        for eigenval in eigenvalues:
          if abs(val - eigenval) < tolerance:
            duplicate = True
            break
        if not duplicate:
          eigenvalues.append(val)
    self.eigenvalues = np.array(eigenvalues)

  def eigvec(self):
    self.eigenvectors = []
    I = np.eye(self.A.shape[0])

    for eigenval in self.eigenvalues:
      B = self.A - eigenval * I

      _, _, V = np.linalg.svd(B)
      eigenvector = V[-1]
      eigenvector = eigenvector / np.linalg.norm(eigenvector)
      if eigenvector[0] != 0:
        reciprocal = 1 / eigenvector[0]
        for i in range(len(eigenvector)):
          eigenvector[i] = reciprocal * eigenvector[i]
      self.eigenvectors.append(eigenvector)

    self.eigenvectors = np.array(self.eigenvectors)

  def __init__(self, matrix):
    self.A = matrix
    self.eigenvalues = None
    self.eigval()
    self.eigenvectors = None
    self.eigvec()