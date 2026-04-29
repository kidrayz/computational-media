
import numpy as np  # fast array operations

images        = []  # holds all loaded images
current_index = 0  # tracks which image is showing
mode          = 3  # default to combined mode
original      = None  # stores unmodified pixel snapshot


def apply_temp_np(y_sl, x_sl, t):  # applies color temp shift to one quadrant
    factor = t / 100.0  # normalize temp to -1.0 to 1.0 range
    np_pixels[y_sl, x_sl, 1] = np.clip(original[y_sl, x_sl, 1] + factor * 80, 0, 255)  # shift red channel up or down
    np_pixels[y_sl, x_sl, 3] = np.clip(original[y_sl, x_sl, 3] - factor * 80, 0, 255)  # shift blue channel opposite direction


def setup():  # runs once at start
    size(960, 540)  # set window to 960x540
    global images  # allow writing to images list
    folder_path = 'PICTURES'  # name of image folder
    for filename in os.listdir(folder_path):  # loop through every file in folder
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # skip non-image files
            images.append(load_image(os.path.join(folder_path, filename)))  # load image and add to list
    frame_rate(20)  # cap at 60fps


def draw():  # runs every frame
    global current_index, original  # allow modifying index and snapshot

    background(0)  # clear screen to black
    if not images:  # skip everything if no images loaded
        return

    img = images[current_index]  # grab current image from list
    img.resize(width, height)  # stretch image to fill window
    image(img, 0, 0)  # draw image to screen

    load_np_pixels()  # load screen pixels into numpy array
    original = np_pixels.copy()  # save clean copy before tinting

    half_w, half_h = width // 2, height // 2  # compute center point of window

    temp      = remap(mouse_x, 0, width,  -100,  100)  # map mouse x to temperature range
    intensity = remap(mouse_y, 0, height,  0.5,  1.5)  # map mouse y to intensity scale

    if mode == 1:  # cool mode
        temps = [-25, -50, -75, -100]  # fixed cold values per quadrant
    elif mode == 2:  # warm mode
        temps = [ 25,  50,  75,  100]  # fixed warm values per quadrant
    else:  # combined mode
        temps = [-temp, temp, -temp * 0.5, temp * 0.5]  # mouse x drives warm/cool split

    temps = [t * intensity for t in temps]  # scale all temps by mouse y intensity

    quadrants = [  # define four screen regions with their temp values
        (slice(0,      half_h), slice(0,      half_w), temps[0]),  # top-left
        (slice(0,      half_h), slice(half_w, width),  temps[1]),  # top-right
        (slice(half_h, height), slice(0,      half_w), temps[2]),  # bottom-left
        (slice(half_h, height), slice(half_w, width),  temps[3]),  # bottom-right
    ]

    for y_sl, x_sl, t in quadrants:  # iterate over each quadrant
        apply_temp_np(y_sl, x_sl, t)  # apply temperature shift to that region

    update_np_pixels()  # push modified pixel array back to screen

    current_index = (current_index + 1) % len(images)  # advance to next image, wrap around


def mouse_pressed():  # runs on every mouse click
    global mode  # allow changing mode
    if   mouse_button == LEFT:   mode = 1  # left click sets cool mode
    elif mouse_button == RIGHT:  mode = 2  # right click sets warm mode
    elif mouse_button == CENTER: mode = 3  # middle click sets combined mode