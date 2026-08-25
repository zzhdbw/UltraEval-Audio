import argparse
import json
import logging
import os
import select
import sys
import tempfile

import numpy as np
import soundfile as sf
import torch
import torchaudio


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _load_via_soundfile(path, *args, **kwargs):
    data, sample_rate = sf.read(str(path), dtype="float32", always_2d=True)
    return torch.from_numpy(data.T.copy()), sample_rate


def _save_via_soundfile(path, src, sample_rate, *args, **kwargs):
    array = (
        src.detach().to("cpu").float().numpy()
        if isinstance(src, torch.Tensor)
        else np.asarray(src, dtype="float32")
    )
    if array.ndim == 2:
        array = array.T
        if array.shape[1] == 1:
            array = array[:, 0]
    sf.write(str(path), array, sample_rate)


# The shared container's torchaudio backend can fail while loading FFmpeg.
# FireRedTTS3 only needs ordinary WAV I/O, so keep it on soundfile.
torchaudio.load = _load_via_soundfile
torchaudio.save = _save_via_soundfile


def _load_upstream(source_path):
    source_path = os.path.abspath(source_path)
    if source_path not in sys.path:
        sys.path.insert(0, source_path)

    from transformers import Qwen3Config

    original_init = Qwen3Config.__init__

    def init_with_sdpa(self, *args, **kwargs):
        kwargs["attn_implementation"] = "sdpa"
        original_init(self, *args, **kwargs)
        self._attn_implementation = "sdpa"
        self._attn_implementation_internal = "sdpa"

    Qwen3Config.__init__ = init_with_sdpa

    def force_sdpa(result):
        if isinstance(result, tuple):
            config, unused_kwargs = result
            config._attn_implementation = "sdpa"
            config._attn_implementation_internal = "sdpa"
            return config, unused_kwargs
        result._attn_implementation = "sdpa"
        result._attn_implementation_internal = "sdpa"
        return result

    original_from_dict = Qwen3Config.from_dict

    def from_dict_with_sdpa(cls, config_dict, **kwargs):
        return force_sdpa(original_from_dict(config_dict, **kwargs))

    Qwen3Config.from_dict = classmethod(from_dict_with_sdpa)

    original_from_pretrained = Qwen3Config.from_pretrained

    def from_pretrained_with_sdpa(cls, *args, **kwargs):
        return force_sdpa(original_from_pretrained(*args, **kwargs))

    Qwen3Config.from_pretrained = classmethod(from_pretrained_with_sdpa)

    from fireredtts3 import core
    from fireredtts3.llm import fireredtts3_base

    # The upstream config requests flash_attention_2 unconditionally.  SDPA is
    # the supported fallback in this isolated environment.
    fireredtts3_base.Qwen3_1_7B_ConfigDict["attn_implementation"] = "sdpa"
    return core


def _load_audio(path):
    audio, sample_rate = torchaudio.load(path)
    return audio, int(sample_rate)


def _write_audio(audio, sample_rate):
    if audio.ndim > 1:
        audio = audio.squeeze(0)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as output:
        output_path = output.name
    sf.write(output_path, audio.detach().float().cpu().numpy(), int(sample_rate))
    return output_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--mode", choices=["base", "instruct"], default="base")
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--use-wetext", action="store_true")
    args = parser.parse_args()

    if torch.cuda.is_available() and args.device.startswith("cuda"):
        torch.cuda.set_device(args.device)

    upstream = _load_upstream(args.source_path)
    if args.mode == "base":
        model = upstream.FireRedTTS3(
            args.path,
            use_wetext=args.use_wetext,
            use_llm_tn=False,
        )
    else:
        model = upstream.FireRedTTS3Instruct(
            args.path,
            use_wetext=args.use_wetext,
            use_llm_tn=False,
        )
    logger.info("FireRedTTS3 %s model loaded", args.mode)

    while True:
        try:
            request = input()
            anchor = request.find("->")
            if anchor < 0:
                print("Error: invalid request format", flush=True)
                continue
            prefix = request[:anchor].strip() + "->"
            payload = json.loads(request[anchor + 2 :])
            text = payload.pop("text")
            instruction = payload.pop("instruction", None)
            prompt_audio_path = payload.pop("prompt_audio", None)
            prompt_text = payload.pop("prompt_text", "")
            language = payload.pop("language", None)
            payload.pop("lang", None)

            if args.mode == "base":
                if not prompt_audio_path:
                    raise ValueError("prompt_audio is required for FireRedTTS3 Base")
                prompt_audio, prompt_audio_sr = _load_audio(prompt_audio_path)
                audio, sample_rate = model.generate(
                    text=text,
                    language=language,
                    prompt_text=prompt_text,
                    prompt_audio=prompt_audio,
                    prompt_audio_sr=prompt_audio_sr,
                    **payload,
                )
            elif prompt_audio_path and prompt_text:
                # ICL cloning ignores `instruction`; refuse rather than silently
                # dropping it, which would score as instruction-following.
                if instruction:
                    raise ValueError(
                        "instruction cannot be combined with prompt_audio + "
                        "prompt_text: FireRedTTS3 Instruct ICL cloning would "
                        "ignore it. Drop prompt_text to use voice design."
                    )
                prompt_audio, prompt_audio_sr = _load_audio(prompt_audio_path)
                audio, sample_rate = model.generate_tts(
                    prompt_text=prompt_text,
                    prompt_audio=prompt_audio,
                    prompt_audio_sr=prompt_audio_sr,
                    text=text,
                    language=language,
                    **payload,
                )
            else:
                if not instruction:
                    raise ValueError(
                        "instruction is required for FireRedTTS3 Instruct voice design"
                    )
                audio, sample_rate, _ = model.generate_voice_design(
                    instruction=instruction,
                    text=text,
                    language=language,
                    **payload,
                )

            output_path = _write_audio(audio, sample_rate)
            for _ in range(3):
                print(f"{prefix}{output_path}", flush=True)
                ready, _, _ = select.select([sys.stdin], [], [], 1)
                if ready and sys.stdin.readline().strip() == f"{prefix}close":
                    break
        except Exception as error:
            import traceback

            traceback.print_exc()
            print(f"Error: {error}", flush=True)


if __name__ == "__main__":
    main()
