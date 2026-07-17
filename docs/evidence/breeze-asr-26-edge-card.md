---
license: apache-2.0
base_model: MediaTek-Research/Breeze-ASR-26
language:
- zh
- nan
pipeline_tag: automatic-speech-recognition
tags:
- whisper
- taiwanese-hokkien
- taigi
- onnx
- ctranslate2
- faster-whisper
- sherpa-onnx
- edge
- real-time
library_name: ctranslate2
---

# Breeze-ASR-26 — Edge Deployment Formats (INT8)

Quantized redistributions of [MediaTek-Research/Breeze-ASR-26](https://huggingface.co/MediaTek-Research/Breeze-ASR-26)
(Whisper-large-v2 fine-tuned for Taiwanese Hokkien / 台語) in **two runtime formats**,
plus a measured benchmark showing which one to pick.

We converted, quantized, and **measured** — the numbers below are from real
multi-speaker meeting audio, not synthetic clips.

## Which format should I use?

| | **CT2** (`ct2/`) | **ONNX** (`onnx/`) |
|---|---|---|
| Runtime | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) / CTranslate2 | [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) / onnxruntime |
| Size | 1.5 GB | 1.7 GB (encoder + decoder, single files each) |
| **RTF** (CPU, 4 threads) | **0.18 – 0.23** | 1.17 – 1.76 |
| Real-time capable on CPU | **Yes** | No |
| Platforms | Linux / macOS / Windows (x86, ARM) | + **Android / iOS / WASM / RPi** |
| Use it for | **Live captioning**, meeting transcription, servers | Mobile & browser, non-real-time edge |

**Short version:** use **CT2** unless you need mobile/WASM, where **ONNX** is the only option.

## Benchmark method (reproducible)

- **Audio:** 5 minutes of real Mandarin meeting audio (multi-speaker, spontaneous
  speech, crosstalk), 16 kHz mono, processed in full 30 s windows.
- **Hardware:** AMD/Intel desktop CPU, 4 threads, no GPU. `OMP_NUM_THREADS=4`.
- **RTF** = processing time ÷ audio duration. Lower is better; **< 1.0 is real-time**.

### Why the 6× gap

Whisper's decoder is autoregressive — it emits one token at a time and does not
parallelize. Thread count barely moves the needle (we measured 4/8/16 threads:
RTF 1.28 → 1.52 → 1.39 for ONNX, i.e. noise). CTranslate2 wins because of an
optimized KV-cache and fused kernels, not because of more cores.

**Beware of benchmarks on short clips.** Whisper pads every input to a 30 s
window, so a 2.5 s clip costs almost as much encoder time as a 30 s one. We
measured RTF 0.88 on 2.5 s clips and RTF 0.17 on a *repetitive* 30 s clip —
both misleading. Only dense, full-window speech gives an honest number.

### Transcription quality (same audio, same threads)

CT2 was also *more accurate*, not just faster:

| | Output |
|---|---|
| CT2 | 「你說就是去**客戶**那邊 **對對對** 就是**導入**這些…現在的**版圖**」 |
| ONNX | 「你說就是去**客**那邊 **對** 就是**投入**這些…現在的**版**」 |

## Notes on the base model's behaviour

Two properties worth knowing before you deploy (verified, not from the card):

1. **Mandarin does not regress.** Despite the Taigi fine-tune, transcription of
   pure Mandarin meetings is fully usable. A dual-model router (ASR-25 for
   Mandarin + ASR-26 for Taigi) is unnecessary in our tests.
2. **Taigi is transcribed as Mandarin *meaning*, not Taigi characters.** Verified
   against ground truth:

   | Ground truth (Taigi) | Model output (Mandarin) |
   |---|---|
   | 我沒咧驚 (guá bô leh kiann) | 我沒在怕 |
   | 無一下著 (bô tsi̍t-ē tio̍h) | 沒有一個對 |
   | 烏白試 (oo-pe̍h tshì) | 黑白試 |

   Semantics are right; the characters differ. This is by design (the base model
   card states it outputs Mandarin characters) and explains its ~30% CER on
   character-level Taigi benchmarks. **Good** for "understand the meeting";
   **not** a verbatim Taigi transcript — don't use it where the original wording
   is legally material.

## Usage

### CT2 / faster-whisper (recommended)

```python
from faster_whisper import WhisperModel

model = WhisperModel("weemed/Breeze-ASR-26-edge", device="cpu",
                     compute_type="int8", cpu_threads=4)   # subfolder: ct2/
segments, _ = model.transcribe("meeting.wav", language="zh", beam_size=1)
print("".join(s.text for s in segments))
```

### ONNX / sherpa-onnx (mobile, WASM, RPi)

```python
import sherpa_onnx

rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder="onnx/breeze-asr-26-large-v2-encoder.int8.onnx",
    decoder="onnx/breeze-asr-26-large-v2-decoder.int8.onnx",
    tokens="onnx/breeze-asr-26-large-v2-tokens.txt",
    language="zh", task="transcribe", num_threads=4)
```

### Live captioning architecture

Whisper is a 30-second batch model, not a streaming one. For live captions
(Google Meet / Teams / in-person):

```
system loopback + mic (separate tracks)
  → 16 kHz mono → VAD (silero, bundled with sherpa-onnx)
  → accumulate speech toward a full ~30 s window   ← don't send 2 s chunks:
  → CT2 transcribe                                    a short clip costs a full
  → caption overlay / transcript                      encoder pass anyway
```

Per-track capture gives you speaker separation for free (you vs. everyone else).

## Limitations

- **No code-switched (Mandarin↔Taigi within one utterance) evaluation.** We could
  not find a labelled public sample; the official benchmark ships *parallel*
  monolingual pairs, not code-switched audio. The base model's training data
  reportedly includes code-switching, but we have no measurement. **Open gap.**
- Base model trained on ~10,000 h of **synthetic** Taigi speech; real-world
  accents, far-field mics and crosstalk are out of that distribution.
- CER numbers here are not re-measured against the official benchmark; we report
  RTF and qualitative comparisons only.
- INT8 quantization is dynamic (MatMul only), matching sherpa-onnx conventions.

## License & attribution

Apache-2.0, inherited from the base model. All credit for the model itself goes
to **MediaTek Research**. This repo contributes only format conversion,
quantization and measurement.

Computation provided by the **Medical Image Processing Laboratory (MIPL),
National Yunlin University of Science and Technology**.
