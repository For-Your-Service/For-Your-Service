# For Your Service — Scaffolding from architecture_sketch.png

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
