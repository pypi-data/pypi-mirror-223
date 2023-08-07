import os
import subprocess
import tempfile
import pandas as pd
from pydub import AudioSegment
from pydub.silence import split_on_silence
from touchtouch import touch

filefolder = os.sep.join(__file__.split(os.sep)[:-1])
os.environ["HF_HOME"] = filefolder
os.environ["HUGGINGFACE_HUB_CACHE"] = filefolder
from huggingface_hub import hf_hub_download

hf_hub_download(repo_id="ggerganov/whisper.cpp", filename="ggml-small.bin")
hf_hub_download(repo_id="ggerganov/whisper.cpp", filename="ggml-large.bin")


def get_all_files(rootpath):
    all_files = []

    def _get_all_files(path):
        file_list = os.listdir(path)
        try:
            _ = [
                _get_all_files(fp)
                if os.path.isdir(fp := os.path.join(path, file))
                else all_files.append(fp)
                for file in file_list
            ]
        except PermissionError:
            pass

    _get_all_files(rootpath)
    return [os.path.normpath(f) for f in all_files]


rt = [x for x in get_all_files(filefolder) if os.path.islink(x)]
rt = {x.split(os.sep)[-1].split("-")[-1].split(".")[0].lower(): x for x in rt}


def read_audio_file(
    filename, silence_threshold=-30, min_silence_len=500, keep_silence=1000
):
    audio_data = AudioSegment.from_file(filename)
    if silence_threshold:
        non_silent_segments = split_on_silence(
            audio_data,
            min_silence_len=min_silence_len,
            silence_thresh=silence_threshold,
            keep_silence=keep_silence,
        )

        output_audio = non_silent_segments[0]
        for segment in non_silent_segments[1:]:
            output_audio += segment
    else:
        output_audio = audio_data

    num_channels = output_audio.channels
    sample_width = output_audio.sample_width
    frame_rate = output_audio.frame_rate

    return output_audio, num_channels, sample_width, frame_rate


def convert_sample_width(audio_data, sample_width, target_sample_width):
    audio = audio_data.set_frame_rate(target_sample_width)
    return audio


def concatenate_audio(audio_data1, audio_data2):
    combined_audio = audio_data1 + audio_data2
    return combined_audio


def convert_audio_files(
    audio_file_list,
    output_file,
    silence_threshold=-30,
    min_silence_len=500,
    keep_silence=1000,
    file_format="wav",
):
    audio_data1, num_channels1, sample_width1, frame_rate1 = read_audio_file(
        audio_file_list,
        silence_threshold=silence_threshold,
        min_silence_len=min_silence_len,
        keep_silence=keep_silence,
    )
    audio_data2 = convert_sample_width(audio_data1, sample_width1, 16000)

    audio_data2.export(output_file, format=file_format)


def get_tmpfile(suffix=".wav"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def transcribe_audio(
    inputfile: str,
    small_large: str = "small",
    blas: bool = True,
    silence_threshold: int | None = -30,  # ignored if == 0 or None
    min_silence_len: int | None = 500,  # ignored if silence_threshold == 0 or None
    keep_silence: int | None = 1000,  # ignored if silence_threshold == 0 or None
    threads: int = 4,  # number of threads to use during computation
    processors: int = 1,  # number of processors to use during computation
    offset_t: int = 0,  # time offset in milliseconds
    offset_n: int = 0,  # segment index offset
    duration: int = 0,  # duration of audio to process in milliseconds
    max_context: int = -1,  # maximum number of text context tokens to store
    max_len: int = 0,  # maximum segment length in characters
    best_of: int = 5,  # number of best candidates to keep
    beam_size: int = -1,  # beam size for beam search
    word_thold: float = 0.01,  # word timestamp probability threshold
    entropy_thold: float = 2.40,  # entropy threshold for decoder fail
    logprob_thold: float = -1.00,  # log probability threshold for decoder fail
    speed_up: bool = False,  # speed up audio by x2 (reduced accuracy)
    translate: bool = False,  # translate from source language to english
    diarize: bool = False,  # stereo audio diarization
    language: str = "auto",  # spoken language ('auto' for auto_detect)
) -> pd.DataFrame | str:
    r"""
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
    """
    model = rt[small_large.lower()]

    output_file = get_tmpfile(suffix=".wav")
    convert_audio_files(
        audio_file_list=inputfile,
        output_file=output_file,
        silence_threshold=silence_threshold,
        min_silence_len=min_silence_len,
        keep_silence=keep_silence,
        file_format="wav",
    )

    if blas:
        exefile = os.path.normpath(os.path.join(filefolder, "blasx64", "main.exe"))
    else:
        exefile = os.path.normpath(os.path.join(filefolder, "x64", "main.exe"))

    addtocommand = []
    if speed_up:
        addtocommand.append("""--speed-up""")
    if translate:
        addtocommand.append("""--translate""")
    if diarize:
        addtocommand.append("""--diarize""")

    cmdline = [
        exefile,
        """--threads""",
        f"""{threads}""",
        """--processors""",
        f"""{processors}""",
        """--offset-t""",
        f"""{offset_t}""",
        """--offset-n""",
        f"""{offset_n}""",
        """--duration""",
        f"""{duration}""",
        """--max-context""",
        f"""{max_context}""",
        """--max-len""",
        f"""{max_len}""",
        """--best-of""",
        f"""{best_of}""",
        """--beam-size""",
        f"""{beam_size}""",
        """--word-thold""",
        f"""{word_thold}""",
        """--entropy-thold""",
        f"""{entropy_thold}""",
        """--logprob-thold""",
        f"""{logprob_thold}""",
        *addtocommand,
        """--output-csv""",
        """--language""",
        f"""{language}""",
        """--model""",
        f"""{model}""",
        """--file""",
        f"""{output_file}""",
    ]
    subprocess.run(cmdline)
    try:
        df = pd.read_csv(
            output_file + ".csv",
            sep=",",
            engine="python",
            encoding_errors="backslashreplace",
            on_bad_lines="warn",
        )
        try:
            os.remove(output_file)
        except Exception:
            pass
        try:
            os.remove(output_file + ".csv")
        except Exception:
            pass
        return df
    except Exception:
        return output_file + ".csv"
