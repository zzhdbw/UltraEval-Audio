# FireRedTTS3 评测结果 / Evaluation Results

**模型 / Model**: [fireredtts3-base / fireredtts3-instruct](../registry/model/fireredtts3.yaml) ([FireRedTeam/FireRedTTS3](https://huggingface.co/FireRedTeam/FireRedTTS3))
- `fireredtts3-base`：zero-shot 音色克隆；24 语 + 21 种中文方言
- `fireredtts3-instruct`：自然语言指令控制（voice design / speech editing）

**推理环境**: `envs/FireRedTTS3`
**官方结果来源**: [FireRedTTS3 README](https://github.com/FireRedTeam/FireRedTTS3)（技术报告尚未发布）
**结果目录**: `res/fireredtts3-base/`、`res/fireredtts3-instruct/`（`res/` 未纳入版本库）
**评测日期**: 2026/08/17 – 2026/08/22


**指标说明 / Metrics**:
- **WER⬇️ / CER⬇️**: ASR 识别错误率（越低越好）
- **SIM⬆️**: 说话人相似度（越高越好）
- **APS⬆️ / DSD⬆️ / RP⬆️**: InstructTTSEval 三类指令跟随准确率（%，越高越好）——APS 细粒度声学控制、DSD 描述性风格、RP 角色扮演/场景风格；judge 为 `gemini-2.5-pro`

---

## Seed-TTS-Eval Benchmark

格式为 `复现值(官方值)`。

| 数据集 | dataset | 样本数 | WER/CER⬇️ | SIM⬆️ | eval_cli | note |
|---|---|---:|---:|---:|---|---|
| SEED-test-en | `seed_tts_eval_en` | 1088 | 1.81 (1.64) | 77.20 (77.2) | [1] | EN WER 1.81 与用seed-tts-eval官方评测脚本复算结果一致，与官方 1.64 略有差异 |
| SEED-test-zh | `seed_tts_eval_zh` | 2020 | 0.95 (1.01) | 80.77 (80.9) | [2] |  |

---

## MiniMax TTS 多语言 Benchmark

> 来源数据集: [MiniMaxAI/TTS-Multilingual-Test-Set](https://huggingface.co/datasets/MiniMaxAI/TTS-Multilingual-Test-Set)，每语 100 条。
>
> 官方值来自 [FireRedTTS3 README](https://github.com/FireRedTeam/FireRedTTS3)。**注意**：FireRedTTS3 README 的 MiniMax 表对 Arabic、Hindi、Greek、Vietnamese 报的是 **CER**，但 [MiniMax-Speech 原论文](https://arxiv.org/abs/2505.07916) Table 2 **对所有 24 语统一报 WER**（Whisper-large-v3 ASR）。FireRedTTS3 README 自行将部分语种换为 CER 口径，与 MiniMax 原论文基准不一致。本仓库这四格走的是 Whisper WER，**与 MiniMax 原论文口径一致，但与 FireRedTTS3 README 的 CER 数字不可直接比较**，故不标注官方对照值。
>

| 语种 | dataset | WER/CER⬇️ | SIM⬆️ | eval_cli | note |
|---|---|:---:|:---:|---|---|
| Arabic | `minimax_tts_arabic` | 12.13 (WER, —) | 78.7 (78.9) | [3] | |
| Cantonese | `minimax_tts_cantonese` | 39.80 (40.32)  | 83.6 (83.9) | [4] | |
| Chinese | `minimax_tts_chinese` | 0.94 (0.91) | 83.9 (84.2) | [5] | |
| Czech | `minimax_tts_czech` | 3.53 (3.17) | 86.2 (86.1) | [6] | |
| Dutch | `minimax_tts_dutch` | 0.98 (1.15)  | 84.1 (84.3) | [7] | |
| English | `minimax_tts_english` | 2.17 (2.12) | 86.9 (86.8) | [8] | |
| Finnish | `minimax_tts_finnish` | 3.29 (3.10) | 89.9 (89.9) | [9] | |
| French | `minimax_tts_french` | 5.85 (5.28) | 80.6 (81.0) | [10] | |
| German | `minimax_tts_german` | 0.40 (0.69)  | 83.0 (83.3) | [11] | |
| Greek | `minimax_tts_greek` | 3.03 (WER, —) | 89.1 (89.3) | [12] | |
| Hindi | `minimax_tts_hindi` | 19.41 (WER, —) | 86.8 (87.2) | [13] | |
| Indonesian | `minimax_tts_indonesian` | 1.12 (1.42)  | 83.2 (83.3) | [14] | |
| Italian | `minimax_tts_italian` | 2.05 (2.28)  | 83.5 (83.6) | [15] | |
| Japanese | `minimax_tts_japanese` | 3.45 (3.60)  | 83.0 (82.8) | [16] | |
| Korean | `minimax_tts_korean` | 2.52 (2.42) | 86.8 (86.6) | [17] | |
| Polish | `minimax_tts_polish` | 0.99 (1.22)  | 89.7 (89.8) | [18] | |
| Portuguese | `minimax_tts_portuguese` | 1.73 (1.79)  | 86.4 (86.3) | [19] | |
| Romanian | `minimax_tts_romanian` | 2.62 (1.93) | 86.3 (86.2) | [20] | |
| Russian | `minimax_tts_russian` | 5.03 (3.28) | 84.6 (84.7) | [21] | |
| Spanish | `minimax_tts_spanish` | 1.15 (1.21)  | 86.3 (86.3) | [22] | |
| Thai | `minimax_tts_thai` | 2.16 (1.87) | 83.3 (83.3) | [23] | |
| Turkish | `minimax_tts_turkish` | 1.39 (0.92) | 86.8 (86.6) | [24] | |
| Ukrainian | `minimax_tts_ukrainian` | 0.68 (0.55) | 79.6 (79.8) | [25] | |
| Vietnamese | `minimax_tts_vietnamese` | 1.32 (WER, —) | 80.9 (81.3) | [26] | |


> **Arabic / Hindi / Greek / Vietnamese 说明**：FireRedTTS3 README 对这四格报的是 CER，但 [MiniMax-Speech 原论文](https://arxiv.org/abs/2505.07916) Table 2 对所有 24 语统一报 WER。本仓库走 Whisper WER，与 MiniMax 原论文口径一致，但与原论文基准（Arabic 1.67、Hindi 6.96、Greek 2.02、Vietnamese 0.88）仍有差距。本表不将 FireRedTTS3 README 的 CER 数字作为这四格的官方对照值。

---

## InstructTTSEval Benchmark (FireRedTTS3-Instruct)

> 数据集：[CaasiHUANG/InstructTTSEval](https://huggingface.co/datasets/CaasiHUANG/InstructTTSEval)，en/zh 各 1000 条，每条展开 APS / DSD / RP 三种指令 → 每个 split 3000 条评测行。集成对齐详见 [InstructTTSEval.md](InstructTTSEval.md)。
>
> 官方值取自 [FireRedTTS3 README](https://github.com/FireRedTeam/FireRedTTS3) 的 Instruct TTS 表（README 明确说明因 `gemini-2.5-pro-preview` 下线，全部系统改用 `gemini-2.5-pro` 打分，与本仓库 judge 一致）。README 未给 AVG，表中官方 AVG 为三项算术平均。格式为 `复现值(官方值)`。

| 数据集 | 样本数 | APS⬆️ | DSD⬆️ | RP⬆️ | AVG⬆️ | eval_cli | note |
|---|---:|---:|---:|---:|---:|---|---|
| `instruct-tts-eval-zh` | 1000 | 84.20 (85.8) −1.60 | 80.50 (82.0) −1.50 | 69.10 (69.7) −0.60 | **77.93 (79.17) −1.24** | [27] | |
| `instruct-tts-eval-en` | 999 | 79.48 (80.7) −1.22 | 82.28 (82.3) −0.02 | 66.77 (72.0) −5.23 | **76.18 (78.33) −2.15** | [28] | 999/1000：1 条未产出评测结果，`res/` 未纳入版本库，成因未追溯 |

---

## 评测配置

- **推理路径**：Base 走 zero-shot 音色克隆（参考音频 + 参考文本）；Instruct 走 voice design（文本 + 自然语言指令，不传参考音频）。
- **推理参数**（见 [registry/model/fireredtts3.yaml](../registry/model/fireredtts3.yaml)）：
  - `fireredtts3-base`：`stop_threshold=0.5`、`n_timesteps=10`、`inference_cfg=2.0`、`seed=1234`、`do_tn=true`
  - `fireredtts3-instruct`：`n_timesteps=10`、`inference_cfg=1.2`、`seed=2`
  - 两者均 `use_wetext=true`，隔离环境 `envs/FireRedTTS3`；上游 commit 由 wrapper 常量 `_UPSTREAM_COMMIT` 固定（[audio_evals/models/TTS/fireredtts3.py](../audio_evals/models/TTS/fireredtts3.py)）。
- **语种标签**：Base 的所有命令都显式指定 `--prompt fireredtts3-voice-clone-<language>`。这批 prompt 在默认 `voice-clone` 模板的基础上多传一个 `language` 字段，用于绕开上游的 fastText 自动语种检测——后者需要评测镜像未携带的 `lid.176.ftz`（见 [registry/prompt/fireredtts3.yaml](../registry/prompt/fireredtts3.yaml) 注释）。
- **评测后端**：
  - Seed-TTS-Eval / MiniMax 的 WER 用 `openai/whisper-large-v3`，中文改用 Paraformer（`speech_seaco_paraformer_large_asr_nat-zh-cn`）
  - SIM 用 `wavlm_large`（`simo` evaluator）
  - InstructTTSEval judge 用 `gemini-2.5-pro`

---

## Evaluation Commands

[1] `python audio_evals/main.py --dataset seed_tts_eval_en --model fireredtts3-base --prompt fireredtts3-voice-clone-english --two_phase --workers 1`

[2] `python audio_evals/main.py --dataset seed_tts_eval_zh --model fireredtts3-base --prompt fireredtts3-voice-clone-chinese --two_phase --workers 1`

[3] `python audio_evals/main.py --dataset minimax_tts_arabic --model fireredtts3-base --prompt fireredtts3-voice-clone-arabic --two_phase --workers 1`

[4] `python audio_evals/main.py --dataset minimax_tts_cantonese --model fireredtts3-base --prompt fireredtts3-voice-clone-cantonese --two_phase --workers 1`

[5] `python audio_evals/main.py --dataset minimax_tts_chinese --model fireredtts3-base --prompt fireredtts3-voice-clone-chinese --two_phase --workers 1`

[6] `python audio_evals/main.py --dataset minimax_tts_czech --model fireredtts3-base --prompt fireredtts3-voice-clone-czech --two_phase --workers 1`

[7] `python audio_evals/main.py --dataset minimax_tts_dutch --model fireredtts3-base --prompt fireredtts3-voice-clone-dutch --two_phase --workers 1`

[8] `python audio_evals/main.py --dataset minimax_tts_english --model fireredtts3-base --prompt fireredtts3-voice-clone-english --two_phase --workers 1`

[9] `python audio_evals/main.py --dataset minimax_tts_finnish --model fireredtts3-base --prompt fireredtts3-voice-clone-finnish --two_phase --workers 1`

[10] `python audio_evals/main.py --dataset minimax_tts_french --model fireredtts3-base --prompt fireredtts3-voice-clone-french --two_phase --workers 1`

[11] `python audio_evals/main.py --dataset minimax_tts_german --model fireredtts3-base --prompt fireredtts3-voice-clone-german --two_phase --workers 1`

[12] `python audio_evals/main.py --dataset minimax_tts_greek --model fireredtts3-base --prompt fireredtts3-voice-clone-greek --two_phase --workers 1`

[13] `python audio_evals/main.py --dataset minimax_tts_hindi --model fireredtts3-base --prompt fireredtts3-voice-clone-hindi --two_phase --workers 1`

[14] `python audio_evals/main.py --dataset minimax_tts_indonesian --model fireredtts3-base --prompt fireredtts3-voice-clone-indonesian --two_phase --workers 1`

[15] `python audio_evals/main.py --dataset minimax_tts_italian --model fireredtts3-base --prompt fireredtts3-voice-clone-italian --two_phase --workers 1`

[16] `python audio_evals/main.py --dataset minimax_tts_japanese --model fireredtts3-base --prompt fireredtts3-voice-clone-japanese --two_phase --workers 1`

[17] `python audio_evals/main.py --dataset minimax_tts_korean --model fireredtts3-base --prompt fireredtts3-voice-clone-korean --two_phase --workers 1`

[18] `python audio_evals/main.py --dataset minimax_tts_polish --model fireredtts3-base --prompt fireredtts3-voice-clone-polish --two_phase --workers 1`

[19] `python audio_evals/main.py --dataset minimax_tts_portuguese --model fireredtts3-base --prompt fireredtts3-voice-clone-portuguese --two_phase --workers 1`

[20] `python audio_evals/main.py --dataset minimax_tts_romanian --model fireredtts3-base --prompt fireredtts3-voice-clone-romanian --two_phase --workers 1`

[21] `python audio_evals/main.py --dataset minimax_tts_russian --model fireredtts3-base --prompt fireredtts3-voice-clone-russian --two_phase --workers 1`

[22] `python audio_evals/main.py --dataset minimax_tts_spanish --model fireredtts3-base --prompt fireredtts3-voice-clone-spanish --two_phase --workers 1`

[23] `python audio_evals/main.py --dataset minimax_tts_thai --model fireredtts3-base --prompt fireredtts3-voice-clone-thai --two_phase --workers 1`

[24] `python audio_evals/main.py --dataset minimax_tts_turkish --model fireredtts3-base --prompt fireredtts3-voice-clone-turkish --two_phase --workers 1`

[25] `python audio_evals/main.py --dataset minimax_tts_ukrainian --model fireredtts3-base --prompt fireredtts3-voice-clone-ukrainian --two_phase --workers 1`

[26] `python audio_evals/main.py --dataset minimax_tts_vietnamese --model fireredtts3-base --prompt fireredtts3-voice-clone-vietnamese --two_phase --workers 1`

[27] `export GOOGLE_API_KEY="<your-gemini-api-key>" && python audio_evals/main.py --dataset instruct-tts-eval-zh --model fireredtts3-instruct --workers 4`

[28] `export GOOGLE_API_KEY="<your-gemini-api-key>" && python audio_evals/main.py --dataset instruct-tts-eval-en --model fireredtts3-instruct --workers 4`
