from graphics import SkierAnnimation
from settings import FRAME_SIZE, A, B, ZOOM_FACTOR, NUMERICAL_DERIVATIVE_STEP_SIZE, G, PERSON_HEIGHT, TARGET_VELOCITY
import time
import math



def constant_speed():
    curX = 0
    animator = SkierAnnimation(sampleFunction)
    while True:
        animator.updateBackground(curX,)
        time.sleep(.001)
        curX = curX + 5

class SkierPhysicsSim:
    def __init__(self, animator, backgroundHillFunction, d_backgroundHillFunction = None, d2_backgroundHillFunction = None, h = None, startX = 0, startV = 0):
        self.backgroundHillFunction = backgroundHillFunction
        self.d_backgroundHillFunction = d_backgroundHillFunction
        self.d2_backgroundHillFunction = d2_backgroundHillFunction
        self.x = startX
        self.s = 0
        for i in range(self.x):
            self.s = self.s + self.ds_of_dx(i, i+1)
        self.v = startV
        self.animator = animator
        if h is None:
            self.h = self.balance
        else:
            self.h = h

    def default_h_of_s(self, s):
        return 0

    #SEEENNND ITTTT!!! Idea: Accelerating == get as far from center as possible. Decellerating: get as close to center as possible
    def send_it(self,s):

        if (self.R(self.x)< 0 and ((self.v < 0 and self.d_func(self.x) >0) or (self.v > 0 and self.d_func(self.x) < 0))): #Curvature negative accelerating
            return PERSON_HEIGHT
        elif self.R(self.x) > 0 and ((self.v < 0 and self.d_func(self.x) < 0) or (self.v > 0 and self.d_func(self.x) > 0)): #Curvature positive decelerating
            return PERSON_HEIGHT
        elif self.R(self.x) < 0 and ((self.v < 0 and self.d_func(self.x) < 0) or (self.v > 0 and self.d_func(self.x) > 0)): #Curvature negative decelerating
            return 0
        else: #Curvature positive accelerating
            return 0
    
    # Bang bang controller.
    def balance(self, s):
        val = self.send_it(s)
        if abs(self.v) > TARGET_VELOCITY:
            #print("Stopping")
            return PERSON_HEIGHT if val == 0 else 0
        else:
            return val

    def d_func(self, x):
        if not self.d_backgroundHillFunction is None:
            dfdx = self.d_backgroundHillFunction(x)
        else: # Derive numerically
            dfdx = (self.backgroundHillFunction(x+NUMERICAL_DERIVATIVE_STEP_SIZE) - self.backgroundHillFunction(x- NUMERICAL_DERIVATIVE_STEP_SIZE))/ \
                (2*NUMERICAL_DERIVATIVE_STEP_SIZE)
        return dfdx
    
    def df_angle(self, x):
        return -math.atan(self.d_func(x))

    def d2_func(self, x):
        if not self.d2_backgroundHillFunction is None:
            d2fdx2 = self.d2_backgroundHillFunction(x)
        else:
            d2fdx2 = (self.d_func(x+NUMERICAL_DERIVATIVE_STEP_SIZE) - self.d_func(x- NUMERICAL_DERIVATIVE_STEP_SIZE))/ \
                (2*NUMERICAL_DERIVATIVE_STEP_SIZE)

        return d2fdx2
    
    # Radius of curavture with respect of x (not s)
    def R(self, x):
        # Solve numerically:
        dfdx = self.d_func(x)
        df2dx = self.d2_func(x)
        if abs(self.d2_func(x)) < 1e-8:
            return float('inf')
        return pow((1+pow(dfdx,2)), 1.5)/self.d2_func(x)
    
    def ds_of_dx(self, oldX, newX):
        return (newX - oldX)/math.cos(self.df_angle(oldX))
    
    def dx_of_ds(self, oldS, newS, x):
        return (newS - oldS)* math.cos(self.df_angle(x))



    def simulate(self):
        while True:
            
            time.sleep(.03)
            self.v = self.v + G*math.sin(self.df_angle(self.x))
            print(str(self.v)+"    "+ str(self.R(self.x)))
            if abs(self.R(self.x)) < self.h(self.x):
                print("Faceplant!")
                return
            if (self.R(self.x)) == float('inf'):
                deltaX = self.v
                self.s = self.s + self.v
            else:
                self.newS = self.s + (self.R(self.x)/(self.R(self.x) - self.h(self.x)))*self.ds_of_dx(self.x, self.v+self.x)
                deltaX = self.dx_of_ds(self.s, self.newS, self.x)
                #deltaX = (self.R(self.x)/(self.R(self.x) - self.h(self.x)))*self.v
                
                self.s = self.newS

            self.x = self.x + deltaX
            self.animator.updateBackground(self.x,)
            self.animator.updateBall(self.h(self.x), self.d_func(self.x))
        

def sampleFunction(x):
        return A*math.sin(x) - B*x
def d_sampleFunction(x):
    return A*math.cos(x) - B
def d2_sampleFunction(x):
    return -A*math.sin(x)

# For testing purposes
if __name__ == "__main__":
    animator = SkierAnnimation(sampleFunction)
    sim = SkierPhysicsSim(animator, sampleFunction, d_sampleFunction, d2_sampleFunction, startX = 4)
    sim.simulate()
    