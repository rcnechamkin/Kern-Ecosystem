import sys
import yaml
import gnupg
from pathlib import Path

# === AIRIK Dependency Paths ===
# You can toggle this depending on whether you're enforcing full AIRIK or the compressed GPT version.
USE_GPT_MANIFEST = True

MANIFEST_FILENAME = "airik_manifesto_gpt.yaml" if USE_GPT_MANIFEST else "airik_manifesto.yaml"
AIRIK_PATH = Path(f"filing_cabinet/core/{MANIFEST_FILENAME}")
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

# === Metadata Presence Validation ===
def validate_metadata(data):
    metadata = data["airik_manifesto"].get("creator_signature", {})
    required_fields = ["name", "date", "digital_signature_required"]

    missing = [field for field in required_fields if field not in metadata]
    if missing:
        sys.exit(f"Metadata missing required field(s): {', '.join(missing)}")

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
    print(f"Enforcing AIRIK from {AIRIK_PATH.name}...")
    data = load_airik_manifesto()
    validate_metadata(data)
    verify_signature()
    print("AIRIK manifest verified. System integrity confirmed.")

# === Optional: Run when script is called directly ===
if __name__ == "__main__":
    enforce_airik()
