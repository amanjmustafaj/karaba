import streamlit as st

# ==========================================
# 1. Page Configuration & Styling
# ==========================================
st.set_page_config(page_title="هەژمارکردنی کارەبا", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { text-align: center; direction: rtl; }
    h1, h2, h3, p, div { text-align: center !important; }
    .stSelectbox label, .stNumberInput label, .stRadio label {
        text-align: center !important; width: 100%; font-size: 18px; font-weight: bold;
    }
    .stButton > button {
        display: block; margin: 20px auto !important; width: 250px !important;
        height: 50px; background-color: #007bff; color: white; font-size: 18px !important;
        border: none; border-radius: 8px;
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

    def run(self):
        st.title("سیستەمی پێشکەوتووی هەژمارکردنی کارەبا")
        st.write("---")

        category = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )

        st.write("")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔢 kWh ➡️ دینار"):
                st.session_state.mode = "kwh_to_dinar"
        
        with col2:
            if st.button("💰 دینار ➡️ kWh"):
                st.session_state.mode = "dinar_to_kwh"

        if "mode" not in st.session_state:
            st.session_state.mode = "kwh_to_dinar"

        st.write("---")

        if st.session_state.mode == "kwh_to_dinar":
            kwh = st.number_input("بڕی کارەبا داخڵ بکە (kWh):", min_value=0, step=1)
            if st.button("هەژمارکردن ⚡"):
                self.calculate_price(category, kwh)
        else:
            money = st.number_input("بڕی پارە داخڵ بکە (دینار):", min_value=0, step=1000)
            if st.button("هەژمارکردن ⚡"):
                self.calculate_units(category, money)

    def calculate_price(self, category, kwh):
        total_cost = 0
        if category == "ماڵان":
            temp_usage = kwh
            tiers = [(400, 72), (400, 108), (400, 172), (400, 260), (999999, 350)]
            for limit, price in tiers:
                if temp_usage > 0:
                    consumed = min(temp_usage, limit)
                    total_cost += consumed * price
                    temp_usage -= consumed
        else:
            total_cost = kwh * self.flat_rates[category]
        
        st.success(f"💰 **تێچووی گشتی: {total_cost:,} دینار**")

    def calculate_units(self, category, money):
        total_units = 0
        
        if category == "ماڵان":
            remaining = money
            tiers = [(400, 72), (400, 108), (400, 172), (400, 260), (999999, 350)]
            
            for limit, price in tiers:
                if remaining > 0:
                    max_cost_this_tier = limit * price
                    if remaining >= max_cost_this_tier:
                        total_units += limit
                        remaining -= max_cost_this_tier
                    else:
                        total_units += remaining / price
                        remaining = 0
                        break
        else:
            total_units = money / self.flat_rates[category]

        st.info(f"⚡ **بڕی کارەبا: {round(total_units, 2):,} kWh**")

if __name__ == "__main__":
    app = ElectricityCalculator()
    app.run()
