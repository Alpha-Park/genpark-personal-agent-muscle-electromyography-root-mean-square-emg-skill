"""
MCP Server for Surface Electromyography (sEMG) RMS Amplitude Skill.
Exposes JSON-RPC Model Context Protocol tools for evaluating muscular %MVC workload and fatigue spectral shifts.
"""

import sys
import json
from typing import Dict, Any
from client import MuscleElectromyographyClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_emg_workload",
                "description": "Calculates surface EMG percentage of Maximum Voluntary Contraction (%MVC), median frequency fatigue, and neuromuscular strain score.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "emg_rms_amplitude_uv": {
                            "type": "number",
                            "description": "Root-mean-square amplitude of surface EMG in microvolts (e.g. 18.0 uV)."
                        },
                        "mvc_reference_uv": {
                            "type": "number",
                            "description": "Maximum Voluntary Contraction (MVC) baseline amplitude in microvolts (e.g. 300.0 uV)."
                        },
                        "median_frequency_hz": {
                            "type": "number",
                            "description": "Optional median power frequency of the EMG spectrum in Hz (e.g. 78.0 Hz)."
                        },
                        "muscle_group": {
                            "type": "string",
                            "description": "Anatomical muscle group tested (e.g. UPPER_TRAPEZIUS, EXTENSOR_CARPI_RADIALIS).",
                            "default": "UPPER_TRAPEZIUS"
                        }
                    },
                    "required": ["emg_rms_amplitude_uv", "mvc_reference_uv"]
                }
            }
        ]
    }


def handle_request(client: MuscleElectromyographyClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_emg_workload":
            mdf = args.get("median_frequency_hz")
            if mdf is not None:
                mdf = float(mdf)

            res = client.evaluate_emg_workload(
                emg_rms_amplitude_uv=float(args.get("emg_rms_amplitude_uv", 15.0)),
                mvc_reference_uv=float(args.get("mvc_reference_uv", 300.0)),
                median_frequency_hz=mdf,
                muscle_group=str(args.get("muscle_group", "UPPER_TRAPEZIUS"))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method {name} not found"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": "Invalid request"
            }
        }


def main():
    client = MuscleElectromyographyClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
