# Getting Started — SVTRAF Dissertation

Run the SVTRAF framework notebooks locally or on Google Colab.

---

## 🚀 Option 1: Google Colab (Easiest — No Setup Required)

No installation needed. Open directly in your browser:

1. **Notebook 1 — Framework Definition**  
   https://colab.research.google.com/github/udhayakumar-palani/svtraf-dissertation/blob/main/notebooks/Notebook_1_Framework_Definition.ipynb

2. **Notebook 2 — Dataset Preparation**  
   https://colab.research.google.com/github/udhayakumar-palani/svtraf-dissertation/blob/main/notebooks/Notebook_2_Dataset_Preparation.ipynb

3. **Notebook 3 — Scoring Implementation**  
   https://colab.research.google.com/github/udhayakumar-palani/svtraf-dissertation/blob/main/notebooks/Notebook_3_Scoring_Implementation.ipynb

4. **Notebook 4 — Statistical Validation**  
   https://colab.research.google.com/github/udhayakumar-palani/svtraf-dissertation/blob/main/notebooks/Notebook_4_Statistical_Validation.ipynb

5. **Notebook 5 — Framework Comparison**  
   https://colab.research.google.com/github/udhayakumar-palani/svtraf-dissertation/blob/main/notebooks/Notebook_5_Framework_Comparison.ipynb

✅ Colab includes all dependencies; just click **Run All** in each notebook.

---

## 💻 Option 2: Local Setup

### Prerequisites
- **Python 3.9 or higher**
- **pip** (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/udhayakumar-palani/svtraf-dissertation.git
cd svtraf-dissertation
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- pandas, numpy, scipy (data science)
- matplotlib, seaborn (visualization)
- jupyter, notebook (Jupyter environment)

**Installation time:** ~2 minutes

### Step 4: Launch Jupyter
```bash
jupyter notebook
```

Then navigate to `svtraf-dissertation/notebooks/` and open notebooks in order:
1. Notebook_1_Framework_Definition.ipynb
2. Notebook_2_Dataset_Preparation.ipynb
3. Notebook_3_Scoring_Implementation.ipynb
4. Notebook_4_Statistical_Validation.ipynb
5. Notebook_5_Framework_Comparison.ipynb

---

## 🔄 Run All Notebooks Automatically

To execute all 5 notebooks in sequence with reproducible results:

```bash
bash run_notebooks.sh
```

**Expected output:**
- Updated `.ipynb` files with execution results
- Console logs for each notebook execution
- Total runtime: ~13 minutes

---

## 📊 Data & Documentation

### Explore the Dataset
The 150-contract dataset is at `svtraf-dissertation/data/svtraf_dataset.csv`

**Quick inspection:**
```bash
cd svtraf-dissertation/data
head svtraf_dataset.csv
```

**Full data dictionary:** See `svtraf-dissertation/data/README.md`

### Understand the Framework
- **Methodology:** `svtraf-dissertation/docs/METHODOLOGY.md`
- **Results Summary:** `svtraf-dissertation/docs/RESULTS.md`
- **Project README:** `svtraf-dissertation/README.md`

---

## ⚙️ Troubleshooting

### "Python not found" or "pip not found"
Ensure you have Python 3.9+ installed and in your PATH:
```bash
python3 --version
pip3 --version
```

If not, download from https://www.python.org/downloads/

### "ModuleNotFoundError: No module named 'X'"
Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Notebook runs slowly
- Colab is generally faster (uses Google's GPU)
- Locally, consider closing other applications
- Expected runtimes: ~13 minutes for all 5 notebooks on modern hardware

### Can't access Colab links
Ensure the repository is public on GitHub. Update the URLs with your GitHub username if you forked the repo:
```
https://colab.research.google.com/github/{YOUR_USERNAME}/svtraf-dissertation/blob/main/notebooks/...
```

---

## 📚 Next Steps

After running the notebooks:

1. **Review Results** → Examine generated tables and figures
2. **Validate Metrics** → Check NDCG, Spearman correlation, effect sizes
3. **Compare Frameworks** → See how SVTRAF compares to CVSS v3.1, BVSS, Ahmad et al.
4. **Read the Dissertation** → Full context in the main thesis document

---

## 🔗 Quick Links

- **GitHub Repository:** https://github.com/udhayakumar-palani/svtraf-dissertation
- **Dataset README:** `svtraf-dissertation/data/README.md`
- **Framework README:** `svtraf-dissertation/README.md`
- **Methodology:** `svtraf-dissertation/docs/METHODOLOGY.md`

---

## 📧 Questions?

For issues, feature requests, or questions about the SVTRAF framework, contact the author.

**Citation (APA):**
> Palani, U. (2026). SVTRAF: Structured Vulnerability Taxonomy and Risk Assessment Framework for Smart Contracts. *MSc Thesis*, National College of Ireland.

