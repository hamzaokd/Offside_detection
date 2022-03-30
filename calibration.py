# package imports
# Warning : the backend below may generate some issues if used
# in a conda environment.
#%matplotlib tk
# Try this backend if %matplotlib tk does not work properly
# In this case do not use the ginput command.
#%matplotlib notebook
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy import linalg
import csv

from string import ascii_uppercase

import warnings

from sklearn.tree import plot_tree

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()


#camera matrix
M=np.array([[-6.18943104e+02,8.54183557e+02,7.87568776e+03,-8.38849792e+04],
 [-1.03230283e+03,8.56338778e+03,-1.29670360e+02,-4.76845108e+04],
 [ 7.55947028e-01,6.54062418e-01,-2.73211383e-02,-5.45165823e+01]])

# We create the origin of the reference frame in homogeneous coordinates.
# Then evaluate the image position of the centre of the ball.
U_w = np.array([[0],[0],[0],[1]])
U_im=np.dot(M,U_w)
U_im = U_im/U_im[2,:]
# print(U_im[:2])
#We have y=0.
# To obtain M', we need to remove the second line of the matrix M which correspond to y
M_prime = M[:,[0,2,3]]
# print(M_prime.shape)
img=mpimg.imread('media/goal.jpg')
def get_player_position(pos):
     
    u_im = np.vstack((np.transpose(pos),np.ones(len(pos))))
    # print(u_im[:2])
    # print(u_im.shape)
    plt.imshow(img)
    plt.scatter(u_im[0,:],u_im[1,:])
    plt.show()

data=[]
with open("GFG.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        
        x = int(row[0])
        y = int(row[1])
        data.append([x,y])
u_im=np.array(data)
get_player_position(u_im)


#To get the real position of the players, we invert $M'$ <br>
#we already know that $M'$ is invertible. So:
M_inv = np.linalg.inv(M_prime)
U_w=np.dot(M_inv,u_im)
print(np.shape(U_w))
#To pass from homogenious coordinates to cartesian coordinates, we divide by the last coordinate. <br>
#We then have to add the coordinate corresponding to y which equals to 0
U_w = U_w/U_w[2,:]
U=U_w[:1]
U=np.vstack((U,np.zeros(11)))
U=np.vstack((U,U_w[1:,]))
U_w=U
print(U_w[:3])

U_sim=np.dot(M,U_w)
U_sim = U_sim/U_sim[2,:]

img=mpimg.imread('goal.jpg')
plt.imshow(img)
plt.scatter(U_sim[0,:],U_sim[1,:])
plt.show()


for i in range(1,12):
    print(f'Position of the player {ascii_uppercase[i-1]} : x = {np.round(U_w[0][i-1],2)} , y = {np.round(U_w[1][i-1],2)} , z = {np.round(U_w[2][i-1],2)}')
