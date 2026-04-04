import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>F9 Armory Security Executive Report</title>
    <style>
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 40px;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #ff00ff;
            padding-bottom: 20px;
            margin-bottom: 40px;
        }
        h1 { color: #0ffff0; text-transform: uppercase; letter-spacing: 2px; }
        h2 { color: #ff00ff; border-left: 4px solid #0ffff0; padding-left: 10px; margin-top: 40px; }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
            overflow-x: auto;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-box {
            background: #161b22;
            border-top: 3px solid #ff00ff;
            padding: 20px;
            text-align: center;
            border-radius: 4px;
        }
        .stat-number { font-size: 3em; font-weight: bold; color: #0ffff0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #30363d; }
        th { background-color: #21262d; color: #0ffff0; }
        .severity-critical { color: #f85149; font-weight: bold; }
        .severity-high { color: #d29922; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>F9 Armory</h1>
        <p>Executive Security & Misconfiguration Report</p>
    </div>

    <div class="stat-grid">
        <div class="stat-box">
            <div class="stat-number">{total_secrets}</div>
            <div>Exposed Secrets</div>
        </div>
        <div class="stat-box" style="border-top-color: #f85149;">
            <div class="stat-number" style="color: #f85149;">{total_critical_vulns}</div>
            <div>Critical Vulnerabilities</div>
        </div>
        <div class="stat-box" style="border-top-color: #d29922;">
            <div class="stat-number" style="color: #d29922;">{total_high_vulns}</div>
            <div>High Vulnerabilities</div>
        </div>
    </div>

    <h2>[+] Hardcoded Secrets Audit</h2>
    <div class="card">
        {secrets_table}
    </div>

    <h2>[+] IaC Misconfigurations</h2>
    <div class="card">
        {iac_table}
    </div>
</body>
</html>
"""

def generate_html_report(secrets_data: list, iac_data: dict, output_path: str = "F9-Executive-Report.html") -> str:
    """Generates the enterprise HTML report mapping the parsed data into pure styled HTML."""
    secrets_rows = ""
    for secret in secrets_data:
        file_path = f"{secret.get('File', 'Unknown')}:{secret.get('StartLine', '?')}"
        severity = secret.get('Severity', 'CRITICAL').upper()
        sev_class = "severity-critical" if severity in ["CRITICAL", "HIGH"] else "severity-high"
        
        raw_secret = secret.get("Secret", "")
        masked_secret = raw_secret[:3] + "..." + raw_secret[-3:] if len(raw_secret) > 6 else "***"
        
        secrets_rows += f"""<tr>
            <td>{file_path}</td>
            <td>{secret.get('RuleID', 'Unknown')}</td>
            <td><code>{masked_secret}</code></td>
            <td class="{sev_class}">{severity}</td>
        </tr>"""

    if not secrets_rows:
        secrets_table = "<p style='color: #2ea043; font-weight: bold;'>[+] Clean Directory. No secrets found.</p>"
    else:
        secrets_table = f"""<table>
            <tr><th>File Location</th><th>Rule</th><th>Secret (Redacted)</th><th>Severity</th></tr>
            {secrets_rows}
        </table>"""

    iac_rows = ""
    critical_count = 0
    high_count = 0
    
    if "Results" in iac_data:
        for res in iac_data.get("Results", []):
            target = res.get("Target", "Unknown File")
            for vuln in res.get("Misconfigurations", []):
                severity = vuln.get("Severity", "")
                if severity == "CRITICAL":
                    critical_count += 1
                    sev_class = "severity-critical"
                elif severity == "HIGH":
                    high_count += 1
                    sev_class = "severity-high"
                else:
                    continue
                    
                iac_rows += f"""<tr>
                    <td>{target}</td>
                    <td>{vuln.get('Type', 'Config')}</td>
                    <td>{vuln.get('Message', '')}</td>
                    <td class="{sev_class}">{severity}</td>
                </tr>"""

    if not iac_rows:
        iac_table = "<p style='color: #2ea043; font-weight: bold;'>[+] Secure Infrastructure. No HIGH or CRITICAL issues found.</p>"
    else:
        iac_table = f"""<table>
            <tr><th>Target File</th><th>Type</th><th>Issue</th><th>Severity</th></tr>
            {iac_rows}
        </table>"""

    html_content = HTML_TEMPLATE.format(
        total_secrets=len(secrets_data),
        total_critical_vulns=critical_count,
        total_high_vulns=high_count,
        secrets_table=secrets_table,
        iac_table=iac_table
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return output_path
