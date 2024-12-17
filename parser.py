import mido
import os
import csv
import random
import operator

# --- MIDI Note to String Conversion ---

def note_to_string(note_number):
    """Converts a MIDI note number to a string representation (e.g., C#4, D5, etc.)."""
    if not 0 <= note_number <= 127:
        return "Invalid Note"  # Or handle it in some other way

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (note_number // 12)
    note_index = note_number % 12
    return f"{notes[note_index]}{octave}"

# --- String to MIDI Note Conversion ---
    
def string_to_note(note_string):
    """Converts a note string (e.g., C#4, D5) to a MIDI note number."""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    if not note_string:
        print("Error: Empty note string provided.")
        return None

    try:
        note_part = note_string[:-1]  # Extract note part (e.g., C, C#, D)
        octave_part = note_string[-1]  # Extract octave part (e.g., 4, 5)

        if not note_part or not octave_part:
            print(f"Error: Invalid note string format: '{note_string}'. Missing note or octave.")
            return None

        note_index = notes.index(note_part)
        octave = int(octave_part)
        note_number = note_index + (octave * 12)

        if 0 <= note_number <= 127:
            return note_number
        else:
            print(f"Error: Note number out of range (0-127): '{note_string}'.")
            return None

    except ValueError:
        print(f"Error: Invalid note string: '{note_string}'.")
        return None

# --- MIDI File Processing ---

def process_midi_file(file_path, output_csv_writer):
    """
    Processes a single MIDI file, extracts note data for each track, and writes to the CSV.
    """
    try:
        mid = mido.MidiFile(file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return

    for i, track in enumerate(mid.tracks):
        simplified_track = simplify_track(track)

        # Split into input/output sequences
        if len(simplified_track) >= 108:
          for _ in range(5):
            input_len = random.randint(8,32)
            start_index = random.randint(0, len(simplified_track) - (input_len + 100))
            input_sequence = simplified_track[start_index : start_index + input_len]
            output_sequence = simplified_track[start_index + input_len : start_index + input_len + 100]
            
            input_str = "|".join(input_sequence)
            output_str = "|".join(output_sequence)

            output_csv_writer.writerow([input_str, output_str])

# --- Track Simplification ---
def simplify_track(track):
    """
    Simplifies a MIDI track into the desired format: ON,time,note|OFF,time,note|...
    """
    simplified_events = []
    notes_on = {}  # Keep track of which notes are currently on

    full_notes = []
    current_time = 0

    for idx, msg in enumerate(track):
        if(msg.type not in ('note_on', 'note_off')):
            continue
        
        time = msg.time
        note = msg.note
      
        current_time += time

        if note in notes_on and msg.type == 'note_off':
            prior_note = notes_on[note]
            prior_note['duration'] = current_time - prior_note['time']
            full_notes.append(prior_note)
            notes_on.pop(note)
            # print("Note is on!")
        elif note not in notes_on and msg.type == 'note_on':
            # print("Adding to notes on")
            notes_on[note] = { 'time': current_time, 'note': note, 'on_msg': msg }

    full_notes = sorted(full_notes, key=operator.itemgetter('time'))

    if len(full_notes) == 0:
        return []

    start_time_offset = full_notes[0]['time']


    simplified_events = list(map(lambda note: f"{note_to_string(note['note'])}-{note['time'] - start_time_offset}-{note['duration']}", full_notes))
    print("|".join(simplified_events))
    return simplified_events

# --- Main Function ---

def main():
    midi_dir = "/Users/zachdicklin/Downloads/50000-MIDI-FILES"  # Replace with your directory of MIDI files
    output_csv = "midi_dataset.csv"

    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['input', 'output'])  # Header row

        for root, _, files in os.walk(midi_dir):
            for file in files:
                if file.endswith(".mid") or file.endswith(".midi"):
                    file_path = os.path.join(root, file)
                    print(f"Processing: {file_path}")
                    # try:
                    process_midi_file(file_path, csv_writer)
                    # except:
                    #     print("Failed for some reaosni")
                    exit()
if __name__ == "__main__":
    main()
