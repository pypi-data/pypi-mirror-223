import os
import subprocess
import sys
import time
from tempfile import SpooledTemporaryFile

import kthread
from ffmpegdevices import get_all_devices
from pydub import AudioSegment
from subprocess_alive import is_process_alive
from subprocesskiller import kill_process_children_parents


startupinfo = subprocess.STARTUPINFO()
creationflags = 0 | subprocess.CREATE_NO_WINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
}

deviceconfig = sys.modules[__name__]
deviceconfig.devices = {}
deviceconfig.devi = []


def create_spooledtempfile_with_content(f, content):
    f.seek(0)
    f.flush()
    f.seek(0)
    f.write(b"".join(content))
    f.seek(0)


def kill_ffmpeg(ffmprocproc: subprocess.Popen, t: kthread.KThread) -> None:
    try:
        # let's try to terminate it gracefully
        try:
            ffmprocproc.stdout.close()
        except Exception:
            pass
        try:
            ffmprocproc.stdin.close()
        except Exception:
            pass
        try:
            ffmprocproc.stderr.close()
        except Exception:
            pass
        try:
            ffmprocproc.wait(timeout=0.0001)
        except Exception:
            pass
        try:
            ffmprocproc.terminate()
        except Exception:
            pass
    except Exception:
        pass

    try:
        try:
            if t.is_alive():
                try:
                    t.kill()
                except Exception:
                    pass
        except Exception:
            pass
        if is_process_alive(ffmprocproc.pid):
            try:
                kill_process_children_parents(
                    pid=ffmprocproc.pid,
                    max_parent_exe="ffmpeg.exe",
                    dontkill=(
                        "Caption",
                        "conhost.exe",
                    ),
                )
            except Exception:
                pass
    except Exception:
        pass


def start_recording(
    ffmpegexe: str,
    audiodevice: tuple | int | str,
    silent_seconds_stop: int = 3,
    silence_threshold: int = -30,
) -> AudioSegment:
    r"""
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

    Example:
        from ffmpegaudiorecord import start_recording
        audio_data = start_recording(
        ffmpegexe = r"C:\ffmpeg\ffmpeg.exe", audiodevice=1, silent_seconds_stop=3, silence_threshold=-30)
        audio_data.export("c:\\bababababa.wav")
    """
    ffmpegexe = os.path.normpath(ffmpegexe)
    if not os.environ["PATH"].startswith(ffmpegexe):
        os.environ["PATH"] = ffmpegexe + ";" + os.environ["PATH"]

    if not deviceconfig.devices:
        deviceconfig.devices = get_all_devices(ffmpegexe)
        deviceconfig.devi = [
            (y[0],) + y[1]
            for y in enumerate(
                sorted(
                    [
                        (
                            deviceconfig.devices["audio"][x]["name"],
                            deviceconfig.devices["audio"][x]["alternative_name"],
                        )
                        for x in deviceconfig.devices["audio"]
                    ]
                )
            )
        ]
    try:
        virtualaudio = [
            x for x in deviceconfig.devi if audiodevice in x or x == audiodevice
        ][0][-1]
    except Exception as fe:
        sys.stderr.write("\n\n\nDevice no found! Select one of these:")
        for d in deviceconfig.devi:
            sys.stderr.write("\n" + str(d) + "\n")
        sys.stderr.write("\n\n\n")
        raise fe

    def start_ffmpeg():
        cmd = [
            f'"{ffmpegexe}"',
            "-loglevel",
            "-8",
            "-hide_banner",
            "-nostats",
            "-probesize",
            "32",
            "-analyzeduration",
            "0",
            "-y",
            "-nostdin",
            "-f",
            "dshow",
            "-i",
            f"audio={virtualaudio}",
            "-vn",
            "-c:a",
            "pcm_s16le",
            "-ar",
            "44100",
            "-ac",
            "2",
            "-f",
            "wav",
            "-",
        ]

        stderr = subprocess.DEVNULL
        start_new_session = True
        addproc.append(
            subprocess.Popen(
                " ".join(cmd),
                stdout=subprocess.PIPE,
                stderr=stderr,
                stdin=subprocess.DEVNULL,
                start_new_session=start_new_session,
                **invisibledict,
            )
        )

    addproc = []
    t = kthread.KThread(name=f"{time.time()}", target=start_ffmpeg)
    t.start()
    allreadbytes = []

    min_silence_len = 1240
    padding = 0
    didstart = False
    oldlen = 0
    start_second = 0
    f = SpooledTemporaryFile()
    firststarttime = 0
    loopsize = int(silent_seconds_stop)
    loopsizestart = 0
    totalduration = 0
    try:
        while True:
            try:
                allreadbytes.append(addproc[-1].stdout.read(22048 * 10))
                try:
                    create_spooledtempfile_with_content(f, content=allreadbytes)
                    audio_data = AudioSegment.from_file(
                        f, format="wav", start_second=start_second / 1000
                    )
                    audio_data2 = audio_data.strip_silence(
                        silence_len=min_silence_len,
                        silence_thresh=silence_threshold,
                        padding=padding,
                    )
                    audiolen = len(audio_data2)
                    audiolenraw = len(audio_data)

                    if audiolen > 0 and not didstart:
                        didstart = True
                        firststarttime = start_second

                    if oldlen > audiolen:
                        start_second = start_second + audiolenraw
                        totalduration = totalduration + audiolenraw
                        if loopsizestart >= loopsize:
                            kill_ffmpeg(ffmprocproc=addproc[-1], t=t)
                            break
                        else:
                            loopsizestart += 1
                            continue
                    else:
                        oldlen = audiolen

                        start_second = start_second + audiolenraw
                        if didstart:
                            totalduration = totalduration + audiolenraw
                        loopsizestart = 0

                except Exception:
                    continue
            except Exception:
                pass
    except KeyboardInterrupt:
        pass

    f.seek(0)

    audio_data = AudioSegment.from_file(
        f,
        format="wav",
        start_second=firststarttime / 1000,
        duration=((totalduration - (loopsize * 1000)) / 1000),
    )
    try:
        f.close()
    except Exception:
        pass
    return audio_data
