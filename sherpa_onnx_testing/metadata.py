#!/usr/bin/env python3
import json
import os
from typing import Any, Dict
import onnx


def add_meta_data(filename: str, meta_data: Dict[str, Any]):
    """Add metadata to an ONNX model (in-place)."""
    model = onnx.load(filename)
    for key, value in meta_data.items():
        meta = model.metadata_props.add()
        meta.key = key
        meta.value = str(value)
    onnx.save(model, filename)


def resolve_config_path(model_path: str) -> str:
    """
    Accepts either:
      - foo.onnx  -> try foo.json, then foo.onnx.json
      - foo       -> try foo.json
      - foo.json  -> return as-is
    """
    if model_path.endswith(".json"):
        return model_path

    base = model_path
    if model_path.endswith(".onnx"):
        base = model_path[:-5]  # strip ".onnx"

    cand1 = f"{base}.json"            # foo.json
    cand2 = f"{model_path}.json"      # foo.onnx.json

    if os.path.exists(cand1):
        return cand1
    if os.path.exists(cand2):
        return cand2
    raise FileNotFoundError(f"Cannot find config JSON: tried {cand1} and {cand2}")


def load_config(model_path: str) -> Dict[str, Any]:
    cfg_path = resolve_config_path(model_path)
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_tokens(config: Dict[str, Any], out_path: str = "tokens.txt"):
    id_map = config.get("phoneme_id_map", {})
    # output the sequence according ID, avoiding unstable sequence.
    sorted_items = sorted(id_map.items(), key=lambda kv: kv[1][0] if kv[1] else 1e18)
    with open(out_path, "w", encoding="utf-8") as f:
        for s, ids in sorted_items:
            idx = ids[0] if isinstance(ids, list) and ids else ids
            f.write(f"{s} {idx}\n")
    print(f"Generated {out_path} ({len(sorted_items)} tokens)")


LANG_MAP = {
    "en": "English",
    "en-us": "English (US)",
    "en-gb": "English (UK)",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "pt-br": "Portuguese (Brazil)",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
}


def guess_language_from_espeak(config: Dict[str, Any]) -> str:
    voice = config.get("espeak", {}).get("voice", "")
    # common format：en-us、en, fr、de etc. we only have en-us for now.
    code = (voice or "").strip().lower()
    if not code:
        return "unknown"
    if code in LANG_MAP:
        return LANG_MAP[code]
    major = code.split("-")[0]
    return LANG_MAP.get(major, code)


def main():
    # change to your model name here.
    filename = "en_US-ljspeech-medium.onnx"

    config = load_config(filename)

    print("generate tokens")
    generate_tokens(config)

    print("add model metadata")
    language = (
        config.get("language", {}).get("name_english")
        or guess_language_from_espeak(config)
    )

    meta_data = {
        "model_type": "vits",
        "comment": "piper",  # piper model use this one.
        "language": language,
        "voice": config.get("espeak", {}).get("voice", "unknown"),
        "has_espeak": 1,
        "n_speakers": config.get("num_speakers", 1),
        "sample_rate": config.get("audio", {}).get("sample_rate", 22050),
        # optional, just for more information
        "piper_version": config.get("piper_version", ""),
        "phoneme_type": config.get("phoneme_type", ""),
        "hop_length": config.get("hop_length", ""),
    }

    print(meta_data)
    add_meta_data(filename, meta_data)


if __name__ == "__main__":
    main()
