## PyGravity
### A gravity simulator in Python

![Screenshot 2025-08-14 at 8.43.58 PM.png](https://silberberg.digital/static/uploads/4777555811.png)

## What is it
PyGravity is a simple Python application that simulates gravity to **demonstrate the effect of an objects mass on the surrounding space**, "fabric".

## How does it actually work 
PyGravity simulates a massive object deforming space fabric in real time using simple physics and OpenGL. Here’s the breakdown:

1.Space Fabric Grid
-The flat “fabric” is a grid of points in **3D space**.
-**Each point has coordinates (𝑥,𝑦,𝑧)**, initially with 𝑧 = 0 for a flat 3D cartesian plane style.

2.Mass Dip Effect
-The ball represents a mass that dips the fabric downwards
-The dip is calculated using an exponential falloff as points closer to the ball move more, points farther away move less
-Formula used for each grid point:
**`z = −dip_strength ⋅ e^(−distance^2 ⋅ dip_falloff)`**

3.Circular Motion of the Ball
-The ball moves in a circle on the fabric
-As the ball moves, it continuously updates the plane at its current location, creating **dynamic distortion**

4.Camera & Visualization
-A 3D camera allows the user to move and look around using WASD (left/right forward/back movement) + QE (up/down movement) keys and the mouse for perspective
-The fabric is drawn as a grid, and the ball is rendered as a red sphere above the fabric

## Source Code
Source code is 

## End
thanks kavan for this idea, who originally made it in c++, this ones in PY so syntax should be easy to learn and study, thanks !!

