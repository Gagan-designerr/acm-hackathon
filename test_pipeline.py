"""
Verification test script for KalaSetu components.
"""
from pathlib import Path
from PIL import Image
import app

def test_all():
    print("--- 1. Testing Image Assets & Resizing ---")
    for key, data in app.IMAGE_REGISTRY.items():
        img = app.load_image_asset(data["path"])
        assert img is not None, f"Failed to load image for {key} from {data['path']}"
        resized = app.resize_image_for_gemini(img, max_dim=800)
        assert resized.size[0] <= 800 and resized.size[1] <= 800
        print(f"  [OK] {key} ({data['title']}): original={img.size}, resized={resized.size}")

    print("\n--- 2. Testing Curated Demo Analysis Fallbacks ---")
    for key in ["IMAGE_SET_1", "IMAGE_SET_2", "IMAGE_SET_3", "IMAGE_SET_4"]:
        res, is_demo, msg = app.analyze_scene_image(None, None, "Auto Detect", "Devi Mahatme", preset_key=key)
        assert res is not None
        assert is_demo is True
        assert "art_form" in res
        assert "breakdown" in res
        assert "mudra_detection" in res
        print(f"  [OK] {key}: Art Form = {res.get('art_form')}, Confidence = {res.get('confidence')}%, Mudra = {res.get('mudra_detection', {}).get('name')}")

    print("\n--- 3. Testing Dynamic QR Code Generation ---")
    qr_img = app.generate_stage_qr("http://localhost:8501/?stage=kateel_mela")
    assert qr_img is not None
    assert isinstance(qr_img, Image.Image)
    print(f"  [OK] Venue QR generated with size {qr_img.size} and editorial color palette.")

    print("\n--- 4. Testing Cultural AI Copilot Offline ---")
    queries = [
        "What is the difference between Badagutittu and Tenkutittu?",
        "What is Aramandi in Bharatanatyam?",
        "Why do Yakshagana demons wear artificial fangs?"
    ]
    for q in queries:
        ans, sources, is_offline = app.ask_cultural_copilot(None, q)
        assert len(ans) > 20
        assert len(sources) > 0
        print(f"  [OK] Q: {q[:35]}... -> Answered with {len(sources)} verified source(s)")

    print("\n[SUCCESS] ALL 4 KALASETU PIPELINE INTEGRATION TESTS PASSED 100%!")

if __name__ == "__main__":
    test_all()
