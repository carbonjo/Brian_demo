# Riemann Sums – Proof of Concept

Simple materials to explain Riemann Sums: notebook, LaTeX, Beamer, and an interactive Flask app.

## Contents

| File | Description |
|------|-------------|
| `riemann_sums.ipynb` | Jupyter notebook: formulas, code, and plots |
| `riemann_sums.tex` | LaTeX article on Riemann Sums |
| `riemann_sums_beamer.tex` | Beamer slides |
| `app.py` | Flask app: interactive Riemann Sum (f(x)=x²) |
| `requirements.txt` | Python dependencies |

## Jupyter notebook

```bash
jupyter notebook riemann_sums.ipynb
```

Requires: `numpy`, `matplotlib`

## LaTeX / Beamer

```bash
pdflatex riemann_sums.tex
pdflatex riemann_sums_beamer.tex
```

## Flask app

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 and adjust endpoints **a**, **b**, number of subintervals **n**, and method (Left / Right / Midpoint). The plot and sum update on submit.
