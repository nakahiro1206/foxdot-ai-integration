from FoxDot import *

# Importing external Libraries including FoxDot.
Clock.clear()

# Global Setup
Clock.bpm = 140
Scale.default = "minor"
Root.default = "A"

# Harmony Variables
var.chords = var([0, 5, 3, 7], [8, 16, 16, 8])

# Intro Section (Bars: 8)
def section_intro():
    p1 >> pads(var.chords, dur=PDur(3, 8), sus=4, chop=0, lpf=linvar([400, 800], 16), room=0.3, mix=0.2)
    p2 >> pluck(PWalk()[:8], dur=1/4, amp=0.4, lpf=linvar([400, 800], 8))
    p3 >> bell(var.chords + P*(0, 2, 4), dur=PDur(4, 8), amp=sinvar([0, 0.6], 16), lpf=1200, room=0.4)

    # Bass setup
    b1 >> bass(var.chords, dur=PDur(3, 8), lpf=linvar([400, 1000], 16), lpr=0.3, room=0.1, amp=sinvar([0.2, 0.7], 8))

    # Texture setup
    s1 >> swell([0, 4, 7, 11], dur=8, 
                amp=sinvar([0.1, 0.3], 32), 
                hpf=linvar([200, 1000], 32), 
                room=1, mix=0.3)

    s2 >> play("<s  ><o  >",
               hpf=linvar([500, 2000], 16),
               amp=sinvar([0.1, 0.25], 16), sample=2)

    # Drums setup
    d1 >> play("x   ", dur=[1,1,1,1], amp=sinvar([0,0.5], 8))
    d2 >> play("   o", dur=[1,1,1,1], amp=sinvar([0,0.4], 8))
    d3 >> play("    ", amp=0)  # Silence for atmospheric effect

# Build Section (Bars: 16)
def section_build():
    var.chords.update([5, 3, 7, 0], 16)
    
    p1 >> pads(var.chords, dur=PDur(3, 8), sus=3, delay=0.5, lpf=expvar([800, 1200], 16), mix=0.25)
    p2 >> blip(PWalk(7), dur=1/4, amp=0.6, lpf=expvar([400, 1000], 16), room=0.1)
    p3 >> sinepad(var.chords.accompany(), dur=1, amp=0.5, delay=0.25, tremolo=4)
    
    b1 >> bass(var.chords + var([0, 1, -1], [8, 4, 4]), dur=PDur(5, 8), glide=[0, 2], lpf=expvar([400, 1600], 32), lpr=0.25, room=0.15, oct=var([3, 4], 16))

    s1.every(8, "reverse")
    s2 >> play("(sn)(hh)", 
               amp=expvar([0.05, 0.2], 16),
               pshift=sinvar([-1, 1], 32), 
               room=0.4, mix=0.2)

    d1 >> play("x-o-", dur=PDur(3, 8), delay=[0,0.05], amp=var([0.5,0.8], 8))
    d2 >> play("---(--)o", dur=PDur(5, 8), delay=[0,0.1], amp=var([0.5,0.7], 8))
    d1.every(4, "shuffle")
    d2.every(4, "rotate")

# Climax Section (Bars: 16)
def section_climax():
    var.chords.update([0, 4, 5, 11], 16)

    p1 >> pads(var.chords, dur=PDur(3, 8), sus=3, drive=0.4, room=0.5, mix=0.4)
    p2 >> blip(p1.pitch.accompany([0, 2, 4]), dur=1/8, amp=0.8, lpf=800, room=0.3)
    p3 >> noise(var.chords + P^(0, 2, 4, 0.25), dur=1/4, amp=0.7, chop=4, tremolo=3)
    Group(p1, p2).amplify = var([1, 0.3], 8)

    b1 >> bass(var.chords.accompany([0, 2, 5]), dur=PDur(3, 8), lpf=700, lpr=0.4, room=0.2, amp=1, drive=var([0.3, 0.7], 8), oct=var([4, 5], 16))

    s1 >> loop("ambient_loop", dur=8, 
               amp=0.2, 
               lpf=linvar([600, 200], 16),
               echo=0.5, echotime=8)
    
    s2 >> play("V", amp=0.2, sample=[2, 3],
               pshift=p1.pitch.accompany() + 4, 
               delay=0.5, 
               tremolo=4)
    s2.every(4, "stutter", 4, dur=Cycle([1/4, 1/8]))

    d1 >> play("x-o-ox-o-", dur=1/2, sample=2, amp=var([0.8,1], [8,8]), drive=0.3)
    d2 >> play("<[--]o><[--] >-(---)", amp=var([0.8,1], [8,8]), sample=1)
    d3 >> play("<...( )( )>c", dur=1/4, sample=PRand([0,1,2]), amp=var([0.7, 0.9], [8,8]))
    d3.every(3, "stutter", 4)

# Outro Section (Bars: 8)
def section_outro():
    var.chords.update([7, 3, 5, 0], 8)
    
    p1 >> pads(var.chords, dur=PDur(5, 8), sus=4, lpf=linvar([1200, 400], 8), room=0.3)
    p2 >> pluck(PWalk()[:8], dur=1/2, amp=0, lpf=linvar([800, 200], 8))  # fades
    p3 >> bell(var.chords + P*(0, 2, 4), dur=PDur(6, 8), amp=sinvar([0.5, 0], 8), lpf=400, room=0.4)

    b1 >> bass(var.chords, dur=PDur(3, 8), lpf=linvar([800, 200], [16, 8]), lpr=0.3, room=0.1, amp=linvar([0.7, 0], [8, inf]), glide=[0, 3])

    s1 >> pads([0, 4, 7, 11], dur=16,
               amp=expvar([0.1, 0], 32), room=0.8, mix=0.4)

    s2 >> play("oo(  oo)",
               amp=linvar([0.05, 0.15], 32),
               spin=2, 
               room=0.3, mix=0.2)

    d1 >> play("x   ", dur=[1, rest(1)], amp=linvar([0.7, 0.2], 8))
    d2 >> play("  o ", dur=[1, rest(1)], amp=linvar([0.6, 0.2], 8))
    d3 >> play("    ", amp=0)  # Silence for atmospheric effect

# Schedule sections in sequence
Clock.future(0, section_intro)
Clock.future(8*4, section_build)
Clock.future(24*4, section_climax)
Clock.future(40*4, section_outro)

Go()