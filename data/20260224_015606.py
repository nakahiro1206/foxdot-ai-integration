from FoxDot import *

Clock.bpm = 150

# Drums: play with rapid successions and random choices
d1 >> play("x(-o)-{[xo][o-]}-", amp=2).every(8, "shuffle")

# Melody: high-pitched energetic sequence
p1 >> blip(P[0, 2, 4, 5, 7] + PRand(-1, 1), dur=[1 / 2, 1 / 4, 1 / 4], oct=5, amp=0.8)

# Bass: supportive rhythm with varied pitches
b1 >> bass(P[0, 4, 5, 3], dur=PDur(3, 8), amp=1.2, oct=3)

# Effects: popping sounds with random variation
e1 >> play("{p[o-x]}", sample=1, pan=[-1, 1]).every(4, "rotate")

# Pads/Harmony: Minor scale, harmonically supportive
h1 >> pads(P[0, 2, 4, 6] + [0, 5], dur=[2, 2, 1], oct=4, amp=0.5)

Go()
