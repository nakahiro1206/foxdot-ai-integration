from FoxDot import *

Scale.default = "lydian"
Root.default = "E"
Clock.bpm = 120

# Melody
m1 >> pluck(
    [0, 2, 4, 7] + P[0, 1, 0, -1], dur=[1, 1 / 2, 1 / 4, 1 / 4], amp=0.8, oct=5
).every(3, "shuffle")

# Bass
b1 >> bass([0, -2, -3] + var([0, 2, 5], [8, 8, 8]), dur=PDur(3, 8), amp=0.9, oct=3)

# Drums
d1 >> play("x-o-", amp=1).every(4, "stutter", 2)

# Pads/Harmony
p1 >> pads(var([0, 4, 5], 16), dur=[4, 2, 2], amp=0.6, oct=4)

# Effects
Master().hpf = linvar([200, 4000], 16)

Go()
