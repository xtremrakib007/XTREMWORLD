import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import base64
import json
import os
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="TY PASAR RAYA JIMAT - Stock Management",
    page_icon="🏪",
    layout="wide"
)

# Enhanced CSS with proper dark mode support
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
        border: 1px solid #dee2e6;
    }
    .product-card {
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #A23B72;
        background-color: #ffffff;
        margin: 0.3rem 0;
        font-size: 0.9rem;
        border: 1px solid #e9ecef;
        color: #212529;
    }
    .dark-mode .product-card {
        background-color: #2d3748 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4a5568 !important;
    }
    .available { color: #28a745; font-weight: bold; }
    .not-available { color: #dc3545; font-weight: bold; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .dark-mode {
        background-color: #1a202c;
        color: #e2e8f0;
    }
    .dark-mode .store-card {
        background-color: #2d3748 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4a5568 !important;
    }
    .dark-mode .css-1d391kg, 
    .dark-mode .css-1y4p8pa, 
    .dark-mode .css-1v0mbdj, 
    .dark-mode .css-1r6slb0 {
        background-color: #1a202c !important;
        color: #e2e8f0 !important;
    }
    .price-editor {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.2rem 0;
    }
    .dark-mode .price-editor {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        color: #e2e8f0;
    }
    .danger-button {
        background-color: #dc3545;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .danger-button:hover {
        background-color: #c82333;
    }
    .category-badge {
        background-color: #2E86AB;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .sales-rep-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #dee2e6;
        color: #6c757d;
        font-size: 0.9rem;
    }
    .dark-mode .footer {
        border-top: 1px solid #4a5568;
        color: #a0aec0;
    }
</style>
""", unsafe_allow_html=True)

class DataManager:
    """Manages data persistence using session state and file backup"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables"""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.store_data = DataManager.load_store_data()
            st.session_state.product_prices = DataManager.load_prices()
            st.session_state.product_barcodes = DataManager.load_barcodes()
            st.session_state.product_suppliers = DataManager.load_suppliers()
            st.session_state.product_categories = DataManager.load_categories()
            st.session_state.po_products = []
            st.session_state.po_quantities = []
            st.session_state.po_prices = []
            st.session_state.dark_mode = False
    
    @staticmethod
    def load_store_data():
        """Load store data from file or use sample data"""
        try:
            if os.path.exists('store_data.json'):
                with open('store_data.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return DataManager.sample_store_data()
    
    @staticmethod
    def load_prices():
        """Load product prices from file"""
        try:
            if os.path.exists('product_prices.json'):
                with open('product_prices.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    @staticmethod
    def load_barcodes():
        """Load product barcodes from file"""
        try:
            if os.path.exists('product_barcodes.json'):
                with open('product_barcodes.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    @staticmethod
    def load_suppliers():
        """Load product suppliers from file"""
        try:
            if os.path.exists('product_suppliers.json'):
                with open('product_suppliers.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    @staticmethod
    def load_categories():
        """Load product categories from file"""
        try:
            if os.path.exists('product_categories.json'):
                with open('product_categories.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    @staticmethod
    def save_store_data(data):
        """Save store data to file"""
        try:
            with open('store_data.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    @staticmethod
    def save_prices(data):
        """Save product prices to file"""
        try:
            with open('product_prices.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    @staticmethod
    def save_barcodes(data):
        """Save product barcodes to file"""
        try:
            with open('product_barcodes.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    @staticmethod
    def save_suppliers(data):
        """Save product suppliers to file"""
        try:
            with open('product_suppliers.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    @staticmethod
    def save_categories(data):
        """Save product categories to file"""
        try:
            with open('product_categories.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    @staticmethod
    def sample_store_data():
        """Return sample store data"""
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
                'PRAN MUSTARD OIL 400ML', 'PRAN MUSTARD OIL 200ML', 'PRAN PUFFED RICE 400G',
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
                'PRAN MUSTARD OIL 400ML', 'PRAN CHANACHUR HOT 250G', 'PRAN CHANACHUR BBQ 250G',
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
                'PRAN VEGETABLE GHEE 125G', 'POWER ENERGY DRINK PET 250ML', 'PRAN LASSI 285ML MANGO',
                'PRAN LASSI 285ML YOGURT', 'PRAN SWEETENED CREAMER 500GM'
            ]
        }

class StockManager:
    def __init__(self):
        # Initialize data manager
        DataManager.initialize_session_state()
        
        # Use session state data
        self.data = st.session_state.store_data
        self.all_products = self.get_all_products()
        self.product_prices = st.session_state.product_prices
        self.product_barcodes = st.session_state.product_barcodes
        self.product_suppliers = st.session_state.product_suppliers
        self.product_categories = st.session_state.product_categories
        
        # Initialize default prices and categories for products that don't have them
        self.initialize_default_data()
    
    def initialize_default_data(self):
        """Initialize default prices and categories for products that don't have them"""
        changed = False
        for product in self.all_products:
            if product not in self.product_prices:
                self.product_prices[product] = self.estimate_price(product)
                changed = True
            
            if product not in self.product_categories:
                self.product_categories[product] = self.get_product_category(product)
                changed = True
        
        if changed:
            self.save_all_data()
    
    def save_all_data(self):
        """Save all data to session state and files"""
        # Update session state
        st.session_state.store_data = self.data
        st.session_state.product_prices = self.product_prices
        st.session_state.product_barcodes = self.product_barcodes
        st.session_state.product_suppliers = self.product_suppliers
        st.session_state.product_categories = self.product_categories
        
        # Save to files
        DataManager.save_store_data(self.data)
        DataManager.save_prices(self.product_prices)
        DataManager.save_barcodes(self.product_barcodes)
        DataManager.save_suppliers(self.product_suppliers)
        DataManager.save_categories(self.product_categories)
    
    def get_all_products(self):
        all_products = set()
        for products in self.data.values():
            all_products.update(products)
        return sorted(list(all_products))
    
    def get_product_category(self, product_name):
        """Categorize products based on name"""
        product_upper = product_name.upper()
        
        if 'BARBICAN' in product_upper:
            return 'Barbican'
        elif 'DRINKO' in product_upper and '250ML' in product_upper:
            return 'Drinko 250ml'
        elif 'DRINKO' in product_upper and '330ML' in product_upper:
            return 'Drinko 330ml'
        elif 'MUSTARD OIL' in product_upper:
            return 'Mustard Oil'
        elif 'BASIL SEED' in product_upper:
            return 'Basil Seed'
        elif 'LASSI' in product_upper:
            return 'Lassi'
        elif 'JUS' in product_upper:
            return 'Jus'
        elif 'VEGETABLE GHEE' in product_upper:
            return 'Vegetable Ghee'
        elif 'CHANACHUR' in product_upper:
            return 'Chanachur'
        elif 'ENERGY DRINK' in product_upper:
            return 'Energy Drink'
        elif 'LOLLIPOP' in product_upper:
            return 'Lollipop'
        elif 'CREAMER' in product_upper:
            return 'Creamer'
        elif 'COCONUT WATER' in product_upper:
            return 'Coconut Water'
        elif 'FLOAT' in product_upper:
            return 'Float'
        elif 'TAMARIND' in product_upper or 'SOUR PLUM' in product_upper or 'BIRD NEST' in product_upper:
            if 'PET 320ML' in product_upper:
                return 'PET 320ml'
            return 'Traditional Drinks'
        elif 'SOYA' in product_upper:
            return 'Soya'
        elif 'PUFFED RICE' in product_upper:
            return 'Puffed Rice'
        elif 'BISCUITS' in product_upper or 'POTATA' in product_upper:
            return 'Biscuits'
        elif 'BES MINUMAN' in product_upper:
            return 'BES Minuman'
        elif 'BRIYANI MASALA' in product_upper:
            return 'Spices'
        elif 'HUMPTY DUMPTY' in product_upper:
            return 'Snacks'
        elif 'AIS LEMON TEH' in product_upper:
            return 'Tea'
        elif 'COOLING TAMARIND' in product_upper:
            return 'Traditional Drinks'
        elif 'PREMIO PARADISE' in product_upper:
            return 'Paradise'
        elif 'CHOCO STICK' in product_upper:
            return 'Chocolate'
        else:
            return 'Other'
    
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
        """Updated price estimation with new prices"""
        price_mapping = {
            'BARBICAN': 4.38,
            'BASIL SEED': 2.42,
            'BES MINUMAN': 2.00,
            'HUMPTY DUMPTY': 2.00,
            'POWER ENERGY DRINK': 1.42,
            'VEGETABLE GHEE 450G': 10.63,
            'VEGETABLE GHEE 125G': 4.13,
            'COCONUT WATER': 1.67,
            'AIS LEMON TEH': 1.63,
            'PREMIO PARADISE': 3.11,
            'CHANACHUR': 3.13,
            'JUS PET 1000ML': 3.75,
            'JUS 330ML': 1.50,
            'PET 320ML': 1.50,
            'DRINKO FLOAT 250ML': 1.50,
            'DRINKO FLOAT 330ML': 2.00,
            'LASSI 285ML': 1.69,
            'SOYA CAN': 1.00,
            'COOLING TAMARIND': 1.38,
            'JUS PET VALUE PACK 1.5L': 11.00,
            'MUSTARD OIL 400ML': 5.83,
            'MUSTARD OIL 200ML': 3.00,
            'VARIETY LOLLIPOP': 30.00,
            'PUFFED RICE': 2.75
        }
        
        product_upper = product_name.upper()
        
        # Check for exact matches first
        for key, price in price_mapping.items():
            if key in product_upper:
                return price
        
        # Fallback to category-based pricing
        category_prices = {
            'Barbican': 4.38,
            'Basil Seed': 2.42,
            'BES Minuman': 2.00,
            'Snacks': 2.00,
            'Energy Drink': 1.42,
            'Vegetable Ghee': 10.63,
            'Coconut Water': 1.67,
            'Traditional Drinks': 1.63,
            'Chanachur': 3.13,
            'Jus': 3.75,
            'PET 320ml': 1.50,
            'Drinko 250ml': 1.50,
            'Drinko 330ml': 2.00,
            'Lassi': 1.69,
            'Soya': 1.00,
            'Mustard Oil': 5.83,
            'Lollipop': 30.00,
            'Puffed Rice': 2.75
        }
        
        category = self.get_product_category(product_name)
        return category_prices.get(category, 3.00)
    
    def add_product(self, product_name, stores, price=None, barcode=None, supplier="PINNACLE FOODS (M) SDN BHD", category=None):
        """Add new product to specified stores"""
        if product_name not in self.all_products:
            self.all_products.append(product_name)
            self.all_products.sort()
        
        for store in stores:
            if store in self.data:
                if product_name not in self.data[store]:
                    self.data[store].append(product_name)
        
        # Set price (use estimated price if not provided)
        if price is not None:
            self.product_prices[product_name] = price
        else:
            self.product_prices[product_name] = self.estimate_price(product_name)
        
        if barcode:
            self.product_barcodes[product_name] = barcode
            
        self.product_suppliers[product_name] = supplier
        
        # Set category
        if category:
            self.product_categories[product_name] = category
        else:
            self.product_categories[product_name] = self.get_product_category(product_name)
        
        # Save all changes
        self.save_all_data()
    
    def add_store(self, store_name, initial_products=None):
        """Add new store with optional initial products"""
        if store_name not in self.data:
            if initial_products is None:
                initial_products = []
            self.data[store_name] = initial_products
            self.save_all_data()
            return True
        return False
    
    def add_products_to_store(self, store_name, products):
        """Add multiple products to a specific store"""
        if store_name in self.data:
            for product in products:
                if product not in self.data[store_name]:
                    self.data[store_name].append(product)
            self.save_all_data()
            return True
        return False
    
    def delete_product(self, product_name):
        """Delete a product from all stores and product lists"""
        # Remove from all stores
        for store in self.data:
            if product_name in self.data[store]:
                self.data[store].remove(product_name)
        
        # Remove from product lists
        if product_name in self.all_products:
            self.all_products.remove(product_name)
        
        # Remove from prices, barcodes, and suppliers
        if product_name in self.product_prices:
            del self.product_prices[product_name]
        if product_name in self.product_barcodes:
            del self.product_barcodes[product_name]
        if product_name in self.product_suppliers:
            del self.product_suppliers[product_name]
        if product_name in self.product_categories:
            del self.product_categories[product_name]
        
        # Save all changes
        self.save_all_data()
        
        return True
    
    def merge_products(self, product_to_keep, product_to_remove):
        """Merge two products - keep one and remove the other"""
        if product_to_keep == product_to_remove:
            return False, "Cannot merge the same product"
        
        # Update all stores
        for store in self.data:
            if product_to_remove in self.data[store]:
                self.data[store].remove(product_to_remove)
                if product_to_keep not in self.data[store]:
                    self.data[store].append(product_to_keep)
        
        # Update product lists
        if product_to_remove in self.all_products:
            self.all_products.remove(product_to_remove)
        
        # Update prices, barcodes, suppliers
        if product_to_remove in self.product_prices:
            if product_to_keep not in self.product_prices:
                self.product_prices[product_to_keep] = self.product_prices[product_to_remove]
            del self.product_prices[product_to_remove]
        
        if product_to_remove in self.product_barcodes:
            if product_to_keep not in self.product_barcodes:
                self.product_barcodes[product_to_keep] = self.product_barcodes[product_to_remove]
            del self.product_barcodes[product_to_remove]
            
        if product_to_remove in self.product_suppliers:
            if product_to_keep not in self.product_suppliers:
                self.product_suppliers[product_to_keep] = self.product_suppliers[product_to_remove]
            del self.product_suppliers[product_to_remove]
            
        if product_to_remove in self.product_categories:
            if product_to_keep not in self.product_categories:
                self.product_categories[product_to_keep] = self.product_categories[product_to_remove]
            del self.product_categories[product_to_remove]
        
        # Save all changes
        self.save_all_data()
            
        return True, f"Successfully merged {product_to_remove} into {product_to_keep}"
    
    def update_product(self, old_name, new_name, price, barcode, supplier, stores, category):
        """Update product details"""
        if old_name != new_name:
            # Rename product in all locations
            for store in self.data:
                if old_name in self.data[store]:
                    self.data[store].remove(old_name)
                    self.data[store].append(new_name)
            
            # Update product lists
            if old_name in self.all_products:
                self.all_products.remove(old_name)
                self.all_products.append(new_name)
                self.all_products.sort()
            
            # Update data dictionaries
            if old_name in self.product_prices:
                self.product_prices[new_name] = self.product_prices.pop(old_name)
            if old_name in self.product_barcodes:
                self.product_barcodes[new_name] = self.product_barcodes.pop(old_name)
            if old_name in self.product_suppliers:
                self.product_suppliers[new_name] = self.product_suppliers.pop(old_name)
            if old_name in self.product_categories:
                self.product_categories[new_name] = self.product_categories.pop(old_name)
        
        # Update product details
        self.product_prices[new_name] = price
        self.product_barcodes[new_name] = barcode
        self.product_suppliers[new_name] = supplier
        self.product_categories[new_name] = category
        
        # Update store availability
        for store in self.data:
            if store in stores:
                if new_name not in self.data[store]:
                    self.data[store].append(new_name)
            else:
                if new_name in self.data[store]:
                    self.data[store].remove(new_name)
        
        # Save all changes
        self.save_all_data()
        
        return True, f"Successfully updated {new_name}"

def apply_dark_mode():
    """Apply dark mode styles"""
    if st.session_state.get('dark_mode', False):
        st.markdown("""
        <style>
            .main { background-color: #1a202c; color: #e2e8f0; }
            .stApp { background-color: #1a202c; color: #e2e8f0; }
            .css-1d391kg { background-color: #1a202c; }
            .css-1y4p8pa { background-color: #2d3748; color: #e2e8f0; }
            .css-1v0mbdj { background-color: #2d3748; color: #e2e8f0; }
            .css-1r6slb0 { background-color: #2d3748; color: #e2e8f0; }
        </style>
        """, unsafe_allow_html=True)

def main():
    # Initialize data manager
    DataManager.initialize_session_state()

    # Apply dark mode
    apply_dark_mode()

    # Initialize stock manager
    stock_manager = StockManager()
    
    # Header with dark mode toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="main-header">🏪 TY PASAR RAYA JIMAT SDN BHD</h1>', unsafe_allow_html=True)
        st.markdown("### Stock Management & Purchase Order System")
    with col2:
        if st.button("🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Sidebar with Sales Representative Details
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose a feature",
        ["📊 Dashboard", "🔍 Check Stock", "📍 Find Locations", "🏪 Store Inventory", 
         "📦 All Products", "➕ Add Products/Stores", "✏️ Edit/Merge Products", "💰 Manage Prices", "📋 Generate PO"]
    )
    
    # Sales Representative Details in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📞 Sales Representative")
    st.sidebar.markdown("""
    <div class="sales-rep-card">
        <strong>MD RAKIBUL ISLAM</strong><br>
        📧 gts86@pinnaclefoods.com.my<br>
        📱 0192699618
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-fix products button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Auto-Fix Products", use_container_width=True):
        auto_fix_products(stock_manager)
    
    # Update Prices button
    st.sidebar.markdown("---")
    if st.sidebar.button("💰 Update All Prices", use_container_width=True):
        update_all_prices(stock_manager)
    
    # Data management buttons
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Data Management")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("💾 Save Data", use_container_width=True):
            stock_manager.save_all_data()
            st.sidebar.success("✅ All data saved!")
    with col2:
        if st.button("🔄 Reset Data", use_container_width=True):
            if st.sidebar.checkbox("Confirm reset"):
                # Clear all data files
                for file in ['store_data.json', 'product_prices.json', 'product_barcodes.json', 
                           'product_suppliers.json', 'product_categories.json']:
                    try:
                        if os.path.exists(file):
                            os.remove(file)
                    except:
                        pass
                st.session_state.initialized = False
                st.sidebar.success("✅ Data reset! Refresh the page.")
                st.rerun()
    
    if app_mode == "📊 Dashboard":
        show_dashboard(stock_manager)
    elif app_mode == "🔍 Check Stock":
        check_stock(stock_manager)
    elif app_mode == "📍 Find Locations":
        find_locations(stock_manager)
    elif app_mode == "🏪 Store Inventory":
        store_inventory(stock_manager)
    elif app_mode == "📦 All Products":
        all_products(stock_manager)
    elif app_mode == "➕ Add Products/Stores":
        add_products_stores(stock_manager)
    elif app_mode == "✏️ Edit/Merge Products":
        edit_merge_products(stock_manager)
    elif app_mode == "💰 Manage Prices":
        manage_prices(stock_manager)
    elif app_mode == "📋 Generate PO":
        generate_po(stock_manager)
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">Deployed by "xtremrakib"</div>', unsafe_allow_html=True)

def auto_fix_products(stock_manager):
    """Automatically fix product names and merges"""
    st.info("🔄 Running auto-fix for products...")
    
    # Fix Mustard Oil names
    changes_made = False
    
    # Change MUSTARD OIL 200ML to PRAN MUSTARD OIL 200ML
    if 'MUSTARD OIL 200ML' in stock_manager.all_products:
        success, message = stock_manager.update_product(
            'MUSTARD OIL 200ML', 
            'PRAN MUSTARD OIL 200ML',
            stock_manager.product_prices.get('MUSTARD OIL 200ML', 3.00),
            stock_manager.product_barcodes.get('MUSTARD OIL 200ML', ''),
            stock_manager.product_suppliers.get('MUSTARD OIL 200ML', 'PINNACLE FOODS (M) SDN BHD'),
            [store for store in stock_manager.data if 'MUSTARD OIL 200ML' in stock_manager.data[store]],
            'Mustard Oil'
        )
        if success:
            st.success(f"✅ {message}")
            changes_made = True
    
    # Merge MUSTARD OIL 400ML with PRAN MUSTARD OIL 400ML
    if 'MUSTARD OIL 400ML' in stock_manager.all_products and 'PRAN MUSTARD OIL 400ML' in stock_manager.all_products:
        success, message = stock_manager.merge_products('PRAN MUSTARD OIL 400ML', 'MUSTARD OIL 400ML')
        if success:
            st.success(f"✅ {message}")
            changes_made = True
    
    # Merge POWER ENERGY DRINK 250ML with POWER ENERGY DRINK PET 250ML
    if 'POWER ENERGY DRINK 250ML' in stock_manager.all_products and 'POWER ENERGY DRINK PET 250ML' in stock_manager.all_products:
        success, message = stock_manager.merge_products('POWER ENERGY DRINK PET 250ML', 'POWER ENERGY DRINK 250ML')
        if success:
            st.success(f"✅ {message}")
            changes_made = True
    
    # Update categories for PET 320ml products
    pet_320ml_products = ['PRAN TAMARIND PET 320ML', 'PRAN SOUR PLUM PET 320ML', 'PRAN BIRD NEST PET 320ML']
    for product in pet_320ml_products:
        if product in stock_manager.all_products:
            stock_manager.product_categories[product] = 'PET 320ml'
            changes_made = True
    
    if changes_made:
        stock_manager.save_all_data()
        st.success("✅ Auto-fix completed successfully!")
        st.rerun()
    else:
        st.info("ℹ️ No changes needed - products are already correct.")

def update_all_prices(stock_manager):
    """Update all prices to the new specified prices"""
    st.info("💰 Updating all product prices...")
    
    # Define the new prices
    new_prices = {
        # Barbican products
        'BARBICAN POMEGRANATE': 4.38,
        'BARBICAN RASBERRY': 4.38,
        'BARBICAN APPLE': 4.38,
        'BARBICAN LEMON': 4.38,
        'BARBICAN STRAWBERRY': 4.38,
        'BARBICAN PINEAPPLE': 4.38,
        
        # Basil Seed products
        'PRAN BASIL SEED MANGO': 2.42,
        'PRAN BASIL SEED ORANGE': 2.42,
        'PRAN BASIL SEED STRAWBERRY': 2.42,
        'PRAN BASIL SEED KIWI': 2.42,
        'PRAN BASIL SEED LITCHI': 2.42,
        'PRAN BASIL SEED COCKTAIL': 2.42,
        'PRAN BASIL SEED PINEAPPLE': 2.42,
        'PRAN BASIL SEED POMEGRANATE': 2.42,
        'PRAN BASIL SEED COCONUT': 2.42,
        
        # BES Minuman products
        'PRAN BES MINUMAN BERPERISA ANGGUR': 2.00,
        'PRAN BES MINUMAN BERPERISA OREN': 2.00,
        'PRAN BES MINUMAN BERPERISA JAGUNG': 2.00,
        'PRAN BES MINUMAN BERPERISA LYCHEE': 2.00,
        'PRAN BES MINUMAN BERPERISA ROSE': 2.00,
        'PRAN BES MINUMAN BERPERISA SARSI': 2.00,
        
        # Humpty Dumpty
        'HUMPTY DUMPTY': 2.00,
        
        # Power Energy Drink
        'POWER ENERGY DRINK PET 250ML': 1.42,
        
        # Vegetable Ghee
        'PRAN VEGETABLE GHEE 450G': 10.63,
        'PRAN VEGETABLE GHEE 125G': 4.13,
        
        # Coconut Water
        'PRAN COCONUT WATER': 1.67,
        
        # Lemon Teh
        'PRAN AIS LEMON TEH': 1.63,
        
        # Paradise
        'PRAN PREMIO PARADISE': 3.11,
        
        # Chanachur
        'PRAN CHANACHUR HOT 250G': 3.13,
        'PRAN CHANACHUR BBQ 250G': 3.13,
        
        # Jus 1000ml
        'PRAN JUS PET 1000ML MANGO': 3.75,
        'PRAN JUS PET 1000ML ORANGE': 3.75,
        'PRAN JUS PET 1000ML APPLE': 3.75,
        
        # Jus 330ml
        'PRAN JUS 330ML APPLE': 1.50,
        'PRAN JUS 330ML ORANGE': 1.50,
        'PRAN JUS 330ML MANGO': 1.50,
        
        # PET 320ml
        'PRAN TAMARIND PET 320ML': 1.50,
        'PRAN SOUR PLUM PET 320ML': 1.50,
        'PRAN BIRD NEST PET 320ML': 1.50,
        
        # Drinko 250ml
        'DRINKO FLOAT 250ML MANGO': 1.50,
        'DRINKO FLOAT 250ML STRAWBERRY': 1.50,
        'DRINKO FLOAT 250ML LYCHEE': 1.50,
        
        # Drinko 330ml
        'DRINKO FLOAT 330ML MANGO': 2.00,
        'DRINKO FLOAT 330ML STRAWBERRY': 2.00,
        'DRINKO FLOAT 330ML LYCHEE': 2.00,
        'DRINKO FLOAT 330ML ORANGE': 2.00,
        'DRINKO FLOAT 330ML PINEAPPLE': 2.00,
        
        # Lassi 285ml
        'PRAN LASSI 285ML YOGURT': 1.69,
        'PRAN LASSI 285ML MANGO': 1.69,
        'PRAN LASSI 285ML BANANA': 1.69,
        'PRAN LASSI 285ML STRAWBERRY': 1.69,
        
        # Soya Can
        'PRAN SOYA CAN 300ML': 1.00,
        
        # Cooling Tamarind
        'PRAN COOLING TAMARIND': 1.38,
        
        # Jus 1.5L
        'PRAN JUS PET VALUE PACK 1.5L MANGO': 11.00,
        'PRAN JUS PET VALUE PACK 1.5L ORANGE': 11.00,
        
        # Mustard Oil
        'PRAN MUSTARD OIL 400ML': 5.83,
        'PRAN MUSTARD OIL 200ML': 3.00,
        
        # Lollipop
        'PRAN VARIETY LOLLIPOP': 30.00,
        
        # Puffed Rice
        'PRAN PUFFED RICE 400G': 2.75,
        
        # Other products
        'PRAN CREAMER 500GM': 5.00,
        'PRAN CREAMER 500GM EASY OPEN': 5.00,
        'PRAN CHOCO STICK': 3.00,
        'PRAN SWEETENED CREAMER 500GM': 5.00,
        'BOMBAY BRIYANI MASALA': 4.50,
        'PRAN POTATA BISCUITS 100GM': 3.50,
    }
    
    updated_count = 0
    for product in stock_manager.all_products:
        for key, price in new_prices.items():
            if key in product.upper():
                stock_manager.product_prices[product] = price
                updated_count += 1
                break
    
    stock_manager.save_all_data()
    st.success(f"✅ Updated prices for {updated_count} products!")
    st.rerun()

def add_products_stores(stock_manager):
    st.header("➕ Add Products & Stores")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Add Product", "Add Store", "Add Products to Store", "Manage Barcodes"])
    
    with tab1:
        st.subheader("Add New Product")
        
        col1, col2 = st.columns(2)
        with col1:
            new_product_name = st.text_input("Product Name")
            product_price = st.number_input("Price (RM)", min_value=0.0, value=3.0, step=0.1)
        with col2:
            barcode = st.text_input("Barcode (Optional)")
            available_stores = st.multiselect("Available in Stores", list(stock_manager.data.keys()))
            supplier = st.selectbox("Supplier", ["PINNACLE FOODS (M) SDN BHD", "PRAN", "BARBICAN", "DRINKO", "OTHER"])
        
        # Category selection - FIXED: Ensure all values are strings
        all_categories = sorted(list(set(str(cat) for cat in stock_manager.product_categories.values())))
        category = st.selectbox("Category", all_categories + ["Auto-detect from name"])
        
        if st.button("Add Product"):
            if new_product_name and available_stores:
                final_category = None if category == "Auto-detect from name" else category
                stock_manager.add_product(new_product_name, available_stores, product_price, barcode, supplier, final_category)
                st.success(f"✅ Product '{new_product_name}' added successfully!")
                st.rerun()  # Refresh to show the new product immediately
            else:
                st.error("❌ Please enter product name and select at least one store.")
    
    with tab2:
        st.subheader("Add New Store/Branch")
        
        new_store_name = st.text_input("Store Name")
        
        # Option to add initial products to the new store
        st.subheader("Add Initial Products to New Store (Optional)")
        available_products = stock_manager.all_products
        initial_products = st.multiselect("Select products to add to the new store", available_products)
        
        if st.button("Add Store"):
            if new_store_name:
                if stock_manager.add_store(new_store_name, initial_products):
                    if initial_products:
                        st.success(f"✅ Store '{new_store_name}' added successfully with {len(initial_products)} products!")
                    else:
                        st.success(f"✅ Store '{new_store_name}' added successfully!")
                    st.rerun()  # Refresh to show the new store immediately
                else:
                    st.error("❌ Store already exists!")
            else:
                st.error("❌ Please enter a store name.")
    
    with tab3:
        st.subheader("Add Products to Existing Store")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_store = st.selectbox("Select Store", list(stock_manager.data.keys()))
        with col2:
            # Show current products in the store
            current_products = stock_manager.data.get(selected_store, [])
            st.write(f"**Current products in {selected_store}:** {len(current_products)}")
        
        # Get products not currently in the store
        all_products = stock_manager.all_products
        store_products = stock_manager.data.get(selected_store, [])
        available_products = [p for p in all_products if p not in store_products]
        
        products_to_add = st.multiselect("Select products to add", available_products)
        
        if st.button("Add Products to Store"):
            if selected_store and products_to_add:
                if stock_manager.add_products_to_store(selected_store, products_to_add):
                    st.success(f"✅ Added {len(products_to_add)} products to {selected_store}!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add products to store")
            else:
                st.warning("⚠️ Please select a store and at least one product")
    
    with tab4:
        st.subheader("Manage Product Barcodes")
        
        selected_product = st.selectbox("Select Product", stock_manager.all_products)
        current_barcode = stock_manager.product_barcodes.get(selected_product, "")
        new_barcode = st.text_input("Barcode", value=current_barcode)
        
        if st.button("Update Barcode"):
            if selected_product and new_barcode:
                stock_manager.product_barcodes[selected_product] = new_barcode
                stock_manager.save_all_data()
                st.success(f"✅ Barcode updated for '{selected_product}'")

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
            <h4>{most_stocked_store[:15]}...</h4>
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
        
        # Show product category
        category = stock_manager.product_categories.get(product_name, "Uncategorized")
        st.write(f"**Category:** {category}")
        
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
        
        # Show product category
        category = stock_manager.product_categories.get(product_name, "Uncategorized")
        st.write(f"**Category:** {category}")
        
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
        
        # Group products by category
        products_by_category = {}
        for product in products:
            category = stock_manager.product_categories.get(product, "Uncategorized")
            if category not in products_by_category:
                products_by_category[category] = []
            products_by_category[category].append(product)
        
        search_term = st.text_input("🔍 Search products...")
        
        # Use appropriate styling based on dark mode
        dark_mode = st.session_state.get('dark_mode', False)
        product_class = "product-card dark-mode" if dark_mode else "product-card"
        
        for category, category_products in sorted(products_by_category.items()):
            filtered_products = [p for p in category_products if search_term.lower() in p.lower()] if search_term else category_products
            
            if filtered_products:
                with st.expander(f"{category} ({len(filtered_products)} products)"):
                    cols = st.columns(2)
                    for i, product in enumerate(filtered_products):
                        with cols[i % 2]:
                            barcode = stock_manager.product_barcodes.get(product, "No barcode")
                            price = stock_manager.product_prices.get(product, stock_manager.estimate_price(product))
                            supplier = stock_manager.product_suppliers.get(product, "PINNACLE FOODS (M) SDN BHD")
                            st.markdown(f'''
                            <div class="{product_class}">
                                <strong>{product}</strong><br>
                                <small>Price: RM{price:.2f} | Supplier: {supplier}</small><br>
                                <small>Barcode: {barcode}</small>
                            </div>
                            ''', unsafe_allow_html=True)

def all_products(stock_manager):
    st.header("📦 All Products")
    st.write(f"**Total Unique Products:** {len(stock_manager.all_products)}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Search products...")
    with col2:
        # Get all unique categories - FIXED: Ensure all values are strings
        all_categories = sorted(list(set(str(cat) for cat in stock_manager.product_categories.values())))
        category_filter = st.selectbox("Filter by Category", ["All Categories"] + all_categories)
    
    # Group products by category
    products_by_category = {}
    for product in stock_manager.all_products:
        category = stock_manager.product_categories.get(product, "Uncategorized")
        if category not in products_by_category:
            products_by_category[category] = []
        products_by_category[category].append(product)
    
    # Filter products
    if search_term or category_filter != "All Categories":
        filtered_products_by_category = {}
        for category, products in products_by_category.items():
            if category_filter != "All Categories" and str(category) != category_filter:
                continue
            filtered_products = [p for p in products if search_term.lower() in p.lower()] if search_term else products
            if filtered_products:
                filtered_products_by_category[category] = filtered_products
        products_by_category = filtered_products_by_category
    
    total_filtered = sum(len(products) for products in products_by_category.values())
    st.write(f"**Showing {total_filtered} products:**")
    
    # Use appropriate styling based on dark mode
    dark_mode = st.session_state.get('dark_mode', False)
    product_class = "product-card dark-mode" if dark_mode else "product-card"
    
    # FIXED: Sort categories by string representation to avoid TypeError
    for category, products in sorted(products_by_category.items(), key=lambda x: str(x[0])):
        with st.expander(f"{category} ({len(products)} products)"):
            cols = st.columns(2)
            for i, product in enumerate(products):
                with cols[i % 2]:
                    store_count = len(stock_manager.find_product_locations(product))
                    price = stock_manager.product_prices.get(product, stock_manager.estimate_price(product))
                    barcode = stock_manager.product_barcodes.get(product, "No barcode")
                    supplier = stock_manager.product_suppliers.get(product, "PINNACLE FOODS (M) SDN BHD")
                    
                    st.markdown(f'''
                    <div class="{product_class}">
                        <strong>{product}</strong><br>
                        <small>Stores: {store_count} | Price: RM{price:.2f}</small><br>
                        <small>Supplier: {supplier}</small><br>
                        <small>Barcode: {barcode}</small>
                    </div>
                    ''', unsafe_allow_html=True)

def edit_merge_products(stock_manager):
    st.header("✏️ Edit & Merge Products")
    
    tab1, tab2, tab3 = st.tabs(["Edit Product", "Merge Products", "Delete Product"])
    
    with tab1:
        st.subheader("Edit Product Details")
        
        product_to_edit = st.selectbox("Select Product to Edit", stock_manager.all_products)
        
        if product_to_edit:
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Product Name", value=product_to_edit)
                current_price = stock_manager.product_prices.get(product_to_edit, stock_manager.estimate_price(product_to_edit))
                new_price = st.number_input("Price (RM)", min_value=0.0, value=float(current_price), step=0.1)
            with col2:
                current_barcode = stock_manager.product_barcodes.get(product_to_edit, "")
                new_barcode = st.text_input("Barcode", value=current_barcode)
                current_supplier = stock_manager.product_suppliers.get(product_to_edit, "PINNACLE FOODS (M) SDN BHD")
                new_supplier = st.selectbox("Supplier", 
                                          ["PINNACLE FOODS (M) SDN BHD", "PRAN", "BARBICAN", "DRINKO", "OTHER"],
                                          index=0 if current_supplier == "PINNACLE FOODS (M) SDN BHD" else 
                                                1 if current_supplier == "PRAN" else
                                                2 if current_supplier == "BARBICAN" else
                                                3 if current_supplier == "DRINKO" else 4)
            
            # Category selection - FIXED: Ensure all values are strings
            all_categories = sorted(list(set(str(cat) for cat in stock_manager.product_categories.values())))
            current_category = stock_manager.product_categories.get(product_to_edit, "Uncategorized")
            new_category = st.selectbox("Category", all_categories, index=all_categories.index(str(current_category)) if str(current_category) in all_categories else 0)
            
            current_stores = [store for store in stock_manager.data if product_to_edit in stock_manager.data[store]]
            new_stores = st.multiselect("Available in Stores", 
                                      list(stock_manager.data.keys()),
                                      default=current_stores)
            
            if st.button("Update Product"):
                if new_name:
                    success, message = stock_manager.update_product(
                        product_to_edit, new_name, new_price, new_barcode, new_supplier, new_stores, new_category
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Product name cannot be empty")
    
    with tab2:
        st.subheader("Merge Products")
        st.info("This will combine two products into one. The second product will be removed.")
        
        col1, col2 = st.columns(2)
        with col1:
            product_to_keep = st.selectbox("Product to Keep", stock_manager.all_products, key="keep")
        with col2:
            # Don't show the same product in both dropdowns
            other_products = [p for p in stock_manager.all_products if p != product_to_keep]
            product_to_remove = st.selectbox("Product to Remove", other_products, key="remove")
        
        if product_to_keep and product_to_remove:
            st.warning(f"⚠️ This will merge '{product_to_remove}' into '{product_to_keep}' and remove '{product_to_remove}'")
            
            if st.button("Merge Products", type="primary"):
                success, message = stock_manager.merge_products(product_to_keep, product_to_remove)
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    with tab3:
        st.subheader("Delete Product")
        st.warning("⚠️ This will permanently delete a product from all stores and product lists.")
        
        product_to_delete = st.selectbox("Select Product to Delete", stock_manager.all_products, key="delete")
        
        if product_to_delete:
            # Show product details before deletion
            current_price = stock_manager.product_prices.get(product_to_delete, stock_manager.estimate_price(product_to_delete))
            current_barcode = stock_manager.product_barcodes.get(product_to_delete, "No barcode")
            current_supplier = stock_manager.product_suppliers.get(product_to_delete, "PINNACLE FOODS (M) SDN BHD")
            current_category = stock_manager.product_categories.get(product_to_delete, "Uncategorized")
            store_count = len(stock_manager.find_product_locations(product_to_delete))
            
            st.write(f"**Product Details:**")
            st.write(f"- **Name:** {product_to_delete}")
            st.write(f"- **Category:** {current_category}")
            st.write(f"- **Price:** RM{current_price:.2f}")
            st.write(f"- **Barcode:** {current_barcode}")
            st.write(f"- **Supplier:** {current_supplier}")
            st.write(f"- **Available in:** {store_count} stores")
            
            # Confirmation before deletion
            confirm_delete = st.checkbox("I understand this action cannot be undone")
            
            if st.button("🗑️ Delete Product", type="primary", disabled=not confirm_delete):
                if stock_manager.delete_product(product_to_delete):
                    st.success(f"✅ Product '{product_to_delete}' deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete product")

def manage_prices(stock_manager):
    st.header("💰 Manage Product Prices")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Bulk Price Update", "Individual Price Update", "Price by Category", "Price Overview"])
    
    with tab1:
        st.subheader("Bulk Price Changes")
        
        col1, col2 = st.columns(2)
        with col1:
            price_change_type = st.radio("Change Type", ["Percentage Increase", "Percentage Decrease", "Fixed Amount", "Set New Price"])
            if price_change_type in ["Percentage Increase", "Percentage Decrease"]:
                change_value = st.number_input("Percentage", min_value=0.0, max_value=100.0, value=10.0, step=1.0)
            else:
                change_value = st.number_input("Amount (RM)", min_value=0.0, value=1.0, step=0.1)
        
        with col2:
            # Make all products available in the selection
            products_to_update = st.multiselect("Select Products", stock_manager.all_products, 
                                              default=stock_manager.all_products[:10] if len(stock_manager.all_products) > 10 else stock_manager.all_products)
        
        if st.button("Apply Bulk Price Change"):
            if products_to_update:
                updated_count = 0
                for product in products_to_update:
                    current_price = stock_manager.product_prices.get(product, stock_manager.estimate_price(product))
                    
                    if price_change_type == "Percentage Increase":
                        new_price = current_price * (1 + change_value / 100)
                    elif price_change_type == "Percentage Decrease":
                        new_price = current_price * (1 - change_value / 100)
                    elif price_change_type == "Fixed Amount":
                        new_price = current_price + change_value
                    else:  # Set New Price
                        new_price = change_value
                    
                    stock_manager.product_prices[product] = round(new_price, 2)
                    updated_count += 1
                
                stock_manager.save_all_data()
                st.success(f"✅ Updated prices for {updated_count} products")
            else:
                st.error("❌ Please select at least one product")
    
    with tab2:
        st.subheader("Individual Price Editor")
        
        selected_product = st.selectbox("Select Product", stock_manager.all_products)
        current_price = stock_manager.product_prices.get(selected_product, stock_manager.estimate_price(selected_product))
        new_price = st.number_input("New Price (RM)", min_value=0.0, value=float(current_price), step=0.1)
        
        if st.button("Update Price"):
            stock_manager.product_prices[selected_product] = new_price
            stock_manager.save_all_data()
            st.success(f"✅ Price for '{selected_product}' updated to RM{new_price:.2f}")
    
    with tab3:
        st.subheader("Update Prices by Category")
        
        # Get all unique categories - FIXED: Ensure all values are strings and handle sorting
        all_categories = sorted(list(set(str(cat) for cat in stock_manager.product_categories.values())))
        
        col1, col2 = st.columns(2)
        with col1:
            selected_category = st.selectbox("Select Category", all_categories)
            price_change_type = st.radio("Change Type", 
                                       ["Percentage Increase", "Percentage Decrease", "Fixed Amount", "Set New Price"],
                                       key="category_price")
            if price_change_type in ["Percentage Increase", "Percentage Decrease"]:
                change_value = st.number_input("Percentage", min_value=0.0, max_value=100.0, value=10.0, step=1.0, key="category_percent")
            else:
                change_value = st.number_input("Amount (RM)", min_value=0.0, value=1.0, step=0.1, key="category_amount")
        
        with col2:
            # Show products in this category
            category_products = [p for p in stock_manager.all_products if str(stock_manager.product_categories.get(p)) == selected_category]
            st.write(f"**Products in {selected_category}:**")
            if category_products:
                for product in category_products:
                    current_price = stock_manager.product_prices.get(product, stock_manager.estimate_price(product))
                    st.write(f"- {product}: RM{current_price:.2f}")
                st.write(f"**Total products:** {len(category_products)}")
            else:
                st.info("No products in this category")
        
        if st.button("Apply Category Price Change"):
            if category_products:
                updated_count = 0
                for product in category_products:
                    current_price = stock_manager.product_prices.get(product, stock_manager.estimate_price(product))
                    
                    if price_change_type == "Percentage Increase":
                        new_price = current_price * (1 + change_value / 100)
                    elif price_change_type == "Percentage Decrease":
                        new_price = current_price * (1 - change_value / 100)
                    elif price_change_type == "Fixed Amount":
                        new_price = current_price + change_value
                    else:  # Set New Price
                        new_price = change_value
                    
                    stock_manager.product_prices[product] = round(new_price, 2)
                    updated_count += 1
                
                stock_manager.save_all_data()
                st.success(f"✅ Updated prices for {updated_count} products in {selected_category} category")
            else:
                st.error("❌ No products in selected category")
    
    with tab4:
        st.subheader("Current Price Overview")
        
        # Search and filter
        search_term = st.text_input("🔍 Search products...", key="price_search")
        # Make all products available in the list
        filtered_products = [p for p in stock_manager.all_products if search_term.lower() in p.lower()] if search_term else stock_manager.all_products
        
        # Display prices in an editable format
        price_data = []
        for product in filtered_products[:50]:  # Show first 50 products
            current_price = stock_manager.product_prices.get(product, stock_manager.estimate_price(product))
            category = stock_manager.product_categories.get(product, "Uncategorized")
            price_data.append({
                'Product': product,
                'Category': category,
                'Current Price (RM)': current_price
            })
        
        if price_data:
            df = pd.DataFrame(price_data)
            edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
            
            if st.button("Save All Price Changes"):
                for index, row in edited_df.iterrows():
                    product = row['Product']
                    new_price = row['Current Price (RM)']
                    stock_manager.product_prices[product] = new_price
                stock_manager.save_all_data()
                st.success("✅ All price changes saved successfully!")

def generate_po(stock_manager):
    st.header("📋 Generate Purchase Order")
    
    col1, col2 = st.columns(2)
    with col1:
        supplier = st.selectbox("Supplier", ["PINNACLE FOODS (M) SDN BHD", "PRAN", "BARBICAN", "DRINKO", "OTHER SUPPLIER"])
        company_name = st.text_input("Company Name", "TY PASAR RAYA JIMAT SDN BHD")
    with col2:
        delivery_date = st.date_input("Requested Delivery Date")
        delivery_address = st.text_area("Delivery Address", "Main Warehouse, Kuala Lumpur")
    
    st.subheader("Add Products to PO")
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        # Make all products available in the selection
        new_product = st.selectbox("Select Product", stock_manager.all_products, key="po_product_select")
    with col2:
        new_quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="po_quantity_input")
    with col3:
        default_price = stock_manager.product_prices.get(new_product, stock_manager.estimate_price(new_product))
        new_price = st.number_input("Unit Price (RM)", min_value=0.0, value=float(default_price), step=0.1, key="po_price_input")
    with col4:
        if st.button("Add to PO", use_container_width=True, key="add_po_button"):
            if new_product:
                st.session_state.po_products.append(new_product)
                st.session_state.po_quantities.append(new_quantity)
                st.session_state.po_prices.append(new_price)
                st.success(f"Added {new_product} to PO!")
    
    if st.session_state.po_products:
        st.subheader("Current Purchase Order Items")
        
        total_amount = 0
        for i, (product, qty, price) in enumerate(zip(st.session_state.po_products, st.session_state.po_quantities, st.session_state.po_prices)):
            total = price * qty
            total_amount += total
            
            col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
            with col1:
                st.write(f"**{product}**")
            with col2:
                st.write(f"**Qty:** {qty}")
            with col3:
                # Editable price field
                new_price = st.number_input(f"Price", value=float(price), min_value=0.0, step=0.1, key=f"price_{i}")
                if new_price != price:
                    st.session_state.po_prices[i] = new_price
                    st.rerun()
            with col4:
                item_total = st.session_state.po_prices[i] * qty
                st.write(f"**Total:** RM{item_total:.2f}")
            with col5:
                st.write("")  # Spacer
            with col6:
                if st.button("❌ Remove", key=f"remove_{i}"):
                    st.session_state.po_products.pop(i)
                    st.session_state.po_quantities.pop(i)
                    st.session_state.po_prices.pop(i)
                    st.rerun()
        
        st.markdown(f"**Grand Total: RM{total_amount:.2f}**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Generate PO Document", type="primary", use_container_width=True):
                generate_po_document(stock_manager, st.session_state.po_products, 
                                   st.session_state.po_quantities, st.session_state.po_prices, 
                                   supplier, delivery_date, company_name, delivery_address)
        with col2:
            if st.button("🖨️ Print PO", use_container_width=True):
                st.info("PO ready for printing - Use browser print function (Ctrl+P)")
        with col3:
            if st.button("🗑️ Clear PO", use_container_width=True):
                st.session_state.po_products = []
                st.session_state.po_quantities = []
                st.session_state.po_prices = []
                st.rerun()
    else:
        st.info("No products added to purchase order yet.")

def generate_po_document(stock_manager, products, quantities, prices, supplier, delivery_date, company_name, delivery_address):
    po_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    po_data = []
    total_amount = 0
    
    for i, (product, qty, price) in enumerate(zip(products, quantities, prices)):
        total = price * qty
        total_amount += total
        po_data.append([i + 1, product, qty, f"RM{price:.2f}", f"RM{total:.2f}"])
    
    st.success("✅ Purchase Order Generated Successfully!")
    
    # Create a printable PO document
    po_html = f"""
    <div style="padding: 20px; border: 2px solid #333; border-radius: 10px; background: white; color: black; max-width: 800px; margin: 0 auto;">
        <h1 style="text-align: center; color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 10px;">PURCHASE ORDER</h1>
        
        <table style="width: 100%; margin-bottom: 20px; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>PO Number:</strong> {po_number}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Date:</strong> {timestamp}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Supplier:</strong> {supplier}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Delivery Date:</strong> {delivery_date}</td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Company:</strong> {company_name}</td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 8px;"><strong>Delivery Address:</strong> {delivery_address}</td>
            </tr>
        </table>
        
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background-color: #2E86AB; color: white;">
                <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Item No.</th>
                <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Product Description</th>
                <th style="border: 1px solid #ddd; padding: 12px; text-align: center;">Quantity</th>
                <th style="border: 1px solid #ddd; padding: 12px; text-align: right;">Unit Price (RM)</th>
                <th style="border: 1px solid #ddd; padding: 12px; text-align: right;">Total (RM)</th>
            </tr>
    """
    
    for item in po_data:
        po_html += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 10px;">{item[0]}</td>
                <td style="border: 1px solid #ddd; padding: 10px;">{item[1]}</td>
                <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">{item[2]}</td>
                <td style="border: 1px solid #ddd; padding: 10px; text-align: right;">{item[3]}</td>
                <td style="border: 1px solid #ddd; padding: 10px; text-align: right;">{item[4]}</td>
            </tr>
        """
    
    po_html += f"""
            <tr style="background-color: #f8f9fa; font-weight: bold; font-size: 1.1em;">
                <td colspan="4" style="border: 1px solid #ddd; padding: 12px; text-align: right;">GRAND TOTAL</td>
                <td style="border: 1px solid #ddd; padding: 12px; text-align: right;">RM{total_amount:.2f}</td>
            </tr>
        </table>
        
        <div style="margin-top: 40px; border-top: 2px solid #2E86AB; padding-top: 20px;">
            <div style="float: left; width: 45%;">
                <p><strong>Prepared By:</strong></p>
                <p>_________________________</p>
                <p>Name: ___________________</p>
                <p>Date: ___________________</p>
            </div>
            <div style="float: right; width: 45%;">
                <p><strong>Authorized Signature:</strong></p>
                <p>_________________________</p>
                <p>Name: ___________________</p>
                <p>Date: ___________________</p>
            </div>
            <div style="clear: both;"></div>
        </div>
    </div>
    """
    
    st.markdown(po_html, unsafe_allow_html=True)
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Download as CSV
        df = pd.DataFrame(po_data, columns=['Item No.', 'Product', 'Quantity', 'Unit Price', 'Total'])
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{po_number}.csv" style="background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">📥 Download as CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        # Print button
        st.markdown("""
        <script>
        function printPO() {
            window.print();
        }
        </script>
        <button onclick="printPO()" style="background-color: #008CBA; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 16px;">🖨️ Print Purchase Order</button>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
