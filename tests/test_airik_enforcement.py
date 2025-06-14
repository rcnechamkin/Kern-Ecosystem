# tests/test_airik_enforcement.py

import sys
from pathlib import Path
import pytest

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.airik_enforcer import verify_signature

def test_airik_enforcement_blocks_override(monkeypatch):
    """
    Ensure verify_signature fails if AIRIK is tampered with or missing.
    """

    # Simulate tampering: temporarily rename the AIRIK file
    airik_path = ROOT / "filing_cabinet/core/airik_manifesto_gpt.yaml"
    backup_path = airik_path.with_suffix(".tampered")

    if airik_path.exists():
        airik_path.rename(backup_path)

    # Test should now fail due to missing or invalid signature
    with pytest.raises(SystemExit):
        verify_signature()

    # Restore the original file
    backup_path.rename(airik_path)
