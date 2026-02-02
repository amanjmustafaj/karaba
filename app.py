import streamlit as st

# ڕێکخستنی شێوازی پەڕەکە
st.set_page_config(page_title="هەژمارکردنی کارەبا", page_icon="⚡")

# ستایلی تایبەت بۆ زمانی کوردی (RTL)
st.markdown("""
    <style>
    body, div, p, h1, h2, h3, h4, span, label {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', sans-serif;
    }
    .stSelectbox, .stNumberInput {
        direction: rtl;
    }
    /* بۆ ئەوەی خشتەکان جوان دەرکەون */
    div[data-testid="column"] {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

class CalKWh:
    def __init__(self):
        # نرخی ماڵان (قۆناغ بە قۆناغ)
        self.home_prices = {
            "tier1": 72,   # 1 - 400
            "tier2": 108,  # 401 - 800
            "tier3": 172,  # 801 - 1200
            "tier4": 260,  # 1201 - 1600
            "tier5": 350   # > 1600
        }
        
        # نرخی شوێنەکانی تر (جێگیر)
        self.flat_prices = {
            "بازرگانی": 185,
            "پیشەسازی گەورە": 125,
            "پیشەسازی": 160,
            "میری (حکومی)": 160,
            "کشتوکاڵ": 60
        }

    def run_app(self):
        st.title(" سیستەمی زیرەکی هەژمارکردنی کارەبا")
        st.write("بەخێربێیت ، جۆری هاوبەش هەڵبژێرە بۆ هەژمارکردنی.")

        # دروستکردنی لیستی هەڵبژاردن
        options = ["ماڵان"] + list(self.flat_prices.keys())
        user_type = st.selectbox("جۆری بەکارهێنەر هەڵبژێرە:", options)

        kwh = st.number_input("بڕی بەکارهێنان بە (kWh) بنووسە:", min_value=0, step=1)

        if st.button("هەژمارکردنی بکە "):
            if kwh == 0:
                st.warning("تکایە بڕی کارەبا بنووسە!")
            elif user_type == "ماڵان":
                self.calculate_home(kwh)
            else:
                self.calculate_flat(user_type, kwh)

    def calculate_flat(self, u_type, kwh):
        price = self.flat_prices[u_type]
        total = kwh * price
        st.success(f"جۆری بەکارهێنەر: **{u_type}**")
        st.info(f"نرخی یەکەیەک: {price} دینار")
        st.metric(label="کۆی گشتی پارەکە", value=f"{total:,} دینار")

    def calculate_home(self, kwh):
        total = 0
        remaining_kwh = kwh
        breakdown = [] # بۆ هەڵگرتنی وردەکارییەکان

        # قۆناغی یەکەم (1-400)
        if remaining_kwh > 0:
            amount = min(remaining_kwh, 400)
            cost = amount * self.home_prices["tier1"]
            total += cost
            breakdown.append(f"400 ــی یەکەم: {amount} * {self.home_prices['tier1']} = {cost:,}")
            remaining_kwh -= amount

        # قۆناغی دووەم (401-800)
        if remaining_kwh > 0:
            amount = min(remaining_kwh, 400)
            cost = amount * self.home_prices["tier2"]
            total += cost
            breakdown.append(f"400 ــی دووەم: {amount} * {self.home_prices['tier2']} = {cost:,}")
            remaining_kwh -= amount

        # قۆناغی سێیەم (801-1200) - نرخ 172
        if remaining_kwh > 0:
            amount = min(remaining_kwh, 400)
            cost = amount * self.home_prices["tier3"]
            total += cost
            breakdown.append(f"400 ــی سێیەم: {amount} * {self.home_prices['tier3']} = {cost:,}")
            remaining_kwh -= amount

        # قۆناغی چوارەم (1201-1600) - نرخ 260
        if remaining_kwh > 0:
            amount = min(remaining_kwh, 400)
            cost = amount * self.home_prices["tier4"]
            total += cost
            breakdown.append(f"400 ــی چوارەم: {amount} * {self.home_prices['tier4']} = {cost:,}")
            remaining_kwh -= amount

        # قۆناغی پێنجەم (سەرووی 1600) - نرخ 350
        if remaining_kwh > 0:
            cost = remaining_kwh * self.home_prices["tier5"]
            total += cost
            breakdown.append(f"سەرووی 1600: {remaining_kwh} * {self.home_prices['tier5']} = {cost:,}")

        # نیشاندانی ئەنجامەکان
        st.success("وردەکاری هەژمارکردنی ماڵان:")
        for line in breakdown:
            st.text(line)
        
        st.markdown("---")
        st.metric(label="کۆی گشتی پارەکە", value=f"{total:,} دینار")

if __name__ == "__main__":
    app = CalKWh()
    app.run_app()
