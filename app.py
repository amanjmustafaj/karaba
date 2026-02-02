import streamlit as st

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
        border: none;
        border-radius: 8px;
    }
    /* ستایل بۆ خشتە دەستکردەکە */
    .table-header {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .table-row {
        padding: 8px;
        border-bottom: 1px solid #eee;
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

    def get_input(self):
        st.title("⚡ سیستەمی هەژمارکردنی نرخی کارەبا")
        st.write("---")

        user_type = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )
        kwh = st.number_input("بڕی بەکارهێنان بە (kWh):", min_value=0, step=1)
        return user_type, kwh

    def calculate(self):
        user_type, kwh = self.get_input()

        if st.button("هەژمارکردن"):
            details = []
            total_price = 0

            if user_type == "ماڵان":
                temp_kwh = kwh
                tiers = [
                    ("٤٠٠ی یەکەم", 400, self.prices_home[0]),
                    ("٤٠٠ی دووەم", 400, self.prices_home[1]),
                    ("٤٠٠ی سێیەم", 400, self.prices_home[2]),
                    ("٤٠٠ی چوارەم", 400, self.prices_home[3]),
                    ("سەرووی ١٦٠٠", 999999, self.prices_home[4])
                ]

                for name, limit, price in tiers:
                    if temp_kwh > 0:
                        used = min(temp_kwh, limit)
                        cost = used * price
                        details.append({"part": name, "qty": used, "prc": price, "total": cost})
                        total_price += cost
                        temp_kwh -= used
            else:
                price = self.flat_prices[user_type]
                total_price = kwh * price
                details.append({"part": user_type, "qty": kwh, "prc": price, "total": total_price})

            # نیشاندانی وردەکاری بە شێوەی خشتە (بە ستوونەکان)
            st.markdown("### 📊 وردەکاری هەژمارکردن")
            
            # سەردێڕی خشتە
            h1, h2, h3, h4 = st.columns(4)
            with h1: st.markdown("**قۆناغ / جۆر**")
            with h2: st.markdown("**بڕ (kWh)**")
            with h3: st.markdown("**نرخ**")
            with h4: st.markdown("**تێچوو**")
            st.markdown("---")

            # ڕیزەکانی خشتە
            for item in details:
                r1, r2, r3, r4 = st.columns(4)
                with r1: st.write(item["part"])
                with r2: st.write(f"{item['qty']:,}")
                with r3: st.write(f"{item['prc']}")
                with r4: st.write(f"**{item['total']:,}**")

            st.markdown("---")
            st.success(f"💰 کۆی گشتی پارەکە: **{total_price:,}** دینار")

if __name__ == "__main__":
    app = CalKWh()
    app.calculate()
