"""Stamp a source note at the bottom right of a figure.

Every figure in the paper is saved twice: ``<name>.png`` with "Source: ..." for the
English paper and ``<name>_id.png`` with "Sumber: ..." for the Indonesian papers.

- Matplotlib figures (fig.ipynb) go through ``save_with_source``.
- Static images with no generating code are kept untouched in ``raw/`` and stamped
  by running this file as a script (``python source_note.py``).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

NOTE_STYLE = dict(fontsize=9, style="italic", color="#555555")
GAP_IN = 0.08  # vertical gap between the lowest artist and the note (inches)


def _id_path(path):
    path = Path(path)
    return path.with_name(f"{path.stem}_id{path.suffix}")


def save_with_note(fig, path, text, dpi=300):
    """Save ``fig`` to ``path`` with ``text`` right-aligned below everything else drawn."""
    fig.canvas.draw()
    bbox = fig.get_tightbbox(fig.canvas.get_renderer())  # inches, includes legends/labels
    note = fig.text(bbox.x1 / fig.get_figwidth(), (bbox.y0 - GAP_IN) / fig.get_figheight(),
                    text, ha="right", va="top", **NOTE_STYLE)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    note.remove()
    print(f"Figure saved to: {path}")


def save_with_source(fig, path, source_en, source_id=None, dpi=300):
    """Save ``fig`` to ``path`` (English) and ``<path>_id`` (Indonesian) with a source note."""
    save_with_note(fig, path, f"Source: {source_en}", dpi)
    save_with_note(fig, _id_path(path), f"Sumber: {source_id or source_en}", dpi)


# ── Static images ────────────────────────────────────────────────────────────
# name: (English source, Indonesian source)
STATIC_SOURCES = {
    "map_textile": ("BPS, author's calculation.", "BPS, perhitungan penulis."),
    "footwear_supply_chain": ("Gereffi (1994); Stacey (2019).", "Gereffi (1994); Stacey (2019)."),
    "footwear_production_process": (
        "DEN (2025), based on site visits and interviews with footwear manufacturers.",
        "DEN (2025), berdasarkan kunjungan lapangan dan wawancara dengan manufaktur alas kaki.",
    ),
    "map_footwear": ("APRISINDO (2025); DEN analysis.", "APRISINDO (2025); analisis DEN."),
    "machinery_modernization": ("DEN, ITMF, Gherzi.", "DEN, ITMF, Gherzi."),
    "workforce_projection": ("Ministry of Manpower.", "Kementerian Ketenagakerjaan."),
    "investment_pipeline": ("DEN.", "DEN."),
    "licensing_time": ("DEN.", "DEN."),
}


def _italic_font(px):
    for name in ("DejaVuSans-Oblique.ttf", "ariali.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            pass
    from matplotlib import font_manager
    return ImageFont.truetype(font_manager.findfont("DejaVu Sans:italic"), px)


def stamp_image(src, out, text):
    """Append a white strip under ``src`` with ``text`` right-aligned, and save to ``out``."""
    img = Image.open(src).convert("RGB")
    w, h = img.size
    font = _italic_font(max(12, round(w * 0.013)))
    left, top, right, bottom = font.getbbox(text)
    pad = round(font.size * 0.6)
    canvas = Image.new("RGB", (w, h + (bottom - top) + 2 * pad), "white")
    canvas.paste(img, (0, 0))
    ImageDraw.Draw(canvas).text((w - pad - right, h + pad - top), text, font=font, fill="#555555")
    canvas.save(out, dpi=img.info.get("dpi", (300, 300)))


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, (en, id_) in STATIC_SOURCES.items():
        src = here / "raw" / f"{name}.png"
        stamp_image(src, here / f"{name}.png", f"Source: {en}")
        stamp_image(src, here / f"{name}_id.png", f"Sumber: {id_}")
        print(f"Stamped {name}.png and {name}_id.png")
