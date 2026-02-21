from FoxDot import *

# Effect: sets a fast hyperpop tempo, minor key, sad chord loop, and a rhythmic “pump” + short breakdown every 32 beats.
# WIDE, CHOPPED PAD CHORDS (sad + glossy)

Clock.bpm = 172

Root.default.set("E")
Scale.default = "minor"

# i – VI – III – VII (melancholic-pop staple)
var.ch = var([0, 5, 2, 6], [8, 8, 8, 8])

# “sidechain-ish” pump + section pulsing (drops energy every 32 beats)
var.pump = var([1, 0.25], [3, 1])
var.drop = var([1, 0], [28, 4])

# Effect:
# p1 gives emotional harmony + rhythmic gating (chop) + stereo drift (pan).
# b1 anchors the progression with a pumping, slightly distorted low end.
# p2 is the main hook (sparkly pluck + delay smear).
# ar adds “hyperpop sugar” on top (bright, fast, wide).
# DRUMS: tight, pop-forward, glitch-capable grid

p1 >> pads(
    var.ch + (0, 2, 4, 6),
    dur=4,
    sus=3.7,
    amp=0.55 * var.pump * var.drop,
    chop=var([0, 4, 8], [12, 2, 2]),
    pan=linvar([-0.7, 0.7], 16),
    room=0.85,
    mix=0.35,
)

# SUB/BASS THAT FOLLOWS THE CHORD ROOTS (pumping + filtered)
b1 >> bass(
    var.ch,
    dur=PDur(5, 8),
    oct=3,
    amp=0.8 * var.pump * var.drop,
    lpf=linvar([500, 1800], 16),
    dist=0.12,
)

# SPARKLY LEAD (hyperpop sparkle + occasional slide)
p2 >> pluck(
    var.ch + P[0, 2, 4, 7].rotate(1),
    dur=PDur(3, 8),
    oct=6,
    amp=0.42 * var.drop,
    chop=var([0, 0, 4], [12, 2, 2]),
    echo=0.35,
    echotime=3,
    pan=PWhite(-0.8, 0.8),
    room=0.7,
    mix=0.25,
)

# GLASSY 1/8 ARP “SUGAR” LAYER (very bright, very small)
ar >> blip(
    var.ch + P[0, 2, 4, 6].stutter(2),
    dur=1 / 8,
    oct=7,
    amp=0.18 * var.drop,
    hpf=2200,
    echo=0.25,
    echotime=2,
    pan=PWhite(-1, 1),
)

# Effect: kick/snare/clap sit in a clean pop pocket; hats brighten over 16 beats; fx layers little ear-candy (crash/vocal-ish/noise-ish depending on your sample set).

bd >> play("X   X   X   X   ", dur=1 / 4, amp=1.35 * var.drop)
sn >> play("    o       o   ", dur=1 / 4, amp=0.95 * var.drop, room=0.3, mix=0.08)
hh >> play(
    "-=-=--=-=--=-=-=", dur=1 / 4, amp=0.40 * var.drop, hpf=linvar([3500, 9000], 16)
)
cp >> play("    *       *   ", dur=1 / 4, amp=0.55 * var.drop, hpf=3000)

# GLITCH FILLER (comes alive on transforms)
fx >> play(
    "<  # ><  V >< [--] ><  ~ >",
    dur=1 / 2,
    amp=0.22 * var.drop,
    hpf=2000,
    pan=PWhite(-1, 1),
)

# Effect: periodic glitch edits without you doing anything—lead stutters into tiny bursts, arp reverses for shimmer, hats shuffle for movement, FX stutters for fills.

# AUTOMATION: “hyperpop edits” (stutters + reverses) on a musical schedule
p2.every(8, "stutter", 4, dur=1 / 16, pan=[-1, 1])
ar.every(16, "reverse")
hh.every(8, "shuffle")

fx.every(8, "stutter", 2, dur=1 / 8, pan=[-1, 1])

# # Quick mood knobs (run any of these live)
# # Sadder / more “late-night”: slower + longer chords
# Clock.bpm = 160
# p1.sus = 4.2
# # More hyperpop / more “chopped”: harder gating everywhere
# p1.chop = 8
# p2.chop = 8
# # Bigger drop: longer breakdown every 32 beats
# var.drop = var([1, 0], [24, 8])

Go()
