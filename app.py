import streamlit as st

# ==========================================
# 1. Page Configuration & Styling
# ==========================================
st.set_page_config(page_title="هەژمارکردنی پارەی کارەبا", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { text-align: center; direction: rtl; }
    h1, h2, h3, p, div { text-align: center !important; }
    .stButton > button {
        display: block; margin: 10px auto !important; width: 100% !important;
        border-radius: 12px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

class ElectricityCalculator:
    def __init__(self):
        # نرخە جێگیرەکان
        self.flat_rates = {
            "بازرگانی": 185,
            "پیشەسازی گەورە": 125,
            "پیشەسازی": 160,
            "میری": 160,
            "کشتوکاڵ": 60
        }
        
        # پلەکانی ماڵان (بڕ، نرخ)
        self.home_tiers = [
            (400, 72),   # پلەی ١
            (400, 108),  # پلەی ٢
            (400, 172),  # پلەی ٣
            (400, 260),  # پلەی ٤ (چاککرا بۆ ٢٦٠)
            (999999, 350) # زیاتر
        ]

    def run(self):
        st.title("⚡ ژمێرەری کارەبای هەرێم")
        st.write("بەخێر بێی کاک ئامانج، لێرە پارەی کارەباکەت بزانە")
        st.write("---")

        category = st.selectbox(
            "جۆری بەکارهێنان دەستنیشان بکە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )

        if "mode" not in st.session_state:
            st.session_state.mode = "kwh_to_dinar"

        col1, col2 = st.columns(2)
        with col1:
            if st.button("کیلۆوات بۆ دینار", type="primary" if st.session_state.mode == "kwh_to_dinar" else "secondary"):
                st.session_state.mode = "kwh_to_dinar"
        with col2:
            if st.button("دینار بۆ کیلۆوات", type="primary" if st.session_state.mode == "dinar_to_kwh" else "secondary"):
                st.session_state.mode = "dinar_to_kwh"

        if st.session_state.mode == "kwh_to_dinar":
            kwh = st.number_input("بڕی بەکارهێنانی یەکە (kWh):", min_value=0, step=1)
            if st.button("حیسابی بکە"):
                self.calculate_price(category, kwh)
        else:
            money = st.number_input("بڕی پارەکە (دینار):", min_value=0, step=1000)
            if st.button("حیسابی بکە"):
                self.calculate_units(category, money)

    # ... لێرەدا فەنکشنەکانی calculate_price و calculate_units وەک خۆیان دەمێننەوە بە گۆڕینی نرخی ٢٦٠
