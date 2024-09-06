import numpy as np
import pygame as pg
import sys, os
#import tkinter
import tkinter.filedialog

#pygame setup
pg.init()
pg.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0,0)
successes, failures = pg.init()
width, height = 800, 800
pg.display.set_caption("Orbital Instrument")
font = pg.font.SysFont('Arial', 30)
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()
FPS = 60

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

def vecComponent(vec1, vec2):
    theta = np.arctan((vec2[1]-vec1[1]) / (vec2[0] - vec1[0]))
    if vec2[0] < vec1[0]: theta += np.pi

    return np.array([np.cos(theta), np.sin(theta)])

class body:
    def __init__(self, r: float, vel: float, name: str, file: str, col: tuple[int]):
        self.r = r
        self.pos = np.array([width/2 + r, height/2])
        self.vel = np.array([0, vel])
        self.col = col
        self.name = name
        if name == '':
           pass
        else:
            self.sound = pg.mixer.Sound(file)
    def play(self):
        self.sound.play()


#              r, vel, name, file,                                       col

bodys = [body(150.0, 10, 'kd', 'BVKER - 909 Kit - Kick 21.wav', (255, 0,0)),
         body(200.0, 10, 'sd', 'BVKER - 909 Kit - Snare 09.wav', (0, 255,0)),
         body(100.0, 10, 'cl', 'BVKER - 909 Kit - Clap 03.wav', (0, 0,255)),
         ]

#bodys = []

lineCol = [0, 0, 0]
#filename = None

while True:
    screen.fill((0, 0, 0))
    #pg update
    cursor = pg.mouse.get_pos()
    base, v = cursor[0] - width/2, (cursor[1] - height/2) /10

    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit(0)
        elif event.type == pg.MOUSEBUTTONUP:
            filename = prompt_file()
            try:
                bodys.append(body(base, v, filename.split(' ')[-2], filename, (np.random.randint(100, 255), np.random.randint(100, 255), np.random.randint(100, 255))))
            except:
                pass

    #Interface visualization
    if cursor[0] < width/2:
        pass
    else:
        pg.draw.line(screen, (255, 255, 255), [cursor[0],height/2], cursor)
        screen.blit(font.render('v='+str(v),True, (255, 255, 255)), (cursor+np.array([0, 0])))
    
    #col decay
    for i in range(3):
        lineCol[i] -= 10
        if lineCol[i] < 0: lineCol[i] = 0
        

    for mainSat in bodys:
        trigger = False

        #dynamics
        accMag = (mainSat.vel[0]**2 + mainSat.vel[1]**2)/ mainSat.r
        mainSat.vel = np.add(mainSat.vel, accMag*vecComponent(mainSat.pos, np.array([width/2, height/2])))
        #trigger check
        if mainSat.pos[1] < height/2 < mainSat.pos[1] + mainSat.vel[1] or mainSat.pos[1] > height/2 > mainSat.pos[1] + mainSat.vel[1]:
            trigger = True
        #pos update
        mainSat.pos = np.add(mainSat.pos, mainSat.vel)
        #draw & tag masses
        pg.draw.circle(screen, mainSat.col, mainSat.pos, 20)
        screen.blit(font.render(mainSat.name,True, (255, 255, 255)), (mainSat.pos+np.array([-15, -20])))

        #trigger
        if trigger:
            #animation color
            for i in range(3):
                lineCol[i] += mainSat.col[i]
                if lineCol[i] > 255: lineCol[i] = 255        
            #play
            mainSat.play()

    #trigger animation
    pg.draw.circle(screen, lineCol, (width/2, height/2), 40)
    pg.draw.line(screen, lineCol, (0, height/2),  (width, height/2), 4)
    for i in range(0, width, 100):
        pg.draw.line(screen, lineCol, (i, height/2 - 50), (i, height/2 + 50), 2)
    pg.draw.line(screen, lineCol, (799, height/2 - 50), (799, height/2 + 50), 2)

    pg.display.update()

    #add grid