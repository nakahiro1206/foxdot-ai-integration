# Global Setup
Clock.clear()
Clock.bpm = 140
Scale.default = "minor"
Root.default = "G#"

# Define harmonic variable
var.chords = var([0, 5, 4, 3], 8)

# Harmony Layer
p1 >> pads(var.chords, sus=4, room=0.7, mix=0.3,
           amp=linvar([0.1, 0.3], 32)).every(8, "rotate")

p2 >> pluck(PWalk() + var.chords, dur=1/4,
            amp=linvar([0, 0.2], 32))

p3 >> bell(var.chords + P*(0, 2, 4), dur=4, room=0.5, mix=0.2,
           amp=0)

# Bass Layer
b1 >> bass(var.chords + var([0, -2], 8), 
           dur=PDur(3, 8), 
           amp=linvar([0.2, 0.5], 16), 
           lpf=500, lpr=0.4, 
           room=0.2, 
           glide=[2])

# Drums Layer
d1 >> play("x   ", amp=linvar([0.4, 0.6], 32), room=0.5, mix=0.4)
d2 >> play("---", amp=0.3 * linvar([0.3, 0.5], 32), room=0.5, mix=0.4)
d3 >> play("  o ", amp=0.3, room=0.5, mix=0.4)

# Texture Layer
s1 >> swell(dur=4, amp=linvar([0.05, 0.1], 16), room=0.8, mix=0.2).every(8, "reverse")
s2 >> play(" s n ", dur=1/2, echo=1, echotime=4, lpf=expvar([200, 800], 8), amp=0.15)

# Define section transitions
def section_build(n=0):
    # Harmony
    p1 >> pads(var.chords, sus=4, amp=0.8)  
    p2 >> pluck(PxRand([0, 2, 4, 5]) + var.chords, dur=1/4,
                bend=expvar([0, 2], 16),
                amp=0.6).every(8, "shuffle")
    p3 >> bell(var.chords + P^(-2, 0, 3, step=0.1), dur=1,
               amp=linvar([0, 0.5], 16))

    # Bass
    b1 >> bass(var.chords + var([-3, 0], 16), 
               dur=PDur(4, 8), 
               lpf=600, 
               room=0.15, 
               oct=var([3, 4], 16), 
               glide=[1, 0], 
               amp=expvar([0.4, 0.8], 16)).every(8, "shuffle")

    # Drums
    d1 >> play("x-o-<x  >", amp=var([0.6, 0.8], 16), delay=(0, 0.1))
    d2 >> play("---(-=)", amp=0.5 * var([0.3, 0.5], 16), delay=[0, 0.05])
    d3 >> play("--**--", amp=0.4, sample=2)

    # Texture
    s1 >> pads(dur=4, amp=linvar([0.1, 0.2], 16), hpf=linvar([200, 800], 16), pan=PSine().norm())
    s2 >> play("x-o-  ", echo=1, echotime=4, pshift=expvar([0, 2], 8), amp=0.2).every(16, "shuffle")

    Clock.future(64, section_dense_wave, args=(0,))

def section_dense_wave(n=0):
    # Harmony
    p1 >> pads(var.chords, sus=2,
               amp=0.9).every(4, "stutter", 4)
    p2 >> pluck(PxRand([2, 3, 5, 7]) + var.chords, dur=PDur(3, 8),
                bend=expvar([2, 0], 8),
                amp=0.7)
    p3.amplify = var([1, 0.3], 4)

    # Bass
    b1 >> bass(var.chords + var([-5, -2, 0, 3], 8), 
               dur=PDur(5, 8), 
               lpf=var([400, 800], 8), 
               amp=0.8).every(4, "stutter", 3, dur=Cycle([1/3]))

    # Drums
    d1 >> play("XxXxXxXx", amp=var([0.7, 1], 8), delay=0.05)
    d2 >> play("<[--]><-x[--]>", amp=0.8 * var([0.5, 0.7], 8))
    d3 >> play("|*|*|*|*|", amp=0.6 * var([0.4, 0.6], 8), sample=3)

    # Texture
    s1 >> loop("ambient", dur=8, amp=expvar([0.15, 0.25], 8), pan=PSine().norm(), room=0.6, mix=0.3)
    s2 >> play("{fxyyc}", echo=2, echotime=2, amp=0.25, pshift=expvar([-0.5, 0.5], 8))

    Clock.future(32, section_sparse_wave, args=(0,))

def section_sparse_wave(n=0):
    # Harmony - Invoke temporal recursion for evolving sparse wave
    if n == 0:
        p1 >> pads((0, 4), sus=4, amp=linvar([0.5, 0.25], 16))
    elif n == 4:
        p2 >> pluck(p1.pitch.accompany([0, 3]), dur=PDur(5, 8))
    elif n == 8:
        p3 >> bell(p1.pitch + (0, 2), dur=8)
    Clock.future(8, section_sparse_wave, args=(n + 1,))

    # Bass
    b1 >> bass(var.chords.accompany([0, -2, -1, 2]), 
               dur=PDur(3, 8), 
               lpf=700, 
               oct=var([3, 4], 8), 
               amp=linvar([0.5, 0.3], 8))

    # Drums
    d1 >> play("x   x  ", amp=linvar([0.5, 0.6], 16))
    d2 >> play("- -(--)", amp=0.4 * linvar([0.2, 0.4], 16))
    d3 >> play("  o(o o )", amp=0.3, sample=4)

    # Texture
    s1 >> pads(amp=linvar([0.05, 0.1], 8), dur=8, room=0.5, mix=0.3).every(8, "shuffle")
    s2 >> play(" ethh", dur=1/4, hpf=linvar([200, 600], 4), amp=0.1)

    Clock.future(32, section_outro, args=(0,))

def section_outro(n=0):
    # Harmony
    p1 >> pads(var.chords, sus=8, room=0.7, mix=0.5,
               amp=linvar([0.3, 0], 32))
    p2 >> pluck(PxRand([0, 2, 4, 5]) + var.chords, dur=1/4,
                amp=expvar([0.2, 0], 32))
    p3.stop()

    # Bass
    b1 >> bass(var.chords + var([0, -2], 8), 
               dur=PDur(2, 8), 
               lpf=500, 
               room=0.2, 
               echo=0.5, 
               amp=0.3 * expvar([1, 0], 8))

    # Drums
    d1 >> play("x ", amp=linvar([0.3, 0.1], 32), room=0.5, mix=0.5)
    d2 >> play("---", amp=0.2 * linvar([0.3, 0.1], 32), room=0.5, mix=0.5)
    d3 >> play("  o ", amp=0.2, room=0.5, mix=0.5)

    # Texture
    s1 >> swell(dur=8, amp=linvar([0.05, 0.1], 16), room=0.7, mix=0.3, pan=PSine().norm())
    s2 >> play(" ~ ~ ", echo=1.5, echotime=8, amp=linvar([0.1, 0], 8)).every(4, "reverse")

# Start temporal transitions
Clock.future(32, section_build, args=(0,))

Go()
