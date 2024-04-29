import wave

def loop_wav(input_file, output_file, n):
    # Open the input WAV file
    with wave.open(input_file, 'rb') as wav_in:
        # Get the parameters of the input WAV file
        params = wav_in.getparams()

        # Open the output WAV file for writing
        with wave.open(output_file, 'wb') as wav_out:
            # Set the parameters of the output WAV file
            wav_out.setparams(params)

            # Read and write the audio data 'n' times
            for _ in range(n):
                wav_in.rewind()  # Rewind the input file to the beginning
                data = wav_in.readframes(params.nframes)
                wav_out.writeframes(data)

# Example usage
input_file = 'sample/birds.wav'
output_file = 'sample/birds1.wav'
loop = 10  # Number of times to loop the WAV file

loop_wav(input_file, output_file, loop)
