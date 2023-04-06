"""
identify players in the image .
author:Hamza Oukaddi
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
from PIL import Image
import matplotlib
matplotlib.use('agg')




def get_field_positions(im,input):
    # Open image
    image_path=input
    img = plt.imread(image_path)
    """Identify peoples (players and people standing by) in the image
    and write their positions to a csv file. 
    Also, save the image with the identified people highlighted.
    

    Args:
        im (path): path to the image
    
    """
    img = plt.imread(im)
    classes = None 
    
    # read coco class names
    with open('coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # size of image
    Width = img.shape[1]
    Height = img.shape[0]

    # read pre-trained model and config file
    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

    # create input blob 
    # set input blob for the network
    net.setInput(cv2.dnn.blobFromImage(img, 0.00392, (416,416), (0,0,0), True, crop=False))

    # run inference through the network
    # and gather predictions from output layers

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    #create bounding box 
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
                
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
    
    #check if is people detection
    player_number=0
    u_im=[] # player postion
    boxes_player=[]
    if indices == []:
        return None
    for i in indices:
        box = boxes[i]
        if class_ids[i]==0:
            boxes_player.append(box)

            label = str(f"player{player_number}") 
            player_number +=1
            cv2.rectangle(img, (round(box[0]),round(box[1])), (round(box[0]+box[2]),round(box[1]+box[3])), (0, 0, 0), 2)
            cv2.putText(img, label, (round(box[0])-10,round(box[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            bottom_right_corner=[round(box[0]+box[2]),round(box[1]+box[3])]
            u_im.append(bottom_right_corner)
            
    # save image with identified people highlighted
    fig = plt.figure(figsize=(20,10))
    ax1 = fig.add_subplot(1,1,1)
    # remove axis
    ax1.axis('off')
    ax1.imshow(img)
    output = input.replace('.', '_detected.')
    plt.savefig(output, bbox_inches='tight', pad_inches=0,transparent=True)

    # plt.title("detection")
    
    # save coordinte of players
    return u_im
    with open(input+'.csv', 'w',newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(u_im)
# get_field_positions(image_path)