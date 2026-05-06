def apply_effect():
    global original
    # 3D array (y, x, color); color->[Alpha,red,green,blue]
    A,r,g,b = 0,1,2,3 # unpack variables for the color indices
    np_pixels[:, :, r] = 255 - np.clip(original[:, :, r], 0, 255)
    np_pixels[:, :, g] = 255 - np.clip(original[:, :, g], 0, 255)
    np_pixels[:, :, b] = 255 - np.clip(original[:, :, b], 0, 255)
    update_np_pixels()


def setup():
    global original
    size(700,500)
    img = load_image("PICTURES/patrickgiggleshits.jpg")
    img.resize(width, height)
    image(img, 0, 0)
    load_np_pixels()
    original = np_pixels.copy()
    
def draw():
    apply_effect()

