from FoxDot import *

# Set global tempo
Clock.bpm = 60

# Melody
m1 >> pluck([0, -2, -4, -5], dur=[2, 4], amp=0.7, oct=5, scale=Scale.minor, root="A")

# Bass
b1 >> bass([0], dur=[4], amp=0.5, oct=4, scale=Scale.minor, root="A").follow(m1)

# Drums/Rain Effect
d1 >> play("| | x | | x | | | x |", sample=(0, 2, 3))

# Pads/Harmony
p1 >> pads([0, 2, 4], dur=[8], amp=0.4, oct=3, scale=Scale.minor, root="A")

# Effects
m1.every(8, "reverse")
b1.every(8, "reverse")

Master().hpf = linvar([300, 3000], 16)
Master().lpf = linvar([4000, 500], 32)
Master().room = linvar([0.2, 0.6], 16)
Master().mix = linvar([0.1, 0.4], 8)

Go()
