from FoxDot import *

# ------------------------------------------------------------------------
# Request:  I want to create some chinese traditional vibe and hip hop taste plus trendy electronic taste. wanna represent chinese futuristic AI world crowded with a lot of technologies
# Brief:
#   Imagine a piece that conjures an emotional journey through a
#   futuristic, technologically advanced Chinese metropolis. The opening
#   should evoke a sense of awe and intrigue, as if stepping into a
#   vibrant, bustling cityscape where tradition and innovation coexist.
#   The listener should feel a gradual shift from curiosity to
#   exhilaration as the piece progresses. Rhythmically, the composition
#   should incorporate a blend of straight hip-hop beats with sporadic
#   glitches and syncopations, creating an intricate, yet mechanical flow
#   that mirrors the precise movements of advanced AI systems. This will
#   lead to a dynamic interplay between the beats, ensuring a densely
#   layered rhythmic experience. The harmonic language should juxtapose
#   traditional Chinese scales, like the pentatonic or modal, with
#   elements of hip-hop's soulful and often murky chord progressions.
#   Incorporating both dissonant and consonant elements, the harmony
#   should maintain tension and resolution, symbolizing the balance
#   between past and future. Foregound elements might include a vivid
#   erhu or guzheng melody, blending seamlessly with synthesized
#   textures. Layers of electronic arpeggios and basslines should fill
#   the mid-ground, providing depth, while ambient cityscape sounds
#   create an expansive background layer. The dynamic arc should begin
#   quietly, gradually building energy with layers adding complexity,
#   reaching a crescendo of intense, layered elements before tapering to
#   a serene, reflective close. Draw inspiration from artists like TNGHT
#   and Chinese DJ/producer Jason Hou, with a distinctive element like a
#   bitcrushed gong that echoes at unexpected intervals, adding a
#   uniquely futuristic, yet culturally resonant touch.
# Concept:
#   BPM: 88
#   Scale: Chinese pentatonic
#   Root: G#
#   Mood: Awe-inspiring
#   Genre: Futuristic Hip-Hop
#   Energy arc: Begins quietly and builds with layers of complexity, reaching a crescendo of intense elements before tapering to a reflective close
#   Section count: 5
#   Key techniques: PEuclid hip-hop beats with glitches, bitcrushed effects, var for dynamic layers, pluck with Chinese scales, synth texture blending
# ------------------------------------------------------------------------

Clock.clear()
Clock.bpm = 88
Scale.default = "chinese"
Root.default = "G#"

# Harmony var for consistent musicality across sections
var.chords = var([0, 5, 4, 2], [8, 16, 16, 12, 8])  # Respective var.chords for each section

# Harmony players
p1 >> keys(var.chords + P*(0, 2, 4), dur=PDur(3, 8), lpf=linvar([400, 1600], 8), amp=sinvar([0.2, 0.8], 16))
p2 >> pads(var.chords + (0, 2, 4), dur=PDur(3, 8), lpf=1200, room=0.4)
p2 >> pluck(PWalk(7), dur=1/4, amp=1, pan=sinvar([-1, 1], 8)).every(8, 'rotate')
p3 >> bell(p1.pitch.accompany([0, 3, 5]), dur=1/2, amp=linvar([0, 0.5], 16))

# Bass player following harmony
b1 >> bass(var.chords, dur=PDur(3, 8), amp=0.5, lpf=linvar([400, 800], 16), oct=var([3, 4], [8, 8]), room=0.1)

# Drums setup
d1 >> play("x ", dur=1, amp=0.1, delay=0.05)
d2 >> play("- ", dur=1, amp=0.1)
d3 >> play("[oo] ", dur=1, amp=0.1, delay=[0, 0.025])

# Exploration section setup, introducing more energy
def section_exploration(n=0):
    d1 >> play("x-o-", amp=var([0.5, 0.7], 8), delay=[0, 0.05])
    d2 >> play("<s><- >", dur=PDur(3, 8), amp=var([0.5, 0.6], 8))
    d3 >> play("[(oo)(oo)]", dur=PDur(5, 8), amp=var([0.3, 0.5], 8))

    p1 >> pads(var.chords + (0, 2, 4), dur=PDur(3, 8), lpf=1200, room=0.4)
    p3 >> bell(p1.pitch.accompany([0, 3, 5]), dur=1/2, amp=linvar([0, 0.5], 16))

Clock.future(8 * 4, section_exploration)

# Urban Peak setup with higher energy and bitcrushing
def section_urban_peak(n=0):
    d1 >> play("X-oXO-", amp=var([0.7, 0.9], 8), crush=4)
    d2 >> play("s<-> [--]", dur=PDur(3, 8), amp=var([0.6, 0.8], 8), delay=[0.02, 0.04])
    d3 >> play("<[(oo)oo]><[xx]o>", amp=var([0.5, 0.7], 8))

    p1.every(4, 'stutter', 4)
    p2.every(4, 'stutter', 4)
    p3 >> bell(p1.pitch + P*(0, 2, 4), dur=1/2, amp=expvar([1, 0.2], 16))

Clock.future((8 + 16) * 4, section_urban_peak)

# Reflection setup with expressive and calming features
def section_reflection(n=0):
    d1 >> play("<x[--] >< o >", dur=1, amp=var([0.4, 0.5], 6), delay=0.05)
    d2 >> play("---", dur=PDur(3, 8), amp=var([0.3, 0.4], 6))
    d3 >> play("o-", dur=1, amp=var([0.2, 0.3], 6), delay=[0, 0.05])

    p1 >> soft(var.chords + (0, 2, 4), dur=PDur(3, 8), lpf=expvar([1600, 400], 12))
    p2 >> blip(p1.pitch.accompany([0, 3, 5]), dur=PBern(16, 0.75), amp=linvar([0, 1], 12)).every(6, 'mirror')

Clock.future((8 + 16 + 16) * 4, section_reflection)

# Outro setup with calm and reflective features
def section_outro(n=0):
    b1 >> bass(var.chords, dur=PDur(3, 8), amp=0.5, lpf=linvar([400, 200], 8), glide=[0, 1, 0.5], oct=var([3,4], [4,4]))

    d1.every(4, "reverse")
    d2.every(2, "rotate")

Clock.future((8 + 16 + 16 + 12) * 4, section_outro)

# Texture for intro and evolution
s1 >> swell([0, 2, 4], dur=8, amp=linvar([0.05, 0.2], 16), room=0.7, mix=0.3, hpf=linvar([400, 1200], 32), pan=PSine())
s2 >> play("  * ", dur=1/2, amp=0.1, echo=1, room=0.6, mix=0.2, pshift=sinvar([-4, 4], 16))

Go()