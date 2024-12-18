import mido
import os
import sys

print("Quantize Midi Beats")


def check_is_divisible(lcd, values):
    for value in values:
        if value % lcd != 0:
            return False
    return True


mid = mido.MidiFile(sys.argv[1])
for track_idx, track in enumerate(mid.tracks):
    print(f"Track IDX: {track_idx}")

    messages_by_channel = {}

    for message_idx, message in enumerate(track):
        # print(f"Message: {message_idx}")
        # print(message)
        if message.type not in ('note_on', 'note_off'):
            continue

        # print(message.time)
        # print(message.type)
        # print(message.channel)
        # print(message.note)

        if message.channel not in messages_by_channel:
            messages_by_channel[message.channel] = [message]
        else:
            messages_by_channel[message.channel].append(message)

    for channel_messages in messages_by_channel.values():
        times = list(filter(lambda time: time > 1, map(lambda message: message.time, channel_messages)))
        times_sorted_unique = sorted(set(times))
        smallest_time = times_sorted_unique[0]
        print(times_sorted_unique)
        is_divisible = check_is_divisible(smallest_time, times_sorted_unique)
        print(is_divisible)
