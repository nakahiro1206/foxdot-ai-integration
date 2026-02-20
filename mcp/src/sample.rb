start_notes = ring(60, 62, 63, 62)
loop do
  my_chord = chord(start_notes.tick, :M7)
  play my_chord, release: 2
  16.times do
    play my_chord.choose
    sleep 0.125
  end
end