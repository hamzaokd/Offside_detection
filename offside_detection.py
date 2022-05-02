from turtle import width
from calibration import *
# remove false postives(peoples outside the field detected as players)
# print("shape U_w ",np.shape(U_w))
i=0
while i < np.shape(U_w)[1]:
    # print("current " ,i)
    if U_w[2][i]<-1:
        # print("delete this " ,i)
        U_w=np.delete(U_w,i,1)
    i+=1
# print("shape U_w ",np.shape(U_w))
U_sim=get_positions(M,U_w)
# print("==>> U_sim.shape:\n", U_sim.shape)

show_players(U_sim)
def get_lastPlayer(U_w):
    m=np.min(U_w[2])
    Mx=np.max(U_w[0]+20)
    mx=np.min(U_w[0]-20)
    
    U_min=np.array([[mx,Mx],[0,0],[m,m],[1,1]])
    return U_min
U_simMin=np.dot(M,get_lastPlayer(U_w))
U_simMin = U_simMin/U_simMin[2,:]
x,y=[U_simMin[0,0] , U_simMin[0,1]],[U_simMin[1,0] , U_simMin[1,1]]
print(U_simMin)

img=mpimg.imread('media/goal.jpg')
shape=img.shape
print(shape)
plt.xlim(0,shape[1]), plt.ylim(shape[0],0)
plt.imshow(img)
plt.plot(x,y,color="red",linewidth=3)
plt.show()
    


