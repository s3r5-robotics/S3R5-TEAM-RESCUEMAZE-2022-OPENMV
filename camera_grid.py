import sensor, image, time, utime, pyb
from image import SEARCH_EX, SEARCH_DS
from pyb import LED
#i2c_address = 0x54


debug = True

# MATRIXS

# TODO:
# - implement method for sideways letter reco (basically add 4 more dots.
# - fix colour detection
h_matrix = [
    [1, 0, 1],
    [1, 1, 1],
    [1, 0, 1]
]
s_matrix = [
    [1, 1, 1],
    [0, 1, 1],
    [1, 1, 1]
]
u_matrix = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1]
]



#
# Functions for sending binary output to robot
#
# H - 001
# S - 010
# U - 011
# R - 100
# G - 101
# Y - 110
#
def sendH():
    print("H - 1")
    pin1.low()
    pin2.low()
    pin3.high()
def sendS():
    print("S - 2")
    pin1.low()
    pin2.high()
    pin3.low()
def sendU():
    print("U - 3")
    pin1.low()
    pin2.high()
    pin3.high()
def sendR():
    print("R - 4")
    pin1.high()
    pin2.low()
    pin3.low()
def sendG():
    print("G - 5")
    pin1.high()
    pin2.low()
    pin3.high()
def sendY():
    print("Y - 6")
    pin1.high()
    pin2.high()
    pin3.low()


# sets all pins to 0
def allOff():
    pin1.low()
    pin2.low()
    pin3.low()



#
# Sets up the sensor format and settings at start
#
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # 320x240
sensor.set_framerate(120)

#sensor.set_windowing(0, 40, 280, 240)

sensor.skip_frames(time = 1000)
clock = time.clock()

# thresholds for colours
threshold = (40, 255)
thresholds = [(30, 70, 30, 100, 15, 70),# Red
              (35, 60, -80, -40, -30, 70), # Green
              (55, 80, -15, 20, 25, 80)] # Yellow

#            [(36, 52, 46, 39, 52, 45),# Red
 #             ( 13, -15, 12, 21, -20, 17), # Green
  #            (71, -22, 65, 79, -29, 72)] # Yellow
# thresholds for grayscale (black detect)
#thresholdsGS = [(80, 100, 15, 127, 15, 127),
#                (80, 100, -64, -8, -32, 32),
#                (0, 45, 0, 70, -80, -20)]
                #(24, 60, 32, 54, 0, 42)
#thresholdsGS = [(0, 15, 0, -20, -20, -50)]
thresholdsGS = [(-10, -10, -10, -20, -20, -50)]

# LEDS setup and turn them all on for better lighting
white_led = LED(3)
da_led = LED(2)
red_led = LED(1)
IR_LED = LED(4)

#IR_LED.on()

colorMode = True
utime.sleep_ms(100)
times = 0





def count_squre(blob):
    dots = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    rad = 3

    x = blob.x()
    y = blob.y()


    if debug:

        # TOP
        img.draw_circle(x + int(blob.w() / 7),y + int(blob.h() / 6), 3, color=(255,0,0))
        img.draw_circle(blob.cx(),y + int(blob.h() / 16), 3, color=(255,0,0))
        img.draw_circle(x+blob.w() - int(blob.w() / 7) ,y + int(blob.h() / 6), 3, color=(255,0,0))


        # MID
        img.draw_circle(x + int(blob.w() / 6),blob.cy(), 3, color=(255,0,0))
        img.draw_circle(blob.cx() , blob.cy(), 3, color=(255,0,0))
        img.draw_circle(x+blob.w() - int(blob.w() / 6) ,blob.cy(), 3, color=(255,0,0))


        # BOTTOM
        img.draw_circle(x + int(blob.w() / 7),y + blob.h() - int(blob.h()/6), 3, color=(255,0,0))
        img.draw_circle(blob.cx() ,y + blob.h() - int(blob.h() / 16), 3, color=(255,0,0))
        img.draw_circle(x+blob.w() - int(blob.w() / 7) ,y + blob.h() - int(blob.h()/6), 3, color=(255,0,0))



        # TODO
        # extra 4 dots for sideways detection
        img.draw_circle(x + int(blob.w()/16), blob.cy(), 3, color=(255,0,0))
        img.draw_circle(x + blob.w() - int(blob.w()/16), blob.cy(), 3, color=(255,0,0))



    left_top = img.get_pixel(x + int(blob.w() / 7),y + int(blob.h() / 6)) == (0, 0, 0)
    mid_top = img.get_pixel(blob.cx(),y + int(blob.h() / 16)) == (0, 0, 0)
    right_top = img.get_pixel(x+blob.w() - int(blob.w() / 7) ,y + int(blob.h() / 6)) == (0, 0, 0)

    left_mid = img.get_pixel(x + int(blob.w() / 6),blob.cy()) == (0, 0, 0)
    mid_mid = img.get_pixel(blob.cx() , blob.cy()) == (0, 0, 0)
    right_mid = img.get_pixel(blob.cx() , blob.cy()) == (0, 0, 0)

    left_bottom = img.get_pixel(x + int(blob.w() / 7),y + blob.h() - int(blob.h()/6)) == (0, 0, 0)
    mid_bottom = img.get_pixel(blob.cx() ,y + blob.h() - int(blob.h() / 16)) == (0, 0, 0)
    right_bottom = img.get_pixel(x+blob.w() - int(blob.w() / 7) ,y + blob.h() - int(blob.h()/6)) == (0, 0, 0)


    dots = [
        [left_top, mid_top, right_top],
        [left_mid, mid_mid, right_mid],
        [left_bottom, mid_bottom, right_bottom]

    ]

    #print(img.get_pixel(blob.cx(),y + int(blob.h() / 16)))
    #print(dots)
    return dots


def getHSU(blob):
    data = count_squre(blob)
    #print(data)
    reading = [
        data == h_matrix,
        data == s_matrix,
        data == u_matrix
    ]

    print(reading)
    return reading




# detects letters using 9 dot grid array
def detectHSU(blob):
    data = getHSU(blob)
    if data[0]:
        sendH()
        return True
    elif data[1]:
        sendS()
        return True
    elif data[2]:
        sendU()
        return True
    return False




pin1 = pyb.Pin("P7", pyb.Pin.OUT_PP)
pin2 = pyb.Pin("P8", pyb.Pin.OUT_PP)
pin3 = pyb.Pin("P9", pyb.Pin.OUT_PP)
pin1.low()
pin2.low()
pin3.low()


# main loop
while(True):
    clock.tick()
    sensor.set_hmirror(True)
    sensor.set_transpose(True)
    detected = False
    if not colorMode:
        img = sensor.snapshot()
        img.lens_corr(2.2, 1.0)

        img.binary([threshold])
        for blob in img.find_blobs([(0, 1)], pixels_threshold=320, area_threshold=400):
            #print("OK")

            width_ = blob.w()
            height_ = blob.h()

            if width_ > img.width()/1.1:
                continue
            #print("found")


            if (blob.x() + blob.h()) > ( img.height()/3*2):
                continue

            if blob.perimeter() > 850 or (height_ > (3 * width_)) or width_ < img.width()/3:
                #print("Not letter")
                #break
                continue
            if width_ < 80 or height_ < 80:
                #print("premalo")
                continue
            detected = detectHSU(blob)

            if debug:
                if detected:
                    img.draw_rectangle(blob.rect(), color=(255,0,0))
                else:
                    img.draw_rectangle(blob.rect(), color=(0,255,0))
    else:
        img = sensor.snapshot()

        for blob in img.find_blobs([thresholds[0]], pixels_threshold=200, area_treshold=200, merge=True):
            #if ( (blob.y() + blob.h()) > ( (img.height()/3) * 2 ) ): continue # JUST A HEIGHT LIMIT
            if debug: img.draw_rectangle(blob.rect(), color=(255,0,0))
            detected=True
            sendR()
        for blob in img.find_blobs([thresholds[1]], pixels_threshold=200, area_treshold=200, merge=True):
            #if ( (blob.y() + blob.h()) > ( (img.height()/3) * 2 ) ): continue # JUST A HEIGHT LIMIT
            if debug: img.draw_rectangle(blob.rect(), color=(0,255,0))
            detected=True
            sendG()
        for blob in img.find_blobs([thresholds[2]], pixels_threshold=200, area_treshold=400, merge=True):
            #if ( (blob.y() + blob.h()) > ( (img.height()/3) * 2 ) ): continue # JUST A HEIGHT LIMIT
            height = blob.w() + blob.x()
            #print("H ",height, "|", ((img.height()/3)*2.5))

            if debug: img.draw_rectangle(blob.rect(), color=(255,255,100))
            detected=True
            sendY()
    #colorMode = not colorMode # basically switches from colour to grayscale and so on
    if not detected:
        allOff()
    else:
        white_led.on()
        da_led.on()
        red_led.on()
        utime.sleep_ms(300)
        white_led.off()
        da_led.off()
        red_led.off()
    #print(clock.fps())
