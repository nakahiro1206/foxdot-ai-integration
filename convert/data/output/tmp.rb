use_bpm 128

# Modern drum beat with electronic elements
live_loop :drums do
  sample :drum_heavy_kick, amp: 1.2
  sleep 1
  sample :drum_snare_hard, amp: 0.9
  sample :elec_blip, rate: 0.5, amp: 0.3
  sleep 1
  sample :drum_heavy_kick, amp: 1
  sleep 0.5
  sample :drum_heavy_kick, amp: 0.8
  sleep 0.5
  sample :drum_snare_hard, amp: 0.9
  sample :elec_tick, amp: 0.4
  sleep 1
end

# Futuristic hi-hats with variation
live_loop :hihat do
  sample :drum_cymbal_closed, amp: 0.3, rate: 1.2
  sleep 0.25
  sample :drum_cymbal_closed, amp: 0.2, rate: 1.5
  sleep 0.25
end

# Sidechain effect with pulsing synth
live_loop :sidechained_chords do
  use_synth :blade
  with_fx :reverb, room: 0.7 do
    with_fx :slicer, phase: 0.25, wave: 1 do
      play chord(:C, :major), release: 4, amp: 0.7, cutoff: 90
      sleep 4
      play chord(:G, :major), release: 4, amp: 0.7, cutoff: 90
      sleep 4
      play chord(:A, :minor), release: 4, amp: 0.7, cutoff: 90
      sleep 4
      play chord(:F, :major), release: 4, amp: 0.7, cutoff: 90
      sleep 4
    end
  end
end

# Futuristic arpeggio
live_loop :arp do
  use_synth :prophet
  with_fx :echo, phase: 0.375, decay: 4 do
    use_random_seed 1000
    16.times do
      play scale(:C4, :major).choose, release: 0.1, cutoff: rrand(80, 120), amp: 0.4
      sleep 0.125
    end
  end
end

# Deep sub bass with wobble
live_loop :bass do
  use_synth :zaar
  with_fx :lpf, cutoff: 80 do
    play :C2, release: 1, amp: 1.2, cutoff: 70
    sleep 1
    play :C2, release: 0.5, amp: 0.8, cutoff: 60
    sleep 1
    play :E2, release: 0.5, amp: 0.8, cutoff: 65
    sleep 1
    play :G2, release: 0.5, amp: 0.8, cutoff: 70
    sleep 1
    
    play :G2, release: 1, amp: 1.2, cutoff: 70
    sleep 2
    play :B2, release: 0.5, amp: 0.8, cutoff: 65
    sleep 2
    
    play :A2, release: 1, amp: 1.2, cutoff: 70
    sleep 2
    play :C3, release: 0.5, amp: 0.8, cutoff: 75
    sleep 2
    
    play :F2, release: 1, amp: 1.2, cutoff: 70
    sleep 2
    play :A2, release: 0.5, amp: 0.8, cutoff: 75
    sleep 2
  end
end

# Glitchy electronic melody
live_loop :melody do
  use_synth :tb303
  sleep 16
  with_fx :reverb, room: 0.6 do
    with_fx :distortion, distort: 0.3 do
      play_pattern_timed [:E4, :G4, :C5, :G4, :E4, :D4], [1, 1, 2, 1, 2, 1],
        release: 0.4, cutoff: 100, res: 0.7, amp: 0.6
      sleep 8
      play_pattern_timed [:D4, :E4, :G4, :E4], [2, 2, 3, 1],
        release: 0.4, cutoff: 95, res: 0.7, amp: 0.6
      sleep 8
    end
  end
end

# Futuristic sweep sounds
live_loop :sweeps do
  use_synth :dark_ambience
  with_fx :reverb, room: 0.8 do
    play :C3, attack: 2, release: 6, amp: 0.3, cutoff: 60
    sleep 8
  end
end

# Electronic bleeps and bloops
live_loop :fx_sounds do
  sleep 7.5
  sample :elec_beep, rate: 1.5, amp: 0.5
  sleep 0.5
  sample :elec_ping, rate: 2, amp: 0.4
  sleep 8
end