## Environment

Tested on
* macOS Ventura 13.1
* Python 3.11.1

But any other operating systems (Windows/Linux) should be fine as long as latest Python is installed.


## Dependencies

Only three libraries are used:
* matplotlib
* numpy
* tkinter

The former two packages can be installed through `pip`.

```
python3.11 -m pip install -U matplotlib
// Or pip install matplotlib
python3.11 -m pip install -U numpy
// Or pip install numpy
```

`tkinter` is installed by different methods depending on your platform. On macOS, install by `brew` typing `brew install python-tk`. On Windows, `tkinter` is said to be installed with Python by default, but I cannot verify it since I don't have a Windows environment.

**Note**: `numpy` is mainly used to compute pseudo inverse matrix, instead of its optimization functions.

## Files

* `algorithms.py`: Perform optimizations
* `arm.py`: Define an `Arm` class in object-oriented design
* `gui.py`: Build up the GUI
* `demo_video.mp4`: Demo video
* `README`: Markdown / PDF `README` file

### Run the Program
```
python3.11 gui.py
// Or python gui.py
```

A GUI window should appear after you run the command above, as shown in the demo video. The required info table containing coordinates and angles is printed to `stdout`.

## Algorithm

Assume $B, C, D$ are represented in spherical coordinates, and the angles are $\alpha, \beta, \gamma$ respectively. Then they can be converted to Cartesian coordinates as follows:

* B: $(150\cos\alpha, 150\sin\alpha)$
* C: $(150\cos\alpha + 100\cos\beta, 150\sin\alpha + 100\sin\beta)$
* D: $(150\cos\alpha + 100\cos\beta + 50\cos\gamma, 150\sin\alpha + 100\sin\beta + 50\cos\gamma)$

Given the target coordinates $(x, y)$ of point D, we have

* $x = 150\cos\alpha + 100\cos\beta + 50\cos\gamma$
* $y = 150\sin\alpha + 100\sin\beta + 50\sin\gamma$
* Goal: Minimize $\max(\Delta\alpha, \Delta\beta, \Delta\gamma)$

Define a multivariate function

$F = (150\cos\alpha + 100\cos\beta + 50\cos\gamma, 150\sin\alpha + 100\sin\beta + 50\sin\gamma)$

Then the derivatives are

$\nabla F_x = -150\sin\alpha -100\sin\beta-50\sin\gamma $

$\nabla F_y = 150\cos\alpha + 100\cos\beta + 50\cos\gamma $

According to Newton's method, we can get the root by iterating using the formula below:

$(\alpha_{n+1}, \beta_{n+1}, \gamma_{n+1}) = (\alpha_{n}, \beta_{n}, \gamma_{n}) - [\nabla F(\alpha_{n}, \beta_{n}, \gamma_{n})]^{-1}F(\alpha_{n}, \beta_{n}, \gamma_{n})$

Note $[\nabla F(x_n)]^{-1}$ means pseudo inverse if there's no inverse. It is possible to compute pseudo inverse matrix by hand without `numpy`, but the resulting expression is too long and cumbersome. Thus I use [`numpy.linalg.pinv`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html) (click for details) to calculate it.

20 iterations in general produce a stable solution. However, I didn't prove it to be a optimally minimized solution to the optimization problem. From the perspective of intuition, the algorithm should produce a solution close to optimal with acceptably minimized variable deltas. As a result, the movements of arms are working reasonably fine, as shown in the demo video.
