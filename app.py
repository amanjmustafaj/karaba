import streamlit as st

class ElectricityCalculator:
    """کلاسێک بۆ ژمێرینی نرخی کارەبا"""
    
    def __init__(self):
        # نرخەکانی کارەبای ماڵان (دینار بۆ هەر kWh)
        self.low_price = 72        # بۆ 0-400 kWh
        self.mid_price = 108  # بۆ 401-800 kWh
        self.high_price = 175       # بۆ زیاتر لە 800 kWh
        
        # نرخی کارەبای بازرگانی
        self.business_price = 150
    
    def calculate_home(self, kwh):
        """
        ژمێرینی نرخی کارەبای ماڵان
        
        پارامەتەر:
            kwh: بڕی کارەبای بەکارهاتوو بە کیلۆوات کاتژمێر
            
        گەڕاندنەوە:
            فەرهەنگێک کە کۆی گشتی و وردەکاریەکانی تێدایە
        """
        details = []
        
        if kwh <= 400:
            # هەموو بڕەکە بە نرخی نزم حیساب دەکرێت
            total = kwh * self.low_price
            details.append({
                'section': 'بەشی یەکەم',
                'amount': kwh,
                'price': self.low_price,
                'cost': total
            })
            
        elif kwh <= 800:
            # 400 کیلۆواتی یەکەم بە نرخی نزم
            part1 = 400 * self.low_price
            details.append({
                'section': 'بەشی یەکەم',
                'amount': 400,
                'price': self.low_price,
                'cost': part1
            })
            
            # بڕی ماوە بە نرخی مامناوەند
            part2 = (kwh - 400) * self.mid_price
            details.append({
                'section': 'بەشی دووەم',
                'amount': kwh - 400,
                'price': self.mid_price,
                'cost': part2
            })
            
            total = part1 + part2
            
        else:
            # 400 کیلۆواتی یەکەم بە نرخی نزم
            part1 = 400 * self.low_price
            details.append({
                'section': 'بەشی یەکەم (0-400 kWh)',
                'amount': 400,
                'price': self.low_price,
                'cost': part1
            })
            
            # 400 کیلۆواتی دووەم بە نرخی مامناوەند
            part2 = 400 * self.mid_price
            details.append({
                'section': 'بەشی دووەم (401-800 kWh)',
                'amount': 400,
                'price': self.mid_price,
                'cost': part2
            })
            
            # بڕی ماوە بە نرخی بەرز
            part3 = (kwh - 800) * self.high_price
            details.append({
                'section': 'بەشی سێیەم (زیاتر لە 800 kWh)',
                'amount': kwh - 800,
                'price': self.high_price,
                'cost': part3
            })
            
            total = part1 + part2 + part3
        
        return {'total': total, 'details': details}
    
    def calculate_business(self, kwh):
        """
        ژمێرینی نرخی کارەبای بازرگانی
        
        پارامەتەر:
            kwh: بڕی کارەبای بەکارهاتوو
            
        گەڕاندنەوە:
            فەرهەنگێک کە کۆی گشتی و وردەکاریەکانی تێدایە
        """
        total = kwh * self.business_price
        details = [{
            'section': 'کارەبای بازرگانی',
            'amount': kwh,
            'price': self.business_price,
            'cost': total
        }]
        
        return {'total': total, 'details': details}


def main():
    """فەنکشنی سەرەکی بۆ ڕێکخستنی ڕووکاری بەکارهێنەر"""
    
    # ڕێکخستنی پەڕە
    st.set_page_config(
        page_title="ژمێریاری کارەبا",
        layout="centered"
    )
    
    # سەرناو
    st.title("سیستەمی ژمێرینی نرخی کارەبا")
    st.markdown("---")
    
    # دروستکردنی ژمێریار
    calculator = ElectricityCalculator()
    
    # بەشی هەڵبژاردنی جۆری بەکارهێنەر
    st.subheader("١. جۆری بەکارهێنەر هەڵبژێرە")
    
    user_type = st.radio(
        "تکایە جۆری بەکارهێنەرت هەڵبژێرە:",
        options=['ماڵان', 'بازرگانی'],
        horizontal=True,
        help="کارەبای ماڵان نرخی جیاوازە لە کارەبای بازرگانی"
    )
    
    st.markdown("---")
    
    # بەشی نووسینی بڕی کارەبا
    st.subheader("٢. بڕی کارەبای بەکارهاتوو بنووسە")
    
    kwh_amount = st.number_input(
        "بڕی کارەبا بە کیلۆوات کاتژمێر (kWh):",
        min_value=0,
        max_value=100000,
        value=0,
        step=10,
        help="ئەم ژمارەیە لەسەر پسوڵەی کارەبادا دەبینیتەوە"
    )
    
    st.markdown("---")
    
    # نیشاندانی ئەنجام
    if kwh_amount > 0:
        st.subheader("٣. ئەنجامی ژمێریاری")
        
        # ژمێرینی نرخ بەپێی جۆری بەکارهێنەر
        if user_type == 'ماڵان':
            result = calculator.calculate_home(kwh_amount)
            
            # نیشاندانی وردەکاری
            if len(result['details']) > 1:
                st.info("**وردەکاری ژمێریاریەکە:**")
                
                for section in result['details']:
                    with st.container():
                        col1, col2, col3 = st.columns([2, 2, 2])
                        with col1:
                            st.write(f"**{section['section']}**")
                        with col2:
                            st.write(f"{section['amount']:,} kWh × {section['price']} دینار")
                        with col3:
                            st.write(f"**{section['cost']:,} دینار**")
                
                st.markdown("---")
        
        else:  # بازرگانی
            result = calculator.calculate_business(kwh_amount)
            
            st.info("**وردەکاری ژمێریاریەکە:**")
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 2])
                with col1:
                    st.write(f"**کارەبای بازرگانی**")
                with col2:
                    st.write(f"{kwh_amount:,} kWh × {calculator.business_price} دینار")
                with col3:
                    st.write(f"**{result['total']:,} دینار**")
            
            st.markdown("---")
        
        # نیشاندانی کۆی گشتی
        st.success(f"### کۆی گشتی: **{result['total']:,} دینار عێراقی**")
        
        # زانیاریی زیادە
        with st.expander("زانیاریی زیادە"):
            if user_type == 'ماڵان':
                st.markdown("""
                **نرخەکانی کارەبای ماڵان:**
                - بۆ 0-400 kWh: 72 دینار بۆ هەر kWh
                - بۆ 401-800 kWh: 108 دینار بۆ هەر kWh  
                - بۆ زیاتر لە 800 kWh: 175 دینار بۆ هەر kWh
                """)
            else:
                st.markdown("""
                **نرخی کارەبای بازرگانی:**
                - نرخی یەکسان: 150 دینار بۆ هەر kWh
                """)
    
    else:
        st.info("تکایە بڕی کارەبای بەکارهاتوو بنووسە بۆ بینینی ئەنجام")
    
    # پێی پەڕە
    st.markdown("---")
    st.caption("سیستەمی ژمێرینی نرخی کارەبا - هەرێمی کوردستان")


# جێبەجێکردنی پرۆگرامەکە
if __name__ == "__main__":
    main()
