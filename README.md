# Surface Electromyography (sEMG) RMS Workload Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for non-invasive evaluation of surface electromyography (sEMG) RMS amplitude, percentage MVC, median frequency fatigue, and occupational ergonomics.

```mermaid
flowchart TD
    SurfaceElectrodes["Bipolar Surface EMG Electrodes"] --> RMS_Filter["RMS Sliding-Window & MVC Normalization"]
    RMS_Filter --> Spectrum["Fast Fourier / Median Frequency (MDF) Extraction"]
    Spectrum --> Jonsson["Jonsson Ergonomic Static Load Modeling"]
    Jonsson --> StrainEngine["Neuromuscular Ergonomic Strain Engine"]
    StrainEngine --> Agent["OpenClaw / Hermes Personal Agent Actions"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Biomechanical Ergonomics Standards**: Implements validated Jonsson static muscular load thresholds and %MVC normalization.
- **Spectral Fatigue Shift Detection**: Identifies localized intracellular acidification before subjective pain manifests.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import MuscleElectromyographyClient

client = MuscleElectromyographyClient()
result = client.evaluate_emg_workload(
    emg_rms_amplitude_uv=14.5,
    mvc_reference_uv=320.0,
    muscle_group="UPPER_TRAPEZIUS"
)
print("Activation:", result["mvc_percentage"], "% MVC")
print("Classification:", result["classification"])
```

## License
Apache-2.0
