from FoxDot import *

Clock.bpm = 100

# Heavy industrial kick and snare with "ratcheting" (parentheses)
d1 >> play("x  x (xo) u ", dur=1 / 2, sample=1, amp=1.5)

# Dirty Trap Hats using brackets for rapid fire
d2 >> play("---[--]-[- - -]", amp=linvar([0.4, 1], 16))

# Industrial 'clank' using the 'm' and 's' samples
d3 >> play("  m   s ", echo=0.5, echotime=1 / 4, room=0.5)

# A dark, chromatic-leaning bassline
b1 >> dbass(
    [0, 0, 1, 0, 4, 3],
    dur=[1, 0.5, 0.5, 1, 0.5, 0.5],
    sus=0.75,
    lpf=linvar([500, 3000], 8),
    room=0.3,
)

# Add a periodic "stutter" for that glitchy industrial feel
b1.every(8, "stutter", 4, oct=3, pan=[-0.8, 0.8])

# Use 'zap' for that sharp, electronic industrial lead
# It has a built-in frequency sweep that sounds like a mechanical "chirp"
p1 >> zap(
    [0, 3, 7, 10],
    dur=PDur(3, 8),
    oct=6,
    amp=0.4,
    dist=0.3,  # Adds clipping distortion
    room=0.5,
)  # Industrial warehouse space

# Let's also beef up the bass with 'prophet' if 'dbass' feels too clean
b1 >> prophet(
    [0, 0, 1, 0, 4, 3],
    dur=[1, 0.5, 0.5, 1, 0.5, 0.5],
    sus=0.75,
    lpf=linvar([400, 2000], 8),
    bits=8,
)  # Lower bit-depth for a 'crunchier' digital grit

Go()
