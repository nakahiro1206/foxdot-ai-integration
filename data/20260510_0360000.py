from FoxDot import *

# GLOBAL SETUP
Clock.clear()
Clock.bpm = 85
Scale.default = "minorPentatonic"
Root.default = "G"

# HARMONY LAYER
var.chords = var([0, 2, 4], [8, 16, 32, 8])

# Intro
p1 >> varsaw(var.chords, dur=[2, 4], oct=5, lpf=linvar([500, 1500], 8), amp=0.4, room=0.3, mix=0.2)
p2 >> pluck(dur=PEuclid(3, 8), scale=Scale.minorPentatonic, root="G").accompany(p1.pitch).every(6, "mirror")
p3 >> bell([7, var.chords + 2], dur=8, delay=0.5, lpf=linvar([800, 1000], 8), amp=0)

# Build
p1 >> charm(var.chords + (0, 4, 7), dur=PDur(3, 8), amp=linvar([0.2, 0.4], 16))
p2 >> keys(Pvar([PRange(5,9).arp([0,2,3]), PWalk(3)], [16,16]), dur=1/4, amp=0.5).every(8, 'shuffle')
p3 >> soprano(var.chords, dur=PDur(5,8), oct=6, delay=linvar([0.1,0.2], 16))

# Drop
p1 >> swell(var.chords + (0, 2, 4, 7), dur=PDur(3,8), amp=P[1,0.8,0.6].stretch(16), room=linvar([0.3, 0.6], 16))
p2 >> blip(PWalk(), dur=1/4, amp=sinvar([0.3,0.8], 16)).every(4, 'reverse')
p3 >> soprano(var.chords.accompany([0, 4, 7]), dur=PDur(3,8), amp=0.5, delay=0.25)

# Outro
p1 >> pads(var.chords, dur=4, amp=expvar([0.4, 0.2], 8), lpf=var([800, 1200], [4,4]))
p2 >> soft(var.chords.accompany([0, 2, 4, 5]), dur=1, amp=linvar([0.8, 0.4], 8))
p3 >> charm(var.chords, dur=4, amp=0.3, lpf=1000, room=0.2, mix=0.1).every(4, 'rotate')

# BASS LAYER
b1 >> bass(var.chords + var([0, -1, 2], 8), dur=PDur(3, 8), lpf=linvar([400, 800], 16), lpr=0.7, room=0.15, oct=3)

# DRUMS LAYER
d1 >> play("x  ", dur=1, amp=var([0.5, 0.3], 8), delay=[0, 0.1])
d2 >> play("---", amp=var([0.4, 0.2], 8))
d3 >> play("s", amp=var([0.3, 0.1], 8))

# TEXTURE LAYER
s1 >> swell([0, 2, 4], dur=8, amp=linvar([0.1, 0.3], 16), room=0.4, mix=0.2, hpf=expvar([100, 800], 8)).every(8, "reverse")
s2 >> play("*- ", dur=PEuclid2(3, 8, "-", "*"), amp=0.15).spread()

# TRANSITIONS & SECTIONS
def transition_to_build(n=0):
    # Energy rises, more rhythmic complexity
    b1 >> bass(var.chords + var([0, 2, 4, 5], [8, 4, 2, 2]), dur=PDur(5, 8), lpf=600, lpr=0.8, room=0.15, oct=var([3, 4], 8), glide=[0, 0, 2, 0])
    Clock.future(16 * 4, transition_to_drop, args=(0,))

def transition_to_drop(n=0):
    # High energy drop
    b1 >> bass(var.chords + var([0, -2, 3], 16), dur=PDur(7, 16), lpf=400, lpr=0.6, room=0.2, oct=4, glide=[0, 4])
    g_melody = Group(p1, p2, p3)
    g_melody.amplify = var([1, 0.4], [16 * 4, 8])
    Clock.future(16 * 4, transition_to_outro, args=(0,))

def transition_to_outro(n=0):
    # Descend back to introspection
    b1 >> bass(var.chords + var([0, -1, 2], 8), dur=PDur(4, 8), lpf=expvar([400, 1200], 16), lpr=0.7, room=0.15, oct=3)

Clock.future(8 * 4, transition_to_build, args=(0,))
