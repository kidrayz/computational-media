images = []  # empty list for images
current_index = 0  # wich image were on
mode = 1  # 1=cool, 2=warm, 3=combined

def setup():
    size(480, 270)  # smol window
    global images  # use global list
    folder_path = 'PICTURES'  # folder path
    for filename in os.listdir(folder_path):  # loop thru files
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # images only
            img_path = os.path.join(folder_path, filename)  # build path
            images.append(load_image(img_path))  # load and store
    frame_rate(60)  # 60fps

def apply_temp(rv, gv, bv, temp):  # function to shift color temperture
    t = temp / 100.0  # normalize to -1 to 1
    if t > 0:  # warm: more red less blue
        rv = min(255, rv + t * 80)  # boost red
        bv = max(0, bv - t * 80)  # reduce bleu
    else:  # cool: more blue less red
        bv = min(255, bv + abs(t) * 80)  # boost bule
        rv = max(0, rv - abs(t) * 80)  # reduce red
    return int(rv), int(gv), int(bv)  # return new rgb

def draw():
    global current_index  # need to modify index
    background(0)  # clear screen

    if images:  # only run if images exist
        img = images[current_index]  # grab curent image
        img.resize(width, height)  # stretch to window
        img.load_pixels()  # unlock pixles
        half_w = width // 2  # half width
        half_h = height // 2  # half hieght

        tinted = create_image(width, height, RGB)  # blank canvas
        tinted.load_pixels()  # unlock it

        temp = remap(mouse_x, 0, width, -100, 100)  # mouse to temp value

        if mode == 1:  # cool mode
            temps = [-25, -50, -75, -100]  # each quadrant colder
        elif mode == 2:  # warm mode
            temps = [25, 50, 75, 100]  # each quadrant warmer
        else:  # combined mode
            temps = [-temp, temp, -temp * 0.5, temp * 0.5]  # mouse controls split

        for y in range(height):  # each row
            for x in range(width):  # each col
                c = img.pixels[y * width + x]  # get pixle
                rv, gv, bv = red(c), green(c), blue(c)  # extract rgb

                if x < half_w and y < half_h:  # top left
                    t = temps[0]
                elif x >= half_w and y < half_h:  # top right
                    t = temps[1]
                elif x < half_w and y >= half_h:  # botom left
                    t = temps[2]
                else:  # bottom right
                    t = temps[3]

                nr, ng, nb = apply_temp(rv, gv, bv, t)  # apply the temp shift
                tinted.pixels[y * width + x] = color(nr, ng, nb)  # write new pixel

        tinted.update_pixels()  # lock pixels in
        image(tinted, 0, 0, width, height)  # draw to screen
        current_index = (current_index + 1) % len(images)  # next iamge

def mouse_pressed():  # runs wen mouse clicked
    global mode  # change the mode
    if mouse_button == LEFT:  # left click
        mode = 1  # cool mode
    elif mouse_button == RIGHT:  # right click
        mode = 2  # warm mode
    elif mouse_button == CENTER:  # middle click
        mode = 3  # combined mode