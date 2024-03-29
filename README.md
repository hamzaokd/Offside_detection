[Detection of offsides in football]({{url_for('index')}})
=========================================================


*Personal project still in development, still working on pages layout and functionalities.*

-----------------------------

**This little project will detect offsides in an image input by the user**

Here is an example of an input image:


<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/football.jpg?raw=True" alt="football match" height="300px"/> 


Currently, after the detection we get the detected players on the image:
           
<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/user_image_detected.jpg?raw=True" alt="Detected players" height="300px"/>  

After removing players that are not on the field (managers, side referees, etc...), we get this bird eye view of the field with the players positions, and the lines that represent the offside positions in both sides:

<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/field_with_players.jpg?raw=True" alt="Detected players" height="300px"/> 

We now can go back to the original image and draw the offside lines:

<img src="https://github.com/hamzaokd/Offside_detection/blob/main/media/rep/placeholder-image_lines.jpg?raw=True" alt="Detected players" height="300px"/>


How to use
----------

1. Clone the repository
2. Download the weight file, this is essential for the program to work [link here](https://pjreddie.com/media/files/yolov3.weights). It's from the famous [YOLO project](https://pjreddie.com/darknet/yolo/). And put it in same directory as the app.py file.
3. Run the flask server using the command `python app.py` (`python3 app.py` on Linux) in the terminal and [go to the web page](localhost:5000)
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

 The input images should be a single frame from a football game broadcast like the one on the top. The bigger the field of view the more accurate the detection will be.

One of the features that can be added is possibility of using a video, as such that the offside lines will be drawn in real time

Calibration of the camera
-------------------------

On a single frame, this step is quite easy, the user will need to click on 4 points on the field in the input image, and then click on the corresponding points in a field map. This is a calibration step, which will be used to get the 3d world coordinates of the players.

Get position of the player
--------------------------

Usually, players have at least one foot on the ground, So, their positions on the field is the position of the feet. There are 2 ways to get the position of a player:

1. Manually click the feet of all the players
2. Automatically getting the feet positions

Identification of the players teams
-----------------------------------

Still not implemented



Ball position
-------------

The position of the ball is very important, as it will be used to check for offside. 
Still not implemented

Check for offside
-----------------

After all these steps, this gonna be the easiest one, we will just compare the  positions of players of each team. For now, I will not study the edges cases, like goalkeeper before last defender, or ball in other center of half of the field.

To learn more about the offside rules, you can check [this](https://en.wikipedia.org/wiki/Offside_(association_football)).

Contact
-------
I would really like to hear from you, if you have any questions or suggestions.

[mail](mailto:hamzaokd1@gmail.com)
