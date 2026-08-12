import importlib
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_registry_declares_reproducible_fun_asr_nano_model():
    registry_path = ROOT / "registry/model/fun-asr-nano.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    spec = registry.get("fun-asr-nano-2512")

    assert spec is not None
    assert spec["class"] == "audio_evals.models.asr.fun_asr_nano.FunASRNano"
    assert spec["args"] == {
        "path": "FunAudioLLM/Fun-ASR-Nano-2512",
        "hub": "hf",
        "model_revision": "272c57b82523ada6fd87095e955f8e29100979ab",
        "device": "cuda:0",
        "env_path": "envs/fun_asr_nano",
        "requirements_path": "audio_evals/lib/FunASRNano/requirements.txt",
    }


def test_adapter_builds_worker_command_from_registry_options():
    module = importlib.import_module("audio_evals.models.asr.fun_asr_nano")
    model = object.__new__(module.FunASRNano)

    module.FunASRNano.__init__.__wrapped__(
        model,
        path="FunAudioLLM/Fun-ASR-Nano-2512",
        hub="hf",
        model_revision="revision-123",
        device="cuda:0",
    )

    assert model.command_args == {
        "path": "FunAudioLLM/Fun-ASR-Nano-2512",
        "hub": "hf",
        "model_revision": "revision-123",
        "device": "cuda:0",
    }


def test_adapter_request_uses_prompt_audio_and_language_override():
    module = importlib.import_module("audio_evals.models.asr.fun_asr_nano")

    request = module.build_request(
        {"audio": "/tmp/sample.wav", "language": "en"}, language="zh"
    )

    assert request == {"audio": "/tmp/sample.wav", "language": "en"}


def test_adapter_request_rejects_missing_audio():
    module = importlib.import_module("audio_evals.models.asr.fun_asr_nano")

    with pytest.raises(ValueError, match="audio"):
        module.build_request({"language": "zh"})


def test_adapter_exchanges_request_and_close_signal_with_worker():
    module = importlib.import_module("audio_evals.models.asr.fun_asr_nano")
    model = object.__new__(module.FunASRNano)
    worker_code = """
import json
import sys

request_line = sys.stdin.readline().strip()
prefix, payload = request_line.split("->", 1)
request = json.loads(payload)
assert request == {"audio": "/tmp/sample.wav", "language": "en"}
print(f"{prefix}->hello world", flush=True)
assert sys.stdin.readline().strip() == f"{prefix}->close"
"""
    model.process = subprocess.Popen(
        [sys.executable, "-u", "-c", worker_code],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        assert model._inference({"audio": "/tmp/sample.wav", "language": "en"}) == (
            "hello world"
        )
        assert model.process.wait(timeout=5) == 0
    finally:
        if model.process.poll() is None:
            model.process.terminate()
            model.process.wait(timeout=5)


def _load_worker_module():
    path = ROOT / "audio_evals/lib/FunASRNano/main.py"
    spec = importlib.util.spec_from_file_location("fun_asr_nano_worker", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_worker_returns_normalized_transcript():
    module = _load_worker_module()

    class FakeModel:
        def generate(self, **kwargs):
            assert kwargs == {"input": "/tmp/sample.wav", "language": "en"}
            return [{"text": "  hello\nworld  "}]

    assert module.transcribe(FakeModel(), "/tmp/sample.wav", "en") == "hello world"


def test_worker_rejects_empty_or_malformed_results():
    module = _load_worker_module()

    class EmptyModel:
        def generate(self, **kwargs):
            return []

    class MalformedModel:
        def generate(self, **kwargs):
            return [{"timestamp": []}]

    with pytest.raises(RuntimeError, match="no result"):
        module.transcribe(EmptyModel(), "/tmp/sample.wav")
    with pytest.raises(RuntimeError, match="text"):
        module.transcribe(MalformedModel(), "/tmp/sample.wav")
