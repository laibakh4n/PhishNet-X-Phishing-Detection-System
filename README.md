# 🛡️ PhishNet-X
### Context-Aware & Adversarially Robust Email Phishing Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikit-learn)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

**PhishNet-X** is an advanced phishing detection system that combines Machine Learning, Deep Learning, and Transformer-based models to accurately detect phishing emails and malicious URLs. Unlike traditional rule-based spam filters, PhishNet-X understands the **context** of email content and is robust against adversarial attacks.

---

## ✨ Features

- 📧 **Email Phishing Detection** using TF-IDF + Logistic Regression & Random Forest
- 🤗 **BERT Transformer Model** (pre-trained, zero-shot) for contextual understanding
- 🔗 **URL Analysis** using feature engineering + Random Forest
- ⚔️ **Adversarial Robustness Testing** against 4 attack techniques
- 🔍 **Explainable AI** — word-level explanations for every prediction
- 🌐 **Streamlit Web App** with a clean, interactive interface

---

## 📊 Model Performance

| Model | Type | Accuracy |
|---|---|---|
| Logistic Regression | Email | 98.87% |
| Random Forest | Email | 98.85% |
| BERT (Pre-trained) | Email | 87.40% |
| Random Forest | URL | 83.77% |
| Logistic Regression | URL | 65.60% |

---

## ⚔️ Adversarial Testing Results

| Attack Type | Detection Rate | Status |
|---|---|---|
| Original | 86.0% | ✅ Robust |
| Char Substitution (`v3r1fy`) | 99.0% | ✅ Robust |
| Add Spaces (`v e r i f y`) | 100.0% | ✅ Robust |
| Repeated Chars (`vverifyy`) | 86.0% | ✅ Robust |
| Mixed Case (`VeRiFy`) | 86.0% | ✅ Robust |

**Average Detection Rate: 91.4%** 🏆

---

## 🗂️ Project Structure

```
PhishNet-X/
│
├── 📓 phishnetx.ipynb          # Main Jupyter notebook (all steps)
├── 🌐 app.py                   # Streamlit web application
│
├── data/
│   ├── email_clean.csv         # Cleaned email dataset (46,910 rows)
│   └── url_clean.csv           # Cleaned URL dataset (312,844 rows)
│
├── models/
│   └── bert_phishing_model/    # Saved BERT model
│
├── outputs/
│   ├── explainable_ai.png      # Word importance chart
│   ├── bert_predictions.csv    # BERT evaluation results
│   └── adversarial_results.csv # Adversarial testing results
│
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10 |
| ML Models | Scikit-learn (LR, Random Forest) |
| Deep Learning | Transformers (BERT/DistilBERT) |
| NLP | TF-IDF, HuggingFace Transformers |
| Explainability | SHAP, Feature Coefficients |
| Web App | Streamlit |
| Data Handling | Pandas, NumPy |
| Visualization | Matplotlib |

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/PhishNet-X.git
cd PhishNet-X
```

**2. Install dependencies**
```bash
pip install scikit-learn transformers torch pandas numpy matplotlib streamlit shap
```

**3. Download Datasets**

Place these files in your project folder:
- `email_clean.csv` — Combined phishing email dataset
- `url_clean.csv` — Phishing URL dataset

> Original sources: [Kaggle Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset) | [Kaggle Phishing URLs](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls)

---

## 🚀 How to Run

**Run the Streamlit App:**
```bash
streamlit run app.py
```
Then open your browser at `http://localhost:8501`

**Or run the full pipeline in Jupyter:**
```bash
jupyter notebook phishnetx.ipynb
```

---

## 🔄 Pipeline Steps

```
1. Data Collection      →  4 email datasets + 1 URL dataset
2. Preprocessing        →  Clean text, remove HTML/URLs/symbols
3. Feature Extraction   →  TF-IDF for emails, 10 features for URLs
4. ML Models            →  Logistic Regression + Random Forest
5. BERT Model           →  Pre-trained DistilBERT (HuggingFace)
6. Adversarial Testing  →  4 attack techniques evaluated
7. Explainable AI       →  Word-level phishing indicators
8. Deployment           →  Streamlit web application
```

---

## 🌐 App Screenshots

### 📧 Email Analysis Tab
- Paste any email and get instant phishing probability
- Dual model analysis (BERT + Logistic Regression)
- Word-level explanation of prediction

### 🔗 URL Analysis Tab
- Enter any URL for risk assessment
- Full feature breakdown (domain length, entropy, subdomains etc.)
- Risk level: Low / Medium / High

### 📊 Model Comparison Tab
- All model accuracies in one place
- Adversarial testing results summary

---

## 📁 Datasets Used

| Dataset | Emails | Type |
|---|---|---|
| CEAS_08.csv | ~33,000 | Spam + Legitimate |
| Nazario.csv | ~1,500 | Phishing only |
| Nigerian_Fraud.csv | ~1,000 | Fraud emails |
| Ling_spam.csv | ~2,893 | Spam + Legitimate |
| phishing_site_urls.csv | 549,346 | Phishing + Legitimate URLs |

**Final combined:** 46,910 emails | 312,844 URLs (balanced)

---

## 🔍 Explainable AI Example

```
📧 Email: "Urgent: Your account will be suspended. Click here to verify your details immediately!"

🎯 Prediction : PHISHING
📊 Confidence : 97.71%

🔍 Word-level Explanation:
  your      →  score: +5.34  🔴 Phishing
  account   →  score: +1.82  🔴 Phishing
  will      →  score: +1.51  🔴 Phishing
  click     →  score: +0.36  🔴 Phishing
  verify    →  score: +0.13  🔴 Phishing
```

---

## 👩‍💻 Author

**laiba Khan**
> Built with ❤️ using Python, HuggingFace & Streamlit

---

## 📄 License

This project is licensed under the MIT License — feel free to use and modify!

---

⭐ **If you found this project helpful, please give it a star!** ⭐
#
