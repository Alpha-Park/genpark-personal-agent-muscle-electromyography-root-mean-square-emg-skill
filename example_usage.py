"""
Example Usage: Surface Electromyography (sEMG) RMS Amplitude & Load Evaluation.
Demonstrates calculation of %MVC activation and median frequency fatigue tracking.
"""

from client import MuscleElectromyographyClient


def main():
    client = MuscleElectromyographyClient()
    print("=== Surface Electromyography (sEMG) Ergonomic Load Demo ===")

    # Test Case 1: Ergonomically sound computer typing (Upper Trapezius)
    res1 = client.evaluate_emg_workload(
        emg_rms_amplitude_uv=14.5,
        mvc_reference_uv=320.0,
        median_frequency_hz=82.0,
        muscle_group="UPPER_TRAPEZIUS"
    )
    print("\nTest Case 1: Healthy Ergonomic Typing (Upper Trapezius)")
    print(f"  Muscle: {res1['muscle_group']} | RMS: {res1['emg_rms_amplitude_uv']} uV | MVC Ref: {res1['mvc_reference_uv']} uV")
    print(f"  Activation: {res1['mvc_percentage']}% MVC | Median Frequency: {res1['median_frequency_hz']} Hz")
    print(f"  Neuromuscular Strain Score: {res1['neuromuscular_strain_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Guidance: {res1['actionable_guidance']}")

    # Test Case 2: Excessive static strain & fatigue overload (Forearm extensor carpi radialis)
    res2 = client.evaluate_emg_workload(
        emg_rms_amplitude_uv=78.0,
        mvc_reference_uv=260.0,
        median_frequency_hz=54.0,
        muscle_group="EXTENSOR_CARPI_RADIALIS"
    )
    print("\nTest Case 2: Static Strain & Fatigue (Extensor Carpi Radialis)")
    print(f"  Activation: {res2['mvc_percentage']}% MVC | Median Frequency: {res2['median_frequency_hz']} Hz")
    print(f"  Strain Score: {res2['neuromuscular_strain_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Guidance: {res2['actionable_guidance']}")


if __name__ == "__main__":
    main()
