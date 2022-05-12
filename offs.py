from matplotlib import docstring
from matplotlib.image import imsave
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv


# coord=np.array([[200,110],[200,210],[300,210],[300,110]],[[81,100],[459,80],[450,361],[24,341]],dtype=np.int32)
def get_offsides(coord):
    def coordinate_ajust(coord):
        field,user=coord
        # field 
        img_field=Image.open("flask_app/static/images/field.jpg")
        width_field,height_field=img_field.size
        height_field_html=400
        width_field_html=400*width_field/height_field
        for i in range(4):
            field[i,1]=field[i,1]*height_field/height_field_html
            field[i,0]=field[i,0]*width_field/width_field_html

        # user input
        img_user=Image.open("flask_app/static/user_input/user_image.jpg")
        width_user,height_user=img_user.size
        height_user_html=400
        width_user_html=400*width_user/height_user
        for i in range(4):
            user[i,1]=user[i,1]*height_user/height_user_html
            user[i,0]=user[i,0]*width_user/width_user_html
            
        return field,user




    def quad_coordinate(coord):
        c=coordinate_ajust(coord)
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


    def quad_mapper(coord):
        quad_coords=quad_coordinate(coord)
        pm = PixelMapper(quad_coords["pixel"], quad_coords["lonlat"])
        return pm



    def get_player_position(pos,coord):
        """return the lonlat of the player position

        Args:
            pos (list): list of pixel cooridnates of the players
            coord (list): list of selected 4 coordinates to map the field

        Returns:
            _type_: list of lonlat coordinates
        """
        u_im=[]
        pm=quad_mapper(coord)
        for i in range(len(pos)):
            res=pm.pixel_to_lonlat([pos[i]])
            u=res[0]
            u_im.append(u)
            
        u_im=np.array(u_im)
        return u_im


    data=[]
    with open("GFG.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            
            x = int(row[0])
            y = int(row[1])
            data.append([x,y])
    u_imm=np.array(data)
    u_im=get_player_position(u_imm,coord)

    def get_last_player(u_im):
        m=np.min(u_im[:,0])
        M=np.max(u_im[:,0])
        return m,M
    boundary=[[70,70],[1550,70],[1550,908],[70,908]]
    def delete_non_players(u,boundary):
        index=[]
        for i in range(len(u)):
            if (u[i][0]<boundary[0][0] or u[i][0]>boundary[2][0]) :
                index.append(i)
            elif (u[i][1]<boundary[0][1] or u[i][1]>boundary[3][1]):
                index.append(i)
        u=np.delete(u,index,axis=0)
        return u

    u_im=delete_non_players(u_im,boundary)
       
    
    fig = plt.figure()
    im=plt.imread("flask_app/static/images/field.jpg")
    plt.imshow(im)
    plt.scatter(u_im[:,0],u_im[:,1])
    plt.axis('off')
    plt.vlines(get_last_player(u_im)[0],ymin=0,ymax=980,color='red',linewidth=3)
    plt.vlines(get_last_player(u_im)[1],ymin=0,ymax=980,color='red',linewidth=3)
    plt.savefig("flask_app/static/images/field_with_players.jpg",bbox_inches='tight')

