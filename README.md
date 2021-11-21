# Assignment 1 - Research Track 1
---------------------------------
The  main purpose of this project is to constantly drive the [Student Robotics](https://studentrobotics.org/) simulator robot around the arena in the counter-clockwise direction, while avoiding the golden obstacles, as it also grabs and moves behind it the closely detected silver tokens.

## Installating and Running
---------------------------
The simulator requires a Python 2.7 installation, the [pygame library](https://www.pygame.org/news), [PyPyBox2D library](https://pypi.org/project/pypybox2d/2.1-r331/), and [PyYAML Library](https://pypi.org/project/PyYAML/).

Once the dependencies are installed, simply run the test.py script to test out the simulator.\
In order to run one or more scripts in the simulator, use run.py followed by the file names, as the program can be run by the following command line:
```
$ python run.py RT-Assignment1.py
```
## Code Flowchart
-----------------
![Code Flowchart](https://user-images.githubusercontent.com/79665691/142777103-0f692cef-b265-48c6-8288-090400cc5257.jpg)

The above flowchart describes the logic based on which the robot motion algorithm is implemented to achieve the aforementioned tasks.\
First, the robot will drive forward while checking for Silver and Golden tokens while it will obtain their distances and orientation angles upon detecting them. Afterwards, the robot will check the golden distance first, then if it is greater than the obstacle distance threshold specified in the code, which means there is no close golden token, it will check for a silver token within a specified distance and angle range, which if found, it will check for orientation adjustments until meeting the threshold requirements, and when it is too close to it, it will grab it, move it behind it and then continuously drive and repeat the whole checking procedure. Otherwise, if the silver token isn't detected within the specified distance and angle range, the robot will continue its drive. Moreover, if the first condition of the obstacle distance isn't satisfied, then a close obstacle is detected, thus the robot will check if there is any close silver token to grab it in the same way as for the previous case, and if no silver token is detected and if the orientation angle of the obstacle is within a specified range, it will be detected to be in front of the robot thus it will turn with a large angle to avoid it, while if it isn't in the specified orientation range it is detected to be on the side, thus the robot can turn with a small angle to avoid it, and then all the procedure will be repeated continuously.
## Robot API
------------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

## Project Possible Improvements
--------------------------------
As an improvement for such a project, path planning algorithms can be used to make the robot more robust as it can adjust to changes in its environment. Thus, algorithms such Dijkstra and A* can be used, from which,  Dijkstra's algorithm is a grid map based path planning algorithms, it seeks a possible path starting from an initial position and searching in every direction for the goal position as this algorithm can be applied to find the goal prior to any movement. Moreover, A* algorithm also uses a grid map to plan the shortest collision-free path using its path planning algorithm. Additionally, Rapidly-exploring Random Tree algorithm is another path planning option, as it creates a graph to find a path within it, which may be not the optimal path to follow, constituting the main difference between A* and RRT by making RRT faster but not ensuring the shortest path to be followed.
![Algorithms Representation](https://www.researchgate.net/profile/Laurene-Claussmann/publication/333124691/figure/fig4/AS:768017193500674@1560120976254/Illustrations-of-the-processes-of-a-Dijkstra-b-A-and-c-RRT.png)\
Image Source: https://www.researchgate.net/profile/Laurene-Claussmann/publication/333124691/figure/fig4/AS:768017193500674@1560120976254/Illustrations-of-the-processes-of-a-Dijkstra-b-A-and-c-RRT.png
