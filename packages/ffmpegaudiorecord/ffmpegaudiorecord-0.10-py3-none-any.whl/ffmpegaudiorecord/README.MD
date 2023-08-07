# Starts recording audio from the specified device using ffmpeg and stops recording after a specified number of seconds of silence

## pip install ffmpegaudiorecord 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

```python
The function first checks to see if the ffmpegexe path is in the system path. If not, it adds the path to the system path.

Next, the function gets the list of available audio devices using the get_all_devices function from the
ffmpegdevices module. It then tries to find the audio device that matches the audiodevice argument.
If no match is found, the function raises an exception.

The function then starts a new ffmpeg process to record audio from the specified device.
It creates a temporary file to store the recorded audio.
The function then enters a loop that reads the recorded audio from the temporary file and checks for silence.
If the audio is silent for a specified number of seconds, the function stops recording and returns the recorded
audio as an AudioSegment object. Any silence at the beginning is ignored.

Args:
	ffmpegexe: The path to the ffmpeg executable.
	audiodevice: The ID or name of the audio device to record from.
	silent_seconds_stop: The number of seconds of silence after which recording will stop.
	silence_threshold: The audio level below which silence is considered to have occurred.

Returns:
	The recorded audio as an AudioSegment object.


from ffmpegaudiorecord import start_recording
audio_data = start_recording(
ffmpegexe = r"C:\ffmpeg\ffmpeg.exe", audiodevice=1, silent_seconds_stop=3, silence_threshold=-30)
audio_data.export("c:\\bababababa.wav")
```