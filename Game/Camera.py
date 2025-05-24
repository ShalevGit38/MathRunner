

# camera follow the player and set the position for everything else using the get method
class Camera:
    SPEED = 0.5

    def __init__(self):
        self.x = 0
        self.y = 0
        self.follow_y = True
        self.camShakeTime = 0

    # update the position of the camera to follow the x, y
    def update(self, x, y, DeltaTime):
        self.x += ((x - self.x) / self.SPEED)*DeltaTime
        if self.follow_y:
            self.y += ((y - self.y) / self.SPEED)*DeltaTime
        if self.camShakeTime > 0 and False:
            self.x += random.randint(-5, 5)
            self.y += random.randint(-10, 10)
            self.camShakeTime -= 1

    # returns the position odf the object relative to the camera position
    def get(self, x, y, WIDTH, HEIGHT):
        xPos = WIDTH/2 + (x - self.x) - 100
        yPos = HEIGHT/2 + (y - self.y)
        return xPos, yPos