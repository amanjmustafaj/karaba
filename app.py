import streamlit as st

class CalKWH:
    def __init__(self):
        self.kwh = 0
        self.low_price = 72
        self.mid_price = 108
        self.high_price = 175
        self.business = 150
    
    # حیسابکردنی کارەبای ماڵان
    def calculate_home(self, kwh):
        if kwh <= 400:
            total = kwh * self.low_price
            details = [(kwh, self.low_price, total)]
            return total, details
        
        elif kwh <= 800:
            part1 = 400 * self.low_price
            part2 = (kwh - 400) * self.mid_price
            total = part1 + part2
            details = [
                (400, self.low_price, part1),
                (kwh - 400, self.mid_price, part2)
            ]
            return total, details
        
        else:
            part1 = 400 * self.low_price
            part2 = 400 * self.mid_price
            part3 = (kwh - 800) * self.high_price
            total = part1 + part2 + part3
            details = [
                (400, self.low_price, part1),
                (400, self.mid_price, part2),
                (kwh - 800, self.high_price, part3)
            ]
            return total, details
    
    # حیسابکردنی کارەبای بازرگانی
    def calculate_business(self, kwh):
        total = kwh * self.business
        details = [(kwh, self.business, total)]
        return total, details


# ڕێکخستنی پەڕە
st.set_page_config(page_title="حیسابکردنی کارەبا", layout="centered")

# CSS بۆ ناوەڕاستکردنی نووسین
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }
    div[data-testid="column"] {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# سەرناو
st.title("حیسابکردنی نرخی کارەبا")
st.markdown("---")

# دروستکردنی کلاس
calc = CalKWH()

# هەڵبژاردنی جۆر
st.subheader("جۆری بەکارهێنەر")


user_type = st.radio(
    "جۆر هەڵبژێرە:", 
    [1, 2], 
    format_func=lambda x: "ماڵان" if x == 1 else "بازرگانی",
    horizontal=True
)

st.markdown("---")

# نووسینی بڕی کارەبا
st.subheader("بڕی کارەبا")
kwh = st.number_input(
    "تکایە رێژەی بەکارهێنانی کارەبا بنووسە بە kWh:",
    min_value=0,
    value=0,
    step=10
)

st.markdown("---")

# حیسابکردن و نیشاندان
if kwh > 0:
    st.subheader("ئەنجامی حیساب")
    
    if user_type == 1:
        # ماڵان
        total, details = calc.calculate_home(kwh)
        
        # نیشاندانی وردەکاری
        st.markdown("#### وردەکاری حیسابەکە:")
        
        for i, (amount, price, cost) in enumerate(details, 1):
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(f"**بەشی {i}**")
            with col2:
                st.write(f"{amount:,} kWh × {price} دینار")
            with col3:
                st.write(f"**{cost:,} دینار**")
        
        st.markdown("---")
        st.success(f"### کۆی گشتی: **{total:,} دینار**")
        
    else:
        # بازرگانی
        total, details = calc.calculate_business(kwh)
        
        st.markdown("#### وردەکاری حیسابەکە:")
        
        amount, price, cost = details[0]
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            st.write("**کارەبای بازرگانی**")
        with col2:
            st.write(f"{amount:,} kWh × {price} دینار")
        with col3:
            st.write(f"**{cost:,} دینار**")
        
        st.markdown("---")
        st.success(f"### کۆی گشتی: **{total:,} دینار**")

else:
    st.info("تکایە بڕی کارەبا بنووسە بۆ بینینی ئەنجام")

st.markdown("---")
st.caption("سیستەمی حیسابکردنی نرخی کارەبا - هەرێمی کوردستان")
