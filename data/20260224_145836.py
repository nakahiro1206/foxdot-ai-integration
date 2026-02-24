from FoxDot import *

Clock.bpm = 90

# Melody with pluck synth
p1 >> pluck([0, 2, 4, 7], 
            dur=[3/4, 1/4, 1], 
            amp=0.7, 
            oct=5
).every(8, "reverse")

# Harmony/Pad with pads synth
p2 >> pads([0, 2, 4, 6] + var([0, 5], 16), 
           dur=4, 
           amp=0.5, 
           oct=4)

# Bass with bass synth, follows Harmony
b1 >> bass(var([0, 3, 4, 5], 8), 
           dur=PDur(3,8), 
           amp=0.6, 
           oct=3
).follow(p2)

# Drums with coffee grinding and brewing sounds
d1 >> play("CGCG", 
           sample=[0, 1], 
           amp=0.9)

# Low-pass filter applied to all
Master().lpf = var([200, 800], 16)

Go()