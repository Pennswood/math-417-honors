import tkinter
from settings import FRAME_SIZE, A, B, ZOOM_FACTOR, BALL_SIZE
import math



class SkierAnnimation():
    def __init__(self, backgroundHillFunction):
        self.w = tkinter.Tk()

        # create canvas
        self.myCanvas = tkinter.Canvas(self.w, bg="white", height=FRAME_SIZE, width=FRAME_SIZE)
        self.ground = []
        for i in range(FRAME_SIZE+1):
            self.ground.append(self.myCanvas.create_rectangle(i, FRAME_SIZE, i, FRAME_SIZE/2, fill="brown"))
        self.skier_center = self.myCanvas.create_oval(FRAME_SIZE/2 - BALL_SIZE,FRAME_SIZE/2 - BALL_SIZE, FRAME_SIZE/2 + BALL_SIZE, FRAME_SIZE/2 + BALL_SIZE,  fill="red")
        self.skier_feet = self.myCanvas.create_oval(FRAME_SIZE/2 - BALL_SIZE,FRAME_SIZE/2 - BALL_SIZE, FRAME_SIZE/2 + BALL_SIZE, FRAME_SIZE/2 + BALL_SIZE)
        self.backgroundHillFunction = backgroundHillFunction
        
        self.myCanvas.pack()

        self.updateBackground(0)
    
    def updateBackground(self, curX):
        floorHeight = []
        for i in range(len(self.ground)):
            floorHeight.append(-self.backgroundHillFunction(curX+ (i - FRAME_SIZE/2)/ZOOM_FACTOR)*ZOOM_FACTOR)
            #if i == math.floor(len(self.ground)/2):
                # print(str((curX)))
        offset = (floorHeight[math.floor(len(self.ground)/2)] - round(FRAME_SIZE/2)) 
        for i in range(len(self.ground)):
            
            self.myCanvas.coords(self.ground[i], i, FRAME_SIZE, i, floorHeight[i] - offset)
        self.w.update()
    
    def updateBall(self, height, slope):
        angle = math.atan(slope) + math.pi
        transX = height*math.sin(angle)*ZOOM_FACTOR
        transY = height*math.cos(angle)*ZOOM_FACTOR
        self.myCanvas.coords(self.skier_center, FRAME_SIZE/2 - BALL_SIZE + transX, FRAME_SIZE/2 - BALL_SIZE + transY, FRAME_SIZE/2 + BALL_SIZE + transX, FRAME_SIZE/2 + BALL_SIZE + transY)
        self.skier_feet = self.myCanvas.create_oval(FRAME_SIZE/2 - BALL_SIZE,FRAME_SIZE/2 - BALL_SIZE, FRAME_SIZE/2 + BALL_SIZE, FRAME_SIZE/2 + BALL_SIZE)
        self.w.update()
        

# For testing purposes
if __name__ == "__main__":
    def sampleFunction(x):
        return A*math.sin(x) - B*x

    annimate = SkierAnnimation(sampleFunction)

