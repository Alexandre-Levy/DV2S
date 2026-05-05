# D-V2S: From Driving Videos to Simulatable Scenarios

**[ITSC 2026]** | [Project Page](https://alexandre-levy.github.io/DV2S) | Paper (coming soon)

---

## Overview

**D-V2S** is a framework that automatically generates simulatable driving scenarios from real-world driving videos. It operates in two stages:

1. **Driving Record Analyzer (DRA)** — A Vision Language Model (VLM) with a carefully designed prompt analyzes an input driving video and produces a structured natural-language description of the scene, capturing road topology, traffic participants, and their interactions.

2. **Scenario Generator (SG)** — A Large Language Model (LLM) conditioned on a structured context translates the natural-language description into an executable simulation scenario.

Using simulations, we show that D-V2S generates scenarios where **90% of the relevant semantic elements** of the input videos are present. Our SG also achieves a **75% preference rate** over other state-of-the-art methods in a human evaluation.

<p align="center">
  <img src="assets/overview.png" alt="D-V2S Pipeline" width="800"/>
</p>

## Authors

- [Alexandre Levy](https://github.com/Alexandre-Levy) — Computer Vision Centre (CVC)
- [Ernest Valveny Llobet](https://www.cvc.uab.es/people/ernest-valveny/) — CVC / Universitat Autònoma de Barcelona
- [Antonio Manuel Lopez Peña](https://www.cvc.uab.es/people/antonio-lopez/) — CVC / Universitat Autònoma de Barcelona

## Code

Code will be released upon publication. Star this repo to be notified.

## Citation

If you find this work useful, please cite:

```bibtex
@inproceedings{levy2026dv2s,
  title     = {From Driving Videos to Simulatable Scenarios},
  author    = {Levy, Alexandre and Valveny Llobet, Ernest and Lopez Pe{\~n}a, Antonio Manuel},
  booktitle = {Proceedings of the IEEE International Conference on Intelligent Transportation Systems (ITSC)},
  year      = {2026}
}
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
