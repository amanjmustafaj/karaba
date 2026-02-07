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
    .stRadio > div { justify-content: center !important; }
    .stButton > button {
        display: block; margin: 20px auto !important; width: 250px !important;
        height: 55px; background-color: #28a745; color: white; font-size: 20px !important;
        border: none; border-radius: 10px; font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #218838;
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
        
        # پلەکانی ماڵان: (سنووری kWh، نرخی هەر kWh)
        self.home_tiers = [
            (400, 72),    # یەکەم 400 kWh بە 72 دینار
            (400, 108),   # دووەم 400 kWh بە 108 دینار
            (400, 172),   # سێیەم 400 kWh بە 172 دینار
            (400, 260),   # چوارەم 400 kWh بە 260 دینار
            (999999, 350) # زیاتر بە 350 دینار
        ]

    def run(self):
        st.title("⚡ سیستەمی هەژمارکردنی کارەبا")
        st.write("---")

        # هەڵبژاردنی جۆری هاوبەش
        category = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )

        st.write("")
        
        # ڕادیۆ بۆ هەڵبژاردنی ئاراستە
        mode = st.radio(
            "جۆری هەژمارکردن:",
            ["🔢 kWh ➡️ دینار", "💰 دینار ➡️ kWh"],
            horizontal=True
        )

        st.write("---")

        # هەژمارکردن بەپێی ئاراستە
        if mode == "🔢 kWh ➡️ دینار":
            kwh = st.number_input("بڕی کارەبا داخڵ بکە (kWh):", min_value=0, step=1)
            if st.button("⚡ هەژمارکردن"):
                if kwh > 0:
                    self.calculate_price(category, kwh)
                else:
                    st.warning("تکایە ژمارەیەک زیاتر لە سفر داخڵ بکە!")
        else:
            money = st.number_input("بڕی پارە داخڵ بکە (دینار):", min_value=0, step=1000)
            if st.button("⚡ هەژمارکردن"):
                if money > 0:
                    self.calculate_units(category, money)
                else:
                    st.warning("تکایە ژمارەیەک زیاتر لە سفر داخڵ بکە!")

    def calculate_price(self, category, kwh):
        """kWh دەگۆڕێت بۆ دینار"""
        total_cost = 0
        
        if category == "ماڵان":
            temp_usage = kwh
            for limit, price in self.home_tiers:
                if temp_usage > 0:
                    consumed = min(temp_usage, limit)
                    total_cost += consumed * price
                    temp_usage -= consumed
        else:
            total_cost = kwh * self.flat_rates[category]
        
        st.success(f"💰 **تێچووی گشتی: {total_cost:,} دینار**")
        st.balloons()

    def calculate_units(self, category, money):
        """دینار دەگۆڕێت بۆ kWh"""
        total_units = 0
        
        if category == "ماڵان":
            remaining = money
            
            for limit, price in self.home_tiers:
                if remaining <= 0:
                    break
                
                # تێچووی تەواوی ئەم پلەیە
                max_cost_this_tier = limit * price
                
                if remaining >= max_cost_this_tier:
                    # ئەگەر پارەکە بەسە بۆ تەواوی ئەم پلەیە
                    total_units += limit
                    remaining -= max_cost_this_tier
                else:
                    # ئەگەر تەنها بەشێک لەم پلەیە دەکڕێت
                    total_units += remaining / price
                    remaining = 0
        else:
            total_units = money / self.flat_rates[category]

        st.info(f"⚡ **بڕی کارەبا: {round(total_units, 2):,} kWh**")
        st.balloons()

if __name__ == "__main__":
    app = ElectricityCalculator()
    app.run()
