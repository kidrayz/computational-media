images = []
current_index = 0

def setup():
    size(1920, 1080)
    global images
    folder_path = 'PICTURES'
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            img_path = os.path.join(folder_path, filename)
            images.append(load_image(img_path))
    frame_rate(60)

def draw():
    global current_index
    background(0)
    tint(int(random(255)),int(random(255)),int(random(255)))    
    
    if images:
        image(images[current_index], 0, 0, width, height)
        current_index = (current_index + 1) % len(images)