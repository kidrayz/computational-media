images = []  # list of images
current_index = 0  # current image
def setup():
    size(480, 270)  # window size
    global images
    folder_path = 'PICTURES'  # picture folder
    for filename in os.listdir(folder_path):  # loop files
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # image only
            img_path = os.path.join(folder_path, filename)  # full path
            images.append(load_image(img_path))  # load it
    frame_rate(60)  # 60fps
def draw():
    global current_index
    background(0)  # clear screen
    if images:
        img = images[current_index]  # get image
        half_w = width // 2  # half width
        half_h = height // 2  # half height
        tinted = create_image(width, height, RGB)  # blank canvas
        tinted.load_pixels()  # unlock pixels
        img.resize(width, height)  # resize to window
        img.load_pixels()  # read pixels
        r1, g1, b1 = int(random(255)), int(random(255)), int(random(255))  # tint 1
        r2, g2, b2 = int(random(255)), int(random(255)), int(random(255))  # tint 2
        r3, g3, b3 = int(random(255)), int(random(255)), int(random(255))  # tint 3
        r4, g4, b4 = int(random(255)), int(random(255)), int(random(255))  # tint 4
        for y in range(height):  # each row
            for x in range(width):  # each col
                c = img.pixels[y * width + x]  # get pixel
                rv, gv, bv = red(c), green(c), blue(c)  # get rgb
                if x < half_w and y < half_h:  # top left
                    tr, tg, tb = r1, g1, b1
                elif x >= half_w and y < half_h:  # top right
                    tr, tg, tb = r2, g2, b2
                elif x < half_w and y >= half_h:  # bottom left
                    tr, tg, tb = r3, g3, b3
                else:  # bottom right
                    tr, tg, tb = r4, g4, b4
                tinted.pixels[y * width + x] = color(int(rv * tr / 255), int(gv * tg / 255), int(bv * tb / 255))  # apply tint
        tinted.update_pixels()  # lock pixels
        image(tinted, 0, 0, width, height)  # draw it
        current_index = (current_index + 1) % len(images)  # next image