# LangGraph Learning

A learning project for langgraph.

Use ModelScope to download models

```
uv run modelscope download --model "model_name" --local_dir ./dir_path
```

load model with path
```
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("download_path")
```