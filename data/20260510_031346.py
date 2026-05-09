from FoxDot import *

# Clear Clock and set up global settings
Clock.clear()
Clock.bpm = 130
Scale.default = "minorPentatonic"
Root.default = "A"

# Shared variables for chord progressions
var.chords = var([0, 2, 4, 6, 3, 1], [8, 16, 12, 8])

# Harmony Layer
p1 >> pads(var.chords + P*(0, 4, 7), dur=[1, 1/2, 1/4, 1/4], lpf=linvar([800, 2000], [32, inf]), room=0.5, mix=0.2)
p2 >> pluck(PWalk(max=7) | P[12, 9, 5, 7].arp([0, P*[2, 4, 6], 7]), dur=PDur(3, 8), lpf=linvar([800, 1500], 16)).every(4, "rotate").every(8, "shuffle")
p3 >> bell(p1.pitch.accompany([0, 2, 3]), dur=4, amp=0, room=0.4, mix=0.3)

# Bass Line
var.bassline = var([0, 2, 3, 5], [8, 16, 12, 8])
b1 >> bass(var.chords + var.bassline, dur=PDur(3,8), lpf=600, lpr=0.4, room=0.1, glide=[0, 0, 1, 0], oct=var([3, 4], [16, 16]))

# Drums Layer
d1 >> play("<x  x><  * >").every(8, "rotate")
d2 >> play("  ooo")

# Temporal function for transitioning to Build Section
def build_section(n=0):
    d1 >> play("<x[xx] x><( x) o>").every(4, "stutter", 2).every(16, "shuffle")
    d2 >> play("s   s  s[o][--]", sample=2).every(8, "rotate")
    d3 >> play(" n [-n]", delay=var([0, 0.1], 8)).every(4, "stutter", 4, amp=0.5)
    p2 >> pluck(PWalk(max=7) | P[12, 9, 5, 7].arp([0, P*[2, 4, 6], 7]), dur=PDur(3, 8), lpf=linvar([800, 1500], 16)).every(4, "rotate").every(8, "shuffle")
    Clock.future(16 * 4, chill_breakdown, args=(0,))

Clock.future(8 * 4, build_section, args=(0,))

# Break down Section
def chill_breakdown(n=0):
    d1 >> play("x   x xo", amp=var([0.5, 0.2], 12))
    d2 >> play("[--]", amp=var([0.5, 0.2], 12))
    d3 >> play("  n ", sample=3, delay=[0, 0.1])
    p1 >> pads(var.chords + P*(0, 4, 7), dur=[1, 1/2, 1/4, 1/4], lpf=linvar([800, 2000], [32, inf]), room=0.5, mix=0.2)
    p2.stop()  # Stop pluck for contrast
    p3 >> bell(p1.pitch.accompany([0, 2, 3]), dur=4, amp=0, room=0.4, mix=0.3)
    Clock.future(12 * 4, peaceful_outro, args=(0,))

# Peaceful Outro
def peaceful_outro(n=0):
    d1 >> play(" x  x ", amp=0.3).every(8, "reverse")
    d2 >> play("  oo ", amp=0.3)
    d3 >> play("n [n] ", amp=0.2)
    p1 >> pads(var.chords + P*(0, 4, 7), dur=[1, 1/2, 1/4, 1/4], lpf=expvar([400, 800], 16), room=0.5, mix=0.2)
    p3 >> bell(p1.pitch.accompany([0, 2, 3]), dur=4, amp=0.4 * sinvar([0.2, 0.8], 12), room=0.4, mix=0.3)
    s1.every(16, "reverse")

# Texture Layer
s1 >> swell(P[0, 4, 5], oct=4, dur=8, amp=0.15, room=0.5, mix=0.2).every(16, "reverse")
s2 >> play("<x ~[---] >", sample=2, amp=linvar([0.1, 0.3], 16), dur=4, pan=PSine(8)) + p1.pitch.accompany([0, 2, 5])

Go()
