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
    
    /* ستایلی هێدەر و ڕادیۆ بۆ دیزاینی ACBFA4 */
    div.stRadio > div {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 15px;
        border-bottom: 4px solid #ACBFA4;
        margin-bottom: 30px;
        justify-content: center !important;
    }
    
    /* ستایلی نووسینی ناو هێدەرەکە */
    div.stRadio label {
        font-weight: bold !important;
        font-size: 18px !important;
        color: #2c3e50 !important;
    }

    /* ستایلی باکگراوندی لیستەکان کاتێک دەکرێنەوە */
    div[data-baseweb="popover"], div[data-baseweb="listbox"] {
        background-color: #EAEFEF !important;
    }

    /* ستایلی دوگمەکان بە ڕەنگی ACBFA4 */
    .stButton > button {
        display: block; margin: 10px auto !important; width: 100% !important;
        max-width: 300px; height: 55px; color: white !important; font-size: 18px !important;
        border: none; border-radius: 12px; font-weight: bold;
        background-color: #ACBFA4 !important; 
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #94a88d !important; /* تۆختر بۆ کاتی ئاماژە */
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
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-top: 6px solid #ACBFA4;
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
        # دیزاینی هێدەر بە ڕەنگی ACBFA4 لە ژێری
        st.markdown("<h2 style='text-align: center;'>⚡ سیستەمی مۆدێرنی کارەبا</h2>", unsafe_allow_html=True)
        
        selected_page = st.radio(
            "بەشی مەبەست هەڵبژێرە:",
            ["هەژمارکردنی نرخ", "حیسابی تەکنیکی", "دەربارە"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if selected_page == "هەژمارکردنی نرخ":
            self.page_price_calc()
        elif selected_page == "حیسابی تەکنیکی":
            self.page_technical_calc()
        else:
            self.page_about()

    def page_price_calc(self):
        st.header("💰 هەژمارکردنی نرخی کارەبا")
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        category = st.selectbox("جۆری هاوبەش هەڵبژێرە:", ["ماڵان", "بازرگانی", "پیشەسازی", "میری", "کشتوکاڵ"])
        mode = st.radio("جۆری گۆڕین:", ["کیلۆوات بۆ دینار", "دینار بۆ کیلۆوات"], horizontal=True)
        
        if mode == "کیلۆوات بۆ دینار":
            val = st.number_input("بڕی کیلۆوات (kWh):", min_value=0, step=1)
            if st.button("هەژمارکردن"):
                res = self.calc_home_cost(val) if category == "ماڵان" else val * self.flat_rates.get(category, 0)
                st.success(f"تێچووی کۆتایی: {res:,.0f} دینار")
        else:
            money = st.number_input("بڕی پارە (دینار):", min_value=0, step=1000)
            if st.button("هەژمارکردن"):
                units = self.calc_money_to_units(money) if category == "ماڵان" else money / self.flat_rates.get(category, 1)
                st.info(f"بڕی کارەبای وەرگیراو: {units:,.2f} کیلۆوات")
        st.markdown('</div>', unsafe_allow_html=True)

    def page_technical_calc(self):
        st.header("⚙️ حیسابی تەکنیکی")
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        calc_type = st.selectbox("جۆری حیسابکردنەکە:", ["وات بۆ ئەمپێر", "ئەمپێر بۆ کیلۆوات", "بەکارهێنانی مانگانە ئامێرەکان"])
        
        if calc_type == "وات بۆ ئەمپێر":
            w = st.number_input("بڕی وات (Watt):", min_value=0)
            if st.button("هەژمارکردن"):
                st.info(f"ئەنجام: {w/self.volt:.2f} ئەمپێر")
                
        elif calc_type == "ئەمپێر بۆ کیلۆوات":
            a = st.number_input("ئەمپێر (Ampere):", min_value=0.0)
            h = st.number_input("کاتژمێر کارکردن:", min_value=1)
            if st.button("هەژمارکردن"):
                kwh = (a * self.volt * h) / 1000
                st.info(f"ئەنجام: {kwh:.2f} کیلۆوات")
                
        else:
            w = st.number_input("واتی ئامێر (نموونە بۆ سپلیت ٣٠٠٠ وات):", min_value=0)
            h = st.number_input("سەعات لە ڕۆژێکدا:", min_value=0.0)
            d = st.number_input("چەند ڕۆژ لە مانگدا:", value=30)
            if st.button("حیسابی مانگانە"):
                total_kwh = (w * h * d) / 1000
                st.success(f"بەکارهێنانی مانگانە: {total_kwh:.2f} کیلۆوات")
        st.markdown('</div>', unsafe_allow_html=True)

    def page_about(self):
        st.header("ℹ️ دەربارە و نرخەکان")
        st.markdown(f"""
        <div class="custom-card" style="text-align: right;">
            <h4>زانیاری گشتی</h4>
            <p>ئەم پڕۆگرامە بە ڕەنگی تایبەتی <b>#ACBFA4</b> دیزاین کراوە بۆ کاک ئامانج.</p>
            <hr>
            <h5>نرخی ماڵان بەپێی پلەکان:</h5>
            <p>١-٤٠٠ یەکە: ٧٢ دینار</p>
            <p>٤٠١-٨٠٠ یەکە: ١٠٨ دینار</p>
            <p>٨٠١-١٢٠٠ یەکە: ١٧٢ دینار</p>
            <p>١٢٠١-١٦٠٠ یەکە: ٢٦٥ دینار</p>
            <p>زیاتر لە ١٦٠٠: ٣٥٠ دینار</p>
        </div>
        """, unsafe_allow_html=True)

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
