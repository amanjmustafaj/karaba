import streamlit as st

# ==========================================
# 1. Page Configuration & Styling
# ==========================================
st.set_page_config(page_title="هەژمارکردنی کارەبا", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { text-align: center; direction: rtl; }
    h1, h2, h3, p, div { text-align: center !important; }
    .stSelectbox label, .stNumberInput label {
        text-align: center !important; width: 100%; font-size: 18px; font-weight: bold;
    }
    .stButton > button {
        display: block; margin: 10px auto !important; width: 280px !important;
        height: 60px; color: white; font-size: 20px !important;
        border: none; border-radius: 12px; font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .calculator-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .result-box {
        background: white;
        color: #333;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

class ElectricityCalculator:
    def __init__(self):
        self.flat_rates = {
            "بازرگانی": 185,
            "پیشەسازی گەورە": 125,
            "پیشەسازی": 160,
            "میری": 160,
            "کشتوکاڵ": 60
        }
        
        self.home_tiers = [
            (400, 72),
            (400, 108),
            (400, 172),
            (400, 265),
            (999999, 350)
        ]
        
        self.volt = 220  # ڤۆڵتی ستاندارد

    def run(self):
        st.title("⚡ سیستەمی پێشکەوتووی هەژمارکردنی کارەبا ⚡")
        st.write("---")
        
        # دەستپێکردنی حاڵەت
        if "main_mode" not in st.session_state:
            st.session_state.main_mode = "price"
        
        # دوو دووگمە بۆ هەڵبژاردنی بەش
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("هەژمارکردنی نرخ", use_container_width=True, type="primary"):
                st.session_state.main_mode = "price"
        
        with col2:
            if st.button("حیسابی تەکنیکی", use_container_width=True, type="secondary"):
                st.session_state.main_mode = "technical"
        
        st.write("---")
        
        if st.session_state.main_mode == "price":
            self.price_calculator()
        else:
            self.technical_calculator()

    def price_calculator(self):
        """حیسابکردنی نرخی کارەبا"""
        st.subheader("هەژمارکردنی نرخی کارەبا")
        st.write("")
        
        category = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )

        st.write("")
        
        if "mode" not in st.session_state:
            st.session_state.mode = "kwh_to_dinar"

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("kWh بۆ دینار", use_container_width=True, type="primary"):
                st.session_state.mode = "kwh_to_dinar"
        
        with col2:
            if st.button("دینار بۆ kWh", use_container_width=True, type="secondary"):
                st.session_state.mode = "dinar_to_kwh"

        st.write("---")

        if st.session_state.mode == "kwh_to_dinar":
            st.subheader("گۆڕینی kWh بۆ دینار")
            kwh = st.number_input("بڕی کارەبا داخڵ بکە (kWh):", min_value=0, step=1)
            
            if st.button("هەژمارکردن", type="primary", use_container_width=True):
                if kwh > 0:
                    self.calculate_price(category, kwh)
                else:
                    st.warning("تکایە ژمارەیەک زیاتر لە سفر داخڵ بکە")
        
        else:
            st.subheader("گۆڕینی دینار بۆ kWh")
            money = st.number_input("بڕی پارە داخڵ بکە (دینار):", min_value=0, step=1000)
            
            if st.button("هەژمارکردن", type="primary", use_container_width=True):
                if money > 0:
                    self.calculate_units(category, money)
                else:
                    st.warning("تکایە ژمارەیەک زیاتر لە سفر داخڵ بکە")

    def technical_calculator(self):
        """حیسابە تەکنیکییەکان"""
        st.subheader("حیسابە تەکنیکییەکانی کارەبا")
        st.write("")
        
        calc_type = st.selectbox(
            "جۆری حیساب هەڵبژێرە:",
            ["وات بۆ ئەمپێر", "وات بۆ کیلۆوات", "ئەمپێر بۆ کیلۆوات"]
        )
        
        st.write("")
        
        if calc_type == "وات بۆ ئەمپێر":
            self.watt_to_ampere()
        elif calc_type == "وات بۆ کیلۆوات":
            self.watt_to_kwh()
        else:
            self.ampere_to_kwh()

    def watt_to_ampere(self):
        """گۆڕینی وات بۆ ئەمپێر"""
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.write("### گۆڕینی وات بۆ ئەمپێر")
        st.write(f"**ڤۆڵت:** {self.volt} ڤۆڵت")
        st.write("")
        
        col1, col2 = st.columns(2)
        with col1:
            watt = st.number_input("وات داخڵ بکە:", min_value=0, step=10, key="watt_amp")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("حیسابکردن", type="primary", use_container_width=True, key="calc_watt_amp"):
            if watt > 0:
                ampere = watt / self.volt
                st.markdown(f'<div class="result-box">ئەنجام: {ampere:.2f} ئەمپێر</div>', unsafe_allow_html=True)
                st.info(f"**فۆرمول:** ئەمپێر = وات ÷ ڤۆڵت")
                st.info(f"**حیساب:** {watt} ÷ {self.volt} = {ampere:.2f} ئەمپێر")

    def watt_to_kwh(self):
        """گۆڕینی وات بۆ کیلۆوات"""
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.write("### گۆڕینی وات بۆ کیلۆوات")
        st.write("")
        
        col1, col2 = st.columns(2)
        with col1:
            watt = st.number_input("وات داخڵ بکە:", min_value=0, step=10, key="watt_kwh")
        with col2:
            hours = st.number_input("کاتژمێر داخڵ بکە:", min_value=0, step=1, key="hours_kwh")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("حیسابکردن", type="primary", use_container_width=True, key="calc_watt_kwh"):
            if watt > 0 and hours > 0:
                kwh = (watt * hours) / 1000
                st.markdown(f'<div class="result-box">ئەنجام: {kwh:.2f} کیلۆوات</div>', unsafe_allow_html=True)
                st.info(f"**فۆرمول:** کیلۆوات = (وات × کاتژمێر) ÷ 1000")
                st.info(f"**حیساب:** ({watt} × {hours}) ÷ 1000 = {kwh:.2f} کیلۆوات")

    def ampere_to_kwh(self):
        """گۆڕینی ئەمپێر بۆ کیلۆوات"""
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.write("### گۆڕینی ئەمپێر بۆ کیلۆوات")
        st.write(f"**ڤۆڵت:** {self.volt} ڤۆڵت")
        st.write("")
        
        col1, col2 = st.columns(2)
        with col1:
            ampere = st.number_input("ئەمپێر داخڵ بکە:", min_value=0.0, step=0.1, key="amp_kwh")
        with col2:
            hours = st.number_input("کاتژمێر داخڵ بکە:", min_value=0, step=1, key="hours_amp")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("حیسابکردن", type="primary", use_container_width=True, key="calc_amp_kwh"):
            if ampere > 0 and hours > 0:
                kwh = (ampere * self.volt * hours) / 1000
                st.markdown(f'<div class="result-box">ئەنجام: {kwh:.2f} کیلۆوات</div>', unsafe_allow_html=True)
                st.info(f"**فۆرمول:** کیلۆوات = (ئەمپێر × ڤۆڵت × کاتژمێر) ÷ 1000")
                st.info(f"**حیساب:** ({ampere} × {self.volt} × {hours}) ÷ 1000 = {kwh:.2f} کیلۆوات")

    def calculate_price(self, category, kwh):
        """kWh دەگۆڕێت بۆ دینار"""
        total_cost = 0
        
        if category == "ماڵان":
            st.write("### وردەکاری هەژمارکردن:")
            st.write("")
            
            temp_usage = kwh
            tier_names = ["پلەی یەکەم", "پلەی دووەم", "پلەی سێیەم", "پلەی چوارەم", "پلەی پێنجەم"]
            
            for idx, (limit, price) in enumerate(self.home_tiers):
                if temp_usage > 0:
                    consumed = min(temp_usage, limit)
                    cost = consumed * price
                    total_cost += cost
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"**{tier_names[idx]}**")
                    with col2:
                        st.write(f"{consumed:,.0f} kWh")
                    with col3:
                        st.write(f"{price} دینار")
                    with col4:
                        st.write(f"{cost:,.0f} دینار")
                    
                    temp_usage -= consumed
            
            st.markdown("---")
            st.success(f"### کۆی گشتی: {total_cost:,} دینار")
            
            st.markdown("---")
            st.write("### نرخەکانی کارەبا بۆ ماڵان:")
            st.write("")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write("**تا 400**")
                st.write("72 دینار")
            with col2:
                st.write("**تا 800**")
                st.write("108 دینار")
            with col3:
                st.write("**تا 1200**")
                st.write("172 دینار")
            with col4:
                st.write("**تا 1600**")
                st.write("265 دینار")
            with col5:
                st.write("**زیاتر**")
                st.write("350 دینار")
            
        else:
            total_cost = kwh * self.flat_rates[category]
            st.success(f"### کۆی گشتی: {total_cost:,} دینار")
            
            st.markdown("---")
            st.write(f"### نرخی کارەبا بۆ {category}:")
            st.write("")
            st.write(f"**نرخی هەر یەکە:** {self.flat_rates[category]} دینار/kWh")

    def calculate_units(self, category, money):
        """دینار دەگۆڕێت بۆ kWh"""
        total_units = 0
        
        if category == "ماڵان":
            remaining = money
            
            for limit, price in self.home_tiers:
                if remaining <= 0:
                    break
                
                max_cost_this_tier = limit * price
                
                if remaining >= max_cost_this_tier:
                    total_units += limit
                    remaining -= max_cost_this_tier
                else:
                    total_units += remaining / price
                    remaining = 0
        else:
            total_units = money / self.flat_rates[category]

        st.info(f"### بڕی کارەبا: {round(total_units, 2):,} kWh")
        
        st.markdown("---")
        if category == "ماڵان":
            st.write("### نرخەکانی کارەبا بۆ ماڵان:")
            st.write("")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write("**تا 400**")
                st.write("72 دینار")
            with col2:
                st.write("**تا 800**")
                st.write("108 دینار")
            with col3:
                st.write("**تا 1200**")
                st.write("172 دینار")
            with col4:
                st.write("**تا 1600**")
                st.write("265 دینار")
            with col5:
                st.write("**زیاتر**")
                st.write("350 دینار")
        else:
            st.write(f"### نرخی کارەبا بۆ {category}:")
            st.write("")
            st.write(f"**نرخی هەر یەکە:** {self.flat_rates[category]} دینار/kWh")

if __name__ == "__main__":
    app = ElectricityCalculator()
    app.run()
