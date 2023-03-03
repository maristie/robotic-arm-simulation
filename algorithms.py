import numpy as np
from arm import Arm


ITERATIONS = 20

def optimize(arm_obj, x, y):
    """
    Iterate for fixed number of loops, and return the resulting arms.
    (x, y) is the target of D point.
    """
    for _ in range(ITERATIONS):
        arm_obj = _next_arguments(arm_obj, x, y)
    return arm_obj

def _next_arguments(arm_obj, x, y):
    """A single iteration of Newton's method."""
    mat = np.matrix(arm_obj.derivative())
    pinv = np.linalg.pinv(mat) # evaluate pseudo inverse matrix
    args = [arm_obj.alpha, arm_obj.beta, arm_obj.gamma]
    next_args = np.array(args) - np.array((pinv @ np.matrix(arm_obj.eval(x, y)).T).T)[0]
    return Arm(*next_args)
