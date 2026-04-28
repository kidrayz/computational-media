images = []
current_index = 0

def setup():
    size(480, 270)  # smol window
    global images  # use global list
    folder_path = 'PICTURES'  # folder path
    for filename in os.listdir(folder_path):  # loop thru files
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # images only
            img_path = os.path.join(folder_path, filename)  # build path
            images.append(load_image(img_path))  # load and store
    frame_rate(60)  # 60fps

def draw():
    global current_index  # need to modify index
    background(0)  # clear screen

    if images:  # only run if images exist
        img = images[current_index]  # grab current image
        img.resize(width, height)  # stretch to window
        img.load_pixels()  # unlock pixels

        threshold = 30  # edge sensitivity, lower=more edges, higher=less

        for y in range(height):  # each row
            for x in range(width):  # each col
                c = img.pixels[y * width + x]  # get current pixel
                bright = (red(c) + green(c) + blue(c)) / 3  # avg brightness of this pixel

                if x + 1 < width:  # check right neighbor exists
                    cr = img.pixels[y * width + (x + 1)]  # pixel to the right
                    bright_r = (red(cr) + green(cr) + blue(cr)) / 3  # avg brightness of right pixel
                else:
                    bright_r = bright  # no neighbor so no difference

                if y + 1 < height:  # check below neighbor exists
                    cb = img.pixels[(y + 1) * width + x]  # pixel below
                    bright_b = (red(cb) + green(cb) + blue(cb)) / 3  # avg brighntess of below pixel
                else:
                    bright_b = bright  # no neighbor so no diference

                diff_r = abs(bright - bright_r)  # difference with right pixel
                diff_b = abs(bright - bright_b)  # difference with below pixel

                if diff_r > threshold or diff_b > threshold:  # if either diff is big enuf
                    img.pixels[y * width + x] = color(255)  # its an edge, make it white
                else:
                    img.pixels[y * width + x] = color(0)  # not an edge, make it blakc

        img.update_pixels()  # lock pixels back in
        image(img, 0, 0, width, height)  # draw to screen
        current_index = (current_index + 1) % len(images)  # next image