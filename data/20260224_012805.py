from FoxDot import *

p1 >> pluck(P[8, 7, 5, 3, 0], dur=[1, 0.5, 1.5, 1], amp=0.6, oct=4, scale=Scale.minor)

b1 >> bass(P[0, -2, -3], dur=[1, 1, 2], slidefrom=-2, oct=3)

d1 >> play("x  ", amp=0.5, sample=2)

p2 >> pads(P(0, 4, 7), dur=[4, 4], sus=4, pan=(-1, 1), amp=0.5, scale=Scale.minor)

d2 >> play("H", sample=5, dur=8, amp=2).every(32, "stutter", 4)

b1.follow(p1.root)

p2.follow(p1)

Go()
