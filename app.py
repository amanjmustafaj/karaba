import streamlit as st

class CalKWH:
    def __init__(self):
        self.kwh = 0
        self.low_price = 72
        self.mid_price = 108
        self.high_price = 175
        self.business = 150
        
    def calculate_home(self, kwh):
        """حیسابکردنی کارەبای ماڵان"""
        if kwh <= 400:
            total = kwh * self.low_price
            return f"رێژەی بەکارهێنانی کارەبا {kwh} kWh ە کۆی گشتی دەکاتە {total:,} دینار"
        
        elif kwh <= 800:
            part1 = 400 * self.low_price
            part2 = (kwh - 400) * self.mid_price
            total = part1 + part2
            return f"""
لە 400 kWh × {self.low_price} ← {part1:,} دینار
لە {kwh-400} kWh × {self.mid_price} ← {part2:,} دینار
کۆی گشتی: {total:,} دینار
"""
        
        else:
            part1 = 400 * self.low_price
            part2 = 400 * self.mid_price
            part3 = (kwh - 800) * self.high_price
            total = part1 + part2 + part3
            return f"""
لە 400 kWh × {self.low_price} ← {part1:,} دینار
لە 400 kWh × {self.mid_price} ← {part2:,} دینار
لە {kwh-800} kWh × {self.high_price} ← {part3:,} دینار
کۆی گشتی: {total:,} دینار
"""
    
    def calculate_business(self, kwh):
        """حیسابکردنی کارەبای بازرگانی"""
        total = kwh * self.business
        return f"رێژەی بەکارهێنانی کارەبا {kwh} × {self.business} ← {total:,} دینار"


# پرۆگرامی سەرەکی
st.title("حیسابکردنی نرخی کارەبا")

# دروستکردنی کلاس
calc = CalKWH()



user_type = st.radio("جۆر هەڵبژێرە:", [1, 2], format_func=lambda x: "ماڵان" if x == 1 else "بازرگانی")

# نووسینی بڕی کارەبا
st.write("تکایە رێژەی بەکارهێنانی کارەبا بنووسە بە kWh")
kwh = st.number_input("kWh:", min_value=0, value=0, step=1)

# حیسابکردن و نیشاندان
if kwh > 0:
    if user_type == 1:
        result = calc.calculate_home(kwh)
    else:
        result = calc.calculate_business(kwh)
    
    st.success(result)

