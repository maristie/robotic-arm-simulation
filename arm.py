import math

class Arm:

    # Arm lengths
    ARM1 = 150
    ARM2 = 100
    ARM3 = 50

    def __init__(self, alpha=math.pi/2, beta=0, gamma=-math.pi/2):
        """
        Default values represent initial positions of the arms.
        alpha, beta, gamma are angles of AB, BC, CD based on spherical coordinate.
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def eval(self, x=0, y=0, point='D'):
        """
        Evaluate the coordinates of points B, C, D.
        Optionally, evaluate the different between this point and another specific point (x, y).
        """
        return [
            self.ARM1 * math.cos(self.alpha) + (self.ARM2 * math.cos(self.beta) if point != 'B' else 0) + (self.ARM3 * math.cos(self.gamma) if point == 'D' else 0) - x,
            self.ARM1 * math.sin(self.alpha) + (self.ARM2 * math.sin(self.beta) if point != 'B' else 0) + (self.ARM3 * math.sin(self.gamma) if point == 'D' else 0) - y,
        ]

    def derivative(self):
        """
        Evaluate the partial derivatives of D(x, y) against variables (alpha, beta, gamma).
        The result is a 2*3 matrix.
        """
        return [
            [-self.ARM1 * math.sin(self.alpha), -self.ARM2 * math.sin(self.beta), -self.ARM3 * math.sin(self.gamma)],
            [self.ARM1 * math.cos(self.alpha), self.ARM2 * math.cos(self.beta), self.ARM3 * math.cos(self.gamma)],
        ]