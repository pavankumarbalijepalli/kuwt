import os
from utils import log
import torchaudio as ta
from faster_whisper import WhisperModel
from kokoro import KPipeline
import soundfile as sf

# Load the Turbo model
tts = KPipeline(repo_id='hexgrad/Kokoro-82M', lang_code='a')
log("Chatterbox Turbo TTS model loaded")

whisper = WhisperModel(
    "medium",          # small / medium / large-v3
    device="cuda",     # or "cpu"
    compute_type="float16"
)
log("Whisper model loaded")

def generate_speech_with_subtitles(text, output_path, voice='af_bella'):
    try:
        generator = tts(text, voice=voice)
        seconds = 0
        for i, (gs, ps, audio) in enumerate(generator):
            sf.write(f'{output_path}/{i}.wav', audio, 24000)
            f = sf.SoundFile(f'{output_path}/{i}.wav')
            seconds += f.frames / f.samplerate
            log(f"Generated speech audio and saved to {output_path}")
            segments, info = whisper.transcribe(f'{output_path}/{i}.wav', word_timestamps=True)
            words = []
            for segment in segments:
                for word in segment.words:
                    words.append({
                        "word": word.word,
                        "start": round(word.start, 3),
                        "end": round(word.end, 3)
                    })
            srt = generate_srt(words, max_words=2)
            open(f"{output_path}/{i}.srt", "wb").write(srt.encode("utf-8"))
            log(f"Generated subtitles for {output_path} and saved to {output_path}/{i}.srt")
        return True, seconds
    except Exception as e:
        print(f"Error in generate_speech_with_subtitles: {e}")
        log(f"Error in generate_speech_with_subtitles: {e}")
        return False, None

def srt_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def generate_srt(words, max_words=2):
    """
    words = [
      {"word": "Hello", "start": 0.12, "end": 0.38},
      ...
    ]
    """
    srt = []
    index = 1
    buffer = []

    for w in words:
        buffer.append(w)

        if len(buffer) == max_words:
            start = buffer[0]["start"]
            end   = buffer[-1]["end"]
            text  = " ".join(x["word"] for x in buffer)

            srt.append(
                f"{index}\n"
                f"{srt_time(start)} --> {srt_time(end)}\n"
                f"{text.strip()}\n"
            )
            index += 1
            buffer = []

    # flush remaining words
    if buffer:
        start = buffer[0]["start"]
        end   = buffer[-1]["end"]
        text  = " ".join(x["word"] for x in buffer)

        srt.append(
            f"{index}\n"
            f"{srt_time(start)} --> {srt_time(end)}\n"
            f"{text}\n"
        )

    return "\n".join(srt)