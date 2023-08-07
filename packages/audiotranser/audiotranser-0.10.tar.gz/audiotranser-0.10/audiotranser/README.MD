# Transcribes audio files 

## pip install audiotranser 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

Uses the models from https://huggingface.co/ggerganov/whisper.cpp/tree/main

```python
    Args:
        inputfile: path to the input audio file
        small_large: model size (small or large)
        blas: use BLAS library for faster decoding
        silence_threshold: silence threshold in milliseconds
        min_silence_len: minimum silence length in milliseconds
        keep_silence: minimum silence length to keep after silence removal
        threads: number of threads to use
        processors: number of processors to use
        offset_t: time offset in milliseconds
        offset_n: segment index offset
        duration: duration of audio to process in milliseconds
        max_context: maximum number of text context tokens to store
        max_len: maximum segment length in characters
        best_of: number of best candidates to keep
        beam_size: beam size for beam search
        word_thold: word timestamp probability threshold
        entropy_thold: entropy threshold for decoder fail
        logprob_thold: log probability threshold for decoder fail
        speed_up: speed up audio by x2 (reduced accuracy)
        translate: translate from source language to english
        diarize: stereo audio diarization
        language: spoken language ('auto' for auto_detect)

    Returns:
        Pandas DataFrame with the results of the inference or the path to the output CSV file if pd.read_csv fails.

from audiotranser import transcribe_audio
df = transcribe_audio(
    inputfile=r"C:\untitled.wav",
    small_large="large",
    blas=True,
    silence_threshold=-30,  # ignored if == 0 or None
    min_silence_len=500,  # ignored if silence_threshold == 0 or None
    keep_silence=1000,  # ignored if silence_threshold == 0 or None
    threads=3,  # number of threads to use during computation
    processors=1,  # number of processors to use during computation
    offset_t=0,  # time offset in milliseconds
    offset_n=0,  # segment index offset
    duration=0,  # duration of audio to process in milliseconds
    max_context=-1,  # maximum number of text context tokens to store
    max_len=0,  # maximum segment length in characters
    best_of=5,  # number of best candidates to keep
    beam_size=-1,  # beam size for beam search
    word_thold=0.01,  # word timestamp probability threshold
    entropy_thold=2.40,  # entropy threshold for decoder fail
    logprob_thold=-1.00,  # log probability threshold for decoder fail
    speed_up=True,  # speed up audio by x2 (reduced accuracy)
    translate=False,  # translate from source language to english
    diarize=False,  # stereo audio diarization
    language="en",  # spoken language ('auto' for auto_detect)
)
print(df)
```