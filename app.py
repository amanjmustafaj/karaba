import streamlit as st

class CalKWH:
    def __init__(self):
        self.low_price = 72
        self.mid_price = 108
        self.high_price = 175
        self.business_price = 150
        
    def calculate_home(self, kwh):
        """حیسابکردنی کارەبای ماڵان"""
        if kwh <= 400:
            total = kwh * self.low_price
            return {"total": total, "details": [(kwh, self.low_price, total)]}
        
        elif kwh <= 800:
            part1 = 400 * self.low_price
            part2 = (kwh - 400) * self.mid_price
            total = part1 + part2
            return {
                "total": total,
                "details": [
                    (400, self.low_price, part1),
                    (kwh - 400, self.mid_price, part2)
                ]
            }
        else:
            part1 = 400 * self.low_price
            part2 = 400 * self.mid_price
            part3 = (kwh - 800) * self.high_price
            total = part1 + part2 + part3
            return {
                "total": total,
                "details": [
                    (400, self.low_price, part1),
                    (400, self.mid_price, part2),
                    (kwh - 800, self.high_price, part3)
                ]
            }
    
    def calculate_business(self, kwh):
        """حیسابکردنی کارەبای بازرگانی"""
        total = kwh * self.business_price
        return {"total": total, "details": [(kwh, self.business_price, total)]}

def main():
    st.set_page_config(page_title="حیسابکردنی کارەبا", layout="centered")
    st.title("⚡ سیستەمی حیسابکردنی نرخی کارەبا")
    
    calculator = CalKWH()
    
    # هەڵبژاردنی جۆری بەکارهێنەر
    user_type = st.radio(
        "جۆری بەکارهێنەر هەڵبژێرە:",
        options=[("ماڵان", 1), ("بازرگانی", 2)],
        format_func=lambda x: x[0],
        horizontal=True
    )
    
    # خانەی نووسینی kwh
    kwh = st.number_input(
        "رێژەی بەکارهێنانی کارەبا بنووسە (kWh):",
        min_value=0,
        value=0,
        step=1
    )
    
    # حیسابکردن
    if kwh > 0:
        if user_type[1] == 1:
            st.subheader("📊 کارەبای ماڵان")
            result = calculator.calculate_home(kwh)
            
            if len(result["details"]) > 1:
                st.markdown("### وردەکاری حیسابەکە:")
                for i, (amount, price, cost) in enumerate(result["details"], 1):
                    st.info(f"🔹 بەشی {i}: {amount} kWh × {price} دینار = {cost:,} دینار")
                st.divider()
            
            st.success(f"💰 **کۆی گشتی: {result['total']:,} دینار**")
            
        else:  # بازرگانی
            st.subheader("🏢 کارەبای بازرگانی")
            result = calculator.calculate_business(kwh)
            st.info(f"📊 {kwh} kWh × {calculator.business_price} دینار")
            st.success(f"💰 **کۆی گشتی: {result['total']:,} دینار**")

if __name__ == "__main__":
    main()
