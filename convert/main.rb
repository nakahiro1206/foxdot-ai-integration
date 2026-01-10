#! /usr/bin/env ruby
require 'midilib/sequence'

if ARGV.empty?
  STDERR.puts "Usage: #{$0} input.mid [output.rb]"
  STDERR.puts "Generates a Sonic Pi friendly Ruby file from input.mid"
  exit 2
end

# Read from MIDI file
infile = ARGV[0]
outfile = ARGV[1] || 'out.rb'

seq = MIDI::Sequence.new()

File.open(infile, 'rb') do |file|
  if file.nil?
    STDERR.puts "Cannot open file #{infile}"
    exit 1
  end
  seq.read(file) do |track, num_tracks, i|
    # progress hook (optional)
  end
end

PPQN = seq.ppqn # Pulses per quarter note, the number of ticks in one beat

def to_note (ticks)
  # Converts the time in ticks to time in notes
  return (ticks*1.0)/PPQN
end

melodies = {}
sleeps = {}
bpm = seq.bpm.round.to_s
seq.each_with_index do |track, idx|
  # Filter the track so it only had Note On events
  track = track.select { |e| e.is_a?(MIDI::NoteOn) }
  melody = []
  slps = []
  track.each_with_index do |e, i|
    # Get the first sleep
    if i == 0 
      first_slp = to_note(e.time_from_start)
      slps.push(first_slp)
    end

    # Calculate duration of note by comparing the time between on and off events. Convert from ticks to beats.
    dur_delta = e.off.time_from_start - e.time_from_start
    duration = to_note(dur_delta)
    # Round duration to the closest 1/16
    #duration = (duration*16).round / 16.0

    note = e.note
    melody.push({note: note, duration: duration})

    # There is one more note than there is sleep, so we have to break early on the last iteration
    break if i == (track.length - 1)
    slp_delta = track[i+1].time_from_start - e.time_from_start
    slp = to_note(slp_delta)
    slps.push(slp)
  end
  melodies[idx] = melody
  sleeps[idx] = slps
end

#= Sonic Pi Output
# This section creates a file that's readable by sonic pi

#== Attack/sutain/release ratios
ATTACK = 0
SUSTAIN = 0.8
RELEASE = 0.2

out = File.new(outfile, 'w')
out.write("use_bpm #{bpm}\n\n")

melodies.each do |key,value|
  idx = key.to_s
  out.write("melody#{idx} = #{value}\n")
  out.write("sleeps#{idx} = #{sleeps[key]}\n\n")
  out.write("in_thread do\n")
  out.write("  sleep sleeps#{idx}[0]\n")
  out.write("  melody#{idx}.each_with_index do |item,i|\n")
  out.write("    play item[:note]")
  out.write(", attack: item[:duration]*#{ATTACK}") if ATTACK > 0
  out.write(", sustain: item[:duration]*#{SUSTAIN}") if SUSTAIN > 0
  out.write(", release: item[:duration]*#{RELEASE}") if RELEASE > 0
  out.write("\n")
  out.write("    sleep sleeps#{idx}[i+1] if i+1 < sleeps#{idx}.length\n")
  out.write("  end\n")
  out.write("end\n\n")
end
out.close     