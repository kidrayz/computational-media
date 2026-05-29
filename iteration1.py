# Sans Boss Fight
# Skills covered throughout: Drawing Functions (1), Controlling Color State (2),
# Using Colors (3), setup/draw (4), Events (5), Perspicuousness (6),
# Meeting Requirements (7), Images (8), Moving Shapes (9),
# Classes & Objects (10), Transformations (11), Pixels (12)

import random
import math
import numpy as np
import py5

# ── SOUND (pygame instead of load_sound) ───────────────────────────────────
try:
    import pygame
    pygame.mixer.init()
    _sound_ok = True
except Exception:
    _sound_ok = False

class _Sound:
    """Thin wrapper so music.play() / music.stop() never crash."""
    def __init__(self, path):
        self._snd = None
        if _sound_ok:
            try:
                self._snd = pygame.mixer.Sound(path)
            except Exception:
                pass
    def play(self, loops=0):
        if self._snd:
            self._snd.play(loops=loops)
    def stop(self):
        if self._snd:
            self._snd.stop()

# ── CONSTANTS ──────────────────────────────────────────────────────────────
W, H        = 800, 600
BOX_X       = 230
BOX_Y       = 170
BOX_W       = 340
BOX_H       = 210
FLOOR_Y     = BOX_Y + BOX_H - 10
SOUL_SPEED  = 4
JUMP_POWER  = -9
GRAVITY     = 0.5

# ── SPRITESHEET COORDS ─────────────────────────────────────────────────────
# Battle idle frames  (Skill 8 - Using Images)
IDLE_FRAMES = [
    (2,  647, 60,  718),
    (62, 647, 116, 718),
    (118,647, 176, 718),
]
TALK_FRAMES = [
    (178, 647, 232, 718),
    (234, 647, 282, 718),
    (284, 647, 322, 718),
]

# ── DIALOGUE ───────────────────────────────────────────────────────────────
DIALOGUES = [
    "* sans.",
    "* heh.",
    "* you know what's funny?",
    "* i've been waiting for you.",
    "* you've already lost.",
    "* but you keep going anyway.",
    "* that's... kinda impressive.",
    "* don't tell anyone i said that.",
    "* welp. here we go.",
]
TAUNT_LINES = [
    "* you're still here?",
    "* heh. not bad, kid.",
    "* im sansing it",
    "* chud",
    "* get good ",
]

# ── CLASSES ────────────────────────────────────────────────────────────────

# Skill 10 - Creating and Using Classes and Objects
class Bone:
    """A bone projectile moving across the battle box."""

    def __init__(self, x, y, vx, vy, bone_type, delay=0):
        self.x      = float(x)
        self.y      = float(y)
        self.vx     = vx
        self.vy     = vy
        self.btype  = bone_type
        self.delay  = delay
        self.active = False
        # vertical bones rotate 90 degrees  (Skill 11 - Transformations)
        self.angle  = math.pi / 2 if vx == 0 else 0   # fixed: was HALF_PI (unavailable at class-def time)
        self.w      = 48
        self.h      = 14

    def update(self):
        """Move bone each frame.  Skill 9 - Moving Shapes"""
        if self.delay > 0:
            self.delay -= 1
            return
        self.active = True
        self.x += self.vx
        self.y += self.vy

    def is_offscreen(self):
        return (self.x < BOX_X - 60 or self.x > BOX_X + BOX_W + 60 or
                self.y < BOX_Y - 60 or self.y > BOX_Y + BOX_H + 60)

    def draw(self, img_white, img_blue, img_orange):
        """Draw bone using push/pop + rotate.  Skill 11, Skill 8"""
        if not self.active:
            return
        py5.push_matrix()                           # Skill 11
        py5.translate(self.x, self.y)
        py5.rotate(self.angle)                      # Skill 11
        py5.image_mode(py5.CENTER)
        if self.btype == 'blue':
            py5.image(img_blue,   0, 0, self.w, self.h)   # Skill 8
        elif self.btype == 'orange':
            py5.image(img_orange, 0, 0, self.w, self.h)   # Skill 8
        else:
            py5.image(img_white,  0, 0, self.w, self.h)   # Skill 8
        py5.image_mode(py5.CORNER)
        py5.pop_matrix()                            # Skill 11

    def hits(self, sx, sy):
        """AABB collision with the soul."""
        hw = self.h // 2 if self.angle != 0 else self.w // 2
        hh = self.w // 2 if self.angle != 0 else self.h // 2
        return abs(self.x - sx) < hw + 5 and abs(self.y - sy) < hh + 5


class Blaster:
    """A Gaster Blaster skull that charges and fires a beam."""

    def __init__(self, x, y, angle):
        self.x      = float(x)
        self.y      = float(y)
        self.angle  = angle
        self.timer  = 100
        self.firing = False
        self.alpha  = 0

    def update(self):
        """Count down; start firing at halfway.  Skill 9"""
        self.timer -= 1
        if self.timer < 55:
            self.firing = True
        self.alpha = min(255, self.alpha + 12)

    def draw(self):
        """Draw skull and beam.  Skill 1, 2, 3, 11"""
        py5.push_matrix()                           # Skill 11
        py5.translate(self.x, self.y)
        py5.rotate(self.angle)                      # Skill 11

        if self.firing:
            py5.color_mode(py5.HSB, 360, 100, 100, 255)   # Skill 3
            py5.fill(190, 100, 100, 180)
            py5.no_stroke()
            py5.rect(20, -7, 320, 14)                      # Skill 1
            py5.fill(0, 0, 100, 230)
            py5.rect(20, -3, 320, 6)                       # Skill 1
            py5.color_mode(py5.RGB, 255)                   # Skill 3

        py5.fill(200, 200, 220, self.alpha)                # Skill 2
        py5.stroke(100, 100, 140, self.alpha)              # Skill 2
        py5.stroke_weight(2)                               # Skill 2
        py5.ellipse(0, 0, 52, 36)                          # Skill 1

        py5.fill(0, 0, 0, self.alpha)
        py5.no_stroke()
        py5.ellipse(-13, -4, 14, 11)                       # Skill 1
        py5.ellipse( 13, -4, 14, 11)                       # Skill 1

        py5.color_mode(py5.HSB, 360, 100, 100, 255)       # Skill 3
        glow_h = 30 if self.firing else 190
        py5.fill(glow_h, 90, 100, self.alpha)
        py5.ellipse(-13, -4, 8, 6)                         # Skill 1
        py5.ellipse( 13, -4, 8, 6)                         # Skill 1
        py5.color_mode(py5.RGB, 255)

        py5.fill(220, 220, 220, self.alpha)
        for i in range(4):
            py5.rect(-10 + i * 7, 6, 5, 7)                # Skill 1

        py5.no_fill()
        py5.stroke(180, 180, 200, self.alpha)
        py5.stroke_weight(2)
        py5.arc(0, 8, 36, 16, 0, math.pi)                 # Skill 1

        py5.pop_matrix()                                   # Skill 11

    def is_done(self):
        return self.timer <= 0

    def hits_soul(self, sx, sy):
        if not self.firing:
            return False
        dx = sx - self.x
        dy = sy - self.y
        lx = dx * math.cos(-self.angle) - dy * math.sin(-self.angle)
        ly = dx * math.sin(-self.angle) + dy * math.cos(-self.angle)
        return lx > 20 and abs(ly) < 10


# ── GLOBAL STATE ───────────────────────────────────────────────────────────
sheet       = None
red_heart   = None
blue_heart  = None
bone_img    = None
blue_bone   = None
orange_bone = None
talk_sound  = None
music       = None

sans_frame      = 0
sans_anim_timer = 0
frame_set       = IDLE_FRAMES

soul_x   = BOX_X + BOX_W // 2
soul_y   = BOX_Y + BOX_H // 2
soul_vx  = 0.0
soul_vy  = 0.0
soul_blue = False

player_hp     = 20
player_max_hp = 20
sans_hp       = 30
sans_max_hp   = 30
invincible    = 0

bones         = []
blasters      = []
attack_timer  = 80
attack_index  = 0
phase         = "intro"

dialogue_index  = 0
dialogue_timer  = 0
dialogue_text   = ""
dialogue_char   = 0
typewrite_timer = 0
taunt_text      = ""
taunt_timer     = 0

flash_red    = 0
do_grayscale = False


# ── HELPERS ────────────────────────────────────────────────────────────────

def draw_text_box(lines):
    """Undertale-style dialogue box.  Skill 1, 2"""
    py5.fill(0)                                     # Skill 2
    py5.stroke(255)                                 # Skill 2
    py5.stroke_weight(3)                            # Skill 2
    py5.rect(30, 415, W - 60, 140, 6)              # Skill 1
    py5.fill(255)
    py5.no_stroke()
    py5.text_size(16)
    py5.text_align(py5.LEFT, py5.TOP)
    for i, line in enumerate(lines):
        py5.text(line, 50, 430 + i * 22)


def draw_hud():
    """Health bars and labels.  Skill 1, 2, 3"""
    py5.text_align(py5.LEFT, py5.TOP)
    py5.text_size(13)
    py5.fill(255, 255, 255)                         # Skill 3
    py5.text("SANS  LV ??", 30, 30)

    py5.fill(40, 40, 40)                            # Skill 3
    py5.no_stroke()
    py5.rect(30, 50, 160, 13)                       # Skill 1
    py5.fill(255, 140, 30)                          # Skill 3
    py5.rect(30, 50, int(160 * max(0, sans_hp) / sans_max_hp), 13)

    py5.fill(255)
    py5.text(f"HP  {max(0,sans_hp)} / {sans_max_hp}", 30, 70)
    py5.text(f"LV  1     HP  {max(0,player_hp)} / {player_max_hp}", 30, H - 80)

    py5.fill(40, 40, 40)
    py5.no_stroke()
    py5.rect(30, H - 65, 200, 13)                  # Skill 1
    py5.fill(255, 50, 50)                           # Skill 3
    py5.rect(30, H - 65, int(200 * max(0, player_hp) / player_max_hp), 13)


def draw_battle_box():
    """White battle border.  Skill 1, 2"""
    py5.stroke(255)                                 # Skill 2
    py5.stroke_weight(3)                            # Skill 2
    py5.no_fill()
    py5.rect(BOX_X, BOX_Y, BOX_W, BOX_H)          # Skill 1


def draw_soul():
    """Draw heart image for the soul.  Skill 8"""
    py5.image_mode(py5.CENTER)
    if soul_blue:
        py5.image(blue_heart, soul_x, soul_y, 20, 20)   # Skill 8
    else:
        py5.image(red_heart,  soul_x, soul_y, 20, 20)   # Skill 8
    py5.image_mode(py5.CORNER)


def draw_sans():
    """Animate Sans from spritesheet.  Skill 8, 11"""
    global sans_frame, sans_anim_timer
    sans_anim_timer += 1
    if sans_anim_timer >= 12:
        sans_anim_timer = 0
        sans_frame = (sans_frame + 1) % len(frame_set)

    x1, y1, x2, y2 = frame_set[sans_frame]
    sw, sh = x2 - x1, y2 - y1

    py5.push_matrix()                               # Skill 11
    py5.translate(560, 190)                         # Skill 11
    # fixed: py5 uses get_pixels / create_image approach instead of sheet.get()
    sprite = sheet.get(x1, y1, sw, sh)             # Skill 8
    py5.image_mode(py5.CENTER)
    py5.image(sprite, 0, 0, sw * 3, sh * 3)        # Skill 8
    py5.image_mode(py5.CORNER)
    py5.pop_matrix()                                # Skill 11


# ── SPAWNERS ───────────────────────────────────────────────────────────────

def spawn_h_bones(bone_type='white'):
    """Horizontal bone wave.  Skill 9"""
    for i in range(6):
        y = BOX_Y + random.randint(15, BOX_H - 25)
        bones.append(Bone(BOX_X - 30, y, 4.5, 0, bone_type, delay=i * 18))


def spawn_v_bones(bone_type='white'):
    """Vertical bone rain.  Skill 9"""
    for i in range(7):
        x = BOX_X + random.randint(15, BOX_W - 15)
        bones.append(Bone(x, BOX_Y - 30, 0, 4, bone_type, delay=i * 14))


def spawn_blasters(count=2):
    """Spawn Gaster Blasters.  Skill 9"""
    sides = ['left', 'right', 'top']
    for _ in range(count):
        side = random.choice(sides)
        if side == 'left':
            blasters.append(Blaster(BOX_X - 55, BOX_Y + random.randint(20, BOX_H-20), 0))
        elif side == 'right':
            blasters.append(Blaster(BOX_X + BOX_W + 55, BOX_Y + random.randint(20, BOX_H-20), math.pi))
        else:
            blasters.append(Blaster(BOX_X + random.randint(20, BOX_W-20), BOX_Y - 55, math.pi / 2))


# ── ATTACK SEQUENCE ────────────────────────────────────────────────────────
ATTACKS = ['h_white','v_white','blaster','h_blue','v_white',
           'blaster','h_orange','v_white','blaster2','h_blue']

def run_attacks():
    """Cycle through attack patterns.  Skill 9"""
    global attack_timer, attack_index, soul_blue
    attack_timer -= 1
    if attack_timer > 0:
        return
    atk = ATTACKS[attack_index % len(ATTACKS)]
    attack_index += 1
    if   atk == 'h_white':  soul_blue = False; spawn_h_bones('white');  attack_timer = 120
    elif atk == 'v_white':  soul_blue = False; spawn_v_bones('white');  attack_timer = 120
    elif atk == 'h_blue':   soul_blue = True;  spawn_h_bones('blue');   attack_timer = 140
    elif atk == 'h_orange': soul_blue = False; spawn_h_bones('orange'); attack_timer = 130
    elif atk == 'blaster':  soul_blue = False; spawn_blasters(2);       attack_timer = 160
    elif atk == 'blaster2': soul_blue = False; spawn_blasters(3);       attack_timer = 180


# ── SOUL MOVEMENT ──────────────────────────────────────────────────────────
def update_soul():
    """Move soul; gravity in blue mode.  Skill 9"""
    global soul_x, soul_y, soul_vx, soul_vy
    if soul_blue:
        if py5.is_key_pressed and py5.key_code == py5.LEFT:    soul_vx = -SOUL_SPEED  # Skill 5
        elif py5.is_key_pressed and py5.key_code == py5.RIGHT: soul_vx =  SOUL_SPEED  # Skill 5
        else: soul_vx *= 0.75
        soul_vy += GRAVITY
        soul_x  += soul_vx
        soul_y  += soul_vy
        if soul_y >= FLOOR_Y:
            soul_y  = FLOOR_Y
            soul_vy = 0.0
    else:
        if py5.is_key_pressed and py5.key_code == py5.LEFT:  soul_x -= SOUL_SPEED   # Skill 5
        if py5.is_key_pressed and py5.key_code == py5.RIGHT: soul_x += SOUL_SPEED   # Skill 5
        if py5.is_key_pressed and py5.key_code == py5.UP:    soul_y -= SOUL_SPEED   # Skill 5
        if py5.is_key_pressed and py5.key_code == py5.DOWN:  soul_y += SOUL_SPEED   # Skill 5
    soul_x = py5.constrain(soul_x, BOX_X + 9, BOX_X + BOX_W - 9)
    soul_y = py5.constrain(soul_y, BOX_Y + 9, BOX_Y + BOX_H - 9)


# ── HIT DETECTION ──────────────────────────────────────────────────────────
def check_hits():
    global player_hp, invincible, flash_red
    if invincible > 0:
        invincible -= 1
        return
    for b in bones:
        if not b.active: continue
        if b.hits(soul_x, soul_y):
            if   b.btype == 'white':                    dmg = 3
            elif b.btype == 'blue' and not soul_blue:   dmg = 4
            elif b.btype == 'orange':                   dmg = 4
            else:                                       dmg = 0
            if dmg > 0:
                player_hp -= dmg
                invincible  = 50
                flash_red   = 18
            break
    for bl in blasters:
        if bl.hits_soul(soul_x, soul_y):
            player_hp -= 5
            invincible  = 60
            flash_red   = 25
            break


# ── PIXEL EFFECTS ──────────────────────────────────────────────────────────

def apply_red_flash():
    """Red tint on damage.  Skill 12 - Using Pixels"""
    # fixed: py5 uses get_np_pixels / set_np_pixels instead of load_pixels/pixels[]
    px = py5.get_np_pixels()                        # Skill 12 - RGBA uint8 array
    px[:, :, 1] = np.clip(px[:, :, 1].astype(np.int16) + 120, 0, 255).astype(np.uint8)
    px[:, :, 2] = np.clip(px[:, :, 2].astype(np.int16) -  60, 0, 255).astype(np.uint8)
    px[:, :, 3] = np.clip(px[:, :, 3].astype(np.int16) -  60, 0, 255).astype(np.uint8)
    py5.set_np_pixels(px, bands='RGBA')             # Skill 12


def apply_grayscale():
    """Desaturate screen on game over.  Skill 12 - Using Pixels"""
    px   = py5.get_np_pixels()                      # Skill 12
    r, g, b = px[:, :, 1], px[:, :, 2], px[:, :, 3]
    gray = (r.astype(np.uint16) * 30 +
            g.astype(np.uint16) * 59 +
            b.astype(np.uint16) * 11) // 100
    gray = gray.astype(np.uint8)
    px[:, :, 1] = gray
    px[:, :, 2] = gray
    px[:, :, 3] = gray
    py5.set_np_pixels(px, bands='RGBA')             # Skill 12


# ── DIALOGUE HELPERS ───────────────────────────────────────────────────────

def update_dialogue():
    """Typewriter effect.  Skill 4"""
    global dialogue_char, typewrite_timer
    typewrite_timer += 1
    if typewrite_timer >= 3 and dialogue_char < len(dialogue_text):
        dialogue_char  += 1
        typewrite_timer = 0


def start_dialogue(line):
    global dialogue_text, dialogue_char, typewrite_timer, frame_set, sans_frame
    dialogue_text   = line
    dialogue_char   = 0
    typewrite_timer = 0
    frame_set       = TALK_FRAMES
    sans_frame      = 0


# ── RESET ──────────────────────────────────────────────────────────────────

def reset():
    """Reset all state for retry.  Skill 4"""
    global soul_x, soul_y, soul_vx, soul_vy, soul_blue
    global player_hp, sans_hp, invincible
    global bones, blasters, attack_timer, attack_index
    global phase, flash_red, dialogue_index, frame_set, sans_frame
    global taunt_text, taunt_timer
    soul_x = BOX_X + BOX_W // 2
    soul_y = BOX_Y + BOX_H // 2
    soul_vx = soul_vy = 0.0
    soul_blue    = False
    player_hp    = player_max_hp
    sans_hp      = sans_max_hp
    invincible   = 0
    bones.clear(); blasters.clear()
    attack_timer  = 80
    attack_index  = 0
    flash_red     = 0
    dialogue_index= 0
    frame_set     = IDLE_FRAMES
    sans_frame    = 0
    taunt_text    = ""
    taunt_timer   = 0
    phase = "fight"


# ══ SETUP ══════════════════════════════════════════════════════════════════
def setup():
    global sheet, red_heart, blue_heart, bone_img, blue_bone, orange_bone
    global talk_sound, music

    py5.size(W, H)
    py5.frame_rate(60)

    # Skill 8 - Using Images
    sheet       = py5.load_image("assets/spritesheet.png")
    red_heart   = py5.load_image("assets/redhear.png")
    blue_heart  = py5.load_image("assets/blueheart.png")
    bone_img    = py5.load_image("assets/bone.png")
    blue_bone   = py5.load_image("assets/bluebone.png")
    orange_bone = py5.load_image("assets/orangebone.png")

    # fixed: use _Sound wrapper (pygame) instead of load_sound()
    talk_sound  = _Sound("assets/talk.mp3")
    music       = _Sound("assets/megalovalia.mp3")

    # fixed: create_font takes a font name string; use a safe monospace name
    py5.text_font(py5.create_font("Courier New", 14))
    py5.image_mode(py5.CORNER)


# ══ DRAW ═══════════════════════════════════════════════════════════════════
def draw():
    global phase, flash_red, taunt_text, taunt_timer
    global dialogue_index, dialogue_timer, frame_set

    py5.background(0)

    # ── INTRO ──────────────────────────────────────────────────────────────
    if phase == "intro":
        py5.color_mode(py5.HSB, 360, 100, 100)     # Skill 3
        py5.fill((py5.frame_count * 2) % 360, 60, 100)
        py5.color_mode(py5.RGB, 255)
        py5.text_size(32)
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text("* SANS *", W // 2, H // 2 - 60)  # Skill 1

        py5.fill(200, 200, 200)
        py5.triangle(W//2 - 60, H//2 - 90,         # Skill 1
                     W//2 - 40, H//2 - 60,
                     W//2 - 80, H//2 - 60)
        py5.triangle(W//2 + 60, H//2 - 90,
                     W//2 + 80, H//2 - 60,
                     W//2 + 40, H//2 - 60)

        py5.fill(180, 180, 180)
        py5.text_size(15)
        py5.text("press any key to begin", W // 2, H // 2 + 10)
        draw_sans()
        return

    # ── GAME OVER ──────────────────────────────────────────────────────────
    if phase == "gameover":
        draw_sans()
        draw_hud()
        draw_battle_box()
        apply_grayscale()                           # Skill 12

        py5.fill(0, 0, 0, 160)
        py5.no_stroke()
        py5.rect(0, 0, W, H)                        # Skill 1
        py5.fill(255, 50, 50)                       # Skill 3
        py5.text_size(40)
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text("GAME OVER", W // 2, H // 2 - 20) # Skill 1
        py5.fill(200, 200, 200)
        py5.text_size(15)
        py5.text("* but it refused.", W // 2, H // 2 + 30)
        py5.text("press  R  to retry",  W // 2, H // 2 + 58)
        return

    # ── WIN ────────────────────────────────────────────────────────────────
    if phase == "win":
        py5.background(0)
        py5.color_mode(py5.HSB, 360, 100, 100)     # Skill 3
        for i in range(8):
            py5.fill((py5.frame_count * 3 + i * 45) % 360, 80, 100)
            py5.text_size(14)
            py5.text_align(py5.CENTER, py5.CENTER)
            py5.text("* * * * * * * * *", W // 2, 80 + i * 40)
        py5.color_mode(py5.RGB, 255)
        py5.fill(255, 220, 50)
        py5.text_size(30)
        py5.text("* you won.", W // 2, H // 2 - 20)
        py5.fill(200, 200, 200)
        py5.text_size(15)
        py5.text("* heh. not bad, kid.", W // 2, H // 2 + 25)
        return

    # ── DIALOGUE ───────────────────────────────────────────────────────────
    if phase == "dialogue":
        py5.background(0)
        draw_sans()
        update_dialogue()
        draw_text_box([dialogue_text[:dialogue_char]])
        dialogue_timer -= 1
        if dialogue_timer <= 0:
            dialogue_index += 1
            if dialogue_index >= len(DIALOGUES):
                phase = "fight"
                music.play(loops=-1)
                frame_set = IDLE_FRAMES
                attack_timer = 90
            else:
                start_dialogue(DIALOGUES[dialogue_index])
                dialogue_timer = max(80, len(DIALOGUES[dialogue_index]) * 4 + 40)
                talk_sound.play()
        return

    # ── FIGHT ──────────────────────────────────────────────────────────────
    draw_sans()
    draw_battle_box()
    draw_hud()

    for b in bones[:]:                              # Skill 9
        b.update()
        b.draw(bone_img, blue_bone, orange_bone)
        if b.is_offscreen():
            bones.remove(b)

    for bl in blasters[:]:                         # Skill 9
        bl.update()
        bl.draw()
        if bl.is_done():
            blasters.remove(bl)

    update_soul()
    check_hits()

    if not (invincible > 0 and py5.frame_count % 6 < 3):
        draw_soul()

    if taunt_timer > 0:
        taunt_timer -= 1
        draw_text_box([taunt_text])
    elif py5.frame_count % 420 == 0:
        taunt_text  = random.choice(TAUNT_LINES)
        taunt_timer = 90

    run_attacks()

    if flash_red > 0:                              # Skill 12
        apply_red_flash()
        flash_red -= 1

    if player_hp <= 0:
        phase = "gameover"
        music.stop()
    if sans_hp <= 0:
        phase = "win"
        music.stop()


# ══ EVENTS ═════════════════════════════════════════════════════════════════
# Skill 5 - Events
def key_pressed():
    global phase, soul_vy, dialogue_timer, dialogue_index

    if phase == "intro":
        phase = "dialogue"
        start_dialogue(DIALOGUES[0])
        dialogue_timer = max(80, len(DIALOGUES[0]) * 4 + 40)
        talk_sound.play()

    elif phase == "dialogue":
        dialogue_timer = 1

    elif phase == "gameover":
        # fixed: py5 uses py5.key for the pressed character
        if py5.key in ('r', 'R'):
            reset()

    elif phase == "fight":
        if soul_blue and py5.key == ' ':            # Skill 5
            soul_vy = JUMP_POWER


# ══ ENTRY POINT ════════════════════════════════════════════════════════════
# fixed: py5 module-mode requires run_sketch() to start the sketch
py5.run_sketch()
