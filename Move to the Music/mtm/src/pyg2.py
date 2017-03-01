HIT_TOL = 0.200
BEAT_TOL = 0.033

DoClap = False

import sys
import os
import pygame
music = pygame.mixer.music
from bisect import bisect

pygame.mixer.pre_init(44100,-16,2,1024*2)
pygame.init()


songfile = r'E:\eclipse\workspace3.3\mtm\songs\MissYou.wav'
timefile = r'E:\eclipse\workspace3.3\mtm\beats\MissYou.times'

music.load(songfile)
#clap = pygame.mixer.Sound(r'E:\eclipse\workspace3.3\mtm\src\Utils\soundeffects\clap.wav')

times = [ float(t.strip()) for t in file(timefile, 'rt') ]
def GetDelta(t):
    n = bisect(times, t)
    d1 = t - times[n-1]
    d2 = times[n] - t
    if d1 < d2:
        return -d1
    else:
        return d2

size = width, height = 320, 240
origin = height/2
scale = height/2
bar_w = 16
bar_n = width/bar_w

screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except pygame.error:
    pass

music.play()

errors = []

run = True
while run:
    t = music.get_pos() * 0.001
    dt = GetDelta(t)
    hit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            f = max(-1, min(1, (dt / HIT_TOL)))
            hit = abs(f) < 0.5
            errors.append(f)
        if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            f = max(-1, min(1, (dt / HIT_TOL)))
            hit = abs(f) < 0.5
            errors.append(f)
    else:
        pygame.time.wait(2)

    if hit and DoClap:
        c = clap.play()
        #c.Volume = (1 - abs(f)) * 100
        pass

    if abs(dt) < BEAT_TOL:
        screen.fill((255,255,255))
    else:
        screen.fill((0,0,0))
    for i,f in enumerate(errors[-bar_n:]):
        x1 = i*bar_w
        w = bar_w
        if f < 0:
            y1 = origin + f * scale
        else:
            y1 = origin
        h = abs(f) * scale
        if f < 0:
            c = (255,0,0)
        else:
            c = (0,255,0)
        screen.fill(c, pygame.Rect(x1, y1, w, h))
    pygame.display.flip()

print 'exiting'
