import streamlit as st

# Page configuration
st.set_page_config(
    page_title="سیستەمی کارەبا",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* RTL Support */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* Modern Card Style */
    .custom-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 1rem 0;
        color: white;
    }
    
    .result-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
    }
    
    .tech-result {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);
    }
    
    .stats-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 15px;
        text-align: center;
        font-size: 1.1rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Tables */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #667eea;
        font-weight: 900;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 15px;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_appliances' not in st.session_state:
    st.session_state.selected_appliances = []

# Sidebar Navigation
with st.sidebar:
    st.markdown("# ⚡ سیستەمی کارەبا")
    st.markdown("---")
    
    page = st.radio(
        "هەڵبژاردنی لاپەڕە",
        ["🧮 حیسابی نرخ", "⚙️ حیسابی تەکنیکی", "💡 زانیاری و ئامێرەکان", "📱 دەربارە"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### دەربارە")
    st.info("سیستەمی کارەبا\n\nوەشانی 1.0.7\n\nگەشەپێدەر: AMANJ")

# Main content
st.title("هەژمارکردنی کارەبا ⚡")

# ===== PAGE 1: Price Calculator =====
if page == "🧮 حیسابی نرخ":
    st.markdown("## 💰 حیساب کردنی نرخی کارەبا")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        category = st.selectbox(
            "جۆری بەکارهێنەر",
            ["ماڵان", "بازرگانی", "پیشەسازی", "پیشەسازی گەورە", "میری", "کشتوکاڵ"]
        )
    
    with col2:
        kwh_input = st.number_input(
            "بڕی کیلۆوات (kWh)",
            min_value=0.0,
            step=10.0,
            format="%.1f"
        )
    
    if st.button("🧮 حیساب بکە"):
        if kwh_input > 0:
            if category == "ماڵان":
                # Tiered pricing for residential
                tiers = [
                    {"نرخ": "پلەی ١", "سنوور": 400, "نرخ_دینار": 72},
                    {"نرخ": "پلەی ٢", "سنوور": 400, "نرخ_دینار": 108},
                    {"نرخ": "پلەی ٣", "سنوور": 400, "نرخ_دینار": 175},
                    {"نرخ": "پلەی ٤", "سنوور": 400, "نرخ_دینار": 265},
                    {"نرخ": "پلەی پێنج", "سنوور": 999999, "نرخ_دینار": 350},
                ]
                
                total_cost = 0
                remaining = kwh_input
                tier_details = []
                
                for tier in tiers:
                    if remaining <= 0:
                        break
                    used = min(remaining, tier["سنوور"])
                    cost = used * tier["نرخ_دینار"]
                    tier_details.append({
                        "پلە": tier["نرخ"],
                        "بڕی بەکارهاتوو": f"{used:.0f}",
                        "نرخ": f"{tier['نرخ_دینار']}",
                        "کۆی تێچوو": f"{cost:.0f}"
                    })
                    total_cost += cost
                    remaining -= used
                
                # Display tier breakdown with modern HTML table
                st.markdown("### 📊 وردەکاری پلەکان")
                
                table_html = """
                <div style="overflow-x: auto; margin: 1rem 0;">
                    <table style="width: 100%; border-collapse: separate; border-spacing: 0; 
                                  background: white; border-radius: 15px; overflow: hidden; 
                                  box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                        <thead>
                            <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                                <th style="padding: 1rem; text-align: center; font-weight: bold;">پلە</th>
                                <th style="padding: 1rem; text-align: center; font-weight: bold;">بڕی بەکارهاتوو</th>
                                <th style="padding: 1rem; text-align: center; font-weight: bold;">نرخ</th>
                                <th style="padding: 1rem; text-align: center; font-weight: bold;">کۆی تێچوو</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                
                for i, detail in enumerate(tier_details):
                    bg_color = "#f8f9fa" if i % 2 == 0 else "white"
                    table_html += f"""
                        <tr style="background: {bg_color};">
                            <td style="padding: 0.8rem; text-align: center; border-bottom: 1px solid #e0e0e0;">{detail['پلە']}</td>
                            <td style="padding: 0.8rem; text-align: center; border-bottom: 1px solid #e0e0e0;">{detail['بڕی بەکارهاتوو']} kWh</td>
                            <td style="padding: 0.8rem; text-align: center; border-bottom: 1px solid #e0e0e0;">{detail['نرخ']} دینار</td>
                            <td style="padding: 0.8rem; text-align: center; font-weight: bold; 
                                       color: #667eea; border-bottom: 1px solid #e0e0e0;">{detail['کۆی تێچوو']} دینار</td>
                        </tr>
                    """
                
                table_html += """
                        </tbody>
                    </table>
                </div>
                """
                
                st.markdown(table_html, unsafe_allow_html=True)
                
                # Display total
                st.markdown(f"""
                <div class="result-card">
                    کۆی گشتی: {total_cost:,.0f} دینار
                </div>
                """, unsafe_allow_html=True)
                
            else:
                # Flat rate for other categories
                rates = {
                    "بازرگانی": 185,
                    "پیشەسازی": 160,
                    "پیشەسازی گەورە": 125,
                    "میری": 160,
                    "کشتوکاڵ": 60
                }
                
                rate = rates[category]
                total = kwh_input * rate
                
                st.markdown(f"""
                <div class="result-card">
                    تێچوو: {total:,.0f} دینار
                    <br>
                    <small style="font-size: 1rem;">({kwh_input:.0f} kWh × {rate} دینار)</small>
                </div>
                """, unsafe_allow_html=True)

# ===== PAGE 2: Technical Calculator =====
elif page == "⚙️ حیسابی تەکنیکی":
    st.markdown("## ⚡ حیساب کردنی تەکنیکی")
    
    calc_type = st.selectbox(
        "جۆری حیساب",
        ["وات بۆ کیلۆوات", "وات بۆ ئەمپێر", "ئەمپێر بۆ کیلۆوات", "حیسابی مانگانە"]
    )
    
    st.markdown("---")
    
    if calc_type == "حیسابی مانگانە":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            watts = st.number_input("بڕی وات (Watt)", min_value=0.0, step=10.0)
        with col2:
            hours = st.number_input("سەعاتی کارکردن لە ڕۆژێکدا", min_value=0.0, step=0.5)
        with col3:
            days = st.number_input("چەند ڕۆژ لە مانگدا", min_value=0.0, step=1.0, value=30.0)
        
        if st.button("🧮 حیساب بکە"):
            if watts > 0 and hours > 0 and days > 0:
                monthly_kwh = (watts * hours * days) / 1000
                st.markdown(f"""
                <div class="tech-result">
                    {monthly_kwh:.2f} kWh / مانگ
                </div>
                """, unsafe_allow_html=True)
    else:
        value = st.number_input("بڕەکە داخڵ بکە", min_value=0.0, step=10.0)
        
        if st.button("🧮 حیساب بکە"):
            if value > 0:
                result = ""
                if calc_type == "وات بۆ کیلۆوات":
                    result = f"{value / 1000:.2f} kWh"
                elif calc_type == "وات بۆ ئەمپێر":
                    result = f"{value / 220:.2f} Ampere"
                elif calc_type == "ئەمپێر بۆ کیلۆوات":
                    result = f"{(value * 220) / 1000:.2f} kWh"
                
                st.markdown(f"""
                <div class="tech-result">
                    {result}
                </div>
                """, unsafe_allow_html=True)

# ===== PAGE 3: Info & Appliances =====
elif page == "💡 زانیاری و ئامێرەکان":
    st.markdown("## 💡 ئامێرە کارەباییەکان")
    
    # Appliance database
    appliances = [
        {"ناو": "بۆیلەر (سەخان)", "وات": 3000, "icon": "🔥"},
        {"ناو": "سپلێت ١تەن", "وات": 1200, "icon": "❄️"},
        {"ناو": "سپلێت ٢تەن", "وات": 2400, "icon": "❄️"},
        {"ناو": "سەلاجە", "وات": 250, "icon": "🧊"},
        {"ناو": "موجەمیدە", "وات": 300, "icon": "🌊"},
        {"ناو": "غەسالە (ئاسایی)", "وات": 500, "icon": "🧺"},
        {"ناو": "غەسالە (ئۆتۆماتیک)", "وات": 2000, "icon": "🧺"},
        {"ناو": "ئوتو", "وات": 2200, "icon": "👔"},
        {"ناو": "مایکرۆوەیڤ", "وات": 1500, "icon": "📦"},
        {"ناو": "هیتەری کارەبایی", "وات": 2000, "icon": "🔥"},
        {"ناو": "کۆمپیوتەر (PC)", "وات": 400, "icon": "💻"},
        {"ناو": "لاپتۆپ", "وات": 65, "icon": "💻"},
        {"ناو": "تەلەفزیۆن LED", "وات": 100, "icon": "📺"},
        {"ناو": "گسکە کارەبایی", "وات": 1800, "icon": "🧹"},
        {"ناو": "ماتۆڕی ئاو", "وات": 750, "icon": "💧"},
        {"ناو": "فڕنی کارەبایی", "وات": 2500, "icon": "🍳"},
        {"ناو": "گلۆپ", "وات": 20, "icon": "💡"},
    ]
    
    # Calculate totals
    total_watts = sum([item['وات'] for item in st.session_state.selected_appliances])
    total_amps = total_watts / 220
    
    # Display stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-box">
            <h3>کۆی وات</h3>
            <h1>{total_watts:,.0f} W</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-box">
            <h3>کۆی ئەمپێر</h3>
            <h1>{total_amps:.1f} A</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔌 هەڵبژاردنی ئامێر")
    
    # Appliance selection
    cols = st.columns(4)
    for i, appliance in enumerate(appliances):
        with cols[i % 4]:
            if st.button(f"{appliance['icon']} {appliance['ناو']}", key=f"add_{i}"):
                st.session_state.selected_appliances.append(appliance.copy())
                st.rerun()
    
    # Display selected appliances
    if st.session_state.selected_appliances:
        st.markdown("---")
        st.markdown("### 📋 ئامێرە هەڵبژێردراوەکان")
        
        for i, item in enumerate(st.session_state.selected_appliances):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(f"{item['icon']} **{item['ناو']}**")
            with col2:
                new_watt = st.number_input(
                    "وات",
                    value=float(item['وات']),
                    key=f"watt_{i}",
                    label_visibility="collapsed"
                )
                st.session_state.selected_appliances[i]['وات'] = new_watt
            with col3:
                st.write(f"**{item['وات']:,.0f} وات**")
            with col4:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.selected_appliances.pop(i)
                    st.rerun()
        
        if st.button("🗑️ سڕینەوەی هەموو"):
            st.session_state.selected_appliances = []
            st.rerun()
    
    # Price table
    st.markdown("---")
    st.markdown("### 📊 خشتەی نرخەکان بەپێی وێنەی فەرمی")
    
    price_table_html = """
    <div style="overflow-x: auto; margin: 1rem 0;">
        <table style="width: 100%; border-collapse: separate; border-spacing: 0; 
                      background: white; border-radius: 15px; overflow: hidden; 
                      box-shadow: 0 8px 20px rgba(0,0,0,0.12);">
            <thead>
                <tr style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
                    <th style="padding: 1rem; text-align: center; font-weight: bold; font-size: 1.1rem;">جۆری بەکارهێنەر</th>
                    <th style="padding: 1rem; text-align: center; font-weight: bold; font-size: 1.1rem;">نرخ (دینار)</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">ماڵان (0-400)</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #667eea; font-weight: bold;">72</td>
                </tr>
                <tr style="background: white;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">ماڵان (401-800)</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #667eea; font-weight: bold;">108</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">ماڵان (801-1200)</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #667eea; font-weight: bold;">175</td>
                </tr>
                <tr style="background: white;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">ماڵان (1201-1600)</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #667eea; font-weight: bold;">265</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">ماڵان (1600+)</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #667eea; font-weight: bold;">350</td>
                </tr>
                <tr style="background: white;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">بازرگانی</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #fa709a; font-weight: bold;">185</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">پیشەسازی</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #fa709a; font-weight: bold;">160</td>
                </tr>
                <tr style="background: white;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">پیشەسازی گەورە</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #fa709a; font-weight: bold;">125</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; font-weight: 500;">میری</td>
                    <td style="padding: 0.9rem; text-align: center; border-bottom: 1px solid #e0e0e0; color: #43e97b; font-weight: bold;">160</td>
                </tr>
                <tr style="background: white;">
                    <td style="padding: 0.9rem; text-align: center; font-weight: 500;">کشتوکاڵ</td>
                    <td style="padding: 0.9rem; text-align: center; color: #43e97b; font-weight: bold;">60</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(price_table_html, unsafe_allow_html=True)

# ===== PAGE 4: About/Info =====
else:
    st.markdown("## 📱 دەربارەی ئەپڵیکەیشن")
    
    # Hero Section
    st.markdown("""
    <div class="custom-card">
        <h1 style="color: white; text-align: center; font-size: 2.5rem; margin-bottom: 0;">⚡ سیستەمی کارەبا</h1>
        <p style="text-align: center; font-size: 1.2rem; margin-top: 0.5rem; color: rgba(255,255,255,0.9);">
            ئەپڵیکەیشنێکی پیشەیی بۆ حیسابکردنی کارەبا
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3 style="color: white;">💰 حیسابی نرخ</h3>
            <p style="color: rgba(255,255,255,0.9);">
            حیسابکردنی نرخی کارەبا بەپێی سیستەمی پلەبەندی بۆ ماڵان و نرخی جیاواز بۆ بازرگانی، پیشەسازی، میری و کشتوکاڵ
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <h3 style="color: white;">💡 زانیاری ئامێرەکان</h3>
            <p style="color: rgba(255,255,255,0.9);">
            زانیاری تەواو دەربارەی بڕی بەکارهێنانی ئامێرە کارەباییەکان و حیسابکردنی کۆی وات و ئەمپێر
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
            <h3 style="color: #333;">⚙️ حیسابی تەکنیکی</h3>
            <p style="color: #555;">
            گۆڕینی یەکەکان: وات بۆ کیلۆوات، وات بۆ ئەمپێر، ئەمپێر بۆ کیلۆوات و حیسابکردنی بەکارهێنانی مانگانە
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
            <h3 style="color: #333;">📊 خشتەی نرخەکان</h3>
            <p style="color: #555;">
            خشتەی تەواوی نرخەکانی کارەبا بەپێی جۆری بەکارهێنەر و وردەکاری پلەبەندی بۆ ماڵان
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics Section
    st.markdown("### 📊 ئامارەکان")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.markdown("""
        <div class="metric-card" style="text-align: center; border-left: 4px solid #667eea;">
            <h1 style="color: #667eea; margin: 0;">17+</h1>
            <p style="color: #888; margin: 0.5rem 0 0 0;">ئامێری کارەبایی</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown("""
        <div class="metric-card" style="text-align: center; border-left: 4px solid #fa709a;">
            <h1 style="color: #fa709a; margin: 0;">6</h1>
            <p style="color: #888; margin: 0.5rem 0 0 0;">جۆری بەکارهێنەر</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col3:
        st.markdown("""
        <div class="metric-card" style="text-align: center; border-left: 4px solid #43e97b;">
            <h1 style="color: #43e97b; margin: 0;">4</h1>
            <p style="color: #888; margin: 0.5rem 0 0 0;">جۆری حیساب</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("### 🔧 تەکنەلۆجیا بەکارهاتووەکان")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h1 style="font-size: 3rem; margin: 0;">🐍</h1>
            <h4 style="margin: 0.5rem 0 0 0; color: #333;">Python</h4>
            <p style="color: #888; font-size: 0.9rem; margin: 0.3rem 0 0 0;">زمانی پڕۆگرامسازی</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h1 style="font-size: 3rem; margin: 0;">🚀</h1>
            <h4 style="margin: 0.5rem 0 0 0; color: #333;">Streamlit</h4>
            <p style="color: #888; font-size: 0.9rem; margin: 0.3rem 0 0 0;">فریموۆرکی وێب</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h1 style="font-size: 3rem; margin: 0;">🎨</h1>
            <h4 style="margin: 0.5rem 0 0 0; color: #333;">CSS3</h4>
            <p style="color: #888; font-size: 0.9rem; margin: 0.3rem 0 0 0;">دیزاینی مۆدێرن</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Developer Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; text-align: center; color: white;">
        <h2 style="margin: 0; color: white;">👨‍💻 گەشەپێدەر</h2>
        <h1 style="margin: 0.5rem 0; color: white; font-size: 2.5rem;">AMANJ</h1>
        <p style="margin: 0.5rem 0; color: rgba(255,255,255,0.9); font-size: 1.1rem;">
            گەشەپێدەری ئەپڵیکەیشن و نەرمەواڵە
        </p>
        <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.2);">
            <p style="margin: 0; color: rgba(255,255,255,0.8);">
                وەشانی 1.0.7 - ٢٠٢٤
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tips Section
    with st.expander("💡 ڕاوێژ و ئامۆژگاری", expanded=False):
        st.markdown("""
        ### چۆن باشترین بەکارهێنان بکەیت لەم ئەپڵیکەیشنە؟
        
        **بۆ حیسابی نرخ:**
        - نرخی ماڵان بە سیستەمی پلەبەندییە (٥ پلە)
        - زۆرترین بەکارهێنان = نرخی زۆرتر
        - سەیر بە وردەکاری پلەکان بکە بۆ فێربوونی زیاتر
        
        **بۆ حیسابی تەکنیکی:**
        - بۆ زانینی بەکارهێنانی مانگانە: وات × سەعات × ڕۆژ
        - بۆ زانینی ئەمپێر: وات ÷ ٢٢٠
        - بۆ زانینی کیلۆوات: وات ÷ ١٠٠٠
        
        **بۆ حیسابی ئامێرەکان:**
        - هەموو ئامێرەکانی ماڵەکەت زیاد بکە
        - کۆی گشتی بە شێوەی ئۆتۆماتیک حیساب دەکرێت
        - دەتوانیت بڕی وات دەستکاری بکەیت بۆ هەر ئامێرێک
        """)
    
    # Contact Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 15px;">
        <p style="color: #666; margin: 0;">
            بۆ هەر پرسیار، پێشنیار، یان کێشەیەک
        </p>
        <p style="color: #667eea; font-weight: bold; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            پەیوەندیمان پێوە بکە ✉️
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem;">
    <p>سیستەمی کارەبا © 2024 | گەشەپێدراوە بە ❤️ لەلایەن AMANJ</p>
</div>
""", unsafe_allow_html=True)
