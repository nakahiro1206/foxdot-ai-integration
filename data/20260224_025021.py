from FoxDot import *

# Melody
p1 >> pluck([0, 2, 4, 5, 7, 9, 11], dur=[1/2, 1/4, 1/4], oct=5, amp=0.7)

# Bass
b1 >> bass([-2, 0, 3, 0], dur=[1, 1/2, rest(1)], oct=3).every(8, "stutter", 4)

# Drums
d1 >> play("x-o{-o}z", amp=1.2)

# Pads/Harmony
p2 >> pads(var([0, 4, 5, 3], 8), dur=[4], amp=linvar([0.5, 0.8], 16), pan=[-1, 1]).every(16, "reverse")

# Effects
d_all.hpf = var([0, 3000], [28, 4])

Clock.bpm = 120

Go()