from FoxDot import *

# Drums: Metallic and heavy pattern
d1 >> play("xox(oxo)", amp=1.2, sample=4)

# Melody: Brass synth with short decay using major pentatonic scale
Scale.default = Scale.majorPentatonic
Root.default = "C#"
m1 >> brass(
    [0, 7, 4, 5, 2], dur=[1 / 4, 1 / 4, 1 / 8, 1 / 8, 1 / 2], amp=0.8, oct=5
).every(3, "stutter", 4, amp=1.5)

# Bass: Saw bass following melody with an offset
b1 >> sawbass(m1.degree - 12, dur=PDur(3, 8), amp=1, oct=3)

# Pad/Harmony: Blip with a long sustaining sound
p1 >> blip(var([0, 5, 7], 8), dur=4, amp=linvar([0.5, 1], 16), oct=4)

Go()
