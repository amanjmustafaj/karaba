import streamlit as st

# ==========================================
# 1. ڕێکخستنی دیزاین و سەنتەرکردن (CSS)
# ==========================================
st.set_page_config(page_title="هەژمارکردنی کارەبا", page_icon="⚡")

st.markdown("""
    <style>
    /* هەموو شتێک بهێنە ناوەڕاست */
    .stApp {
        text-align: center;
        direction: rtl;
    }
    
    /* سەنتەرکردنی ناونیشان و نووسینەکان */
    h1, h2, h3, p, div {
        text-align: center !important;
    }

    /* سەنتەرکردنی لیستی هەڵبژاردن و شوێنی ژمارە */
    .stSelectbox label, .stNumberInput label {
        text-align: center !important;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* سەنتەرکردنی ناوەڕۆکی ئینپوتەکان */
    .stSelectbox div[data-baseweb="select"] {
        direction: rtl; 
        text-align: center;
    }

    /* چاککردنی دوگمەکە بۆ ئەوەی تێک نەچێت و بکەوێتە ناوەڕاست */
    .stButton > button {
        display: block;
        margin: 20px auto !important;
        width: 200px !important;
        height: 50px;
        font-size: 18px !important;
        border-radius: 10px;
        background-color: #007bff;
        color: white;
    }
    
    /* بۆکسەکانی ئەنجام */
    .stAlert {
        direction: rtl;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. دروستکردنی کڵاس (Class Structure)
# ==========================================
class CalKWh:
    def __init__(self):
        # نرخەکان
        self.prices_home = [72, 108, 172, 260, 350] # نرخەکانی ماڵان
        self.price_business = 185      # بازرگانی
        self.price_large_ind = 125     # پیشەسازی گەورە
        self.price_ind = 160           # پیشەسازی
        self.price_gov = 160           # میری
        self.price_agri = 60           # کشتوکاڵ

    def get_user_input(self):
        st.title("⚡ سیستەمی هەژمارکردنی نرخی کارەبا")
        st.write("بۆ زانینی تێچووی کارەباکەت، زانیارییەکان پڕ بکەرەوە")
        st.write("---")

        # وەرگرتنی زانیاری
        user_type = st.selectbox(
            "جۆری هاوبەش هەڵبژێرە:",
            ["ماڵان", "بازرگانی", "پیشەسازی گەورە", "پیشەسازی", "میری", "کشتوکاڵ"]
        )

        kwh = st.number_input("بڕی بەکارهێنان بە (kWh):", min_value=0, step=1)
        
        return user_type, kwh

    def calculate(self):
        # وەرگرتنی زانیارییەکان
        user_type, kwh = self.get_user_input()

        # کاتێک کلیک لەسەر دوگمەی هەژمارکردن دەکرێت
        if st.button("هەژمارکردن"):
            total_price = 0
            
            # --- هەژمارکردنی ماڵان ---
            if user_type == "ماڵان":
                if kwh <= 400:
                    total_price = kwh * self.prices_home[0]
                elif kwh <= 800:
                    total_price = (400 * self.prices_home[0]) + \
                                  ((kwh - 400) * self.prices_home[1])
                elif kwh <= 1200:
                    total_price = (400 * self.prices_home[0]) + \
                                  (400 * self.prices_home[1]) + \
                                  ((kwh - 800) * self.prices_home[2])
                elif kwh <= 1600:
                    total_price = (400 * self.prices_home[0]) + \
                                  (400 * self.prices_home[1]) + \
                                  (400 * self.prices_home[2]) + \
                                  ((kwh - 1200) * self.prices_home[3])
                else: 
                    total_price = (400 * self.prices_home[0]) + \
                                  (400 * self.prices_home[1]) + \
                                  (400 * self.prices_home[2]) + \
                                  (400 * self.prices_home[3]) + \
                                  ((kwh - 1600) * self.prices_home[4])

            # --- هەژمارکردنی جۆرەکانی تر ---
            elif user_type == "بازرگانی":
                total_price = kwh * self.price_business
            
            elif user_type == "پیشەسازی گەورە":
                total_price = kwh * self.price_large_ind
            
            elif user_type == "پیشەسازی":
                total_price = kwh * self.price_ind
            
            elif user_type == "میری":
                total_price = kwh * self.price_gov
            
            elif user_type == "کشتوکاڵ":
                total_price = kwh * self.price_agri

            # --- نیشاندانی ئەنجام ---
            st.markdown("---")
            st.success(f"جۆری هاوبەش: {user_type}")
            st.success(f"💰 کۆی گشتی پارەکە: **{total_price:,}** دینار")

# ==========================================
# 3. کارپێکردنی بەرنامەکە
# ==========================================
if __name__ == "__main__":
    app = CalKWh()
    app.calculate()
