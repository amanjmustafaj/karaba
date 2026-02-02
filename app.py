import streamlit as st

class calkwh:
    def __init__(self):
        self.kwh = 0
        self.low_price = 72
        self.mid_price = 108
        self.high_price = 175
        self.bussnis = 150
        self.user_type = 0
        
        st.set_page_config(page_title="حیسابکردنی کارەبا", layout="centered")
        st.title("سیستەمی حیسابکردنی نرخی کارەبا")
        
        st.info("بۆ زانینی نرخی کارەبای ماڵان ژمارە یەک داگرە | بۆ زانینی نرخی کارەبای دووکان یان بازرگانی ژمارە دوو داگرە")
        
        # لێرە بەکارهێنەر ژمارەکە هەڵدەبژێرێت
        self.user_type = st.number_input("تکایە ژمارەکە بنووسە (1 یان 2):", min_value=0, max_value=2, step=1)

    def calculate_kwh(self):
        kwh1, kwh2, kwh3, kwh4, kwh5 = 0, 0, 0, 0, 0
        
        if self.user_type == 1:
            st.subheader("بەشی کارەبای ماڵان")
            self.kwh = st.number_input("kwh تکایە رێژەی بەکار هێنانی کارەبا بنووسە بە", min_value=0, key="home_input")
            
            if st.button("حیساب بکە"):
                if self.kwh <= 400: 
                    kwh1 = (self.kwh * self.low_price)
                    st.success(f"⚡ بڕی بەکارهێنان: {self.kwh} kWh | 💰 کۆی گشتی پارەی کارەبا: {kwh1:,} دینار")
                elif self.kwh <= 800:
                    kwh1 = (400 * self.low_price) 
                    kwh2 = (self.kwh - 400) * self.mid_price
                    kwh3 = kwh1 + kwh2
                    st.info(f"📊 قۆناغی یەکەم: 400kWh × {self.low_price} ← {kwh1:,} دینار")
                    st.info(f"📊 قۆناغی دووەم: {self.kwh-400}kWh × {self.mid_price} ← {kwh2:,} دینار")

                    st.success(f"✅ کۆی گشتی پارەی کارەبا: **{kwh3:,}** دینار")
                else: 
                    kwh1 = (400 * self.low_price)
                    kwh2 = (400 * self.mid_price)
                    kwh3 = (self.kwh - 800) * self.high_price
                    kwh4 = kwh1 + kwh2 + kwh3
                    st.markdown("### 📊 وردەکاری حیسابەکە:")

                   # لێرە تەنیا وردەکارییەکان بە ڕوونی نیشان دەدەین
                    st.info(f"🔹 ٤٠٠ کیلۆواتی یەکەم (بە {self.low_price}): {kwh1:,} دینار")
                    st.info(f"🔹 ٤٠٠ کیلۆواتی دووەم (بە {self.mid_price}): {kwh2:,} دینار")
                    st.info(f"🔹 بڕی زیادە لە ٨٠٠ کیلۆوات (بە {self.high_price}): {kwh3:,} دینار")

                    st.divider() # هێڵێکی جیاکەرەوە بۆ جوانی
                    st.success(f"💰 کۆی گشتی پارەی کارەبا: **{kwh4:,}** دینار")
            
        elif self.user_type == 2:
            st.subheader("بەشی کارەبای بازرگانی")
            self.kwh = st.number_input("kwh تکای رێژەی بەکار هێنانی کارەبا بنووسە بە", min_value=0, key="biz_input")
            
            if st.button("حیساب بکە"):
                kwh5 = self.kwh * self.bussnis
                st.success(f"🏢 کارەبای بازرگانی: {self.kwh} kWh × {self.bussnis} دینار ← کۆی گشتی: **{kwh5:,}** دینار")            
        elif self.user_type != 0:
            st.error("ببورە ژمارەکە هەڵەیە تکایە تەنیا ژمارە یەک یان دوو هەڵبژێرە")

# لێرەدا دەستپێدەکات
if __name__ == "__main__":
    k = calkwh()

    k.calculate_kwh()





