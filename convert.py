from pydub import AudioSegment

def process_wav(input_file, output_file):
    # Load the WAV file
    sound = AudioSegment.from_wav(input_file)

    # Set the sample rate to 44100 Hz and the bitrate to 16 bits
    sound = sound.set_frame_rate(44100).set_sample_width(2)

    # Convert stereo to mono
    sound = sound.set_channels(1)

    # Decrease the volume by 20 dB
    sound = sound - 20

    # Export the processed audio to a new WAV file
    sound.export(output_file, format="wav")

# Example usage
input_file = 'sample/ken.wav'
output_file = 'sample/output.wav'

process_wav(input_file, output_file)
