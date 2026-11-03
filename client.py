"""
Surface Electromyography (sEMG) RMS Amplitude & Neuromuscular Load Engine.
Provides deterministic, zero-dependency modeling of sEMG root-mean-square amplitude,
percentage of maximum voluntary contraction (%MVC), median frequency fatigue shifts, and ergonomic muscular strain.
"""

from typing import Dict, Any, List, Optional


class MuscleElectromyographyClient:
    """
    Deterministic client for calculating surface electromyography (sEMG) metrics.
    Assesses muscular electrical drive (%MVC), static postural load limits (Jonsson model),
    and spectral shift fatigue markers to optimize occupational ergonomics.
    """

    def __init__(self):
        pass

    def evaluate_emg_workload(
        self,
        emg_rms_amplitude_uv: float,
        mvc_reference_uv: float,
        median_frequency_hz: Optional[float] = None,
        muscle_group: str = "UPPER_TRAPEZIUS"
    ) -> Dict[str, Any]:
        """
        Calculates %MVC = (RMS / MVC) * 100.
        Jonsson ergonomic static load limits:
        - Continuous static load: <= 2% to 5% MVC
        - Median sustained load: <= 10% MVC
        - Peak intermittent load: <= 50% to 70% MVC
        """
        if emg_rms_amplitude_uv < 0 or mvc_reference_uv <= 0:
            return {"error": "EMG RMS must be non-negative and MVC reference strictly positive"}

        mvc_pct = round((emg_rms_amplitude_uv / mvc_reference_uv) * 100.0, 1)
        muscle = muscle_group.upper()

        # Neuromuscular Ergonomic Strain Score (0 - 100):
        # %MVC <= 6% with preserved median frequency -> 90 - 100
        # %MVC > 25% or median frequency < 58 Hz -> < 45
        if mvc_pct <= 5.0:
            score = 92.0 + (5.0 - mvc_pct) * 1.5
        elif mvc_pct <= 12.0:
            score = 78.0 + ((12.0 - mvc_pct) / 7.0) * 14.0
        elif mvc_pct <= 25.0:
            score = 55.0 + ((25.0 - mvc_pct) / 13.0) * 23.0
        else:
            score = max(5.0, 55.0 - (mvc_pct - 25.0) * 1.8)

        if median_frequency_hz is not None:
            if median_frequency_hz < 55.0:
                score = min(score, 40.0)
            elif median_frequency_hz < 65.0:
                score -= 10.0

        final_score = round(min(100.0, max(5.0, score)), 1)

        is_fatigued = median_frequency_hz is not None and median_frequency_hz < 60.0

        if mvc_pct <= 6.0 and not is_fatigued:
            tier = "OPTIMAL_ERGONOMIC_LOAD"
            interp = f"Ideal low-level muscular activity ({mvc_pct}% MVC) in {muscle}; within Jonsson static ergonomics safety envelope."
            guidance = "Optimal muscle tone with zero static fatigue accumulation. Maintain current neutral postural alignment."
        elif mvc_pct <= 14.0 and not is_fatigued:
            tier = "MODERATE_DYNAMIC_ENGAGEMENT"
            interp = f"Acceptable intermittent muscle engagement ({mvc_pct}% MVC) in {muscle}; normal task-related contraction."
            guidance = "Moderate load. Ensure muscles relax completely to baseline during pauses in typing/mouse activity."
        elif not is_fatigued:
            tier = "ELEVATED_STATIC_MUSCLE_TENSION"
            interp = f"Elevated sustained contraction ({mvc_pct}% MVC); exceeds recommended occupational static limits."
            guidance = "High static muscle load detected. Adjust armrests, lower keyboard tray, and drop shoulders to reduce trapezius tension."
        else:
            tier = "NEUROMUSCULAR_FATIGUE_OVERLOAD"
            interp = f"Significant spectral fatigue shift (MDF {median_frequency_hz} Hz < 60 Hz) and high load ({mvc_pct}% MVC) in {muscle}."
            guidance = "Acute neuromuscular fatigue and lactic acidification. Cease task for 5 minutes, stretch forearms/shoulders, and realign workstation."

        return {
            "muscle_group": muscle,
            "emg_rms_amplitude_uv": emg_rms_amplitude_uv,
            "mvc_reference_uv": mvc_reference_uv,
            "mvc_percentage": mvc_pct,
            "median_frequency_hz": median_frequency_hz,
            "neuromuscular_strain_score": final_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }
