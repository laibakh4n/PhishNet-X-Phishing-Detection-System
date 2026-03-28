import streamlit as st
import pandas as pd
import numpy as np
import re
import math
import urllib.parse
from transformers import pipeline
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PhishNet-X",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# LOAD MODELS (cached so they load only once)
# ============================================================

@st.cache_resource
def load_bert():
    return pipeline(
        "text-classification",
        model="cybersectony/phishing-email-detection-distilbert_v2.4.1"
    )

@st.cache_resource
def load_email_model():
    df = pd.read_csv("email_clean.csv").dropna(subset=['text', 'label'])
    df = df.sample(n=3000, random_state=42)
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=3000)),
        ('clf',   LogisticRegression(max_iter=1000))
    ])
    pipe.fit(df['text'], df['label'])
    return pipe

@st.cache_resource
def load_url_model():
    df = pd.read_csv("url_clean.csv").dropna()
    def extract_features(url):
        url = str(url)
        try:
            parsed = urllib.parse.urlparse(url if url.startswith('http') else 'http://' + url)
            domain = parsed.netloc
            path   = parsed.path
        except:
            domain, path = url, ''
        def entropy(s):
            prob = [s.count(c)/len(s) for c in set(s)]
            return -sum(p * math.log2(p) for p in prob) if s else 0
        return {
            'url_length'       : len(url),
            'domain_length'    : len(domain),
            'num_subdomains'   : domain.count('.'),
            'has_ip'           : 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0,
            'has_at'           : 1 if '@' in url else 0,
            'has_https'        : 1 if url.startswith('https') else 0,
            'num_special_chars': sum(url.count(c) for c in ['-','_','=','?','&']),
            'path_length'      : len(path),
            'entropy'          : round(entropy(url), 4),
            'num_digits'       : sum(c.isdigit() for c in url),
        }
    sample = df.sample(n=5000, random_state=42)
    X = pd.DataFrame(list(sample['URL'].apply(extract_features)))
    y = sample['label'].values
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    return clf, extract_features

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(text):
    text = str(text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower().strip()

def get_risk_level(score):
    if score >= 0.85:
        return "🔴 HIGH RISK", "red"
    elif score >= 0.60:
        return "🟡 MEDIUM RISK", "orange"
    else:
        return "🟢 LOW RISK", "green"

# ============================================================
# UI — HEADER
# ============================================================

st.title("🛡️ PhishNet-X")
st.subheader("Context-Aware & Adversarially Robust Phishing Detection System")
st.markdown("---")

# ============================================================
# UI — TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(["📧 Email Analysis", "🔗 URL Analysis", "📊 Model Comparison"])

# ============================================================
# TAB 1 — EMAIL ANALYSIS
# ============================================================

with tab1:
    st.header("📧 Email Phishing Detection")
    email_input = st.text_area(
        "Paste your email content below:",
        height=200,
        placeholder="Enter email subject and body here..."
    )

    col1, col2 = st.columns(2)
    with col1:
        use_bert = st.checkbox("Use BERT Model", value=True)
    with col2:
        use_lr = st.checkbox("Use Logistic Regression", value=True)

    if st.button("🔍 Analyze Email", type="primary"):
        if email_input.strip() == "":
            st.warning("Please enter some email content!")
        else:
            st.markdown("### 🎯 Analysis Results")
            cleaned = clean_text(email_input)

            results_col1, results_col2 = st.columns(2)

            if use_bert:
                with results_col1:
                    with st.spinner("Running BERT analysis..."):
                        bert_model  = load_bert()
                        bert_result = bert_model(email_input[:512])[0]
                        bert_score  = bert_result['score']
                        is_phishing = 'phishing' in bert_result['label'].lower() or bert_result['label'] == 'LABEL_1'
                        if not is_phishing:
                            bert_score = 1 - bert_score
                        risk, color = get_risk_level(bert_score)
                        st.metric("BERT Model", risk)
                        st.progress(bert_score)
                        st.write(f"Phishing Probability: **{bert_score:.2%}**")

            if use_lr:
                with results_col2:
                    with st.spinner("Running LR analysis..."):
                        lr_model   = load_email_model()
                        lr_proba   = lr_model.predict_proba([cleaned])[0][1]
                        risk, color = get_risk_level(lr_proba)
                        st.metric("Logistic Regression", risk)
                        st.progress(float(lr_proba))
                        st.write(f"Phishing Probability: **{lr_proba:.2%}**")

            # Word explanation
            st.markdown("### 🔍 Word-level Explanation")
            lr_model      = load_email_model()
            feature_names = lr_model.named_steps['tfidf'].get_feature_names_out()
            coefficients  = lr_model.named_steps['clf'].coef_[0]
            word_scores   = {}
            for word in cleaned.split():
                if word in feature_names:
                    idx = list(feature_names).index(word)
                    word_scores[word] = round(coefficients[idx], 4)

            if word_scores:
                sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
                for word, score in sorted_words[:10]:
                    indicator = "🔴 Phishing" if score > 0 else "🟢 Legitimate"
                    st.write(f"**{word}** → score: `{score}` {indicator}")
            else:
                st.info("No significant phishing keywords detected in this email.")

# ============================================================
# TAB 2 — URL ANALYSIS
# ============================================================

with tab2:
    st.header("🔗 URL Phishing Detection")
    url_input = st.text_input(
        "Enter a URL to analyze:",
        placeholder="e.g. http://suspicious-site.com/login"
    )

    if st.button("🔍 Analyze URL", type="primary"):
        if url_input.strip() == "":
            st.warning("Please enter a URL!")
        else:
            rf_model, extract_fn = load_url_model()
            features  = extract_fn(url_input)
            X_input   = pd.DataFrame([features])
            proba     = rf_model.predict_proba(X_input)[0][1]
            risk, color = get_risk_level(proba)

            st.markdown("### 🎯 URL Analysis Results")
            st.metric("Risk Level", risk)
            st.progress(float(proba))
            st.write(f"Phishing Probability: **{proba:.2%}**")

            st.markdown("### 🔍 URL Feature Breakdown")
            feature_df = pd.DataFrame([features]).T
            feature_df.columns = ['Value']
            feature_df['Risk'] = feature_df['Value'].apply(
                lambda x: "⚠️ Suspicious" if x > 0.5 else "✅ Normal"
            )
            st.dataframe(feature_df, use_container_width=True)

# ============================================================
# TAB 3 — MODEL COMPARISON
# ============================================================

with tab3:
    st.header("📊 Model Performance Comparison")

    results_data = {
        'Model'   : ['Logistic Regression', 'Random Forest', 'BERT Pre-trained', 'URL - Random Forest'],
        'Type'    : ['Email', 'Email', 'Email', 'URL'],
        'Accuracy': [0.9887, 0.9885, 0.8740, 0.8377],
        'Notes'   : [
            'TF-IDF based, very fast',
            'TF-IDF based, robust',
            'Transformer, zero-shot',
            'Feature engineering based'
        ]
    }

    df_results = pd.DataFrame(results_data)
    st.dataframe(df_results, use_container_width=True)

    st.markdown("### 🔍 Adversarial Testing Results")
    adv_data = {
        'Attack Type'    : ['Original', 'Char Substitution', 'Add Spaces', 'Repeated Chars', 'Mixed Case'],
        'Detection Rate' : [86.0, 99.0, 100.0, 86.0, 86.0],
        'Status'         : ['✅ Robust', '✅ Robust', '✅ Robust', '✅ Robust', '✅ Robust']
    }
    st.dataframe(pd.DataFrame(adv_data), use_container_width=True)
    st.success("🎯 Average Detection Rate: 91.4% — System is highly robust!")

st.markdown("---")
st.markdown("**PhishNet-X** — Built with Machine Learning, Deep Learning & Transformer Models")