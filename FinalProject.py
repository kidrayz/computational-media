# battle box
BOX_X = 200
BOX_Y = 150
BOX_W = 200
BOX_H = 180
SPEED = 3
keys = set() # skill 5
hit_timer = 0
# skill 10
class Player:
    def __init__(self):
        self.x = BOX_X + BOX_W / 2
        self.y = BOX_Y + BOX_H / 2
        self.size = 10
        self.hp = 100
    def move(self):
        if UP in keys:
            self.y -= SPEED
        if DOWN in keys:
            self.y += SPEED
        if LEFT in keys:
            self.x -= SPEED
        if RIGHT in keys:
            self.x += SPEED
        m = self.size
        self.x = constrain(self.x, BOX_X + m, BOX_X + BOX_W - m) # skill 9
        self.y = constrain(self.y, BOX_Y + m, BOX_Y + BOX_H - m)
    def show(self):
        s = self.size
        color_mode(RGB, 255) # skill 3
        fill(255, 0, 0) # skill 2
        no_stroke()
        ellipse(self.x - s * 0.5, self.y - s * 0.25, s, s) # skill 1
        ellipse(self.x + s * 0.5, self.y - s * 0.25, s, s)
        triangle(self.x - s, self.y + s * 0.25, self.x + s, self.y + s * 0.25, self.x, self.y + s)
    def hits(self, bone):
        return (self.x < bone.x + bone.w and self.x + self.size > bone.x and
                self.y < bone.y + bone.h and self.y + self.size > bone.y)
# skill 10
class Bone:
    def __init__(self, y, spd):
        self.x = float(BOX_X - 20)
        self.y = y
        self.w = 60
        self.h = 10
        self.spd = spd
        self.hue = random(360)
    def move(self):
        self.x += self.spd # skill 9
        self.hue = (self.hue + 1) % 360
    def offscreen(self):
        return self.x > BOX_X + BOX_W + 20
    def show(self):
        color_mode(HSB, 360, 100, 100) # skill 3
        stroke(self.hue, 60, 100) # skill 2
        stroke_weight(2)
        fill(self.hue, 40, 100)
        rect(self.x, self.y, self.w, self.h) # skill 1
# skill 10
class GasterBlaster:
    def __init__(self):
        self.x = BOX_X + BOX_W / 2
        self.y = BOX_Y - 60
        self.angle = 0
        self.size = 40
    def update(self, px, py):
        self.angle = atan2(py - self.y, px - self.x)
    def show(self):
        push_matrix() # skill 11
        translate(self.x, self.y)
        rotate(self.angle)
        color_mode(RGB, 255) # skill 3
        fill(255) # skill 2
        stroke(200)
        stroke_weight(1)
        ellipse(0, 0, self.size, self.size * 0.6) # skill 1
        triangle(-self.size * 0.3, self.size * 0.3, self.size * 0.3, self.size * 0.3, 0, self.size * 0.7)
        pop_matrix() # skill 11
sans_img = None
player = None
bones = []
blaster = None
timer = 0
hit_timer = 0
def setup():
    global player, sans_img, blaster
    size(600, 480)
    frame_rate(60)
    window_title("undertale - battle")
    sans_img = load_image("sans.png") # skill 8
    player = Player() # skill 10
    blaster = GasterBlaster() # skill 10
def draw():
    global timer, bones, hit_timer
    background(0)
    color_mode(RGB, 255)
    if sans_img:
        image(sans_img, 50, 150, 100, 100) # skill 8
    no_stroke() # skill 2
    fill(0)
    rect(BOX_X, BOX_Y, BOX_W, BOX_H) # skill 1
    timer += 1
    if timer >= 60:
        timer = 0
        bones.append(Bone(random(BOX_Y + 10, BOX_Y + BOX_H - 20), random(2, 5))) # skill 10
    for bone in bones[:]: # skill 9, skill 10
        bone.move()
        bone.show()
        if player.hits(bone):
            hit_timer = 10
            bones.remove(bone)
        elif bone.offscreen():
            bones.remove(bone)
    blaster.update(player.x, player.y)
    blaster.show()
    player.move()
    player.show()
    if hit_timer > 0: # skill 12
        load_np_pixels()
        np_pixels[:, :, 2] = np_pixels[:, :, 2] // 4
        np_pixels[:, :, 3] = np_pixels[:, :, 3] // 4
        update_np_pixels()
        hit_timer -= 1
    stroke(255) # skill 2
    stroke_weight(3)
    no_fill()
    rect(BOX_X, BOX_Y, BOX_W, BOX_H) # skill 1
def key_pressed(): # skill 5
    keys.add(key_code)
def key_released(): # skill 5
    keys.discard(key_code)