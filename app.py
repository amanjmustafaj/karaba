import streamlit as st

# ==========================================
# 1. Page Configuration & Styling
# ==========================================
st.set_page_config(page_title="هەژمارکردنی کارەبا", page_icon="⚡")

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
        
        # پلەکانی ماڵان
        self.home_tiers = [
            (400, 72),
            (400, 108),
            (400, 172),
            (400, 260),
            (999999, 350)
        ]

    def run(self):
        st.title("سیستەمی هەژمارکردنی کارەبا")
        st.write("---")

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
            
        else:
            total_cost = kwh * self.flat_rates[category]
            st.success(f"### کۆی گشتی: {total_cost:,} دینار")

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

if __name__ == "__main__":
    app = ElectricityCalculator()
    app.run()
