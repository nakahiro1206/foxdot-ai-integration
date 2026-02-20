use_bpm 120

melody0 = []
sleeps0 = []

in_thread do
  sleep sleeps0[0]
  melody0.each_with_index do |item,i|
    play item[:note], sustain: item[:duration]*0.8, release: item[:duration]*0.2
    sleep sleeps0[i+1] if i+1 < sleeps0.length
  end
end

