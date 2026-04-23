def setup():
  size(400, 400)
  img = load_image('PICTURES/sleketon.jpg')
  no_stroke()
  tint(255,0,0)  
  image(img, 0, 0, width, height)

