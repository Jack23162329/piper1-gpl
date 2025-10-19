![Piper](etc/logo.png)

A fast and local neural text-to-speech engine that embeds [espeak-ng][] for phonemization.

Install with:

``` sh
pip install piper-tts
```

* 🎧 [Samples][samples]
* 💡 [Demo][demo]
* 🗣️ [Voices][voices]
* 🖥️ [Command-line interface][cli]
* 🌐 [Web server][api-http]
* 🐍 [Python API][api-python]
* 🔧 [C/C++ API][libpiper]
* 🏋️ [Training new voices][training]
* 🛠️ [Building manually][building]

---

People/projects using Piper:

* [Home Assistant](https://github.com/home-assistant/addons/blob/master/piper/README.md)
* [NVDA - NonVisual Desktop Access](https://www.nvaccess.org/post/in-process-8th-may-2023/#voices)
* [Image Captioning for the Visually Impaired and Blind: A Recipe for Low-Resource Languages](https://www.techrxiv.org/articles/preprint/Image_Captioning_for_the_Visually_Impaired_and_Blind_A_Recipe_for_Low-Resource_Languages/22133894)
* [Video tutorial by Thorsten Müller](https://youtu.be/rjq5eZoWWSo)
* [Open Voice Operating System](https://github.com/OpenVoiceOS/ovos-tts-plugin-piper)
* [JetsonGPT](https://github.com/shahizat/jetsonGPT)
* [LocalAI](https://github.com/go-skynet/LocalAI)
* [Lernstick EDU / EXAM: reading clipboard content aloud with language detection](https://lernstick.ch/)
* [Natural Speech - A plugin for Runelite, an OSRS Client](https://github.com/phyce/rl-natural-speech)
* [mintPiper](https://github.com/evuraan/mintPiper)
* [Vim-Piper](https://github.com/wolandark/vim-piper)
* [POTaTOS](https://www.youtube.com/watch?v=Dz95q6XYjwY)
* [Narration Studio](https://github.com/phyce/Narration-Studio)
* [Basic TTS](https://basictts.com/) - Simple online text-to-speech converter.

[![A library from the Open Home Foundation](https://www.openhomefoundation.org/badges/ohf-library.png)](https://www.openhomefoundation.org/)

<!-- Links -->
[espeak-ng]: https://github.com/espeak-ng/espeak-ng
[cli]: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md
[api-http]: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md
[api-python]: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_PYTHON.md
[training]: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/TRAINING.md
[building]: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/BUILDING.md
[voices]: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md
[samples]: https://rhasspy.github.io/piper-samples
[demo]: https://rhasspy.github.io/piper-samples/demo.html
[libpiper]: https://github.com/OHF-Voice/piper1-gpl/tree/main/libpiper



<!-- Training settings -->
Basically we follow the training guild, just modify some of the process, below is what you need to do inorder to train ur new voice with pytorch 2.9
1. follow the steps in training section and stop before started to train ur model, also if `python3 -m pip install -e .[train]` keep failing, use `pip install -e . [train] —timeout 1200 —retries 10 -v` instead.
2. train ur dataset (LJSpeech-1.1 for example) from zero for 1 round and get ur first checkpoints files, would be something like epoch=11-step=8856.ckpt
4. you need to do some extra works before training from pretrained checkpoints
- [download pretrained checkpoints]: https://huggingface.co/datasets/rhasspy/piper-checkpoints/tree/main/en/en_US
- use convert_ckpt2pt.py (inside merge/) to convert ur downloaded checkpoints into pure w&b file .pt
- use merge_weights_into_ckpt.py (inside merge/) to merge your own first checkpoint and pretrained .pt file into new checkpoint file.
``` sh
python3 merge_weight_into_ckpt.py [epoch=11-step=8856.ckpt](out first few checkpoint file) [epoch=6679-step=1554200.pt](pretrained w&b .pt file) [merged.ckpt](output file :inside runs/merged)
```
- we'll get and merged.ckpt checkpoint file and we can started to train from pretrained checkpoints, simply use the command from the training guild, and put the merged.ckpt inside --ckpt_path

<!-- Export onnx settings -->


