import numpy as np

class LinearRegression:

  def __init__(self, learning_rate = 0.01, max_iters = 100000, tolerance = 1e-10):
    self.learning_rate = learning_rate
    self.max_iters = max_iters
    self.tolerance = tolerance
    self.params = None
    self.bias = None

  def h(self, X):
        return np.dot(X, self.params) + self.bias

  def j(self, X, y):
      se = np.mean((self.h(X) - y) ** 2)/2
      return se

  def fit(self, X, Y, progress=False):
    self.num_features = X.shape[1]
    self.num_samples = X.shape[0]

    self.params = np.zeros(self.num_features)
    self.bias = 0

    if Y.size != self.num_samples:
        raise ValueError("Number of samples in X and Y do not match.")

    iters = 0

    prev_cost = float('inf')

    for _ in range(self.max_iters):
      index = np.random.randint(self.num_samples)
      
      x = X[index]
      y = Y[index]

      predicted = np.dot(x, self.params) + self.bias

      grad_coef = (2/self.num_samples) * np.dot(x.T, predicted - y)
      grad_inte = (2/self.num_samples) * np.sum(predicted - y)

      self.params -= self.learning_rate * grad_coef
      self.bias -= self.learning_rate * grad_inte

      current_cost = self.j(X, Y)

      if abs(current_cost - prev_cost) < self.tolerance:
          break

      prev_cost = current_cost

      if progress:
          print("Squared error: ", self.j(X, Y))
          iters += 1

    if progress:
       print("Iterations: ", iters)

  def predict(self, x):
    return np.dot(x, self.params) + self.bias