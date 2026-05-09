from FoxDot import *

Clock.clear()
Clock.bpm = 92

Scale.default = "minor"
Root.default = 0

var.chords = var([0, 5, 3, 4], [8, 8, 8, 8])
var.bassline = var([0, -2, -1, -3], [16, 8, 8, 16])

p1 >> pads(
    var.chords + P[(0, 2, 4), (2, 4, 6), (0, 3, 5), (1, 3, 5)],
    dur=4,
    sus=6,
    amp=0.7,
    room=0.8,
    mix=0.35,
    chop=0,
    lpf=linvar([900, 2200], 32),
)

p2 >> pluck(
    P[var.chords, var.chords + 2, var.chords + 4, var.chords + 7].rotate(1),
    dur=[1 / 2, 1 / 2, 1, 1 / 2, 1 / 2, 1, 2],
    oct=[5, 5, 6, 5],
    amp=linvar([0.35, 0.6], 16),
    pan=PSine(16),
    room=0.6,
    mix=0.25,
    blur=1.2,
)

p3 >> bell(
    P[var.chords + (0, 2, 4), var.chords + (2, 4, 6)],
    dur=8,
    sus=6,
    oct=6,
    amp=0.28,
    pan=[-0.7, 0.7],
    room=0.9,
    mix=0.4,
)

b1 >> bass(
    var.chords + var.bassline,
    dur=PDur(3, 8),
    oct=4,
    amp=0.55,
    lpf=900,
    room=0.2,
    mix=0.1,
)

d1 >> play(
    "<x   ><  o >< -[-] ><   s>",
    dur=1,
    amp=var([0, 0.45], [[32, 64], [64, 32]]),
    room=0.35,
    mix=0.12,
)

d2 >> play(
    "  * [--]  *   [-*]",
    dur=1 / 2,
    amp=0.22,
    pan=[-0.4, 0.4],
    room=0.5,
    mix=0.2,
    sample=2,
)

d3 >> play(
    "{~   }   { - }   ",
    dur=1 / 2,
    amp=0.16 * var([0, 1], [16, 32]),
    pan=PWhite(-0.8, 0.8),
    room=0.7,
    mix=0.3,
)

s1 >> swell(
    var.chords + PWalk(5),
    dur=8,
    sus=7,
    oct=var([5, 6], [24, 8]),
    amp=0.18,
    pan=linvar([-1, 1], 24),
    room=0.95,
    mix=0.45,
    hpf=linvar([0, 800], 32),
)

# Then add gentle movement:
p2.every(8, "rotate")
p2.every(16, "shuffle")
d2.every(8, "stutter", 2, pan=[-1, 1], amp=0.18)
s1.every(32, "reverse")

# For a more dreamy and emotional version, re-run these exact lines:
Scale.default = "minorPentatonic"

p1.lpf = linvar([700, 1800], 48)
p1.amp = 0.85

p2.blur = 1.8
p2.room = 0.8
p2.mix = 0.35

b1.amp = 0.42

d1.amp = 0.25
d2.amp = 0.12
d3.amp = 0.1

# For a more luxurious, elegant climax, run:
p3.amp = 0.4
s1.amp = 0.26

p1 >> pads(
    var.chords + P[(0, 2, 4, 6), (2, 4, 6, 8), (0, 3, 5, 7), (1, 3, 5, 6)],
    dur=4,
    sus=7,
    amp=0.75,
    room=0.9,
    mix=0.4,
    lpf=linvar([1200, 2600], 32),
)

Go()
