import subprocess
import json
from typing import Dict, Any, List

def run_trivy_scan(image_name: str) -> List[Dict[str, Any]]:
    """
    Runs trivy silently against an image and parses High/Critical vulnerabilities.
    Returns a list of vulnerability dictionaries.
    """
    try:
        result = subprocess.run(
            ["trivy", "image", "--format", "json", "--quiet", image_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Trivy can return exit codes even on success if findings exist.
        # But if there's no stdout and stderr has content, it's a fatal error.
        if result.returncode != 0 and not result.stdout.strip():
            raise RuntimeError(f"Trivy scan failed: {result.stderr}")
            
        if not result.stdout.strip():
            return []
            
        data = json.loads(result.stdout)
        
        high_critical = []
        if "Results" in data:
            for result_block in data["Results"]:
                target = result_block.get("Target", "Unknown Target")
                for vuln in result_block.get("Vulnerabilities", []):
                    severity = vuln.get("Severity", "")
                    if severity in ["HIGH", "CRITICAL"]:
                        # Safely grab Layer DiffID if available
                        layer = vuln.get("Layer", {}).get("DiffID", "Unknown Layer")
                        if layer.startswith("sha256:"):
                            layer = layer[7:22]
                            
                        high_critical.append({
                            "Layer ID": layer,
                            "Target": target,
                            "Vulnerability": vuln.get("VulnerabilityID", "Unknown"),
                            "Severity": severity,
                            "Fixed Version": vuln.get("FixedVersion", "Unpatched")
                        })
        return high_critical
        
    except FileNotFoundError:
        raise RuntimeError("Trivy is not installed or not found in system PATH. Please install it first.")
    except json.JSONDecodeError:
        raise RuntimeError("Failed to parse output. Ensure Trivy is functioning correctly.")
