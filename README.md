Detection of offsides in football
=========================================================


*Personal project still in developemnt, still working on pages layout and functionalities.*

*Languages and libraries used: -Python -OpenCV -scikit-learn -Flask -HTML,CSS and JavaScript.*

-----------------------------

**This little project will detect offsides in an image input by the user**

Here is an example of an input image:


<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/football.jpg" alt="football match" height="300px"/> 


For the moment, after the detection we get the detected players on the image:

Detected players             |  Positions on the field
:-------------------------:|:-------------------------:
<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/user_image_detected.jpg" alt="Detected players" height="300px"/> | <img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/field_with_players.jpg" alt="Detected players" height="300px"/> 


After removing players that are not on the field (managers, referees, etc...), we get this bird eye view of the field with the players positions, and the lines that represent the offside lines in both sides

How to use
----------

1. Download the repository
2. Download the weight file, this is essential for the program to work [link here](https://pjreddie.com/media/files/yolov3.weights). It's from the famous [YOLO project](https://pjreddie.com/darknet/yolo/).
3. Run the Flask app server
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

The input images should be a single frame from a footbal game broadcast (Like this). The bigger the field of view the more accurate the detection will be.

One of the features that can be added is possibility of using a video, as such that the offside lines will be drawn in real time

Calibration of the camera
-------------------------

On a single frame, this step is quite easy, the user will need to click on 4 points on the field in the input image, and then click on the corresponding points in a field map. The program will then calculate the homography matrix, which will be used to get the 3d world coordinates of the players.

Get position of the player
--------------------------

Usually, players have at least one foot on the ground, So, their positions on the field is the postion of the feet. There are 2 ways to get the position of a player:

1. Manually click the feets of all the players (manual, not intersting)
2. Automatically getting the feet positions(what I wanted to achieve but a bit tricky)

After using OpenCV functions, and a trained machine learning model, I've got the positions of the players.

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
