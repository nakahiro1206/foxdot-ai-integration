from FoxDot import *


# Melody
p1 >> pluck([0, 2, 4, 5, 4, 2], dur=[1, 1 / 2, 1, rest(1 / 2)], amp=0.6, oct=4)

# Bass
b1 >> bass([0, -1, -2, -1], dur=[1, 1, 1 / 2, 1 / 2], amp=0.5, oct=3)

# Drums
d1 >> play("---(-=)", amp=0.3)

# Pads / Harmony
p2 >> pads([(0, 2, 4), (5, 7, 9)], dur=[2, 2], oct=5, pan=[-0.2, 0.2])

# Effects on Melody and Pads
p1.hpf = linvar([500, 1000], 16)
p2.hpf = linvar([500, 1000], 16)

# Time-Varying Changes
p2 >> pads(var([0, 2, 4, 5], 8), dur=8)
p1.every(8, "rotate")


# Heavy Bass Element
b2 >> sawbass(
    [0, 0, rest(1)],  # Emphasizes the root note, with silence on the third beat
    dur=[1, 1, rest(1)],  # Basic pulse-like pattern emphasizing the downbeats
    amp=0.8,  # Higher amplitude for emphasis
    oct=2,  # Set octave to 2 for deep bass tones
    hpf=linvar([300, 600], 8),  # Subtle filter sweep effect for dynamic sound texture
)

Go()
