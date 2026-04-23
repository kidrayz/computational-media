def setup():
    size(800, 600)
    global img
    img = load_image('PICTURES/angry_bird.jpg')  
    no_stroke()
    background(0)

def draw():
    background(0)
 
    image(img, 0, 0, width, height)
    
    fill(255) 
    circle_radius = 10
    if is_mouse_pressed:
   
        ellipse(mouse_x, mouse_y, circle_radius * 2, circle_radius * 2)
    else:

        ellipse(mouse_x, mouse_y, circle_radius * 2, circle_radius * 2)