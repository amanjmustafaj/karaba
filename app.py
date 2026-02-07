import streamlit as st

# ==========================================
# 1. Page Configuration & Styling
# ==========================================
st.set_page_config(page_title="سیستەمی کارەبا", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { text-align: center; direction: rtl; }
    h1, h2, h3 { color: #2c3e50; }
    
    /* ستایلی گشتی دوگمەکان بە ڕەنگی داواکراوی تۆ */
    .stButton > button {
        display: block; margin: 5px auto !important; width: 100% !important;
        max-width: 280px; height: 50px; color: white !important; font-size: 17px !important;
        border: none; border-radius: 10px; font-weight: bold;
        background-color: #ACBFA4 !important; 
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        opacity: 0.8;
        transform: translateY(-1px);
    }

    .stButton > button:active {
        background-color: red !important;
    }

    /* ستایلی لیستەکان کاتێک دەکرێنەوە */
    div[data-baseweb="popover"], div[data-baseweb="listbox"] {
        background-color: #EAEFEF !important;
    }

    hr { border-top: 1px solid #ACBFA4; opacity: 0.3; margin: 20px 0; }
    
    .custom-section { padding: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

class ElectricityPro:
    def __init__(self):
        self.flat_rates = {
            "بازرگانی": 185, "پیشەسازی گەورە": 125, "پیشەسازی": 160, "میری": 160, "کشتوکاڵ": 60
        }
        self.home_tiers = [(400, 72), (400, 108), (400, 172), (400, 265), (999999, 350)]
        self.volt = 220

        # ئامادەکردنی Session State بۆ گۆڕینی لاپەڕەکان
        if 'page' not in st.session_state:
            st.session_state.page = "price"
        if 'sub_mode' not in st.session_state:
            st.session_state.sub_mode = "kwh_to_money"

    def main(self):
        st.markdown("<h2 style='text-align: center;'>⚡ سیستەمی مۆدێرنی کارەبا</h2>", unsafe_allow_html=True)
        
        # دروستکردنی هێدەری سەرەوە بە دوگمە
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💰 هەژمارکردنی نرخ"):
                st.session_state.page = "price"
        with col2:
            if st.button("⚙️ حیسابی تەکنیکی"):
                st.session_state.page = "technical"
        with col3:
            if st.button("ℹ️ دەربارە"):
                st.session_state.page = "about"
        
        st.markdown("<hr>", unsafe_allow_html=True)

        # نیشاندانی لاپەڕەکان بەپێی هەڵبژاردەی دوگمەکان
        if st.session_state.page == "price":
            self.page_price_calc()
        elif st.session_state.page == "technical":
            self.page_technical_calc()
        else:
            self.page_about()

    def page_price_calc(self):
        st.header("هەژمارکردنی نرخ")
        category = st.selectbox("جۆری هاوبەش:", ["ماڵان", "بازرگانی", "پیشەسازی", "میری", "کشتوکاڵ"])
        
        # دوگمە ناوخۆییەکان بۆ گۆڕینی جۆری حیسابەکە
        c1, c2 = st.columns(2)
        with c1:
            if st.button("کیلۆوات ⬅️ دینار"):
                st.session_state.sub_mode = "kwh_to_money"
        with c2:
            if st.button("دینار ⬅️ کیلۆوات"):
                st.session_state.sub_mode = "money_to_kwh"
        
        st.write("---")
        
        if st.session_state.sub_mode == "kwh_to_money":
            val = st.number_input("بڕی کیلۆوات (kWh):", min_value=0, step=1)
            if st.button("ئەنجام حیساب بکە"):
                res = self.calc_home_cost(val) if category == "ماڵان" else val * self.flat_rates.get(category, 0)
                st.success(f"تێچووی کۆتایی: {res:,.0f} دینار")
        else:
            money = st.number_input("بڕی پارە (دینار):", min_value=0, step=1000)
            if st.button("ئەنجام حیساب بکە"):
                units = self.calc_money_to_units(money) if category == "ماڵان" else money / self.flat_rates.get(category, 1)
                st.info(f"بڕی کارەبا: {units:,.2f} کیلۆوات")

    def page_technical_calc(self):
        st.header("حیسابی تەکنیکی")
        calc_type = st.selectbox("جۆری حیسابکردن:", ["وات بۆ ئەمپێر", "ئەمپێر بۆ کیلۆوات", "بەکارهێنانی مانگانە"])
        
        if calc_type == "وات بۆ ئەمپێر":
            w = st.number_input("وات (Watt):", min_value=0)
            if st.button("حیسابی بکە"):
                st.info(f"ئەنجام: {w/self.volt:.2f} ئەمپێر")
        elif calc_type == "ئەمپێر بۆ کیلۆوات":
            a = st.number_input("ئەمپێر (Ampere):", min_value=0.0)
            h = st.number_input("کاتژمێر:", min_value=1)
            if st.button("حیسابی بکە"):
                kwh = (a * self.volt * h) / 1000
                st.info(f"ئەنجام: {kwh:.2f} کیلۆوات")
        else:
            w = st.number_input("واتی ئامێر:", min_value=0)
            h = st.number_input("سەعات لە ڕۆژێکدا:", min_value=0.0)
            d = st.number_input("ڕۆژ لە مانگدا:", value=30)
            if st.button("حیسابی مانگانە بکە"):
                total_kwh = (w * h * d) / 1000
                st.success(f"بەکارهێنانی مانگانە: {total_kwh:.2f} کیلۆوات")

    def page_about(self):
        st.header("دەربارە")
        st.write("ئەم پڕۆگرامە تەنیا بە دوگمە و بە ڕەنگی ACBFA4 دیزاین کراوەتەوە.")
        st.markdown("<p style='color: #ACBFA4; font-weight: bold;'>تایبەت بۆ کاک ئامانج</p>", unsafe_allow_html=True)

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
