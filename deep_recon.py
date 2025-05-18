# deep_recon.py

import os
import argparse
import subprocess
import shutil
import time
from fpdf import FPDF
from concurrent.futures import ThreadPoolExecutor, as_completed

# Output folder setup
os.makedirs("outputs/raw", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

TOOLS = {
    "subfinder": "subfinder",
    "amass": "amass",
    "theHarvester": "theHarvester",
    "whatweb": "whatweb",
    "nmap": "nmap",
    "rustscan": "rustscan",
    "nikto": "nikto",
    "wapiti": "wapiti",
    "nuclei": "nuclei",
    "wpscan": "wpscan",
    "gobuster": "gobuster",
    "cloud_enum": "cloud_enum.py",
    "aws_enum": "ScoutSuite",
    "gcp_enum": "gcp_scanner.py",
    "trufflehog": "trufflehog",
    "httpx": "httpx",
    "sslscan": "sslscan",
    "wafw00f": "wafw00f",
    "dnscan": "dnscan.py",
    "aquatone": "aquatone",
    "metabigor": "metabigor",
    "waybackurls": "waybackurls",
    "ffuf": "ffuf",
    "dirsearch": "dirsearch.py",
    "shcheck": "shcheck.py",
    "gitleaks": "gitleaks",
    "git-dumper": "git-dumper.py",
    "gau": "gau",
    "jsfinder": "jsfinder.py"
}

TOOL_DESCRIPTIONS = {
    "subfinder": "🔎 Finds subdomains of the target.",
    "amass": "🔬 Performs DNS enumeration to find subdomains.",
    "theHarvester": "🕵️ Gathers emails, subdomains, and names from public sources.",
    "whatweb": "🧠 Identifies web technologies used on the site.",
    "httpx": "📡 Checks HTTP response, status, and headers.",
    "nmap": "📊 Scans for open ports and services.",
    "rustscan": "⚡ Fast port scanner with service detection.",
    "sslscan": "🔐 Scans SSL/TLS configuration and certificates.",
    "nikto": "🛡️ Detects vulnerabilities in web servers.",
    "nuclei": "🚨 Detects known vulnerabilities using templates.",
    "wapiti": "🛠️ Performs web vulnerability scanning.",
    "wpscan": "📌 WordPress vulnerability scanner.",
    "trufflehog": "🔓 Searches for secrets and keys in code or files.",
    "cloud_enum": "☁️ Finds cloud storage misconfigurations.",
    "aws_enum": "🔐 Audits AWS account with ScoutSuite.",
    "gcp_enum": "🔐 Audits GCP environment.",
    "gobuster": "🔍 Directory brute-forcing.",
    "wafw00f": "🛡️ Detects Web Application Firewalls.",
    "dnscan": "🔍 DNS subdomain brute-forcing.",
    "aquatone": "📸 Take screenshots of websites.",
    "metabigor": "🌍 IP/ASN/Geolocation OSINT tool.",
    "waybackurls": "📜 Extract URLs from the Wayback Machine.",
    "ffuf": "🚀 Fast web fuzzer for discovering hidden endpoints.",
    "dirsearch": "📂 Brute force web paths and directories.",
    "shcheck": "🔒 Check HTTPS headers and best practices.",
    "gitleaks": "🔑 Scan for hardcoded secrets in Git repos.",
    "git-dumper": "📦 Dump exposed .git repositories.",
    "gau": "🧾 GetAllURLs from public sources like Wayback.",
    "jsfinder": "📜 Extract URLs/endpoints from JavaScript files."
}

# Tool installation checker (with basic version check if possible)
def check_tools():
    missing = []
    for tool, cmd in TOOLS.items():
        bin_name = cmd.split()[0]
        if shutil.which(bin_name) is None:
            missing.append(tool)
        else:
            print(f"✅ Found tool: {tool} ({bin_name})")
    return missing

# Attempt to install tools if missing
def install_tool(tool):
    print(f"⚙️ Installing missing tool: {tool}...")
    try:
        if tool in ["subfinder", "amass", "nuclei", "httpx", "gau", "waybackurls", "metabigor", "ffuf"]:
            subprocess.run(["go", "install", f"github.com/projectdiscovery/{tool}/v2/cmd/{tool}@latest"], check=True)
        elif tool == "theHarvester":
            subprocess.run(["pip3", "install", "--upgrade", "theHarvester"], check=True)
        elif tool in ["whatweb", "nmap", "nikto", "wapiti", "sslscan"]:
            subprocess.run(["sudo", "apt-get", "install", "-y", tool], check=True)
        elif tool == "wpscan":
            subprocess.run(["sudo", "gem", "install", "wpscan"], check=True)
        elif tool == "rustscan":
            subprocess.run(["sudo", "snap", "install", "rustscan"], check=True)
        elif tool in ["trufflehog", "wafw00f", "ScoutSuite"]:
            subprocess.run(["pip3", "install", "--upgrade", tool], check=True)
        elif tool in ["gitleaks"]:
            subprocess.run(["brew", "install", "gitleaks"], check=True)
        else:
            print(f"⚠️ Manual installation may be needed for: {tool}")
        print(f"✅ {tool} installed successfully.")
        return True
    except Exception as e:
        print(f"❌ Failed to install {tool}: {e}")
        return False
