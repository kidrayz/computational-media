# im sansing it
import random
import math
import numpy as np

W, H       = 800, 600
BOX_X      = 230
BOX_Y      = 280
BOX_W      = 340
BOX_H      = 210
SOUL_SPEED = 4
SANS_X     = BOX_X + BOX_W // 2  # centered over box
SANS_Y     = 155                  # wont clip into box

IDLE_FRAMES = [(2,647,60,718),(62,647,116,718),(118,647,176,718)]
TALK_FRAMES = [(178,647,232,718),(234,647,282,718),(284,647,322,718)]

DIALOGUES = [
    "* guess what?.",
    "* chicken butt"
]
TAUNT_LINES = [
    "* uninstall",
    "* im sansing it",
    "* chud",
    "* get good",
]

keys_held = set()  # held keys for diagonal mvmt - skill 5

class Bone:  # skill 10
    def __init__(self, x, y, vx, vy, delay=0):
        self.x      = float(x)
        self.y      = float(y)
        self.vx     = vx
        self.vy     = vy
        self.delay  = delay  # delay before bone activates
        self.active = False
        self.angle  = math.pi / 2 if vx == 0 else 0  # vertical bones need 90 deg - skill 11
        self.w      = 48
        self.h      = 14
    def update(self):
        if self.delay > 0:
            self.delay -= 1
            return
        self.active = True
        self.x += self.vx  # skill 9
        self.y += self.vy  # skill 9
    def is_offscreen(self):
        return (self.x < BOX_X - 60 or self.x > BOX_X + BOX_W + 60 or
                self.y < BOX_Y - 60 or self.y > BOX_Y + BOX_H + 60)
    def draw(self, img):
        if not self.active:
            return
        no_tint()  # stop color leaking - skill 2
        push_matrix()  # skill 11
        translate(self.x, self.y)  # skill 11
        rotate(self.angle)  # rotates vertical bones - skill 11
        image_mode(CENTER)
        image(img, 0, 0, self.w, self.h)  # skill 8
        image_mode(CORNER)
        pop_matrix()  # skill 11
    def hits(self, sx, sy):
        hw = self.h // 2 if self.angle != 0 else self.w // 2  # swap dims when rotated
        hh = self.w // 2 if self.angle != 0 else self.h // 2
        return abs(self.x - sx) < hw + 5 and abs(self.y - sy) < hh + 5

class Blaster:  # skill 10
    # 5 cols 5 rows each frame 44x57px
    # row 0 closed 1-2 opening 3-4 firing
    COL_X  = [2, 48, 95, 140, 186]  # x start per column
    ROW_Y  = [3, 63, 122, 181, 240]  # y start per row
    FW, FH = 44, 57
    def __init__(self, x, y, side):
        self.x      = float(x)
        self.y      = float(y)
        self.side   = side  # which side its on
        self.timer  = 130
        self.anim   = 0  # current row
        self.col    = 0  # current col
        self.anim_t = 0
        self.firing = False
    def update(self):
        self.timer  -= 1  # skill 9
        self.anim_t += 1
        if self.anim_t >= 6:
            self.anim_t = 0
            self.col = (self.col + 1) % 5  # cycle animation cols
        if self.timer < 90: self.anim = 1  # open mouth
        if self.timer < 65: self.anim = 2
        if self.timer < 40:
            self.anim   = 3
            self.firing = True  # beam active
        if self.timer < 18: self.anim = 4
    def draw(self):
        x1     = self.COL_X[self.col]
        y1     = self.ROW_Y[self.anim]
        sprite = gaster_sheet.get_pixels(x1, y1, self.FW, self.FH)  # crop frame - skill 8
        if not self.firing:
            pulse = abs(math.sin(frame_count * 0.15))  # sin for smooth pulse - skill 11
            # HSB: hue=0 (red), sat=88, bri=100, alpha pulse — vivid red warning line
            stroke(0, 88, 100, int(pulse * 86))  # pulsing red warning - skill 2 3
            stroke_weight(2)
            no_fill()
            if self.side == 'left':
                line(self.x, self.y, BOX_X + BOX_W, self.y)  # skill 1
            elif self.side == 'right':
                line(self.x, self.y, BOX_X, self.y)  # skill 1
            else:
                line(self.x, self.y, self.x, BOX_Y + BOX_H)  # skill 1
            no_stroke()
        push_matrix()  # skill 11
        translate(self.x, self.y)  # skill 11
        if self.side == 'left':
            rotate(-math.pi / 2)  # -90 makes it face right - skill 11
        elif self.side == 'right':
            rotate(math.pi / 2)  # +90 cw faces left - skill 11
        # top already faces down
        if self.firing:
            no_stroke()
            if self.side == 'left':
                # HSB: hue=195 (cyan-blue), sat=61, bri=100 — gaster beam outer
                fill(195, 61, 100, 63)  # skill 3
                rect(-8, self.FH, 16, BOX_X + BOX_W - self.x)  # outer beam - skill 1
                fill(0, 0, 100, 86)  # pure white inner beam
                rect(-3, self.FH, 6,  BOX_X + BOX_W - self.x)  # inner beam - skill 1
            elif self.side == 'right':
                # HSB: hue=195 (cyan-blue), sat=61, bri=100 — gaster beam outer
                fill(195, 61, 100, 63)  # skill 3
                rect(-8, self.FH, 16, self.x - BOX_X)  # skill 1
                fill(0, 0, 100, 86)  # pure white inner beam
                rect(-3, self.FH, 6,  self.x - BOX_X)  # skill 1
            else:
                # HSB: hue=195 (cyan-blue), sat=61, bri=100 — gaster beam outer
                fill(195, 61, 100, 63)  # skill 3
                rect(-8, self.FH, 16, BOX_Y + BOX_H - self.y)  # skill 1
                fill(0, 0, 100, 86)  # pure white inner beam
                rect(-3, self.FH, 6,  BOX_Y + BOX_H - self.y)  # skill 1
        no_tint()
        image_mode(CENTER)
        image(sprite, 0, 0, self.FW * 2, self.FH * 2)  # skull 2x scale - skill 8
        image_mode(CORNER)
        pop_matrix()  # skill 11
    def is_done(self):
        return self.timer <= 0
    def hits_soul(self, sx, sy):
        if not self.firing:
            return False
        if self.side == 'left':
            return self.x < sx < BOX_X + BOX_W and abs(sy - self.y) < 10
        elif self.side == 'right':
            return BOX_X < sx < self.x and abs(sy - self.y) < 10
        else:
            return self.y < sy < BOX_Y + BOX_H and abs(sx - self.x) < 10

# globals set in setup - skill 4
sheet        = None
red_heart    = None
bone_img     = None
gaster_sheet = None
ltg_img      = None
sans_frame      = 0
sans_anim_timer = 0
frame_set       = IDLE_FRAMES
soul_x          = float(BOX_X + BOX_W // 2)
soul_y          = float(BOX_Y + BOX_H // 2)
player_hp       = 20
player_max_hp   = 20
sans_hp         = 30
sans_max_hp     = 30
invincible      = 0  # invincibility frame count
bones           = []
blasters        = []
attack_timer    = 80
attack_index    = 0
phase           = "dialogue"
dialogue_index  = 0
dialogue_timer  = 0
dialogue_text   = ""
dialogue_char   = 0  # chars revealed so far
typewrite_timer = 0
taunt_text      = ""
taunt_timer     = 0
show_ltg_taunt  = False  # show ltg this taunt
flash_red       = 0

def draw_text_box(txt_lines, show_ltg=False):  # skill 1 2 8
    fill(0, 0, 0)  # black — achromatic, HSB S=0 B=0
    stroke(0, 0, 100)  # white stroke — achromatic, HSB S=0 B=100 - skill 2
    stroke_weight(3)  # skill 2
    rect(30, 415, W - 60, 140, 6)  # dialogue box - skill 1
    no_stroke()
    if show_ltg and ltg_img is not None:
        no_tint()
        image_mode(CORNER)
        image(ltg_img, 38, 423, 95, 95)  # ltg portrait in box - skill 8
        fill(0, 0, 100)  # white text
        text_size(16)
        text_align(LEFT, TOP)
        for i, txt in enumerate(txt_lines):
            text(txt, 148, 435 + i * 24)  # text beside ltg image
    else:
        fill(0, 0, 100)  # white text
        text_size(16)
        text_align(LEFT, TOP)
        for i, txt in enumerate(txt_lines):
            text(txt, 50, 430 + i * 22)

def draw_hud():  # skill 1, 3
    no_stroke()
    fill(0, 0, 16)  # dark gray track — HSB achromatic bri=16 ≈ rgb(40,40,40) - skill 3
    rect(BOX_X, H - 30, BOX_W, 14)  # dark bar track - skill 1
    # HSB: hue=0 (red), sat=80, bri=100 — vivid HP bar red
    fill(0, 80, 100)  # skill 3
    rect(BOX_X, H - 30, int(BOX_W * max(0, player_hp) / player_max_hp), 14)  # scaled hp bar - skill 1

def draw_battle_box():  # skill 1 2
    stroke(0, 0, 100)  # white stroke — achromatic - skill 2
    stroke_weight(3)
    no_fill()
    rect(BOX_X, BOX_Y, BOX_W, BOX_H)  # skill 1

def draw_soul():  # skill 1 2 8
    no_tint()
    image_mode(CENTER)
    image(red_heart, soul_x, soul_y, 20, 20)  # skill 8
    image_mode(CORNER)
    if invincible > 0:
        no_fill()
        # HSB: hue=0 (red), sat=69, bri=100, alpha=63 — soft red iframes arc
        stroke(0, 69, 100, 63)  # arc while invincible - skill 2
        stroke_weight(2)
        arc(soul_x, soul_y + 8, 22, 10, 0, math.pi)  # arc below soul - skill 1
        no_stroke()

def draw_sans():  # skill 8, 11
    global sans_frame, sans_anim_timer
    sans_anim_timer += 1
    if sans_anim_timer >= 12:
        sans_anim_timer = 0
        sans_frame = (sans_frame + 1) % len(frame_set)  # advance frame
    x1, y1, x2, y2 = frame_set[sans_frame]
    sw, sh = x2 - x1, y2 - y1
    no_tint()
    push_matrix()  # skill 11
    translate(SANS_X, SANS_Y)  # center above box - skill 11
    sprite = sheet.get_pixels(x1, y1, sw, sh)  # crop frame - skill 8
    image_mode(CENTER)
    image(sprite, 0, 0, sw * 3, sh * 3)  # 3x scale - skill 8
    image_mode(CORNER)
    pop_matrix()  # skill 11

def spawn_h_bones():
    for i in range(6):
        y = BOX_Y + random.randint(15, BOX_H - 25)
        bones.append(Bone(BOX_X - 30, y, 4.5, 0, delay=i * 18))  # staggered delay - skill 9

def spawn_v_bones():
    for i in range(7):
        x = BOX_X + random.randint(15, BOX_W - 15)
        bones.append(Bone(x, BOX_Y - 30, 0, 4, delay=i * 14))  # skill 9

def spawn_blasters(count=2):
    sides = ['left', 'right', 'top']
    for _ in range(count):
        side = random.choice(sides)
        if side == 'left':
            blasters.append(Blaster(BOX_X - 60, BOX_Y + random.randint(20, BOX_H - 20), 'left'))
        elif side == 'right':
            blasters.append(Blaster(BOX_X + BOX_W + 60, BOX_Y + random.randint(20, BOX_H - 20), 'right'))
        else:
            blasters.append(Blaster(BOX_X + random.randint(20, BOX_W - 20), BOX_Y - 60, 'top'))

ATTACKS = ['h_white','v_white','blaster','h_white','v_white','blaster','h_white','v_white','blaster2','h_white']

def run_attacks():
    global attack_timer, attack_index
    attack_timer -= 1
    if attack_timer > 0:
        return
    atk = ATTACKS[attack_index % len(ATTACKS)]  # wraps around
    attack_index += 1
    if   atk == 'h_white':  spawn_h_bones();    attack_timer = 120
    elif atk == 'v_white':  spawn_v_bones();    attack_timer = 120
    elif atk == 'blaster':  spawn_blasters(2);  attack_timer = 160
    elif atk == 'blaster2': spawn_blasters(3);  attack_timer = 180

def update_soul():  # skill 5 9
    global soul_x, soul_y
    if 'a' in keys_held: soul_x -= SOUL_SPEED  # skill 5
    if 'd' in keys_held: soul_x += SOUL_SPEED  # skill 5
    if 'w' in keys_held: soul_y -= SOUL_SPEED  # skill 5
    if 's' in keys_held: soul_y += SOUL_SPEED  # skill 5
    soul_x = constrain(soul_x, BOX_X + 9, BOX_X + BOX_W - 9)
    soul_y = constrain(soul_y, BOX_Y + 9, BOX_Y + BOX_H - 9)

def check_hits():
    global player_hp, invincible, flash_red, taunt_text, taunt_timer, show_ltg_taunt
    if invincible > 0:
        invincible -= 1
        return
    for b in bones:
        if not b.active: continue
        if b.hits(soul_x, soul_y):
            player_hp      -= 3
            invincible      = 50
            flash_red       = 18
            taunt_text      = random.choice(TAUNT_LINES)
            taunt_timer     = 100
            show_ltg_taunt  = random.random() < 0.35  # 35 pct chance ltg
            break
    for bl in blasters:
        if bl.hits_soul(soul_x, soul_y):
            player_hp      -= 5
            invincible      = 60
            flash_red       = 25
            taunt_text      = random.choice(TAUNT_LINES)
            taunt_timer     = 100
            show_ltg_taunt  = random.random() < 0.35
            break

def apply_red_flash():  # skill 1, 12
    no_stroke()
    # HSB: hue=0 (red), sat=100, bri=78, alpha=31 — red screen flash overlay
    fill(0, 100, 78, 31)
    quad(0, 0, W, 0, W, H, 0, H)  # red overlay - skill 1
    px = get_np_pixels()  # grab argb pixel array - skill 12
    px[:, :, 1] = np.clip(px[:, :, 1].astype(np.int16) + 80, 0, 255).astype(np.uint8)  # boost red
    px[:, :, 2] = np.clip(px[:, :, 2].astype(np.int16) - 60, 0, 255).astype(np.uint8)  # dim green
    px[:, :, 3] = np.clip(px[:, :, 3].astype(np.int16) - 60, 0, 255).astype(np.uint8)  # dim blue
    set_np_pixels(px, bands='ARGB')  # skill 12

def update_dialogue():
    global dialogue_char, typewrite_timer
    typewrite_timer += 1
    if typewrite_timer >= 3 and dialogue_char < len(dialogue_text):
        dialogue_char  += 1  # reveal next char
        typewrite_timer = 0

def start_dialogue(txt):
    global dialogue_text, dialogue_char, typewrite_timer, frame_set, sans_frame
    dialogue_text   = txt
    dialogue_char   = 0
    typewrite_timer = 0
    frame_set       = TALK_FRAMES  # talking anim
    sans_frame      = 0

def reset():
    global soul_x, soul_y, player_hp, sans_hp, invincible
    global bones, blasters, attack_timer, attack_index
    global phase, flash_red, dialogue_index, frame_set, sans_frame
    global taunt_text, taunt_timer, show_ltg_taunt
    soul_x         = float(BOX_X + BOX_W // 2)
    soul_y         = float(BOX_Y + BOX_H // 2)
    player_hp      = player_max_hp
    sans_hp        = sans_max_hp
    invincible     = 0
    bones.clear()
    blasters.clear()
    attack_timer   = 80
    attack_index   = 0
    flash_red      = 0
    dialogue_index = 0
    frame_set      = IDLE_FRAMES
    sans_frame     = 0
    taunt_text     = ""
    taunt_timer    = 0
    show_ltg_taunt = False
    phase          = "fight"

def setup():  # skill 4
    global sheet, red_heart, bone_img, gaster_sheet, ltg_img, dialogue_timer
    size(W, H)
    frame_rate(60)
    color_mode(HSB, 360, 100, 100, 100)  # hue 0-360, sat/bri/alpha 0-100
    sheet        = load_image("assets/spritesheet.png")        # skill 8
    red_heart    = load_image("assets/redhear.png")            # skill 8
    bone_img     = load_image("assets/bone.png")               # skill 8
    gaster_sheet = load_image("assets/spritesheetgaster.png")  # skill 8
    ltg_img      = load_image("assets/lowtiergod.jpg")         # skill 8
    text_font(create_font("Comic Sans MS", 14))
    image_mode(CORNER)
    start_dialogue(DIALOGUES[0])
    dialogue_timer = max(80, len(DIALOGUES[0]) * 4 + 40)

def draw():  # skill 4
    global phase, flash_red, taunt_text, taunt_timer, show_ltg_taunt
    global dialogue_index, dialogue_timer, frame_set
    background(0, 0, 0)  # black background — HSB bri=0
    if phase == "dialogue":
        draw_sans()
        update_dialogue()
        draw_text_box([dialogue_text[:dialogue_char]])  # revealed chars only
        dialogue_timer -= 1
        if dialogue_timer <= 0:
            dialogue_index += 1
            if dialogue_index >= len(DIALOGUES):
                phase        = "fight"
                frame_set    = IDLE_FRAMES
                attack_timer = 90
            else:
                start_dialogue(DIALOGUES[dialogue_index])
                dialogue_timer = max(80, len(DIALOGUES[dialogue_index]) * 4 + 40)
        return
    if phase == "gameover":
        no_tint()
        image_mode(CENTER)
        image(red_heart, W // 2, H // 2 - 60, 40, 40)  # skill 8
        image_mode(CORNER)
        fill(0, 0, 100)  # white text
        text_size(18)
        text_align(CENTER, CENTER)
        text("but it refused.", W // 2, H // 2)
        fill(0, 0, 71)  # light gray — HSB bri=71 ≈ rgb(180,180,180)
        text_size(14)
        text("press  r  to restart", W // 2, H // 2 + 35)
        return
    draw_sans()
    draw_battle_box()
    draw_hud()
    for b in bones[:]:  # copy so we can remove mid loop
        b.update()
        b.draw(bone_img)
        if b.is_offscreen():
            bones.remove(b)
    for bl in blasters[:]:
        bl.update()
        bl.draw()
        if bl.is_done():
            blasters.remove(bl)
    update_soul()
    check_hits()
    if not (invincible > 0 and frame_count % 6 < 3):
        draw_soul()  # blink during iframes
    if taunt_timer > 0:
        taunt_timer -= 1
        draw_text_box([taunt_text], show_ltg=show_ltg_taunt)
    run_attacks()
    if flash_red > 0:
        apply_red_flash()  # skill 12
        flash_red -= 1
    if player_hp <= 0:
        phase = "gameover"
    if sans_hp <= 0:
        phase = "win"

def key_pressed():  # skill 5
    global phase, dialogue_timer
    if key in ('a','d','w','s'):
        keys_held.add(key)  # skill 5
    if phase == "dialogue":
        dialogue_timer = 1  # skip line
    elif phase == "gameover":
        if key in ('r', 'R'):
            reset()

def key_released():  # skill 5
    if key in keys_held:
        keys_held.discard(key)  # remove on release - skill 5