import librosa
import numpy as np
import av
from io import BytesIO


def wav2(i, o, format):
    inp = av.open(i, "r")
    if format == "m4a":
        format = "mp4"
    out = av.open(o, "w", format=format)
    if format == "ogg":
        format = "libvorbis"
    if format == "mp4":
        format = "aac"

    ostream = out.add_stream(format)

    for frame in inp.decode(audio=0):
        for p in ostream.encode(frame):
            out.mux(p)

    for p in ostream.encode(None):
        out.mux(p)

    out.close()
    inp.close()


def audio2(i, o, format, sr):
    inp = av.open(i, "r")
    out = av.open(o, "w", format=format)

    if format == "ogg":
        format = "libvorbis"
    if format == "f32le":
        format = "pcm_f32le"

    ostream = out.add_stream(format, rate=sr)

    for frame in inp.decode(audio=0):
        for p in ostream.encode(frame):
            out.mux(p)

    out.close()
    inp.close()


def load_audio(file, sr):
    try:
        file = (
            file.strip(" ")
            .strip('"')
            .strip("\n")
            .strip('"')
            .strip(" ")
        )

        audio, _ = librosa.load(
            file,
            sr=sr,
            mono=True,
        )
        audio, _ = librosa.load(file, sr=16000, mono=True)
        print(len(audio) / 16000)
        return audio.astype(np.float32)

    except AttributeError:
        audio = file[1] / 32768.0
        if len(audio.shape) == 2:
            audio = np.mean(audio, -1)
        return librosa.resample(
            audio,
            orig_sr=file[0],
            target_sr=16000,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to load audio: {e}")
