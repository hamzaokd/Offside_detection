# Detection of offsides in football
[current notebook](https://github.com/hamzaokd/Offside_detection/blob/main/yolo_person.ipynb)
## Goal 
My idea is to work on a still image of a TV broadcast of a football match following these steps: 
* calibrate the camera to the field to get 3d world coordinate
* get position of the players
* identify the players of different teams 
* check if a player is on an offside position

I will discuss each step separately

## Type of photos i will be working on
For now, I will be working on a single frame, possibly [this](https://github.com/hamzaokd/Offside_detection/blob/main/media/goal.jpg).\
I choose this picture because i already know the dimensions of the field, so the work will be easier. 


I'm planing to make my program work on pictures but the problem is i will have to calibrate the camera each time, given that i know the field dimensions.

## Calibration of the camera
On a single frame, this step is quite easy, i'll be using some OpenCV functions to detect the corners and goal, to get the intrinsic coordinates of the camera. This will allow me to get the positions of a player in the real world from the position of it's corresponding pixel. 

To make this work for other images, maybe i can ask the user to pick the the center of the reference frame (which usually will be center of the goal line) 

## Get position of the player
Usually, players have at least one foot on the ground, So, their positions on the field is the postion of the feet (but which foot we will choose).
I guess the best way is to pick both feet and then compare their postions.\
there are 2 ways to get the position of a player:
1. Manually click the feets of all the players (manual, not intersting)
2. Automatically getting the feet positions( what i wanted to achieve but a bit tricky)
 ## Identification of the players teams
This is the hardest step. I was thinking about some sort of clustering, but i dont think it will work. What if the user had the possibility to pick the color of each team jersey and we then get some algorithm to get the players. \
Or maybe just enter it manually, but i dont like doing things that way. \
I will look for some sort of deep learning model to get this step right. Will work manually for now. 

## Ball position
The position of the ball is very important, because offside rules depends a lot on it (if it was the last after every attacker)
## Check for offside
After all these steps, this gonna be the easiest way, we will just compare the "minimum" $x$ coordinate of each team. \
I will not study the edges cases, like goalkeeper before last defender, or ball in other center of half of the field. 

