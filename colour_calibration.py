# Untitled - By: Gasper - pet. jul. 15 2022

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    # GETTING COLOURS
    cx = int( img.width()/2 )
    cy = int( img.height()/2 )

    pixel = img.get_pixel(cx, cy)
    img.draw_circle(cx, cy,5, color=(255,0,0))

    # yellow. (170, 185, 41) - (181, 210, 41)
    # red. (165, 32, 8) - (173, 40, 16)
    # green. (16, 40, 16) - (24, 56, 24)

    # lab yellow: (71, -22, 65) - ( 79, -29, 72)
    # lab red: (36, 52, 46) - (39, 52, 45)
    # lab green: ( 13, -15, 12) - (21, -20, 17)


    print(pixel)
