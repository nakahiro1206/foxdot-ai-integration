from FoxDot import *

# Background Pad
Clock.bpm = 60
p1 >> pads([0, 4, 5, 3], dur=[4, 4, 2, 6], amp=0.4, oct=4)

# Coffee Grinding (Percussive)
d1 >> play("xxxx", dur=[0.5, 0.25, 0.25, 1], sample=2, amp=0.7)

# Coffee Brewing (Ambient)
s1 >> loop("coffee-brewing.wav", dur=8, amp=0.5)

# Melody (Optional)
p2 >> pluck([0, 2, 4, 5], dur=[1, 1, rest(2), 0.5], amp=0.6, oct=5)

# Time-varying changes
p1.amp = linvar([0.4, 0.6], 16)
s1.amp = var([0.5, 0.3], [8, 8])


Go()