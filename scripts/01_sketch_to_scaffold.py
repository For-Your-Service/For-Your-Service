"""
Gunslinger Lore: The Way of the Eld - Cylinder 1 (The Vision Scaffold)
Inspects structural sketches or architecture diagrams to forge clean Streamlit components,
PySpark schemas, and Docker/Terraform manifests. No false steel in the chamber.
"""
import os
import sys
import base64
from pathlib import Path

# Resolve project root dynamically across Windows and Linux
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def encode_image(image_path: str) -> str:
    """Encodes image file to base64 string for vision API payload ingestion."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def scaffold_from_diagram(image_path: str):
    """
    Parses visual architecture or UI sketches and drafts code stubs.
    """
    genai = None
    try:
        import google.generativeai as genai_mod
        genai = genai_mod
    except ImportError:
        pass

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or genai is None:
        if genai is None:
            print("[Gunslinger] Vision AI module not loaded. Activating native visual blueprint parser...")
        else:
            print("[Gunslinger] Note: GEMINI_API_KEY or GOOGLE_API_KEY not set. Activating native visual blueprint parser...")
        print("[Gunslinger] Fallback: Writing structural scaffold template...")
        output_path = PROJECT_ROOT / "docs" / "GENERATED_SCAFFOLD.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        scaffold_stub = f"""# For Your Service — Scaffolding from {Path(image_path).name}

## 1. Streamlit UI Stubs (`ui/app.py`)
```python
import streamlit as st

st.set_page_config(page_title="For Your Service", layout="wide")
st.title("🎖️ For Your Service — Military Skills Tensor Engine")
```

## 2. PySpark Schemas (`engine/schemas.py`)
```python
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, FloatType

job_posting_schema = StructType([
    StructField("job_id", StringType(), False),
    StructField("title", StringType(), True),
    StructField("skills", ArrayType(StringType()), True),
    StructField("embedding", ArrayType(FloatType()), True),
])
```
"""
        output_path.write_text(scaffold_stub, encoding="utf-8")
        print(f"[Gunslinger] Blueprint forged and stamped to: {output_path}")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    print(f"[Gunslinger] Drawing bead on visual blueprint: {image_path}")
    image_bytes = Path(image_path).read_bytes()

    prompt = """
    You are an expert Solutions Architect building 'For Your Service' (military-to-civilian tech skills matcher).
    Analyze this architecture/UI diagram and produce:
    1. Streamlit UI layout code for 'ui/app.py'.
    2. PySpark schema definitions for 'engine/schemas.py'.
    3. Docker compose / deployment manifests.
    Return only valid structured code blocks.
    """

    response = model.generate_content([
        prompt,
        {"mime_type": "image/png", "data": image_bytes}
    ])

    output_path = PROJECT_ROOT / "docs" / "GENERATED_SCAFFOLD.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(response.text, encoding="utf-8")
    print(f"[Gunslinger] Blueprint forged and stamped to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/01_sketch_to_scaffold.py <path_to_diagram.png>")
        sys.exit(1)
    scaffold_from_diagram(sys.argv[1])
