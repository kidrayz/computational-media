import py5_tools

def setup():
    size(500,500)

run_sketch(block=False)
# create a 10 frame animated GIF saved to '/tmp/animated.gif'
py5_tools.animated_gif('PICTURES/walahi.gif', count=10, period=1, duration=0.5)