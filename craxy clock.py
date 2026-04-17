bank = [0.0] # list so we can change it in mouse_pressed
minutes = [0] # how many mintues you have
hours = [0] # how many housr you have

def setup():
    size(400, 500) # window size
    text_align(CENTER, CENTER) # center text
    text_size(18) # text size
    frame_rate(60) # 60 times per scond

def draw():
    bank[0] += (1 + minutes[0] + hours[0])*60 / 60.0 # add money each frmae

    background(0) # black background
    fill(255) # white text

    text(f"Seconds: {int(bank[0])}", 200, 80) # show seocnds
    text(f"Minutes: {minutes[0]}  (x60 sec/min)", 200, 130) # show mintues
    text(f"Hours:   {hours[0]}  (x60 min/hr)", 200, 180) # show housr

    can_buy_min = bank[0] >= 60 # do you have enoguh
    fill(100, 200, 100) if can_buy_min else fill(80) # green if yes, grey if no
    rect(100, 230, 200, 50, 8) # mintue button box
    fill(255) # white text
    text("Buy Minute (60s)", 200, 255) # button text

    can_buy_hr = minutes[0] >= 60 # do you have enoguh
    fill(100, 150, 255) if can_buy_hr else fill(80) # blue if yes, grey if no
    rect(100, 310, 200, 50, 8) # hour button box
    fill(255) # white text
    text("Buy Hour (60min)", 200, 335) # button text

    fill(160) # grey
    text_size(13) # small text
    text(f"+{60 + minutes[0]*60 + hours[0]*3600} seconds/min", 200, 420) # how fast you earn
    text_size(18) # back to normal

def mouse_pressed():
    if 100 < mouse_x < 300 and 230 < mouse_y < 280: # clicked mintue button
        if bank[0] >= 60: # can you buy it
            bank[0] -= 60 # take the cost
            minutes[0] += 1 # give a mintue

    if 100 < mouse_x < 300 and 310 < mouse_y < 360: # clicked hour button
        if minutes[0] >= 60: # can you buy it
            minutes[0] -= 60 # take the cost
            hours[0] += 1 # give an houyr