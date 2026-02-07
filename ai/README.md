# 🤖 AI Modules

OCR and homework analysis powered by machine learning.

## Structure

```
ai/
├── ocr/                      # Optical Character Recognition
│   ├── models/              # Trained OCR models
│   │   ├── handwriting/    # Handwriting recognition models
│   │   └── printed/        # Printed text models
│   └── processors/          # Image preprocessing
│       ├── preprocessing.py # Image cleanup, enhancement
│       └── extraction.py    # Text extraction logic
├── analysis/                 # Homework Analysis
│   ├── models/              # Analysis models
│   │   ├── grading/        # Auto-grading models
│   │   ├── plagiarism/     # Plagiarism detection
│   │   └── feedback/       # Auto-feedback generation
│   └── processors/          # Analysis processors
│       ├── similarity.py   # Similarity checking
│       └── scoring.py      # Automated scoring
├── training/                 # Model training
│   ├── datasets/           # Training datasets
│   │   ├── handwriting/   # Handwriting samples
│   │   └── homework/      # Homework samples
│   └── scripts/            # Training scripts
│       ├── train_ocr.py
│       └── train_analysis.py
├── utils/                    # Shared utilities
│   ├── image_utils.py
│   └── model_utils.py
├── requirements.txt
└── config.py
```

## Capabilities

| Module | Purpose |
|--------|---------|
| OCR | Convert handwritten/printed homework to text |
| Grading | Suggest grades based on content analysis |
| Plagiarism | Detect copied content |
| Feedback | Generate improvement suggestions |

## Usage

```python
from ai.ocr.processors import extract_text
from ai.analysis.processors import analyze_homework

text = extract_text(image_path)
analysis = analyze_homework(text, rubric)
```

## Model Training

```bash
python training/scripts/train_ocr.py --dataset handwriting
python training/scripts/train_analysis.py --task grading
```
