---
name: genpark-personal-agent-muscle-electromyography-root-mean-square-emg-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for evaluating surface electromyography (sEMG) RMS amplitude, percentage MVC, median frequency fatigue, and ergonomic muscular strain.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Surface Electromyography (sEMG) RMS Workload Skill

A sovereign personal agent capability for assessing skeletal muscle electrical activation (%MVC), evaluating static occupational workload thresholds (Jonsson model), and detecting spectral median frequency fatigue shifts.

## Core Capabilities
- **Percentage MVC Calculation**: Quantifies electrical activation relative to maximum voluntary contraction.
- **Jonsson Ergonomic Static Limits**: Assesses static postural loads to prevent chronic myofascial strain.
- **Spectral Fatigue Shift (MDF)**: Detects localized metabolic fatigue via downward compression of the median frequency spectrum.
- **Ergonomic Workstation Guidance**: Recommends armrest adjustments, wrist angles, and scheduled micro-pauses.

## Fast Invocation
```python
from client import MuscleElectromyographyClient

client = MuscleElectromyographyClient()
res = client.evaluate_emg_workload(
    emg_rms_amplitude_uv=14.5,
    mvc_reference_uv=320.0,
    muscle_group="UPPER_TRAPEZIUS"
)
print("Activation:", res["mvc_percentage"], "% MVC")
print("Strain Score:", res["neuromuscular_strain_score"])
```
