import streamlit as st

# ==========================================
# 1. Page Configuration & Styling (CSS)
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
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Main Class Structure
# ==========================================
class ElectricityCalculator:
    def __init__(self):
        # Residential pricing tiers (Residential/Home)
        self.residential_prices = [72, 108, 172, 260, 350]
        
        # Flat rates for other categories
        self.flat_rates = {
            "بازرگانی": 185,
            "پیشەسازی گەورە": 125,
            "پیشەسازی": 160,
            "میری": 160,
            "کشتوکاڵ": 60
        }

    def show_interface(self):
        st.title(" سیستەمی هەژمارکردنی نرخی کارەبا")
        st.write("---")

        user_category = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری(حکومی)", "کشتوکاڵ"]
        )
        
        usage_kwh = st.number_input("بڕی بەکارهێنان بە (kWh):", min_value=0, step=1)
        
        return user_category, usage_kwh

    def run_calculation(self):
        category, kwh = self.show_interface()

        if st.button("هەژمارکردن"):
            billing_details = []
            total_cost = 0

            if category == "ماڵان":
                temp_usage = kwh
                # Defining the tiers: (Label, Limit per tier, Price)
                tiers = [
                    ("٤٠٠ی یەکەم", 400, self.residential_prices[0]),
                    ("٤٠٠ی دووەم", 400, self.residential_prices[1]),
                    ("٤٠٠ی سێیەم", 400, self.residential_prices[2]),
                    ("٤٠٠ی چوارەم", 400, self.residential_prices[3]),
                    ("سەرووی ١٦٠٠", 9999999, self.residential_prices[4])
                ]

                for label, limit, price in tiers:
                    if temp_usage > 0:
                        consumed = min(temp_usage, limit)
                        cost_per_tier = consumed * price
                        billing_details.append({
                            "description": label, 
                            "units": consumed, 
                            "rate": price, 
                            "subtotal": cost_per_tier
                        })
                        total_cost += cost_per_tier
                        temp_usage -= consumed
            else:
                # Flat rate calculation for non-residential
                unit_price = self.flat_rates[category]
                total_cost = kwh * unit_price
                billing_details.append({
                    "description": category, 
                    "units": kwh, 
                    "rate": unit_price, 
                    "subtotal": total_cost
                })

            # Rendering the breakdown table
            st.markdown("### 📊 وردەکاری هەژمارکردن")
            
            # Header Columns
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.markdown("**قۆناغ / جۆر**")
            with col2: st.markdown("**بڕ (kWh)**")
            with col3: st.markdown("**نرخ**")
            with col4: st.markdown("**تێچوو**")
            st.markdown("---")

            # Row Data
            for item in billing_details:
                c1, c2, c3, c4 = st.columns(4)
                with c1: st.write(item["description"])
                with c2: st.write(f"{item['units']:,}")
                with c3: st.write(f"{item['rate']}")
                with c4: st.write(f"**{item['subtotal']:,}**")

            st.markdown("---")
            st.success(f"💰 کۆی گشتی پارەکە: **{total_cost:,}** دینار")

# ==========================================
# 3. Execution
# ==========================================
if __name__ == "__main__":
    app = ElectricityCalculator()
    app.run_calculation()

