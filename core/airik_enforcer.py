import sys
import yaml
import gnupg
from pathlib import Path

# === AIRIK Dependency Paths ===
AIRIK_PATH = Path("filing_cabinet/core/airik_manifesto.yaml")
SIG_PATH = AIRIK_PATH.with_suffix(".yaml.asc")
PUBKEY_PATH = Path("filing_cabinet/core/kern_pubkey.asc")

# === Load AIRIK Manifesto ===
def load_airik_manifesto():
    if not AIRIK_PATH.exists():
        sys.exit("AIRIK manifest missing. Kern cannot operate without it.")

    try:
        with open(AIRIK_PATH, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError:
        sys.exit("AIRIK manifest is malformed. YAML parsing failed.")

    if not data.get("airik_manifesto"):
        sys.exit("AIRIK structure invalid. Root key 'airik_manifesto' not found.")

    return data

# === Verify GPG Signature ===
def verify_signature():
    gpg = gnupg.GPG()

    if not PUBKEY_PATH.exists():
        sys.exit("Public key missing. AIRIK verification cannot proceed.")
    gpg.import_keys(PUBKEY_PATH.read_text())

    if not SIG_PATH.exists():
        sys.exit("AIRIK signature file missing. Kern cannot operate without verification.")

    with open(SIG_PATH, "rb") as sig_file:
        verified = gpg.verify_file(sig_file, str(AIRIK_PATH))

        if not verified:
            sys.exit("AIRIK signature invalid. File has been altered or forged.")
        if not verified.valid:
            sys.exit(f"Signature check failed: {verified.status or 'unknown error'}")

# === Enforce AIRIK Runtime ===
def enforce_airik():
    print("Enforcing AIRIK...")
    load_airik_manifesto()
    verify_signature()
    print("AIRIK manifest verified. System integrity confirmed.")

# === Optional: Run when script is called directly ===
if __name__ == "__main__":
    enforce_airik()
