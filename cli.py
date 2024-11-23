from core import full_inference_program
import sys, os
import argparse
import torch
import shutil
import unicodedata
import regex as re
from core import download_music

now_dir = os.getcwd()
sys.path.append(now_dir)

model_root = os.path.join(now_dir, "logs")
audio_root = os.path.join(now_dir, "audio_files", "original_files")

model_root_relative = os.path.relpath(model_root, now_dir)
audio_root_relative = os.path.relpath(audio_root, now_dir)

sup_audioext = {
    "wav",
    "mp3",
    "flac",
    "ogg",
    "opus",
    "m4a",
    "mp4",
    "aac",
    "alac",
    "wma",
    "aiff",
    "webm",
    "ac3",
}


def get_indexes():
    indexes_list = [
        os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk(model_root_relative)
        for filename in filenames
        if filename.endswith(".index") and "trained" not in filename
    ]
    return indexes_list if indexes_list else ""


def match_index(model_file_value):
    if model_file_value:
        model_folder = os.path.dirname(model_file_value)
        model_name = os.path.basename(model_file_value)
        index_files = get_indexes()
        pattern = r"^(.*?)_"
        match = re.match(pattern, model_name)
        for index_file in index_files:
            if os.path.dirname(index_file) == model_folder:
                return index_file
            elif match and match.group(1) in os.path.basename(index_file):
                return index_file
            elif model_name in os.path.basename(index_file):
                return index_file
    return ""


def get_number_of_gpus():
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        return "-".join(map(str, range(num_gpus)))
    else:
        return "-"


def format_title(title):
    formatted_title = (
        unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("utf-8")
    )
    formatted_title = re.sub(r"[\u2500-\u257F]+", "", formatted_title)
    formatted_title = re.sub(r"[^\w\s.-]", "", formatted_title)
    formatted_title = re.sub(r"\s+", "_", formatted_title)
    return formatted_title


def main():
    parser = argparse.ArgumentParser(description="RVC Voice Conversion CLI")

    # Required arguments
    parser.add_argument("--model", required=True, help="Path to voice model file")
    parser.add_argument("--index", help="Path to index file")
    parser.add_argument("--input", required=True, help="Input audio file path")

    # Optional arguments with defaults
    parser.add_argument(
        "--pitch", type=int, default=0, help="Pitch adjustment (-12 to 12)"
    )
    parser.add_argument(
        "--filter-radius", type=int, default=3, help="Filter radius (0-7)"
    )
    parser.add_argument(
        "--index-rate", type=float, default=0.75, help="Search feature ratio (0-1)"
    )
    parser.add_argument(
        "--rms-mix-rate",
        type=float,
        default=0.25,
        help="Volume envelope mix rate (0-1)",
    )
    parser.add_argument(
        "--protect",
        type=float,
        default=0.33,
        help="Protect voiceless consonants (0-0.5)",
    )
    parser.add_argument(
        "--pitch-extract",
        choices=["rmvpe", "crepe", "crepe-tiny", "fcp"],
        default="rmvpe",
    )
    parser.add_argument(
        "--device",
        default=get_number_of_gpus(),
        help="Device to use (e.g. '0' for GPU 0, '-' for CPU)",
    )
    parser.add_argument(
        "--output-format", choices=["WAV", "MP3", "FLAC", "OGG", "M4A"], default="WAV"
    )
    parser.add_argument("--autotune", action="store_true", help="Enable autotune")
    parser.add_argument(
        "--split-audio", action="store_true", help="Enable audio splitting"
    )

    args = parser.parse_args()

    # If no index file specified, try to match one
    if not args.index:
        args.index = match_index(args.model)

    # Call the inference function with CLI args
    result = full_inference_program(
        model_file=args.model,
        index_file=args.index,
        audio=args.input,
        output_path=os.path.join(now_dir, "audio_files", "rvc"),
        export_format_rvc=args.output_format,
        split_audio=args.split_audio,
        autotune=args.autotune,
        pitch=args.pitch,
        filter_radius=args.filter_radius,
        index_rate=args.index_rate,
        rms_mix_rate=args.rms_mix_rate,
        protect=args.protect,
        pitch_extract=args.pitch_extract,
        devices=args.device,
    )

    print(result)


if __name__ == "__main__":
    main()
