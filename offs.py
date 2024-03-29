"""
author:Hamza Oukaddi

"""
import numpy as np
import cv2
import csv
import matplotlib.pyplot as plt
from PIL import Image
from copy import deepcopy 
import matplotlib
matplotlib.use('agg')



# coord=np.array([[200,110],[200,210],[300,210],[300,110]],[[81,100],[459,80],[450,361],[24,341]],dtype=np.int32)
def get_offsides(coord,coord_data,input):
    """read the input coordinates, tranform them and return the positions of the players in a map field.
    keep only players and draw offside lines on both sides

    Args:
        coord (2d array): inout coordinates
    """
    # print("coord1",coord)
    def coordinate_ajust(cc):
        """transform the coordinates to the right format
        when the user enters the coordinates, they will need to be normalised

        Args:
            c (2d array): inpout coordinates

        Returns:
            2d array: normalised coordinates
        """
        # print("coord2",coord)
        c = deepcopy(cc)
        field,user=c
        # field 
        img_field=Image.open("static/images/field.jpg")
        width_field,height_field=img_field.size
        height_field_html=400
        width_field_html=400*width_field/height_field
        # print("coord3",coord)
        for i in range(4):
            field[i,1]=field[i,1]*height_field/height_field_html
            field[i,0]=field[i,0]*width_field/width_field_html

        # user input
        img_user=Image.open(input)
        width_user,height_user=img_user.size
        height_user_html=400
        width_user_html=400*width_user/height_user
        for i in range(4):
            user[i,1]=user[i,1]*height_user/height_user_html
            user[i,0]=user[i,0]*width_user/width_user_html
            
        return field,user




    def quad_coordinate(co):
        """returns dictionary of coordinates for the field and map

        Args:
            c (2d array): input coordinates

        Returns:
            dict: map and field coordinates
        """
        c=coordinate_ajust(co)
        quad_coords ={
            "lonlat":np.array(c[0],dtype=np.float32),
            "pixel": np.array(c[1],dtype=np.float32)
        }
        
        return quad_coords

    class PixelMapper(object):
        """
        Create an object for converting pixels to geographic coordinates,
        using four points with known locations which form a quadrilteral in both planes
        Parameters
        ----------
        pixel_array : (4,2) shape numpy array
            The (x,y) pixel coordinates corresponding to the top left, top right, bottom right, bottom left
            pixels of the known region
        lonlat_array : (4,2) shape numpy array
            The (lon, lat) coordinates corresponding to the top left, top right, bottom right, bottom left
            pixels of the known region
        """
        def __init__(self, pixel_array, lonlat_array):
            assert pixel_array.shape==(4,2), "Need (4,2) input array"
            assert lonlat_array.shape==(4,2), "Need (4,2) input array"
            self.M = cv2.getPerspectiveTransform(np.float32(pixel_array),np.float32(lonlat_array))
            self.invM = cv2.getPerspectiveTransform(np.float32(lonlat_array),np.float32(pixel_array))
            
        def pixel_to_lonlat(self, pixel):
            """
            Convert a set of pixel coordinates to lon-lat coordinates
            Parameters
            ----------
            pixel : (N,2) numpy array or (x,y) tuple
                The (x,y) pixel coordinates to be converted
            Returns
            -------
            (N,2) numpy array
                The corresponding (lon, lat) coordinates
            """
            if type(pixel) != np.ndarray:
                pixel = np.array(pixel).reshape(1,2)
            assert pixel.shape[1]==2, "Need (N,2) input array" 
            pixel = np.concatenate([pixel, np.ones((pixel.shape[0],1))], axis=1)
            lonlat = np.dot(self.M,pixel.T)
            
            return (lonlat[:2,:]/lonlat[2,:]).T
        
        def lonlat_to_pixel(self, lonlat):
            """
            Convert a set of lon-lat coordinates to pixel coordinates
            Parameters
            ----------
            lonlat : (N,2) numpy array or (x,y) tuple
                The (lon,lat) coordinates to be converted
            Returns
            -------
            (N,2) numpy array
                The corresponding (x, y) pixel coordinates
            """
            if type(lonlat) != np.ndarray:
                lonlat = np.array(lonlat).reshape(1,2)
            assert lonlat.shape[1]==2, "Need (N,2) input array" 
            lonlat = np.concatenate([lonlat, np.ones((lonlat.shape[0],1))], axis=1)
            pixel = np.dot(self.invM,lonlat.T)
            
            return (pixel[:2,:]/pixel[2,:]).T

        def warpImage(self, image):
            """
            Warp an image using the pixel to lon-lat mapping
            Parameters
            ----------
            image : numpy array
                The image to be warped
            Returns
            -------
            numpy array
                The warped image
            """
            return cv2.warpPerspective(image, self.M, (image.shape[1],image.shape[0]))

    def quad_mapper(c):
        """Transforms the coordinates to the right format and returns the mapper object

        Args:
            c (2d array): input coordinates

        Returns:
            PixelMapper: pixelMapper object which transform cooridinates
        """
        quad_coords=quad_coordinate(c)
        pm = PixelMapper(quad_coords["pixel"], quad_coords["lonlat"])
        return pm



    def get_player_position(pos,c):
        """return the lonlat of the player position

        Args:
            pos (list): list of pixel cooridnates of the players
            c (list): list of selected 4 coordinates to map the field

        Returns:
            _type_: list of lonlat coordinates
        """
        u_im=[]
        pm=quad_mapper(c)
        for i in range(len(pos)):
            res=pm.pixel_to_lonlat([pos[i]])
            u=res[0]
            u_im.append(u)
            
        u_im=np.array(u_im)
        return u_im


    data=[]
    # with open("GFG.csv") as csvfile:
    #     reader = csv.reader(csvfile)
    #     for row in reader:
            
    #         x = int(row[0])
    #         y = int(row[1])
    #         data.append([x,y])
    u_imm=np.array(data)
    
    
    u_imm = np.array(coord_data)
    u_im=get_player_position(u_imm,coord)

    def get_last_player(u_im):
        """return the last player position

        Args:
            u_im (array): list of players

        Returns:
            array: cooridnates of the last player
        """
        m=np.min(u_im[:,0])
        M=np.max(u_im[:,0])
        return m,M
    boundary=[[70,70],[1550,70],[1550,908],[70,908]]
    
    
    def delete_non_players(u,boundary):
        """delete people not players, who generally are standing next to field(sideline refs,ball kids ..)

        Args:
            u (2d array): list of people detected
            boundary (2d array): coordinates of corners of the field

        Returns:
            2d array: array of only players
        """
        index=[]
        for i in range(len(u)):
            if (u[i][0]<boundary[0][0] or u[i][0]>boundary[2][0]) :
                index.append(i)
            elif (u[i][1]<boundary[0][1] or u[i][1]>boundary[3][1]):
                index.append(i)
        u=np.delete(u,index,axis=0)
        return u

    u_im=delete_non_players(u_im,boundary)
    
    def get_offside_line_irl(m,M):
        """return the offside line irl

        Args:
            m (float): min x coordinate of the last player
            M (float): max x coordinate of the last player

        Returns:
            float: offside line
        """
        pm=quad_mapper(coord)
        lower_left = pm.lonlat_to_pixel((m,908))
        upper_left = pm.lonlat_to_pixel((m,70))
        lower_right = pm.lonlat_to_pixel((M,908))
        upper_right = pm.lonlat_to_pixel((M,70))
        
        return lower_left,upper_left,lower_right,upper_right
       
       
    minPlayer,maxPlayer=get_last_player(u_im)
    # Save figure of players position in a map
    fig = plt.figure()
    im=plt.imread("static/images/field.jpg")
    plt.imshow(im)
    plt.scatter(u_im[:,0],u_im[:,1])
    plt.axis('off')
    plt.vlines(minPlayer,ymin=0,ymax=980,color='red',linewidth=3)
    plt.vlines(maxPlayer,ymin=0,ymax=980,color='red',linewidth=3)
    output = input.replace('.', '_top_map.')
    plt.savefig(output,bbox_inches='tight',pad_inches=0,transparent=True)

    # draw in user image
    inputCV2 = cv2.imread(input)
    offside_lines = get_offside_line_irl(minPlayer,maxPlayer)
    # print(offside_lines)
    cv2.line(inputCV2,(int(offside_lines[0][0][0]),int(offside_lines[0][0][1])),(int(offside_lines[1][0][0]),int(offside_lines[1][0][1])),(0,0,255),3)
    cv2.line(inputCV2,(int(offside_lines[2][0][0]),int(offside_lines[2][0][1])),(int(offside_lines[3][0][0]),int(offside_lines[3][0][1])),(0,0,255),3)
    
    pm = quad_mapper(coord)
    distortion = pm.warpImage(inputCV2)
    # draw hough lines
    # distortion = inputCV2
    # gray = cv2.cvtColor(distortion, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    # for line in lines:
    #     rho, theta = line[0]
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 * (a))
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * (a))
    #     cv2.line(distortion, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    cv2.imwrite("static/images/distortion.jpg",distortion)
    outputCV2 = input.replace('.', '_lines.')
    cv2.imwrite(outputCV2, inputCV2)
    