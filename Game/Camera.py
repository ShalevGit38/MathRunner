from random import randint

# camera follow the player and set the position for everything else using the get method
class Camera:
    SPEED = 0.5

    def __init__(self):
        self.x = 0
        self.y = 0
        self.follow_y = True
        self.follow_x = True
        self.followEverywhere = False
        self.camShakeTime = 0

    # update the position of the camera to follow the x, y
    def update(self, x, y, DeltaTime):
        if self.follow_x or self.followEverywhere:
            self.x += ((x - self.x) / self.SPEED)*DeltaTime
        if self.follow_y or self.followEverywhere:
            self.y += ((y - self.y) / self.SPEED)*DeltaTime
        if self.camShakeTime > 0:
            self.x += randint(-2, 2)
            self.y += randint(-2, 2)
            self.camShakeTime -= 1

    # returns the position odf the object relative to the camera position
    def get(self, x, y, WIDTH, HEIGHT):
        xPos = WIDTH/2 + (x - self.x) - 100
        yPos = HEIGHT/2 + (y - self.y)
        return xPos, yPos