from FoxDot import *

```python
# Global Setup
Clock.clear()
Clock.bpm = 150
Scale.default = "minor"
Root.default = "D#"

# Shared Harmony Variables
var.chords = var([0, 3, -2, 5], 8)

# Harmony Players
p1 >> keys(var.chords, dur=4, room=1, mix=0.6, lpf=linvar([800, 400], 8)) 
p2 >> pluck(PWalk()[:8], dur=1/4, amp=0.8, delay=[0, 0.25]) 

def build_section(n=0):
    # Harmony for Build Section
    p1 >> keys(var.chords + P*(0, 2, 4), dur=4, lpf=linvar([400, 1200], 16), amp=sinvar([0.4, 0.9], 8))
    p2 >> pluck(PWalk(), dur=1/4, chop=4, amp=0.7, lpf=var([500, 1500], [16, 8]).transform(lambda v: v * 2))

    # Texture for Build
    s1 >> pads(dur=4, amp=sinvar([0.2, 0.3], 16), room=0.7, mix=0.5, hpf=linvar([200, 800], 32)).every(16, 'shuffle')
    s2 >> play("x-o-[-**]", sample=PRand(0,3), amp=0.18, chop=4, spin=2, tremolo=4)

    # Drums for Build
    d1 >> play("x-x ", dur=1, delay=[0,0.1], amp=var([0.6, 0.3], 16))
    d2 >> play("( * )[-*]", dur=PDur(5,16), delay=[0,0.05], amp=var([0.4, 0.5], 16))
    d3 >> play("~[--]-", dur=PDur(7,16), delay=[0.02, 0.1], amp=var([0.5, 0.2], 16))
    Clock.future(16*4, climax_section)

def climax_section(n=0):
    # Harmony for Climax
    p1 >> charm(var.chords, dur=1/2, lpf=linvar([1200, 500], 16), amp=sinvar([0.6, 1], 8)).every(8, "stutter", 4)
    p2 >> pads(PWalk() + P*(1, 3, 5), dur=PDur(3, 8), amp=1).every(4, "rotate", 2)
    p3 >> bell(p1.pitch.accompany(), dur=PDur(5, 16), amp=0.7).every(4, "mirror")

    # Texture for Climax
    s1 >> loop("ambient", dur=4, amp=linvar([0.3, 0.4], 16), hpf=expvar([800, 1200], 32), room=0.85, mix=0.6)
    s2 >> play("<[%##]>{#-]", sample=P[:4], amp=0.2, cut=0.2, pshift=PRand(-1,1), pan=PWhite(-0.5, 0.5))

    # Drums for Climax
    d1 >> play("x-o-", dur=1/2, delay=[0,0.05], amp=var([0.8, 0.4], 16))
    d2 >> play("<*=(=[- ])>", dur=1/4).every(4, "stutter", 4, dur=PDur(3,8))
    d3 >> play("^^*", dur=PDur(5,8), amp=var([0.7, 0.5], 16))
    Clock.future(16*4, outro_section)

def outro_section(n=0):
    # Harmony for Outro
    p1 >> keys(var.chords, dur=4, room=1.5, mix=0.7, lpf=linvar([400, 100], 8))
    p2 >> pluck(PWalk()[:8], dur=1/4, amp=linvar([0.5, 0], 8), delay=0.1)

    # Texture for Outro
    s1 >> pads(dur=8, amp=linvar([0.3, 0.1], 16), room=0.9, mix=0.5).every(4, 'reverse')
    s2 >> play("- [---]", amp=0.1, echo=0.5, pan=PSine(16), pshift=PWalk(3))

    # Drums for Outro
    d1 >> play("x   ", dur=1, amp=var([0.3, 0.1], 8))
    d2 >> play("  * ", dur=PDur(3,8), amp=var([0.2, 0], 8))
    d3 >> play(" ~ ", dur=[rest(1), 1], amp=var([0.1, 0], 8))

# Bass follows the harmony
b1 >> bass(var.chords + var([0, -1, 2, 1], 8), dur=PDur(3, 8), oct=var([3, 4], 8), lpf=linvar([400, 1000], 16), lpr=0.3, room=0.1, glide=[0, 2, 0, 0])

# Begin the sequence in intro
Clock.future(8*4, build_section)
```

Go()