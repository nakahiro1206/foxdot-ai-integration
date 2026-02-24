from FoxDot import *

# Set the tempo and scale for the composition
Clock.bpm = 80
Scale.default.set("major")
Root.default.set("C")

# Background Pad / Harmony
p1 >> pads([0, 3, 5, 4], dur=[2, 4, 2, 4], amp=0.7, oct=4) + linvar([0, 1], 16)

# Bass
b1 >> bass([0, 3, 5, 4], dur=[4, 4], amp=0.4, oct=3).follow(p1)

# Coffee Grinding Sounds (Percussion)
d1 >> play("g", dur=[0.25, 0.5, 0.75], sample=2, amp=linvar([0.7, 0.5], 8))

# Coffee Brewing Drip Sounds
d2 >> play("d", dur=[1, 0.5, rest(1)], amp=0.6, sample=[1, 2])

# Gentle Ambient Effects
s1 >> sinepad([0, 5], dur=[8], amp=0.3, pan=PWhite(-0.5, 0.5))
s1.every(4, "rotate")

Go()