import streamlit as st

# ==========================================
# 1. Page Configuration & Styling
# ==========================================
st.set_page_config(page_title="سیستەمی کارەبا", layout="wide")

st.markdown("""
    <style>
    .stApp { text-align: center; direction: rtl; }
    
    .main-title {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }

    .stButton > button {
        display: block; margin: 5px auto !important; width: 100% !important;
        max-width: 280px; height: 50px; color: white !important; font-size: 17px !important;
        border: none; border-radius: 10px; font-weight: bold;
        background-color: #ACBFA4 !important; 
        transition: all 0.2s ease;
    }
    
    .stButton > button:focus, .stButton > button:active {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
    }

    hr { border-top: 1px solid #ACBFA4; opacity: 0.3; margin: 20px 0; }
    
    /* ڕێکخستنی ستایلی خشتەکان بۆ ئەوەی لە ناوەڕاست بن */
    table {
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

class ElectricityPro:
    def __init__(self):
        self.flat_rates = {
            "بازرگانی": 185, 
            "پیشەسازی گەورە": 125, 
            "پیشەسازی": 160, 
            "میری": 160, 
            "کشتوکاڵ": 60
        }
        self.home_tiers = [
            ("پلەی ١ (1-400)", 400, 72),
            ("پلەی ٢ (401-800)", 400, 108),
            ("پلەی ٣ (801-1200)", 400, 172),
            ("پلەی ٤ (1201-1600)", 400, 265),
            ("پلەی ٥ (سەروو ١٦٠٠)", 999999, 350)
        ]
        self.volt = 220

        if 'page' not in st.session_state:
            st.session_state.page = "price"
        if 'sub_mode' not in st.session_state:
            st.session_state.sub_mode = "kwh_to_money"

    def main(self):
        st.markdown("<h1 class='main-title'>هەژمارکردنی نرخی کارەبا</h1>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("هەژمارکردنی نرخ"):
                st.session_state.page = "price"
        with col2:
            if st.button("حیسابی تەکنیکی"):
                st.session_state.page = "technical"
        with col3:
            if st.button("زانیاری"):
                st.session_state.page = "info"
        with col4:
            if st.button("دەربارە"):
                st.session_state.page = "about"
        
        st.markdown("<hr>", unsafe_allow_html=True)

        if st.session_state.page == "price":
            self.page_price_calc()
        elif st.session_state.page == "technical":
            self.page_technical_calc()
        elif st.session_state.page == "info":
            self.page_info()
        else:
            self.page_about()

    def page_info(self):
        st.header("زانیاری نرخەکانی کارەبا")
        
        # دروستکردنی دوو ستوون بۆ ئەوەی خشتەکان ببنە هاوتەریب
        left_col, right_col = st.columns(2)
        
        with left_col:
            st.subheader("نرخی جۆرە جیاوازەکان")
            info_md = "| جۆری کارەبا | نرخ (دینار) |\n"
            info_md += "| :--- | :---: |\n"
            for cat, price in self.flat_rates.items():
                info_md += f"| {cat} | {price} |\n"
            st.markdown(info_md)
        
        with right_col:
            st.subheader("خشتەی پلەکانی ماڵان")
            home_md = "| پلەی بەکارهێنان | نرخ (دینار) |\n"
            home_md += "| :--- | :---: |\n"
            for name, limit, price in self.home_tiers:
                home_md += f"| {name} | {price} |\n"
            st.markdown(home_md)

    def page_price_calc(self):
        st.header("هەژمارکردنی نرخ")
        category = st.selectbox("جۆری هاوبەش هەڵبژێرە:", ["ماڵان", "بازرگانی", "پیشەسازی", "میری", "کشتوکاڵ"])
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("کیلۆوات بۆ دینار"):
                st.session_state.sub_mode = "kwh_to_money"
        with c2:
            if st.button("دینار بۆ کیلۆوات"):
                st.session_state.sub_mode = "money_to_kwh"
        
        st.write("---")
        
        if st.session_state.sub_mode == "kwh_to_money":
            val = st.number_input("بڕی کیلۆوات داخڵ بکە:", min_value=0, step=1)
            if st.button("ئەنجامی حیساب"):
                if category == "ماڵان":
                    self.show_home_details_no_pandas(val)
                else:
                    res = val * self.flat_rates.get(category, 0)
                    st.success(f"تێچووی کۆتایی: {res:,.0f} دینار")
        else:
            money = st.number_input("بڕی پارە بە دینار داخڵ بکە:", min_value=0, step=1000)
            if st.button("ئەنجامی حیساب"):
                units = self.calc_money_to_units(money) if category == "ماڵان" else money / self.flat_rates.get(category, 1)
                st.info(f"بڕی کارەبا: {units:,.2f} کیلۆوات")

    def show_home_details_no_pandas(self, kwh):
        temp_kwh = kwh
        total_price = 0
        table_md = "| پلە | یەکە | نرخ | تێچوو |\n"
        table_md += "| :--- | :---: | :---: | :---: |\n"
        
        for name, limit, price in self.home_tiers:
            if temp_kwh <= 0: break
            consumed = min(temp_kwh, limit)
            cost = consumed * price
            total_price += cost
            table_md += f"| {name} | {consumed:,.0f} | {price} | {cost:,.0f} |\n"
            temp_kwh -= consumed
        
        st.write("### وردەکاری هەژمارکردن")
        st.markdown(table_md)
        st.success(f"### کۆی گشتی: {total_price:,.0f} دینار")

    def page_technical_calc(self):
        st.header("حیسابی تەکنیکی")
        calc_type = st.selectbox("جۆری گۆڕین هەڵبژێرە:", ["وات بۆ ئەمپێر", "ئەمپێر بۆ کیلۆوات", "بەکارهێنانی مانگانە"])
        
        if calc_type == "وات بۆ ئەمپێر":
            w = st.number_input("وات:", min_value=0)
            if st.button("حیساب بکە"):
                st.info(f"ئەنجام: {w/self.volt:.2f} ئەمپێر")
        elif calc_type == "ئەمپێر بۆ کیلۆوات":
            a = st.number_input("ئەمپێر:", min_value=0.0)
            h = st.number_input("کاتژمێر:", min_value=1)
            if st.button("حیساب بکە"):
                kwh = (a * self.volt * h) / 1000
                st.info(f"ئەنجام: {kwh:.2f} کیلۆوات")
        else:
            w = st.number_input("واتی ئامێر:", min_value=0)
            h = st.number_input("سەعات لە ڕۆژێکدا:", min_value=0.0)
            d = st.number_input("ڕۆژ لە مانگدا:", value=30)
            if st.button("حیسابی مانگانە"):
                total_kwh = (w * h * d) / 1000
                st.success(f"بەکارهێنانی مانگانە: {total_kwh:.2f} کیلۆوات")

    def page_about(self):
        st.header("دەربارە")
        st.write("ئەم پڕۆگرامە بۆ هەژمارکردنی نرخ و حیسابە تەکنیکییەکان بەکار دێت.")

    def calc_money_to_units(self, money):
        total = 0
        rem = money
        for _, limit, price in self.home_tiers:
            if rem <= 0: break
            max_tier_cost = limit * price
            if rem >= max_tier_cost:
                total += limit
                rem -= max_tier_cost
            else:
                total += rem / price
                rem = 0
        return total

if __name__ == "__main__":
    ElectricityPro().main()
