from supriya.realtime import Server
from supriya.ugens import Out, SinOsc
from supriya.synthdefs import SynthDefBuilder

# 1. Boot the SuperCollider server
server = Server.default().boot()

# 2. Build a Synth Definition (The "Instrument")
with SynthDefBuilder(frequency=440, out=0) as builder:
    # Create a sine oscillator multiplied by an amplitude of 0.1
    sine = SinOsc.ar(frequency=builder["frequency"]) * 0.1
    # Send the signal to the output bus
    out = Out.ar(bus=builder["out"], source=sine)

synthdef = builder.build().allocate()

# 3. Play the sound
# This creates a 'Synth' node on the server
synth = synthdef.play(frequency=440)

# 4. Cleanup (Stop the sound after you're done)
# synth.free()
# server.quit()
