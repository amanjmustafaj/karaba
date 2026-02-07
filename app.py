import streamlit as st

# ==========================================
# 1. Page Configuration & Professional Styling
# ==========================================
st.set_page_config(page_title="سیستەمی کارەبا", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* رێکخستنی گشتی */
    .stApp { text-align: center; direction: rtl; }
    h1, h2, h3 { color: #2c3e50; }
    
    /* ستایلی Sidebar یان Header */
    .stRadio > div {
        flex-direction: row !important;
        justify-content: center !important;
        gap: 20px;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 25px;
    }

    /* ستایلی باکگراوندی لیستەکان */
    div[data-baseweb="popover"], div[data-baseweb="listbox"] {
        background-color: #EAEFEF !important;
    }

    /* ستایلی دوگمەکان (ڕەنگی ACBFA4) */
    .stButton > button {
        display: block; margin: 10px auto !important; width: 100% !important;
        max-width: 300px; height: 55px; color: white !important; font-size: 18px !important;
        border: none; border-radius: 12px; font-weight: bold;
        background-color: #ACBFA4 !important; 
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #667eea !important; 
        transform: translateY(-2px);
    }
    .stButton > button:active {
        background-color: red !important;
    }

    /* کارتەکان بۆ جوانی دیزاین */
    .custom-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-top: 5px solid #ACBFA4;
    }
    
    hr { border-top: 1px solid #ddd; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

class ElectricityPro:
    def __init__(self):
        self.flat_rates = {
            "بازرگانی": 185, "پیشەسازی گەورە": 125, "پیشەسازی": 160, "میری": 160, "کشتوکاڵ": 60
        }
        self.home_tiers = [(400, 72), (400, 108), (400, 172), (400, 265), (999999, 350)]
        self.volt = 220

    def main(self):
        # دروستکردنی هێدەر بۆ گۆڕینی لاپەڕەکان
        selected_page = st.radio(
            "بەشەکان هەڵبژێرە:",
            ["هەژمارکردنی نرخ", "حیسابی تەکنیکی", "دەربارە"],
            horizontal=True
        )
        
        st.markdown("<hr>", unsafe_allow_html=True)

        if selected_page == "هەژمارکردنی نرخ":
            self.page_price_calc()
        elif selected_page == "حیسابی تەکنیکی":
            self.page_technical_calc()
        else:
            self.page_about()

    # ---------------- لاپەڕەی یەکەم: هەژمارکردنی نرخ ----------------
    def page_price_calc(self):
        st.header("💰 هەژمارکردنی نرخی کارەبا")
        
        with st.container():
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            category = st.selectbox("جۆری هاوبەش:", ["ماڵان", "بازرگانی", "پیشەسازی", "میری", "کشتوکاڵ"])
            mode = st.radio("جۆری گۆڕین:", ["کیلۆوات ⬅️ دینار", "دینار ⬅️ کیلۆوات"], horizontal=True)
            
            if mode == "کیلۆوات ⬅️ دینار":
                val = st.number_input("بڕی کیلۆوات (kWh):", min_value=0, step=1)
                if st.button("هەژمار بکە"):
                    res = self.calc_home_cost(val) if category == "ماڵان" else val * self.flat_rates.get(category, 0)
                    st.success(f"کۆی گشتی: {res:,.0f} دینار")
            else:
                money = st.number_input("بڕی پارە (دینار):", min_value=0, step=1000)
                if st.button("هەژمار بکە"):
                    units = self.calc_money_to_units(money) if category == "ماڵان" else money / self.flat_rates.get(category, 1)
                    st.info(f"بڕی کارەبا: {units:,.2f} کیلۆوات")
            st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- لاپەڕەی دووەم: حیسابی تەکنیکی ----------------
    def page_technical_calc(self):
        st.header("⚙️ حیسابی تەکنیکی")
        
        calc_type = st.selectbox("چی هەژمار دەکەیت؟", ["وات بۆ ئەمپێر", "ئەمپێر بۆ کیلۆوات", "بەکارهێنانی مانگانە"])
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if calc_type == "وات بۆ ئەمپێر":
            w = st.number_input("وات (Watt):", min_value=0)
            if st.button("حیسابکردن"):
                st.write(f"ئەنجام: {w/self.volt:.2f} ئەمپێر")
                
        elif calc_type == "ئەمپێر بۆ کیلۆوات":
            a = st.number_input("ئەمپێر (Ampere):", min_value=0.0)
            h = st.number_input("کاتژمێر:", min_value=1)
            if st.button("حیسابکردن"):
                kwh = (a * self.volt * h) / 1000
                st.write(f"ئەنجام: {kwh:.2f} کیلۆوات")
                
        else: # بەکارهێنانی مانگانە
            w = st.number_input("واتی ئامێرەکە:", min_value=0)
            h = st.number_input("سەعات لە ڕۆژێکدا:", min_value=0.0)
            d = st.number_input("چەند ڕۆژ لە مانگدا:", value=30)
            if st.button("حیسابکردنی مانگانە"):
                total_kwh = (w * h * d) / 1000
                st.info(f"بەکارهێنانی مانگانە: {total_kwh:.2f} کیلۆوات")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- لاپەڕەی سێیەم: دەربارە ----------------
    def page_about(self):
        st.header("ℹ️ دەربارەی سیستەم و نرخەکان")
        st.markdown("""
        <div class="custom-card" style="text-align: right;">
            <h4>سیستەمی هەژمارکردنی کارەبای هەرێم</h4>
            <p>ئەم بەرنامەیە بۆ ئاسانکاری هاوڵاتیان دروستکراوە بۆ زانینی تێچووی کارەبا.</p>
            <hr>
            <h5>لیستی نرخەکان (ماڵان):</h5>
            <ul>
                <li>1 - 400 کیلۆوات: 72 دینار</li>
                <li>401 - 800 کیلۆوات: 108 دینار</li>
                <li>801 - 1200 کیلۆوات: 172 دینار</li>
                <li>1201 - 1600 کیلۆوات: 265 دینار</li>
                <li>سەرووی 1600 کیلۆوات: 350 دینار</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # مێتۆدە یارمەتیدەرەکان
    def calc_home_cost(self, kwh):
        total = 0
        temp = kwh
        for limit, price in self.home_tiers:
            if temp > 0:
                use = min(temp, limit)
                total += use * price
                temp -= use
        return total

    def calc_money_to_units(self, money):
        total = 0
        rem = money
        for limit, price in self.home_tiers:
            if rem <= 0: break
            cost = limit * price
            if rem >= cost:
                total += limit
                rem -= cost
            else:
                total += rem / price
                rem = 0
        return total

if __name__ == "__main__":
    ElectricityPro().main()
