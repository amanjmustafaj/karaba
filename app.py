import streamlit as st
import pandas as pd

# ==========================================
# 1. ڕێکخستنی دیزاین و سەنتەرکردن (CSS)
# ==========================================
st.set_page_config(page_title="هەژمارکردنی کارەبا", page_icon="⚡")

st.markdown("""
    <style>
    .stApp {
        text-align: center;
        direction: rtl;
    }
    h1, h2, h3, p, div {
        text-align: center !important;
    }
    .stSelectbox label, .stNumberInput label {
        text-align: center !important;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton > button {
        display: block;
        margin: 20px auto !important;
        width: 200px !important;
        height: 50px;
        background-color: #007bff;
        color: white;
        font-size: 18px !important;
    }
    /* ستایل بۆ خشتەکە */
    .stDataFrame {
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. دروستکردنی کڵاس
# ==========================================
class CalKWh:
    def __init__(self):
        self.prices_home = [72, 108, 172, 260, 350]
        self.flat_prices = {
            "بازرگانی": 185,
            "پیشەسازی گەورە": 125,
            "پیشەسازی": 160,
            "میری": 160,
            "کشتوکاڵ": 60
        }

    def calculate(self):
        st.title("⚡ سیستەمی هەژمارکردنی نرخی کارەبا")
        st.write("---")

        user_type = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )

        kwh = st.number_input("بڕی بەکارهێنان بە (kWh):", min_value=0, step=1)

        if st.button("هەژمارکردن"):
            data_rows = []
            total_price = 0

            if user_type == "ماڵان":
                temp_kwh = kwh
                tiers = [
                    ("٤٠٠ی یەکەم", 400, self.prices_home[0]),
                    ("٤٠٠ی دووەم", 400, self.prices_home[1]),
                    ("٤٠٠ی سێیەم", 400, self.prices_home[2]),
                    ("٤٠٠ی چوارەم", 400, self.prices_home[3]),
                    ("سەرووی ١٦٠٠", float('inf'), self.prices_home[4])
                ]

                for name, limit, price in tiers:
                    if temp_kwh > 0:
                        used = min(temp_kwh, limit)
                        cost = used * price
                        data_rows.append({"قۆناغ": name, "بڕ (kWh)": used, "نرخ (دینار)": price, "تێچوو (دینار)": f"{cost:,}"})
                        total_price += cost
                        temp_kwh -= used
            else:
                # بۆ جۆرەکانی تر کە نرخەکەیان جێگیرە
                price = self.flat_prices[user_type]
                total_price = kwh * price
                data_rows.append({"جۆر": user_type, "بڕ (kWh)": kwh, "نرخ (دینار)": price, "تێچوو (دینار)": f"{total_price:,}"})

            # نیشاندانی ئەنجامەکان بە خشتە
            st.markdown("### 📊 وردەکاری هەژمارکردن")
            df = pd.DataFrame(data_rows)
            st.table(df) # بەکارهێنانی st.table بۆ ئەوەی وەک خشتەیەکی جێگیر دەرکەوێت

            st.markdown("---")
            st.success(f"💰 کۆی گشتی پارەکە: **{total_price:,}** دینار")

if __name__ == "__main__":
    app = CalKWh()
    app.calculate()
