from FoxDot import *

# ------------------------------------------------------------------------
# Request:  I want to create violent and heavy beat beat representing halloween night where draculla leaving their graveyard and attacking civils under full moon, cold air night
# Brief:
#   Picture a tempestuous scene unfolding under a full moon, where
#   Dracula rises with chilling intent. The emotional tone of this piece
#   should evoke a sensation of eerie anticipation that crescendos into
#   sheer, harrowing chaos. Begin with a feeling of lurking danger — a
#   cold, mysterious suspense — before escalating into an intense, almost
#   panic-inducing climax as the attack is unleashed. The rhythmic
#   character should be mechanical yet erratic, utilizing a dense,
#   driving beat that mimics a relentless pursuit. Incorporate a blend of
#   both straight and swung elements to create unease and
#   unpredictability. Pulsing, near-industrial percussion will serve as
#   the unsettling heartbeat of the piece. In harmonic language, employ a
#   deeply dissonant palette, weaving through Phrygian and Locrian scales
#   to emphasize the foreboding and otherworldly nature of the scene,
#   with sparse use of distorted, minor chords that create a sense of
#   unresolved tension. Include layers of sound where an ominous,
#   pulsating bass drones in the background, eerie synths drift mid-layer
#   like ghostly apparitions, and piercing, high-register screeches
#   occasionally shatter the silence in the foreground. The dynamic arc
#   should begin with subtlety, invoking a creeping fear that swells into
#   a furious, cacophonous onslaught, following a pattern reminiscent of
#   artists like Trent Reznor and Fever Ray, who expertly traverse the
#   dark, thematic soundscapes. As a distinctive detail, incorporate an
#   unsettling vocal sample — distorted and echoing — triggered
#   sporadically, as if Dracula’s taunts are cutting through the midnight
#   air, leaving an indelible mark on the listener’s psyche.
# Concept:
#   BPM: 100
#   Scale: Phrygian
#   Root: F#
#   Mood: Eerie anticipation
#   Genre: Industrial gothic
#   Energy arc: Begins with chilling suspense and low intensity, builds rapidly to a chaotic and intense climax, before gradually receding into an ominous silence.
#   Section count: 5
#   Key techniques: linvar distortion effects, PEuclid to create mechanical yet erratic rhythms, Pvar for pattern switching between scales, every() for timing unpredictability, dissonant chord layering, loop() for vocal samples.
# ------------------------------------------------------------------------

# Global Setup
Clock.clear()
Clock.bpm = 100
Scale.default = "phrygian"
Root.default = "F#"

# Harmonic Variables
var.chords = var([0, -1, 2, 1], 8)
var.bassline = var([0, -5, -2, 0], [8, 4, 2, 2])

# Prelude Section (Bars: 8, Energy: low)
def prelude(n=0):
    p1 >> pads(var.chords + P*(0, 7, 10), dur=4, amp=linvar([0.4, 0.6], 16), hpf=linvar([0, 800], 32))
    p2 >> pluck(P[0, 2, 4, 5].arp([0, 1, -1]), dur=4, amp=0.5, delay=[0, 0.1, 0.2], scale=Scale.phrygian, root="F#")
    d1 >> play("x  x ", dur=1, delay=[0, 0.05], amp=var([0.5, 0.8], 16))
    d2 >> play("--- ", dur=1, delay=0.02, sample=2, amp=var([0.4, 0.6], 16))
    s1 >> swell(dur=8, oct=3, amp=linvar([0.05, 0.15], 32), room=0.3, mix=0.3)
    s2 >> play("<v--->", rate=var([0.8, 1.2], 16), amp=0.1, delay=PEuclid(3,8), room=0.2, mix=0.2)

# Rise Section (Bars: 16, Energy: medium)
def rise(n=0):
    var.chords = var([0, -1, -3, 2], 16)
    p1 >> pads(var.chords + PGroup(0, 2, 5), bpm=90, lpf=linvar([200, 700], 16))
    p2 >> pluck(PWalk(), dur=PDur(3, 8), scale=Scale.locrian).accompany(p1.pitch, dur=1/2)
    d1 >> play("x-o-x", dur=PDur(3,8), delay=[0, 0.05, 0], amp=0.7)
    d2 >> play("  *  ", dur=PDur(5,8), delay=0.02, amp=linvar([0.5, 0.8], 16))
    d3 >> play("  @ ", dur=PDur(7,16), delay=0.03, amp=0.5)
    s1 >> pads(Pvar([0,3,-1,2], 16), dur=8, amp=linvar([0.1, 0.2], 32), lpf=expvar([400,1000], 32), formant=2)
    s2 >> play("A.....B", sample=2, echo=1.5, room=0.5, pan=PWhite(-0.5, 0.5), amp=var([0.08, 0.1], 8))

# Tension Section (Bars: 16, Energy: medium-high)
def tension(n=0):
    var.chords = var([2, 5, 4, 3], 16)
    p1 >> pads(var.chords + PGroup(0, -1, 4), dur=2, amp=0.8, lpf=expvar([600, 1200], 16))
    p2 >> donk(p1.pitch.accompany([0, 3, 5]), dur=1/4).every(4, "rotate")
    d1 >> play("x  o  o", dur=1/2, amp=PBern(16, 0.6))
    d2 >> play("[-=]- ", dur=1/4, amp=0.6).every(4, "rotate")
    d3 >> play("( @ )", sample=3, dur=PEuclid(3,8), amp=0.5)
    s1 >> swell(dur=8, oct=3, amp=linvar([0.15, 0.25], 32), lpf=expvar([1200,600], 16)).every(8, "rotate")
    s2 >> play("v----", sample=3, delay=PBern(12, 0.5), amp=0.05, spin=2)

# Onslaught Section (Bars: 16, Energy: high)
def onslaught(n=0):
    var.chords = var([2, 5, 3], 16)
    p1 >> saw(var.chords, dur=1, amp=1.2, room=0.8).every(8, "stutter", 4)
    p2 >> keys(p1.pitch.accompany([0, 7]), dur=1/2, bpm=120, amp=0.7)
    d1 >> play("x-X-xXO", amp=1).every(3, "stutter", 4)
    d2 >> play("<-=><-=>", dur=PDur(5,8), delay=0.01, amp=var([1, 0.7], 8))
    d3 >> play("< @ >< ! >", dur=1/4, amp=linvar([0.8, 1.2], 8))
    s1 >> loop("dracula", dur=8, amp=var([0.2, 0.3], 16), spin=4, echo=0.6)
    s2 >> play("<x..(-[x]-{o})>", sample=linvar([1, 4], 16), rate=P[1, 1.5], amp=linvar([0.05, 0.15], 16))

# Aftermath Section (Bars: 8, Energy: low)
def aftermath(n=0):
    var.chords = var([0, -1, 2, 1], 8)
    p1 >> piano(var.chords, dur=8, amp=linvar([0.2, 0], [8, inf]), echo=0.8, room=0.1)
    p2 >> pluck(p1.pitch, amp=0.2, dur=PDur(3, 8), lpf=linvar([1000, 0], [8, inf]), spin=0.5)
    d1 >> play("x ", dur=4, amp=sinvar([0.5, 0.1], 8)).every(2, "stutter", 2)
    d2 >> play("  - ", dur=4, amp=linvar([0.2, 0], 8))
    s1 >> pads(dur=8, amp=sinvar([0.05, 0.15], 32), room=expvar([0.4, 0], [32, inf]), formant=4)
    s2 >> play("A", sample=6, echo=linvar([0.6, 0], [16, inf]), amp=sinvar([0.02, 0.08], 16))

# Scheduling sections
Clock.future(8 * 4, rise)
Clock.future((8 + 16) * 4, tension)
Clock.future((8 + 16 + 16) * 4, onslaught)
Clock.future((8 + 16 + 16 + 16) * 4, aftermath)

# Bassline
b1 >> bass(var.chords + var.bassline, dur=PDur(3, 8), amp=0.7,
           lpf=400, lpr=0.3, room=0.1,
           glide=[0, 2, 0, 4],
           oct=var([3, 4], 8),
           delay=linvar([0.05, 0.15], 16))

Go()