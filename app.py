import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(
    page_title="TY PASAR RAYA JIMAT - Stock Management",
    page_icon="🏪",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .store-card {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        background-color: #f8f9fa;
        margin: 0.5rem 0;
    }
    .product-card {
        padding: 0.5rem;
        border-radius: 8px;
        border-left: 3px solid #A23B72;
        background-color: #ffffff;
        margin: 0.25rem 0;
        font-size: 0.9rem;
    }
    .available { color: #28a745; font-weight: bold; }
    .not-available { color: #dc3545; font-weight: bold; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class StockManager:
    def __init__(self):
        self.data = self.sample_data()
        self.all_products = self.get_all_products()
        
    def sample_data(self):
        return {
            'TANJONG RAMBUTAN': [
                'PRAN BASIL SEED MANGO', 'PRAN BASIL SEED ORANGE', 'PRAN BASIL SEED STRAWBERRY',
                'PRAN BASIL SEED KIWI', 'PRAN BASIL SEED LITCHI', 'PRAN BASIL SEED COCKTAIL',
                'PRAN BASIL SEED PINEAPPLE', 'PRAN BASIL SEED POMEGRANATE', 'PRAN BASIL SEED COCONUT',
                'PRAN JUS PET VALUE PACK 1.5L MANGO', 'PRAN JUS PET VALUE PACK 1.5L ORANGE',
                'PRAN JUS PET 1000ML MANGO', 'PRAN JUS PET 1000ML ORANGE', 'PRAN LASSI 285ML YOGURT',
                'PRAN LASSI 285ML MANGO', 'PRAN LASSI 285ML BANANA', 'PRAN LASSI 285ML STRAWBERRY',
                'PRAN TAMARIND PET 320ML', 'PRAN SOUR PLUM PET 320ML', 'PRAN BIRD NEST PET 320ML',
                'PRAN SOYA CAN 300ML', 'POWER ENERGY DRINK PET 250ML', 'BARBICAN POMEGRANATE',
                'BARBICAN RASBERRY', 'BARBICAN APPLE', 'BARBICAN LEMON', 'BARBICAN STRAWBERRY',
                'MUSTARD OIL 400ML', 'MUSTARD OIL 200ML', 'PRAN PUFFED RICE 400G',
                'PRAN CHANACHUR HOT 250G', 'PRAN CHANACHUR BBQ 250G', 'PRAN VEGETABLE GHEE 450G',
                'PRAN VEGETABLE GHEE 125G', 'PRAN VARIETY LOLLIPOP', 'HUMPTY DUMPTY'
            ],
            'PERPADUAN': [
                'PRAN BASIL SEED MANGO', 'PRAN BASIL SEED ORANGE', 'PRAN BASIL SEED STRAWBERRY',
                'PRAN BASIL SEED KIWI', 'PRAN BASIL SEED LITCHI', 'PRAN BASIL SEED COCKTAIL',
                'PRAN BASIL SEED PINEAPPLE', 'PRAN BASIL SEED POMEGRANATE', 'PRAN BASIL SEED COCONUT',
                'PRAN JUS PET VALUE PACK 1.5L MANGO', 'PRAN JUS PET VALUE PACK 1.5L ORANGE',
                'PRAN LASSI 285ML YOGURT', 'PRAN LASSI 285ML MANGO', 'PRAN LASSI 285ML BANANA',
                'PRAN LASSI 285ML STRAWBERRY', 'PRAN VEGETABLE GHEE 450G', 'PRAN VEGETABLE GHEE 125G',
                'PRAN VARIETY LOLLIPOP', 'HUMPTY DUMPTY', 'DRINKO FLOAT 330ML MANGO',
                'DRINKO FLOAT 330ML STRAWBERRY', 'DRINKO FLOAT 330ML LYCHEE', 'DRINKO FLOAT 330ML ORANGE',
                'DRINKO FLOAT 330ML PINEAPPLE'
            ],
            'AMPANG': [
                'PRAN VEGETABLE GHEE 450G', 'PRAN VEGETABLE GHEE 125G', 'PRAN VARIETY LOLLIPOP',
                'HUMPTY DUMPTY', 'PRAN CREAMER 500GM', 'PRAN CREAMER 500GM EASY OPEN',
                'PRAN PREMIO PARADISE', 'PRAN CHOCO STICK', 'PRAN BES MINUMAN BERPERISA ANGGUR',
                'PRAN BES MINUMAN BERPERISA OREN', 'PRAN BES MINUMAN BERPERISA JAGUNG',
                'PRAN BES MINUMAN BERPERISA LYCHEE', 'PRAN BES MINUMAN BERPERISA ROSE',
                'PRAN BES MINUMAN BERPERISA SARSI'
            ],
            'BATU GAJAH': [
                'PRAN BASIL SEED MANGO', 'PRAN BASIL SEED STRAWBERRY', 'PRAN BASIL SEED KIWI',
                'PRAN BASIL SEED LITCHI', 'PRAN BASIL SEED COCKTAIL', 'PRAN AIS LEMON TEH',
                'DRINKO FLOAT 250ML MANGO', 'DRINKO FLOAT 250ML STRAWBERRY', 'DRINKO FLOAT 250ML LYCHEE',
                'BARBICAN POMEGRANATE', 'BARBICAN RASBERRY', 'BARBICAN APPLE', 'BARBICAN STRAWBERRY',
                'MUSTARD OIL 400ML', 'PRAN CHANACHUR HOT 250G', 'PRAN CHANACHUR BBQ 250G',
                'PRAN VEGETABLE GHEE 450G', 'PRAN VEGETABLE GHEE 125G', 'PRAN VARIETY LOLLIPOP',
                'PRAN POTATA BISCUITS 100GM', 'PRAN JUS PET VALUE PACK 1.5L MANGO',
                'PRAN JUS PET 1000ML MANGO', 'PRAN JUS PET 1000ML ORANGE', 'PRAN JUS PET 1000ML APPLE',
                'PRAN PUFFED RICE 400G', 'PRAN COCONUT WATER', 'HUMPTY DUMPTY',
                'PRAN BES MINUMAN BERPERISA ANGGUR', 'PRAN BES MINUMAN BERPERISA OREN',
                'PRAN BES MINUMAN BERPERISA JAGUNG', 'PRAN BES MINUMAN BERPERISA LYCHEE',
                'PRAN BES MINUMAN BERPERISA ROSE', 'PRAN BES MINUMAN BERPERISA SARSI',
                'PRAN LASSI 285ML YOGURT', 'PRAN LASSI 285ML MANGO', 'PRAN LASSI 285ML BANANA',
                'PRAN LASSI 285ML STRAWBERRY', 'POWER ENERGY DRINK PET 250ML'
            ],
            'PENGKALAN': [
                'PRAN BASIL SEED MANGO', 'PRAN BASIL SEED STRAWBERRY', 'PRAN BASIL SEED KIWI',
                'PRAN BASIL SEED LITCHI', 'PRAN BASIL SEED COCKTAIL', 'PRAN VEGETABLE GHEE 450G',
                'PRAN VEGETABLE GHEE 125G', 'PRAN VARIETY LOLLIPOP', 'HUMPTY DUMPTY',
                'PRAN JUS 330ML APPLE', 'PRAN JUS 330ML ORANGE', 'PRAN JUS 330ML MANGO',
                'PRAN COCONUT WATER', 'POWER ENERGY DRINK PET 250ML',
                'PRAN BES MINUMAN BERPERISA ANGGUR', 'PRAN BES MINUMAN BERPERISA OREN',
                'PRAN BES MINUMAN BERPERISA JAGUNG', 'PRAN BES MINUMAN BERPERISA LYCHEE',
                'PRAN BES MINUMAN BERPERISA ROSE', 'PRAN BES MINUMAN BERPERISA SARSI',
                'PRAN JUS PET VALUE PACK 1.5L MANGO', 'PRAN JUS PET 1000ML ORANGE',
                'PRAN COOLING TAMARIND'
            ],
            'STATION 18': [
                'PRAN BASIL SEED MANGO', 'PRAN BASIL SEED STRAWBERRY', 'PRAN BASIL SEED KIWI',
                'PRAN BASIL SEED LITCHI', 'PRAN BASIL SEED COCKTAIL', 'PRAN VEGETABLE GHEE 450G',
                'PRAN VEGETABLE GHEE 125G', 'PRAN VARIETY LOLLIPOP', 'HUMPTY DUMPTY',
                'PRAN BES MINUMAN BERPERISA ANGGUR', 'PRAN BES MINUMAN BERPERISA OREN',
                'PRAN BES MINUMAN BERPERISA JAGUNG', 'PRAN BES MINUMAN BERPERISA LYCHEE',
                'PRAN BES MINUMAN BERPERISA ROSE', 'PRAN BES MINUMAN BERPERISA SARSI',
                'PRAN JUS PET VALUE PACK 1.5L MANGO', 'PRAN COOLING TAMARIND',
                'BOMBAY BRIYANI MASALA', 'PRAN PUFFED RICE 400G', 'PRAN MUSTARD OIL 400ML',
                'PRAN CHANACHUR HOT 250G', 'PRAN CHANACHUR BBQ 250G'
            ],
            'TELUK INTAN': [
                'PRAN BASIL SEED MANGO', 'PRAN BASIL SEED LITCHI', 'PRAN BASIL SEED COCKTAIL',
                'PRAN BASIL SEED PINEAPPLE', 'PRAN BASIL SEED POMEGRANATE', 'BARBICAN RASBERRY',
                'BARBICAN STRAWBERRY', 'BARBICAN POMEGRANATE', 'BARBICAN PINEAPPLE', 'BARBICAN APPLE',
                'PRAN VARIETY LOLLIPOP', 'PRAN COCONUT WATER', 'PRAN VEGETABLE GHEE 450G',
                'PRAN VEGETABLE GHEE 125G', 'POWER ENERGY DRINK 250ML', 'PRAN LASSI 285ML MANGO',
                'PRAN LASSI 285ML YOGURT', 'PRAN SWEETENED CREAMER 500GM'
            ]
        }
    
    def get_all_products(self):
        all_products = set()
        for products in self.data.values():
            all_products.update(products)
        return sorted(list(all_products))
    
    def check_stock(self, product_name, store_name=None):
        results = {}
        if store_name:
            if store_name in self.data:
                results[store_name] = product_name in self.data[store_name]
            else:
                results[store_name] = False
        else:
            for store, products in self.data.items():
                results[store] = product_name in products
        return results
    
    def find_product_locations(self, product_name):
        locations = []
        for store, products in self.data.items():
            if product_name in products:
                locations.append(store)
        return locations
    
    def estimate_price(self, product_name):
        price_ranges = {
            'BASIL SEED': 2.50, 'JUS PET': 4.00, 'LASSI': 3.50, 'VEGETABLE GHEE': 8.00,
            'CHANACHUR': 3.00, 'MUSTARD OIL': 6.00, 'BARBICAN': 2.80, 'ENERGY DRINK': 2.00,
            'LOLLIPOP': 1.50, 'CREAMER': 5.00, 'COCONUT WATER': 3.50, 'FLOAT': 2.20,
            'TAMARIND': 2.80, 'SOYA': 2.50, 'BIRD NEST': 8.50, 'PUFFED RICE': 4.50,
            'BISCUITS': 3.50, 'BES MINUMAN': 1.80, 'POTATA': 3.50, 'COOLING': 2.50,
            'SOUR PLUM': 2.80, 'BRIYANI MASALA': 4.50
        }
        for key, price in price_ranges.items():
            if key in product_name.upper():
                return price
        return 3.00

def main():
    # Initialize session state
    if 'po_products' not in st.session_state:
        st.session_state.po_products = []
    if 'po_quantities' not in st.session_state:
        st.session_state.po_quantities = []

    # Initialize stock manager
    stock_manager = StockManager()
    
    # Header
    st.markdown('<h1 class="main-header">🏪 TY PASAR RAYA JIMAT SDN BHD</h1>', unsafe_allow_html=True)
    st.markdown("### Stock Management & Purchase Order System")
    
    # Sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose a feature",
        ["📊 Dashboard", "🔍 Check Stock", "📍 Find Locations", "🏪 Store Inventory", "📋 Generate PO", "📦 All Products"]
    )
    
    if app_mode == "📊 Dashboard":
        show_dashboard(stock_manager)
    elif app_mode == "🔍 Check Stock":
        check_stock(stock_manager)
    elif app_mode == "📍 Find Locations":
        find_locations(stock_manager)
    elif app_mode == "🏪 Store Inventory":
        store_inventory(stock_manager)
    elif app_mode == "📋 Generate PO":
        generate_po(stock_manager)
    elif app_mode == "📦 All Products":
        all_products(stock_manager)

def show_dashboard(stock_manager):
    st.header("📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_stores = len(stock_manager.data)
    total_products = len(stock_manager.all_products)
    avg_products = int(np.mean([len(products) for products in stock_manager.data.values()]))
    most_stocked_store = max(stock_manager.data.keys(), key=lambda x: len(stock_manager.data[x]))
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏪</h3>
            <h2>{total_stores}</h2>
            <p>Total Stores</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📦</h3>
            <h2>{total_products}</h2>
            <p>Total Products</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊</h3>
            <h2>{avg_products}</h2>
            <p>Avg Products per Store</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐</h3>
            <h4>{most_stocked_store}</h4>
            <p>Most Stocked Store</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Store Inventory Distribution")
    store_stats = {store: len(products) for store, products in stock_manager.data.items()}
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        chart_data = pd.DataFrame({
            'Store': list(store_stats.keys()),
            'Products': list(store_stats.values())
        })
        st.bar_chart(chart_data.set_index('Store'))
    
    with col2:
        st.write("**Store Rankings:**")
        for store, count in sorted(store_stats.items(), key=lambda x: x[1], reverse=True):
            st.write(f"• {store}: {count} products")

def check_stock(stock_manager):
    st.header("🔍 Check Product Availability")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        product_name = st.selectbox("Select Product", stock_manager.all_products)
    
    with col2:
        store_filter = st.selectbox("Store Filter", ["All Stores"] + list(stock_manager.data.keys()))
    
    if product_name:
        store_name = None if store_filter == "All Stores" else store_filter
        results = stock_manager.check_stock(product_name, store_name)
        
        st.subheader(f"Stock Status: {product_name}")
        
        if store_filter == "All Stores":
            cols = st.columns(3)
            available_count = 0
            
            for i, (store, available) in enumerate(results.items()):
                col_idx = i % 3
                with cols[col_idx]:
                    if available:
                        st.markdown(f'<div class="store-card"><span class="available">✅ {store}</span></div>', unsafe_allow_html=True)
                        available_count += 1
                    else:
                        st.markdown(f'<div class="store-card"><span class="not-available">❌ {store}</span></div>', unsafe_allow_html=True)
            
            st.info(f"**Summary:** Available in {available_count} out of {len(results)} stores")
        else:
            if results[store_filter]:
                st.success(f"✅ **Available** at {store_filter}")
            else:
                st.error(f"❌ **Not Available** at {store_filter}")

def find_locations(stock_manager):
    st.header("📍 Find Product Locations")
    
    product_name = st.selectbox("Select Product to Find", stock_manager.all_products)
    
    if product_name:
        locations = stock_manager.find_product_locations(product_name)
        
        if locations:
            st.success(f"**{product_name}** is available in **{len(locations)}** stores:")
            cols = st.columns(3)
            for i, location in enumerate(locations):
                with cols[i % 3]:
                    st.markdown(f'<div class="store-card">🏪 {location}</div>', unsafe_allow_html=True)
        else:
            st.error(f"**{product_name}** is not available in any store.")

def store_inventory(stock_manager):
    st.header("🏪 Store Inventory")
    
    selected_store = st.selectbox("Select Store", list(stock_manager.data.keys()))
    
    if selected_store:
        products = stock_manager.data[selected_store]
        
        st.subheader(f"Inventory for {selected_store}")
        st.write(f"**Total Products:** {len(products)}")
        
        search_term = st.text_input("🔍 Search products...")
        filtered_products = [p for p in products if search_term.lower() in p.lower()] if search_term else products
        
        cols = st.columns(2)
        for i, product in enumerate(filtered_products):
            with cols[i % 2]:
                st.markdown(f'<div class="product-card">{product}</div>', unsafe_allow_html=True)

def generate_po(stock_manager):
    st.header("📋 Generate Purchase Order")
    
    col1, col2 = st.columns(2)
    with col1:
        supplier = st.selectbox("Supplier", ["PRAN", "BARBICAN", "DRINKO", "OTHER SUPPLIER"])
    with col2:
        delivery_date = st.date_input("Requested Delivery Date")
    
    st.subheader("Add Products to PO")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        new_product = st.selectbox("Select Product", stock_manager.all_products, key="po_product_select")
    with col2:
        new_quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="po_quantity_input")
    with col3:
        if st.button("Add to PO", use_container_width=True, key="add_po_button"):
            if new_product and new_product not in st.session_state.po_products:
                st.session_state.po_products.append(new_product)
                st.session_state.po_quantities.append(new_quantity)
                st.success(f"Added {new_product} to PO!")
    
    if st.session_state.po_products:
        st.subheader("Current Purchase Order Items")
        
        total_amount = 0
        for i, (product, qty) in enumerate(zip(st.session_state.po_products, st.session_state.po_quantities)):
            unit_price = stock_manager.estimate_price(product)
            total = unit_price * qty
            total_amount += total
            
            col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 1])
            with col1:
                st.write(f"**{product}**")
            with col2:
                st.write(f"**Qty:** {qty}")
            with col3:
                st.write(f"**Price:** RM{unit_price:.2f}")
            with col4:
                st.write(f"**Total:** RM{total:.2f}")
            with col5:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.po_products.pop(i)
                    st.session_state.po_quantities.pop(i)
                    st.rerun()
        
        st.markdown(f"**Grand Total: RM{total_amount:.2f}**")
        
        if st.button("📄 Generate Purchase Order", type="primary"):
            generate_po_document(stock_manager, st.session_state.po_products, st.session_state.po_quantities, supplier, delivery_date)
        
        if st.button("🗑️ Clear PO"):
            st.session_state.po_products = []
            st.session_state.po_quantities = []
            st.rerun()
    else:
        st.info("No products added to purchase order yet.")

def generate_po_document(stock_manager, products, quantities, supplier, delivery_date):
    po_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    po_data = []
    total_amount = 0
    
    for i, (product, qty) in enumerate(zip(products, quantities)):
        unit_price = stock_manager.estimate_price(product)
        total = unit_price * qty
        total_amount += total
        po_data.append([i + 1, product, qty, f"RM{unit_price:.2f}", f"RM{total:.2f}"])
    
    st.success("✅ Purchase Order Generated Successfully!")
    st.markdown("---")
    st.markdown(f"### **PURCHASE ORDER**")
    st.markdown(f"**PO Number:** `{po_number}`")
    st.markdown(f"**Date:** `{timestamp}`")
    st.markdown(f"**Supplier:** `{supplier}`")
    st.markdown(f"**Delivery Date:** `{delivery_date}`")
    st.markdown("---")
    
    df = pd.DataFrame(po_data, columns=['Item No.', 'Product', 'Quantity', 'Unit Price', 'Total'])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown(f"### **GRAND TOTAL: RM{total_amount:.2f}**")
    st.markdown("---")
    
    # Download as CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{po_number}.csv">📥 Download PO as CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

def all_products(stock_manager):
    st.header("📦 All Products")
    st.write(f"**Total Unique Products:** {len(stock_manager.all_products)}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Search products...")
    with col2:
        category_filter = st.selectbox("Filter by Category", ["All Categories", "BASIL SEED", "JUS", "LASSI", "GHEE", "OIL", "DRINK", "SNACK"])
    
    filtered_products = stock_manager.all_products
    if search_term:
        filtered_products = [p for p in filtered_products if search_term.lower() in p.lower()]
    if category_filter != "All Categories":
        filtered_products = [p for p in filtered_products if category_filter in p.upper()]
    
    st.write(f"**Showing {len(filtered_products)} products:**")
    cols = st.columns(2)
    for i, product in enumerate(filtered_products):
        with cols[i % 2]:
            store_count = len(stock_manager.find_product_locations(product))
            st.markdown(f'<div class="product-card"><strong>{product}</strong><br><small>Available in {store_count} stores</small></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()