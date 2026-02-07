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
        display: block; margin: 20px auto !important; width: 200px !important;
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

        # لێرە هەڵدەبژێریت چیت دەوێت
        mode = st.radio(
            "جۆری گۆڕین هەڵبژێرە:",
            ["بڕی یەکە (kWh) ⬅️ نرخ (دینار)", "نرخ (دینار) ⬅️ بڕی یەکە (kWh)"]
        )

        category = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )

        val = st.number_input("بڕەکە داخڵ بکە:", min_value=0, step=1)

        if st.button("هەژمارکردن"):
            if mode == "بڕی یەکە (kWh) ⬅️ نرخ (دینار)":
                self.calculate_price(category, val)
            else:
                self.calculate_units(category, val)

    def calculate_price(self, category, kwh):
        # هەمان لۆژیکی کۆدە کۆنەکەت بۆ دەرکردنی نرخ
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
        
        st.success(f"💰 تێچووی گشتی: **{total_cost:,}** دینار")

    def calculate_units(self, category, money):
        # ئەو لۆژیکەی خۆت کە ناردت بۆ دەرکردنی بڕی یەکە (kWh)
        total_units = 0
        
        if category == "پیشەسازی گەورە":
            total_units = money / 125
        elif category == "بازرگانی":
            total_units = money / 185
        elif category in ["میری", "پیشەسازی"]:
            total_units = money / 160
        elif category == "کشتوکاڵ":
            total_units = money / 60
        else: # ماڵان بەپێی ئەو مەرجانەی خۆت داتنابوو
            if money < 28800:
                total_units = money / 72
            elif 28800 <= money <= 86400:
                total_units = money / 108
            elif 86400 < money <= 210000:
                total_units = money / 175
            elif 210000 < money <= 400000:
                total_units = money / 250
            else:
                total_units = money / 350

        st.info(f"⚡ بڕی کارەبای بەکارهاتوو: **{round(total_units, 2):,}** kWh")

if __name__ == "__main__":
    app = ElectricityCalculator()
    app.run()
