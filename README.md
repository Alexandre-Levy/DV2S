# From Driving Videos to Simulatable Scenarios

*D-V2S: Driving Video to Scenario*

**[ITSC 2026]** | [Project Page](https://alexandre-levy.github.io/DV2S.github.io/) | Paper (coming soon) | Code (coming soon)

---

## Authors

- [Alexandre Levy](https://scholar.google.com/citations?user=Um9rfMwAAAAJ&hl=en)<sup>1,2</sup>
- [Ernest Valveny Llobet](https://scholar.google.com/citations?user=ChmX8ogAAAAJ&hl=en)<sup>1,2</sup>
- [Antonio Manuel Lopez Peña](https://scholar.google.com/citations?user=3LYW1zMAAAAJ&hl=es)<sup>1,2</sup>

<sup>1</sup>Computer Vision Centre (CVC) &nbsp; <sup>2</sup>Dept. Computer Science, Universitat Autònoma de Barcelona (UAB)

---

## Abstract

Autonomous vehicles (AVs) face driving scenarios ranging from routine traffic to rare events. To assess safety it is crucial to reproduce these scenarios in a controllable, repeatable, and scalable manner, with simulation playing a key role. This paper introduces D-V2S, a novel framework that automatically generates simulatable driving scenarios from driving videos. D-V2S operates in two stages: a Driving Record Analyzer (DRA) uses a vision language model (VLM) with our designed prompt to produce natural-language descriptions from input videos, capturing road layouts and dynamic traffic interactions; subsequently, a Scenario Generator (SG) uses a large language model (LLM) and our conditioning context to translate these descriptions into executable scenarios. Using simulations, we show that D-V2S generates scenarios where 90% of the relevant semantic elements of the videos are present. We also provide qualitative results demonstrating D-V2S's capability to transform real-world driving videos into simulatable scenarios. Moreover, we provide both semantic and human driven ablative analyses of D-V2S's modules. In particular, we show how the VLM choice matters for DRA, and how our SG achieves a 75% preference rate over other state-of-the-art methods.

<p align="center">
  <img src="imgs/paper_xai_flow.png" alt="D-V2S Pipeline" width="800"/>
</p>

---

<p align="center">
  <video src="videos/DV2S.mp4" controls autoplay muted loop width="800"></video>
</p>

---

## Citation

```bibtex
@inproceedings{levy2026dv2s,
  title     = {From Driving Videos to Simulatable Scenarios},
  author    = {Levy, Alexandre and Valveny Llobet, Ernest and López, Antonio M.},
  booktitle = {Intelligent Transportation Systems Conference (ITSC)},
  year      = {2026}
}
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
