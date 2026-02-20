from FoxDot import *

# --- Global setup ---
Clock.bpm = 160
Scale.default = "minor"
Root.default = "A"

# --- Song structure (beats) ---
# 32-beat phrases:  A (full) -> B (break) -> A (full) -> C (build) -> A (full)
var.section = var([1, 0.6, 1, 0.8, 1], [32, 32, 32, 32, 64])

# Chord progression (degrees in the current scale)
var.chords = var([0, 5, 3, 4], [8, 8, 8, 8])  # i - VI - iv - v (minor vibe)

# Filter sweeps synced to phrase boundaries
lpf_sweep = linvar([600, 6000], [32, 32], start=Clock.mod(32))
hpf_sweep = linvar([0, 1200], [64, inf], start=Clock.mod(64))


# --- DRUMS ---
# Kick
d1 >> play("X... X... X... X...", amp=0.9 * var.section)

# Snare / clap (backbeat)
d2 >> play("..o. ..o. ..o. ..o.", amp=0.7 * var.section, room=0.2, mix=0.2)

# Closed hats (drive the groove)
d3 >> play("----[--]----[--]", dur=1 / 2, amp=0.35 * var.section, hpf=1200)

# Open hat / accent (variation with braces)
d4 >> play(
    "..{. .}..{. .}", dur=1 / 2, amp=0.25 * var.section, hpf=2000, room=0.3, mix=0.2
)

# Perc layer (ghost hits + shuffle feel)
d5 >> play(
    "..t.[tt]..t.[tt]", dur=1 / 2, amp=0.22 * var.section, pan=[-0.6, 0.6], hpf=1800
)

# Some performance spice
d3.every(8, "shuffle")
d5.every(16, "stutter", 2, dur=1 / 4, amp=0.18, pan=[-1, 1])


# --- BASS ---
# Tight bass with Euclidean rhythm
b1 >> bass(
    var.chords,
    dur=PDur(3, 8),
    oct=3,
    amp=0.85 * var.section,
    lpf=linvar([500, 1400], [16, 16], start=Clock.mod(16)),
    drive=0.08,
)

# Occasional bass movement
b1.every(8, "rotate", 1)
b1.every(16, "stutter", 2, dur=1 / 4, oct=4, amp=0.6)


# --- PADS / ATMOS ---
# Wide pads following chords
p1 >> pads(
    var.chords + (0, 2, 4),
    dur=4,
    sus=3.8,
    oct=5,
    amp=0.35 * var.section,
    room=0.6,
    mix=0.25,
    lpf=lpf_sweep,
    hpf=hpf_sweep,
)

# Slow texture / air
p2 >> star(
    var.chords + P[0, 2, 4].rotate(1),
    dur=2,
    sus=1.8,
    oct=6,
    amp=0.18 * var.section,
    room=0.7,
    mix=0.35,
    hpf=1800,
)


# --- ARP / LEAD ---
# Arp locked to chords, evolving with Pattern ops
p3 >> pluck(
    (var.chords + P[0, 2, 4, 7]).rotate(1),
    dur=1 / 4,
    oct=5,
    amp=0.22 * var.section,
    pan=PSine(16),
    lpf=linvar([800, 3500], [32, 32], start=Clock.mod(32)),
    delay=0.25,
    room=0.3,
    mix=0.2,
)

p3.every(8, "reverse")
p3.every(16, "stutter", 4, dur=1 / 8, amp=0.18)

# Simple top-line hook (comes and goes with section)
p4 >> prophet(
    var.chords + PWalk(max=7, step=1, start=0),
    dur=PDur(5, 16),
    oct=6,
    amp=0.16 * var.section,
    vib=0.2,
    slide=0.1,
    room=0.5,
    mix=0.25,
    hpf=1200,
)


# --- QUICK PERFORMANCE CONTROLS (run live) ---
# 1) breakdown: mute kick + bass for 32 beats
# d1.stop(); b1.stop()

# 2) drop hats for 16 beats then bring back
# d3.stop(); d4.stop()

# 3) instant “bigger” chorus
# p1.amp = 0.5; p3.amp = 0.28

# 4) full stop
# Clock.clear()

Go()
