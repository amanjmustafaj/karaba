import streamlit as st
import pandas as pd

# ڕێکخستنی سەرەتایی لاپەڕەکە
st.set_page_config(
    page_title="سیستەمی کارەبا",
    page_icon="⚡",
    layout="centered",
)

# ستایلی تایبەت بۆ ئەوەی شاشەکە RTL بێت و فۆنت و ڕەنگەکان جوان بن
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 900;
        color: #007AFF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #007AFF;
        color: white;
        font-weight: bold;
    }
    .result-card {
        background-color: #007AFF;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        font-size: 25px;
        font-weight: 900;
    }
    </style>
    """, unsafe_allow_html=True)

# دروستکردنی Navigation Sidebar (وەک فلاتەرەکە)
with st.sidebar:
    st.title("تەختەی کۆنترۆڵ")
    page = st.radio("بڕۆ بۆ بەشی:", ["نرخی کارەبا", "تەکنیکی", "زانیاری ئامێرەکان"])
    st.markdown("---")
    st.write("وەشانی 1.0.7")
    st.write("گەشەپێدەر: AMANJ")

# --- بەشی یەکەم: هەژمارکردنی نرخ ---
if page == "نرخی کارەبا":
    st.markdown('<p class="main-header">هەژمارکردنی نرخی کارەبا</p>', unsafe_allow_html=True)
    
    category = st.selectbox("جۆری بەکارهێنەر", ["ماڵان", "بازرگانی", "پیشەسازی", "پیشەسازی گەورە", "میری", "کشتوکاڵ"])
    units = st.number_input("بڕی کیلۆوات (kWh) داخڵ بکە", min_value=0.0, step=1.0)
    
    if st.button("حیساب بکە"):
        if units > 0:
            if category == "ماڵان":
                tiers = [
                    {"n": "پلەی ١", "l": 400, "p": 72},
                    {"n": "پلەی ٢", "l": 400, "p": 108},
                    {"n": "پلەی ٣", "l": 400, "p": 175},
                    {"n": "پلەی ٤", "l": 400, "p": 265},
                    {"n": "پلەی پێنج", "l": 999999, "p": 350},
                ]
                total = 0
                temp = units
                details = []
                
                for t in tiers:
                    if temp <= 0: break
                    used = min(temp, t['l'])
                    cost = used * t['p']
                    details.append([t['n'], f"{used:.0f}", t['p'], f"{cost:.0f}"])
                    total += cost
                    temp -= used
                
                df = pd.DataFrame(details, columns=["پلە", "بڕ (kW)", "نرخ", "کۆ (دینار)"])
                st.table(df)
                st.markdown(f'<div class="result-card">کۆی گشتی: {total:,.0f} دینار</div>', unsafe_allow_html=True)
            else:
                rates = {"بازرگانی": 185, "پیشەسازی": 160, "پیشەسازی گەورە": 125, "میری": 160, "کشتوکاڵ": 60}
                rate = rates.get(category, 0)
                total = units * rate
                st.markdown(f'<div class="result-card">تێچوو: {total:,.0f} دینار</div>', unsafe_allow_html=True)

# --- بەشی دووەم: تەکنیکی ---
elif page == "تەکنیکی":
    st.markdown('<p class="main-header">هەژمارکردنی تەکنیکی</p>', unsafe_allow_html=True)
    
    tech_mode = st.selectbox("جۆری هەژمارکردن", ["وات بۆ کیلۆوات", "وات بۆ ئەمپێر", "ئەمپێر بۆ کیلۆوات", "مانگانە"])
    
    col1, col2 = st.columns(2)
    
    if tech_mode == "مانگانە":
        watt = col1.number_input("بڕی وات (Watt)", min_value=0.0)
        hours = col2.number_input("سەعات لە ڕۆژێکدا", min_value=0.0, max_value=24.0)
        days = st.number_input("چەند ڕۆژ لە مانگدا", min_value=1, max_value=31, value=30)
        if st.button("حیساب بکە"):
            res = (watt * hours * days) / 1000
            st.success(f"ئەنجام: {res:.2f} kWh / مانگ")
    else:
        val = st.number_input("بڕەکە داخڵ بکە", min_value=0.0)
        if st.button("حیساب بکە"):
            if tech_mode == "وات بۆ کیلۆوات": st.info(f"ئەنجام: {val/1000:.2f} kWh")
            if tech_mode == "وات بۆ ئەمپێر": st.info(f"ئەنجام: {val/220:.2f} Ampere")
            if tech_mode == "ئەمپێر بۆ کیلۆوات": st.info(f"ئەنجام: {(val*220)/1000:.2f} kWh")

# --- بەشی سێیەم: زانیاری ئامێرەکان ---
elif page == "زانیاری ئامێرەکان":
    st.markdown('<p class="main-header">زانیاری و توانای ئامێرەکان</p>', unsafe_allow_html=True)
    
    appliances = {
        "بۆیلەر": 3000, "سپلێت ١ تەن": 1200, "سپلێت ٢ تەن": 2400, "سەلاجە": 250,
        "موجەمیدە": 300, "غەسالە": 2000, "ئوتو": 2200, "مایکرۆوەیڤ": 1500,
        "هیتەر": 2000, "تەلەفزیۆن": 100, "گلۆپ": 20
    }
    
    selected = st.multiselect("ئامێرەکان هەڵبژێرە بۆ زانینی تێچووی کارەبایان:", list(appliances.keys()))
    
    if selected:
        total_w = sum([appliances[x] for x in selected])
        total_a = total_w / 220
        
        c1, c2 = st.columns(2)
        c1.metric("کۆی وات", f"{total_w} W")
        c2.metric("کۆی ئەمپێر", f"{total_a:.1f} A")
        
    st.write("---")
    st.subheader("خشتەی نرخە فەرمییەکان")
    price_data = {
        "جۆری بەکارهێنان": ["ماڵان (پلە ١)", "ماڵان (پلە ٢)", "بازرگانی", "پیشەسازی", "کشتوکاڵ"],
        "نرخ (دینار)": [72, 108, 185, 160, 60]
    }
    st.table(pd.DataFrame(price_data))
