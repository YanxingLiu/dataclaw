from pathlib import Path


def test_export_shell_exists_and_contains_review_publish_flow():
    script = Path("shells/export.sh")
    assert script.exists()

    text = script.read_text()
    assert "dataclaw status" in text
    assert "dataclaw export --no-push" in text
    assert "dataclaw confirm" in text
    assert "--full-name" in text
    assert '--push' in text
    assert 'PUSH=false' in text
    assert 'FULL_NAME="${1:-Yanxing Liu}"' in text
    assert "liuyanxing98@foxmail.com" in text
    assert "YanxingLiu, lyx" in text
    assert "dataclaw export --publish-attestation" in text
    assert "read -r" in text
