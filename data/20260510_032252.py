from FoxDot import *

# Global setup
Clock.clear()
Clock.bpm = 120
Scale.default = "phrygian"
Root.default = "A"

# Define shared variables
var.chords = var([0, 3, 2, 5], 8)

# Introduction Section: 8 Bars
def intro_section(n=0):
    p1 >> pads(var.chords, dur=4, amp=sinvar([0.1, 0.7], 8), room=0.5, mix=0.4).every(8, "rotate")
    p2 >> pluck(PWalk(), dur=2, amp=0.5, echo=1.5, room=0.4).every(8, "shuffle")
    b1 >> bass(var.chords, dur=PDur(3,8), amp=sinvar([0.2, 0.5], 32), lpf=500, lpr=0.3, room=0.1, oct=3)
    d1 >> play("-", dur=1, amp=sinvar([0.1, 0.3], 16), room=0.5, mix=0.3)
    d2 >> play(" ", dur=4)
    d3 >> play("(--)", dur=2, amp=sinvar([0.1, 0.4], 16)).every(8, "stutter", 4, pan=[-1, 1])
    s1 >> swell([0, 1, 2], dur=8, amp=sinvar([0.05, 0.15], 16), room=0.8, mix=0.3, lpf=linvar([400, 800], 32)).every(8, "reverse")
    s2 >> play("v ", echo=0.5, echotime=4, amp=0.1).accompany()
    Clock.future(32, build_section, args=(0,))

# Build Section: 16 Bars
def build_section(n=0):
    var.chords.update([0, 5, 1, 4], 16)
    p1 >> pads(var.chords, dur=PDur(3, 8), amp=sinvar([0.2, 0.8], 16), room=0.6, mix=0.4).every(8, "rotate")
    p2 >> pluck(PChain({0: [1, 3], 1: [0, 2, 4], 4: [3, 5, 6]}), dur=PDur(5, 8), amp=sinvar([0.3, 0.6], 16), echo=0.5, room=0.5).every(8, "shuffle")
    b1 >> bass(var.chords + var([0,2],8), dur=PDur(5,8), lpf=400, lpr=0.4, room=0.15, glide=[0,2,0,-2], amp=sinvar([0.4, 0.7], 16), oct=var([3,4], 16))
    d1 >> play("x-o-", dur=PDur(3, 8), amp=sinvar([0.3, 0.6], 16))
    d2 >> play("  o", dur=PDur(5, 8), amp=sinvar([0.3, 0.5], 16), delay=0.2)
    d3 >> play("<[--]>[--]", dur=PDur(5, 8), amp=sinvar([0.3, 0.7], 32), room=0.4).every(4, "shuffle")
    s1 >> pads([0, 3, 5], dur=4, amp=sinvar([0.1, 0.2], 16), echo=0.5, echotime=8, lpf=linvar([400, 1200], 32)).every(16, "shuffle")
    s2 >> play("n ", formant=var([2, 5, 3], 8), echo=0.3, echotime=6, amp=0.2).accompany()
    Clock.future(64, climax_section, args=(0,))

# Climax Section: 16 Bars
def climax_section(n=0):
    var.chords.update([5, 2, 0, 3], 16)
    p1 >> pads(var.chords, dur=PDur(7, 16), amp=linvar([0.6, 1.0], 16), room=0.7, mix=0.5).every(8, "rotate")
    p2 >> pluck(PChain({0: [2, 4, 5], 5: [1, 3, 0]}), dur=PDur(7, 16), amp=linvar([0.5, 0.9], 16), echo=2, room=0.6).every(8, "shuffle")
    b1 >> bass(var.chords + var([0,-1,2,-2], 4), dur=PDur(7,16), lpf=300, lpr=0.6, room=0.2, glide=[1,-1], oct=var([3,4], 8))
    d1 >> play("<x-o-><  * >", dur=PDur(4, 8), amp=sinvar([0.6, 1], 16))
    d2 >> play("<---o><(x)-(x)-o>", dur=PDur(7, 16), amp=sinvar([0.5, 0.9], 16), delay=[0, 0.1])
    d3 >> play("<{xX}[oo]><hh>", dur=PDur(5, 8), amp=sinvar([0.4, 0.8], 16), room=0.6).every(8, "rotate")
    s1 >> loop("pad_loop", dur=[2,4,2,4], amp=sinvar([0.1, 0.3], 8), room=0.9, mix=0.4, lpf=expvar([400, 1600], 32)).every(8, "reverse")
    s2 >> play("x-o-", pan=PSine(16), tremolo=4, pshift=PRand([0, 1, -1]), echo=0.4, amp=0.3).every([4, 8], "rotate")
    Clock.future(128, outro_section, args=(0,))

# Outro Section: 8 Bars
def outro_section(n=0):
    var.chords.update([3, 0, 2, 5], 8)
    p1 >> pads(var.chords, dur=4, amp=sinvar([0.2, 0.4], 8), room=0.5, mix=0.4).every(8, "shuffle")
    p2 >> pluck(PWalk(), dur=4, amp=0.4 * sinvar([0.6, 0.2], 8), echo=1, room=0.4).every(8, "rotate")
    p3 >> bell(var.chords.accompany(), dur=4, amp=0)
    b1 >> bass(var.chords, dur=PDur(3,8), amp=sinvar([0.1, 0.4], 16), lpf=600, lpr=0.2, room=0.1, oct=3)
    d1 >> play(" ", dur=4)
    d2 >> play("---(-=)", dur=2, amp=sinvar([0.2, 0.4], 16), room=0.5, mix=0.4)
    d3 >> play("[oo]", dur=4, amp=sinvar([0.3, 0.5], 16)).every(4, "rotate")
    s1 >> swell([0, 1, 0], dur=8, amp=expvar([0.2, 0], 16), room=0.5, mix=0.25, lpf=linvar([800, 400], 32)).every(8, "reverse")
    s2 >> play("  s ", room=0.3, mix=0.2, echo=0.3, amp=0.1).every(8, "reverse")

# Start with Intro
intro_section(0)

Go()