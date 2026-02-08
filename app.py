"""
Simple Flask app: interactive Riemann Sums for f(x) = x^2.
"""
from flask import Flask, render_template_string, request
import io
import base64
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)


def f(x):
    return x ** 2


def riemann_sum(a, b, n, method):
    dx = (b - a) / n
    if method == "left":
        x_star = np.linspace(a, b - dx, n)
    elif method == "right":
        x_star = np.linspace(a + dx, b, n)
    else:  # midpoint
        x_star = np.linspace(a + dx / 2, b - dx / 2, n)
    return float(np.sum(f(x_star) * dx))


def plot_riemann(a, b, n, method):
    dx = (b - a) / n
    if method == "left":
        x_star = np.linspace(a, b - dx, n)
    elif method == "right":
        x_star = np.linspace(a + dx, b, n)
    else:
        x_star = np.linspace(a + dx / 2, b - dx / 2, n)

    x_curve = np.linspace(a, b, 200)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_curve, f(x_curve), "b-", lw=2, label="$f(x)=x^2$")

    for i in range(n):
        if method == "left":
            x_left = a + i * dx
            ax.add_patch(
                plt.Rectangle((x_left, 0), dx, f(x_left), fill=True, alpha=0.5, edgecolor="gray")
            )
        elif method == "right":
            x_left = a + (i + 1) * dx - dx
            ax.add_patch(
                plt.Rectangle((x_left, 0), dx, f(x_left + dx), fill=True, alpha=0.5, edgecolor="gray")
            )
        else:
            x_left = a + i * dx
            x_mid = x_left + dx / 2
            ax.add_patch(
                plt.Rectangle((x_left, 0), dx, f(x_mid), fill=True, alpha=0.5, edgecolor="gray")
            )

    ax.set_xlim(a, b)
    ax.set_ylim(0, max(f(x_curve)) * 1.1)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f(x)$")
    ax.set_title(f"{method.capitalize()} Riemann Sum (n={n})")
    ax.legend()
    ax.grid(True, alpha=0.3)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Riemann Sums</title>
  <style>
    body { font-family: sans-serif; max-width: 700px; margin: 2em auto; padding: 0 1em; }
    h1 { color: #333; }
    form { background: #f5f5f5; padding: 1em; border-radius: 8px; margin-bottom: 1em; }
    label { display: inline-block; width: 120px; }
    input, select { margin: 4px 0; }
    button { background: #2563eb; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; }
    button:hover { background: #1d4ed8; }
    .result { margin-top: 1em; }
    .result img { max-width: 100%; height: auto; }
    .info { color: #666; font-size: 0.95em; margin-top: 0.5em; }
  </style>
</head>
<body>
  <h1>Riemann Sums</h1>
  <p>Approximate &int;<sub>a</sub><sup>b</sup> x&sup2; dx using rectangles. Choose method and number of subintervals.</p>
  <form method="get" action="/">
    <label>Left endpoint a:</label> <input type="number" name="a" value="{{ a }}" step="0.1" /><br>
    <label>Right endpoint b:</label> <input type="number" name="b" value="{{ b }}" step="0.1" /><br>
    <label>Subintervals n:</label> <input type="number" name="n" value="{{ n }}" min="1" max="100" /><br>
    <label>Method:</label>
    <select name="method">
      <option value="left" {{ 'selected' if method == 'left' else '' }}>Left</option>
      <option value="right" {{ 'selected' if method == 'right' else '' }}>Right</option>
      <option value="midpoint" {{ 'selected' if method == 'midpoint' else '' }}>Midpoint</option>
    </select><br>
    <button type="submit">Update</button>
  </form>
  {% if plot_b64 %}
  <div class="result">
    <img src="data:image/png;base64,{{ plot_b64 }}" alt="Riemann sum plot" />
    <p class="info">Sum = {{ sum_val }} &nbsp;|&nbsp; Exact &int;x&sup2; dx = (b&sup3;&minus;a&sup3)/3 = {{ exact }}</p>
  </div>
  {% endif %}
</body>
</html>
"""


@app.route("/")
def index():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 2))
    n = int(request.args.get("n", 8))
    method = request.args.get("method", "left")
    if n < 1:
        n = 1
    if n > 100:
        n = 100
    if b <= a:
        b = a + 1

    plot_b64 = None
    sum_val = None
    exact = None
    if request.args:
        sum_val = round(riemann_sum(a, b, n, method), 4)
        exact = round((b**3 - a**3) / 3, 4)
        plot_b64 = plot_riemann(a, b, n, method)

    return render_template_string(
        HTML,
        a=a, b=b, n=n, method=method,
        plot_b64=plot_b64, sum_val=sum_val, exact=exact,
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
