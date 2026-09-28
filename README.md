# Revitalizing Indonesia's Labour-Intensive Industries

Code and source files for the paper *Revitalizing Indonesia's Labour-Intensive Industries: Textiles, Garments, and Footwear under Global Value Chain Pressure*.

The paper reviews the development and competitiveness of Indonesia's textile & garment and footwear industries: investment, trade, value-chain position, technology, workforce readiness, and the policies that support them. The rendered paper is [tekstil.pdf](tekstil.pdf).

This repo is maintained by [Krisna Gupta](mailto:krisna@dewanekonomi.go.id).

## Repository structure

| Path | Contents |
|---|---|
| `tekstil.qmd` | Paper source |
| `ref.bib`, `csl.csl` | Bibliography and citation style |
| `_extensions/den-econ/den-paper/` | DEN paper Quarto format (LaTeX template and class) |
| `fig/fig.ipynb` | Notebook that builds the data-driven figures |
| `fig/source_note.py` | Adds the source note to each figure; also stamps the static images |
| `fig/*.xlsx`, `fig/*_bps.csv` | Input data for the figures |
| `fig/raw/` | Static images from external sources (maps, diagrams), before the source note is added |

Each figure is saved twice: `<name>.png` with an English source note (used in the paper) and `<name>_id.png` with an Indonesian one.

## Requirements

- [Quarto](https://quarto.org) ≥ 1.2 and a TeX distribution with LuaLaTeX (e.g. TinyTeX: `quarto install tinytex`)
- Python 3 with `pandas`, `numpy`, `matplotlib`, `scipy`, `statsmodels`, `requests`, `openpyxl`, `Pillow` and Jupyter
- A BPS WebAPI key in the environment variable `BPS_API_KEY` (free registration at [webapi.bps.go.id](https://webapi.bps.go.id)). It is only needed to re-pull the quarterly GDP data.

## Reproducing the paper

From the repository root:

```bash
# 1. Figures from data (quarterly GDP is pulled live from the BPS WebAPI)
jupyter nbconvert --to notebook --execute --allow-errors --inplace fig/fig.ipynb

# 2. Static figures: add the source note to the images in fig/raw/
python fig/source_note.py

# 3. Render the paper
quarto render tekstil.qmd
```

Notes:

- The notebook saves the BPS data it pulls to `fig/pdb_growth_quarterly_bps.csv` and `fig/pdb_quarterly_bps.csv`. These files are snapshots of the data used in the paper. BPS may revise its figures, so a fresh pull can differ slightly.
- Table 1 (U.S. and EU import market shares) is computed from bilateral UN Comtrade data that is not redistributed here. Its notebook cell and the `fig2.png` cell (not used in the paper) fail without it, hence `--allow-errors` above. The other figures are unaffected.
- Figures in `fig/raw/` and `fig/textile_value_chain.png` come from external sources, cited in each figure. They have no generating code.

## Citation

```bibtex
@techreport{den2026tekstil,
  author      = {Nugroho, Ahmad and Tikahardinda, Annisa and Dhimathera, Artstein and Ramadhan, Gaffari and Gupta, Krisna and Safira, Latasha and Arifin, Shobrina and Ariyanda, Tiara},
  title       = {Revitalizing Indonesia's Labour-Intensive Industries: Textiles, Garments, and Footwear under Global Value Chain Pressure},
  institution = {Dewan Ekonomi Nasional},
  year        = {2026},
  url         = {https://github.com/den-econ/tekstil}
}
```

## License

All assets, code, and data in this repository are released under the **DEN License**. See [LICENSE](LICENSE).

*Copyright (c) 2026 Dewan Ekonomi Nasional Republik Indonesia (DEN)*
