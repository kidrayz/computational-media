#Raymond Zheng 

W, H = 800, 600  # windwo widht n hieght

t            = 0.0  # clock incremnts evry fram
phase        = 0  # wich sceen we r in rigt now
impact_start = 0.0  # tracks wen impact was triggrd
crosses      = []  # list of erupting cros objekts


class Cross:  # clas 4 the erupting ground crosses
    def __init__(self, x=None):  # sets up a singl cross
        self.x     = x if x else random(30, W - 30)  # randum x or givn x
        self.y     = H + random(10, 40)  # starts just below botom edge
        self.speed = random(4.0, 9.0)  # how fast it erupts upwrd
        self.size  = random(250, 500)  # very tall christian cross
        self.alpha = int(random(200, 255))  # how opaque it starts
        self.fade  = random(0.8, 1.5)  # fades slowr so u can see it
        self.col   = random_choice(["white", "orange"])  # wite or oranje
        self.alive = True  # cross is alive wen creatd

    def get_color(self):  # returns rgb tupel 4 color name
        if self.col == "white":  # wite option
            return (255, 245, 230)  # warm wite liek in film
        else:  # oranje option
            return (255, 80, 10)  # deep redy oranje

    def update(self):  # updaets cross positon each fram
        self.y     -= self.speed  # erupts upwrd frm ground
        self.speed *= 0.97  # slows dwon as it rises
        self.alpha -= self.fade  # fades gradualy
        if self.alpha <= 0:  # cheks if fully faded
            self.alive = False  # marks it ded 4 removal

    def draw(self):  # draws the erupting cross
        push_matrix()  # saves current transfrom state
        translate(self.x, self.y)  # moves origin 2 cross positon
        s = self.size  # shorthand 4 size
        r, g, b = self.get_color()  # gets rgb from color name
        no_stroke()  # no outlin on the cross
        fill(r, g, b, int(self.alpha))  # full bright core only no glow
        rect(-s * 0.04, -s * 0.75, s * 0.08, s)  # very thin verticl bar
        rect(-s * 0.25, -s * 0.45, s * 0.5, s * 0.08)  # thin horizontl bar high up
        pop_matrix()  # restors previus transform


def setup():  # py5 setup runs once
    size(W, H)  # sets windwo size
    color_mode(RGB, 255)  # rgb color mode


def draw():  # py5 draw runs evry frame
    global t, crosses, phase  # globals we need
    t += 0.05  # increments master clok

    bg_r = int(10 + sin(t * 0.3) * 5)  # slitely pulsing dark red
    background(bg_r, 0, int(bg_r * 0.3))  # dark reddish bg

    if phase == 0:  # waitin 4 click fase
        if frame_count % 40 == 0:  # very slow trickle of crosses
            crosses.append(Cross())  # adds new cros

        fill(255, 255, 255, 220)  # wite color 4 card text
        text_align(CENTER, CENTER)  # centers text
        text_size(13)  # small elegant text
        text("YOU ARE CORDIALLY INVITED", W // 2, H // 2 - 110)  # invitation header
        text_size(11)  # smaller subtext
        fill(255, 200, 150, 180)  # warm color 4 body text
        text("to bear witness to and participate in", W // 2, H // 2 - 80)  # invite body

        fill(255, 80, 10, 255)  # bright oranje 4 main title
        text_size(42)  # big dramatic title
        text("THE THIRD IMPACT", W // 2, H // 2 - 30)  # main event title

        fill(255, 245, 230, 220)  # warm wite 4 date
        text_size(20)  # medium date text
        text("NEW YEAR'S DAY", W // 2, H // 2 + 30)  # the day
        text_size(28)  # bigger year
        fill(255, 80, 10, 220)  # oranje 4 year
        text("JANUARY 1ST, 2015", W // 2, H // 2 + 65)  # the date

        fill(255, 200, 150, 160)  # dim warm color
        text_size(11)  # small fine print
        text("dress code: none ", W // 2, H // 2 + 105)  # flavor text
        text("NERV Headquarters, Tokyo-3, Japan", W // 2, H // 2 + 125)  # location

        fill(255, 220, 50, 200)  # gold color 4 promtp
        text_size(14)  # medium text size
        if int(t * 2) % 2 == 0:  # flickers on n off
            text("[ CLICK TO ACCEPT YOUR INVITATION ]", W // 2, H - 40)  # clck promtp

    elif phase == 1:  # impact fase
        elapsed = t - impact_start  # time since impact startd

        lcl_flood = min(1.0, elapsed / 8.0)  # how much lcl has floded
        bg_r = int(15 + lcl_flood * 140)  # bg gets redder as lcl floods
        background(bg_r, int(lcl_flood * 20), 0)  # floods red liek lcl sea

        spawn_rate = max(1, int(10 - elapsed))  # crosses erupt faster over time
        if frame_count % spawn_rate == 0:  # spawn on interval
            spread_x = random(30, W - 30)  # spreads across hole earth
            crosses.append(Cross(spread_x))  # adds cross at spread positon

        flash = max(0.0, 1.0 - elapsed / 2.0)  # initial flash fades fast
        if flash > 0:  # only draw flash if present
            no_stroke()  # no outlin
            fill(255, 240, 200, int(flash * 180))  # warm wite flash overlay
            rect(0, 0, W, H)  # covers hole screeen

        fill(255, 245, 230, 220)  # wite impact text
        text_size(22)  # big text size
        text_align(CENTER, CENTER)  # centers text
        text("and it all returns to nothing", W // 2, 45)  # draws impact mesage
        fill(255, 200, 150, 180)  # warm subtext
        text_size(13)  # smaller subtext
        text("it comes tumbling down tumbling down tumbling doowwn", W // 2, 75)  # date reminder

        if elapsed > 8:  # after 8 seconds move on
            phase = 2  # go 2 congrats

    elif phase == 2:  # congrats fase
        background(20, 0, 10)  # dark bg 4 congrats

        if frame_count % 30 == 0:  # sparse crosses still erupt
            crosses.append(Cross())  # adds new cross

        pulse = 1.0 + sin(t * 1.5) * 0.06  # text pulses w sine
        push_matrix()  # saves transform 4 text
        translate(W // 2, H // 2 - 20)  # centers main text
        scale(pulse)  # aplies pulse scale
        no_stroke()  # no outlin on text
        fill(255, 245, 230, 255)  # wite color
        text_size(46)  # big text
        text_align(CENTER, CENTER)  # centers it
        text("congrats", 0, -30)  # congrats
        fill(255, 200, 150, 200)  # warm subtext color
        text_size(16)  # medium subtext
        text("you are now LCL", 0, 30)  # accepted msg
        pop_matrix()  # restors transform
        fill(255, 120, 0, 160)  # orange reset promtp
        text_size(13)  # small promtp
        text_align(CENTER, CENTER)  # centers promtp
        text("[ press R to return ]", W // 2, H - 30)  # reset promtp

    for c in crosses:  # loops thru all erupting crosses
        c.update()  # moves each cross upwrd
        c.draw()  # draws each cross
    crosses[:] = [c for c in crosses if c.alive]  # removes ded crosses


def mouse_pressed():  # runs wen mouse is cliekd
    global phase, impact_start, crosses  # globals we need 2 chanje
    if phase == 0:  # only works in waitin fase
        phase        = 1  # moves 2 impact fase
        impact_start = t  # records wen impact startd
        crosses      = []  # clears old crosses


def key_pressed():  # runs wen a key is pressd
    global phase, crosses, t, impact_start  # globals we need
    if key in ('r', 'R'):  # r key resets evrything
        phase        = 0  # back 2 waitin sceen
        t            = 0.0  # resets master clok
        impact_start = 0.0  # resets impact timer
        crosses      = []  # clears all crosses
    elif phase == 1:  # any key during impact
        phase = 2  # skips 2 congrats
