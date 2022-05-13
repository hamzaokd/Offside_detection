[Detection of offsides in football]({{url_for('index')}})
=========================================================


*Personal project still in developemnt, still working on pages layout and functionalities.*

Here is an example of an input image:


<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/football.jpg" alt="football match" height="300px"/> 


For the moment, after the detection we get this:

Detected players             |  Positions on the field
:-------------------------:|:-------------------------:
<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/user_image_detected.jpg" alt="Detected players" height="300px"/> | <img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/field_with_players.jpg" alt="Detected players" height="300px"/> 

How to use
----------

1. Download the repository
2. Download the weight file, this is essential for the program to work [link here](https://pjreddie.com/media/files/yolov3.weights). It's from the famous [YOLO project](https://pjreddie.com/darknet/yolo/).
3. Run the command file `run.cmd` and open the browser.
4. Further instructions on the web page when launching the program

Goal
----

My idea is to work on a still image of a TV broadcast of a football match following these steps:

* calibrate the camera to the field to get 3d world coordinate
* get position of the players
* identify the players of different teams
* check if a player is on an offside position

I will discuss each step separately

Type of photos I will be working on
-----------------------------------

~~For now, I will be working on a single frame, possibly [this](https://github.com/hamzaokd/Offside_detection/blob/main/media/goal.jpg). I choose this picture because i already know the dimensions of the field, so the work will be easier~~

~~I'm planing to make my program work on pictures but the problem is I will have to calibrate the camera each time, given that I know the field dimensions.~~

The user can now input any picture he wants.

Calibration of the camera
-------------------------

On a single frame, this step is quite easy, I'll be using some OpenCV functions to detect the corners and goal, to get the intrinsic coordinates of the camera. This will allow me to get the positions of a player in the real world from the position of it's corresponding pixel.

Get position of the player
--------------------------

Usually, players have at least one foot on the ground, So, their positions on the field is the postion of the feet. There are 2 ways to get the position of a player:

1. Manually click the feets of all the players (manual, not intersting)
2. Automatically getting the feet positions(what I wanted to achieve but a bit tricky)

Identification of the players teams
-----------------------------------

This is the hardest step. I was thinking about some sort of clustering, then classification. But What if the user had the possibility to pick the color of each team jersey and we then get some algorithm to get the players. Or maybe just enter it manually. I'm not sure about the latter one. I can also look for some sort of deep learning model to get this step right.but it's gonna be the hardest way.

Ball position
-------------

The position of the ball is very important, because offside rules depends a lot on it (if it was the last after every attacker)

Check for offside
-----------------

After all these steps, this gonna be the easiest one, we will just compare the 'minimum'; x coordinate of each team. For now, I will not study the edges cases, like goalkeeper before last defender, or ball in other center of half of the field.

To learn more about the offside rules, you can check [this](https://en.wikipedia.org/wiki/Offside_(association_football)).

Contact
-------
I would really like to hear from you, if you have any questions or suggestions.

[mail](mailto:hamzaokd1@gmail.com)
