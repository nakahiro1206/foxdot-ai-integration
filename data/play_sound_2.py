from FoxDot import *

# --- GLOBAL SETTINGS ---
Clock.bpm = 145
Root.default = "Eb"
Scale.default = "minor"

# --- RHYTHM & PERCUSSION (d1) ---
# High-intensity industrial drumming using < > to layer
# x: heavy kick, o: snare, -: high-hats, =: alternating sample
d1 >> play(
    "<x( x)><  o ><----(-=)>",
    amp=1.5,
    distort=0.2,
    hpf=linvar([0, 3000], [32, inf], start=Clock.mod(32)),
)

# --- BASS (b1) ---
# Using PDur(3,8) for a galloping rhythmic feel
# bass() synth with distort and low-pass filter (lpf)
b1 >> bass(PRange(4).amen(), dur=PDur(3, 8), oct=4, distort=0.4, lpf=500)

# --- LEAD MELODY (p1) ---
# Sawtooth wave with rhythmic stuttering and stereo panning
p1 >> saw([0, 4, 7, 11], dur=1 / 4, sus=0.2, echo=0.25, pan=[-1, 1])

# Periodic transformations for chaotic texture
p1.every(8, "stutter", 4, oct=6, pan=[-1, 1])
p1.every(12, "shuffle")

# --- ATMOSPHERIC STABS (s1) ---
# Power chords (0,7) to fill the harmonic space
s1 >> pluck([(0, 7), (3, 10), (5, 12)], dur=4, delay=0.5, room=0.7, mix=0.5, amp=0.8)

# --- MASTER FX ---
# Run this to clear all if it gets too loud!
# Clock.clear()

Go()
