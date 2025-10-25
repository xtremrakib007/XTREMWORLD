import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import base64
import json
import os
from io import BytesIO
import hashlib
import time

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
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .dark-mode .login-container {
        background-color: #2d3748;
        border: 1px solid #4a5568;
    }
    .user-status {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    .stock-info {
        background-color: #e8f5e8;
        border: 1px solid #28a745;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.2rem 0;
        font-size: 0.8rem;
    }
    .dark-mode .stock-info {
        background-color: #2d4a2d;
        border: 1px solid #38a169;
    }
    .pending-approval {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .dark-mode .pending-approval {
        background-color: #44370a;
        border: 1px solid #d69e2e;
    }
</style>
""", unsafe_allow_html=True)

class UserManager:
    """Manages user authentication and authorization"""
    
    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def initialize_users():
        """Initialize users data"""
        if 'users' not in st.session_state:
            try:
                if os.path.exists('users.json'):
                    with open('users.json', 'r') as f:
                        st.session_state.users = json.load(f)
                else:
                    # Create default admin user
                    st.session_state.users = {
                        'xtremrakib': {
                            'password': UserManager.hash_password('Rakib009'),
                            'role': 'admin',
                            'approved': True,
                            'created_at': datetime.now().isoformat()
                        }
                    }
                    UserManager.save_users()
            except:
                st.session_state.users = {
                    'xtremrakib': {
                        'password': UserManager.hash_password('Rakib009'),
                        'role': 'admin',
                        'approved': True,
                        'created_at': datetime.now().isoformat()
                    }
                }
    
    @staticmethod
    def save_users():
        """Save users to file"""
        try:
            with open('users.json', 'w') as f:
                json.dump(st.session_state.users, f)
        except:
            pass
    
    @staticmethod
    def create_user(username, password, role='user'):
        """Create a new user"""
        if username in st.session_state.users:
            return False, "Username already exists"
        
        st.session_state.users[username] = {
            'password': UserManager.hash_password(password),
            'role': role,
            'approved': role == 'admin',  # Auto-approve admin
            'created_at': datetime.now().isoformat()
        }
        UserManager.save_users()
        return True, "User created successfully. Waiting for admin approval."
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate a user"""
        if username not in st.session_state.users:
            return False, "Invalid username"
        
        user = st.session_state.users[username]
        if user['password'] != UserManager.hash_password(password):
            return False, "Invalid password"
        
        if not user['approved']:
            return False, "Account pending admin approval"
        
        return True, "Login successful"
    
    @staticmethod
    def get_pending_users():
        """Get list of users pending approval"""
        return [username for username, user in st.session_state.users.items() 
                if not user['approved'] and user['role'] != 'admin']
    
    @staticmethod
    def approve_user(username):
        """Approve a user"""
        if username in st.session_state.users:
            st.session_state.users[username]['approved'] = True
            UserManager.save_users()
            return True, f"User {username} approved successfully"
        return False, "User not found"

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
            st.session_state.saved_pos = DataManager.load_saved_pos()
            st.session_state.pending_changes = DataManager.load_pending_changes()
            
            # Initialize user session state if not exists
            if 'user' not in st.session_state:
                st.session_state.user = None
            if 'login_time' not in st.session_state:
                st.session_state.login_time = None
    
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
    def load_saved_pos():
        """Load saved purchase orders"""
        try:
            if os.path.exists('saved_pos.json'):
                with open('saved_pos.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    @staticmethod
    def load_pending_changes():
        """Load pending changes waiting for admin approval"""
        try:
            if os.path.exists('pending_changes.json'):
                with open('pending_changes.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
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
    def save_pos(data):
        """Save purchase orders to file"""
        try:
            with open('saved_pos.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    @staticmethod
    def save_pending_changes(data):
        """Save pending changes to file"""
        try:
            with open('pending_changes.json', 'w') as f:
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
        self.saved_pos = st.session_state.saved_pos
        self.pending_changes = st.session_state.pending_changes
        
        # Initialize default prices for products that don't have prices
        self.initialize_default_prices()
    
    def initialize_default_prices(self):
        """Initialize default prices for products that don't have prices"""
        changed = False
        for product in self.all_products:
            if product not in self.product_prices:
                self.product_prices[product] = self.estimate_price(product)
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
        st.session_state.saved_pos = self.saved_pos
        st.session_state.pending_changes = self.pending_changes
        
        # Save to files
        DataManager.save_store_data(self.data)
        DataManager.save_prices(self.product_prices)
        DataManager.save_barcodes(self.product_barcodes)
        DataManager.save_suppliers(self.product_suppliers)
        DataManager.save_categories(self.product_categories)
        DataManager.save_pos(self.saved_pos)
        DataManager.save_pending_changes(self.pending_changes)
    
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
    
    def get_stock_count(self, product_name):
        """Get total stock count across all stores"""
        count = 0
        for store, products in self.data.items():
            if product_name in products:
                count += 1
        return count
    
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
        # Check if user is admin
        if st.session_state.users[st.session_state.user]['role'] != 'admin':
            # Add to pending changes for admin approval
            change_request = {
                'type': 'add_product',
                'product_name': product_name,
                'stores': stores,
                'price': price,
                'barcode': barcode,
                'supplier': supplier,
                'category': category,
                'requested_by': st.session_state.user,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            }
            self.pending_changes.append(change_request)
            self.save_all_data()
            return False, "Change request submitted for admin approval"
        
        # Admin can make changes directly
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
        return True, f"Product '{product_name}' added successfully!"
    
    def add_store(self, store_name, initial_products=None):
        """Add new store with optional initial products"""
        # Check if user is admin
        if st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can add stores"
        
        if store_name not in self.data:
            if initial_products is None:
                initial_products = []
            self.data[store_name] = initial_products
            self.save_all_data()
            return True
        return False
    
    def add_products_to_store(self, store_name, products):
        """Add multiple products to a specific store"""
        # Check if user is admin
        if st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can add products to stores"
        
        if store_name in self.data:
            for product in products:
                if product not in self.data[store_name]:
                    self.data[store_name].append(product)
            self.save_all_data()
            return True
        return False
    
    def delete_product(self, product_name):
        """Delete a product from all stores and product lists"""
        # Check if user is admin
        if st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can delete products"
        
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
        # Check if user is admin
        if st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can merge products"
        
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
        # Check if user is admin
        if st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can update products"
        
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
    
    def save_po(self, po_data):
        """Save a purchase order"""
        po_number = po_data['po_number']
        self.saved_pos[po_number] = po_data
        self.save_all_data()
        return True
    
    def get_po_categories(self, products):
        """Get categories for PO products"""
        categories = {}
        for product in products:
            category = self.product_categories.get(product, "Uncategorized")
            if category not in categories:
                categories[category] = []
            categories[category].append(product)
        return categories

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

def show_login():
    """Show login/signup form"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True):
            if username and password:
                success, message = UserManager.authenticate(username, password)
                if success:
                    st.session_state.user = username
                    st.session_state.login_time = datetime.now()
                    st.success(f"Welcome {username}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")
    
    with tab2:
        st.subheader("Create Account")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Sign Up", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = UserManager.create_user(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Please fill all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_admin_panel():
    """Show admin panel for user management"""
    st.header("👨‍💼 Admin Panel")
    
    tab1, tab2, tab3 = st.tabs(["Pending Approvals", "User Management", "Pending Changes"])
    
    with tab1:
        st.subheader("Pending User Approvals")
        pending_users = UserManager.get_pending_users()
        
        if pending_users:
            for username in pending_users:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{username}**")
                    st.write(f"Created: {st.session_state.users[username]['created_at'][:10]}")
                with col2:
                    if st.button(f"Approve", key=f"approve_{username}"):
                        success, message = UserManager.approve_user(username)
                        if success:
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(message)
                with col3:
                    if st.button(f"Reject", key=f"reject_{username}"):
                        # Remove user
                        del st.session_state.users[username]
                        UserManager.save_users()
                        st.success(f"User {username} rejected and removed")
                        time.sleep(1)
                        st.rerun()
                st.markdown("---")
        else:
            st.info("No pending user approvals")
    
    with tab2:
        st.subheader("User Management")
        users = st.session_state.users
        
        for username, user_data in users.items():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                role_badge = "👑" if user_data['role'] == 'admin' else "👤"
                status_badge = "✅" if user_data['approved'] else "⏳"
                st.write(f"{role_badge} **{username}** {status_badge}")
                st.write(f"Role: {user_data['role']} | Created: {user_data['created_at'][:10]}")
            with col2:
                if username != 'xtremrakib':  # Don't allow deleting main admin
                    if st.button(f"Make Admin", key=f"admin_{username}"):
                        st.session_state.users[username]['role'] = 'admin'
                        UserManager.save_users()
                        st.success(f"{username} is now an admin")
                        time.sleep(1)
                        st.rerun()
            with col3:
                if username != 'xtremrakib' and not user_data['approved']:
                    if st.button(f"Approve", key=f"app_{username}"):
                        success, message = UserManager.approve_user(username)
                        if success:
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
            with col4:
                if username != 'xtremrakib':  # Don't allow deleting main admin
                    if st.button(f"Delete", key=f"del_{username}"):
                        del st.session_state.users[username]
                        UserManager.save_users()
                        st.success(f"User {username} deleted")
                        time.sleep(1)
                        st.rerun()
            st.markdown("---")
    
    with tab3:
        st.subheader("Pending Changes Approval")
        stock_manager = StockManager()
        pending_changes = stock_manager.pending_changes
        
        if pending_changes:
            for i, change in enumerate(pending_changes):
                st.write(f"**Change Request #{i+1}**")
                st.write(f"Type: {change['type'].replace('_', ' ').title()}")
                st.write(f"Requested by: {change['requested_by']}")
                st.write(f"Date: {change['timestamp'][:19]}")
                
                if change['type'] == 'add_product':
                    st.write(f"Product: {change['product_name']}")
                    st.write(f"Stores: {', '.join(change['stores'])}")
                    st.write(f"Price: RM{change['price']}")
                    st.write(f"Supplier: {change['supplier']}")
                    st.write(f"Category: {change['category']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve Change", key=f"approve_change_{i}"):
                        # Apply the change
                        if change['type'] == 'add_product':
                            success, message = stock_manager.add_product(
                                change['product_name'], change['stores'], change['price'],
                                change.get('barcode'), change['supplier'], change['category']
                            )
                            if success:
                                # Remove from pending changes
                                stock_manager.pending_changes.pop(i)
                                stock_manager.save_all_data()
                                st.success("Change approved and applied!")
                                time.sleep(1)
                                st.rerun()
                with col2:
                    if st.button(f"Reject Change", key=f"reject_change_{i}"):
                        stock_manager.pending_changes.pop(i)
                        stock_manager.save_all_data()
                        st.success("Change rejected!")
                        time.sleep(1)
                        st.rerun()
                st.markdown("---")
        else:
            st.info("No pending changes awaiting approval")

def main():
    # Initialize user manager
    UserManager.initialize_users()
    
    # Check if user is logged in
    if 'user' not in st.session_state or st.session_state.user is None:
        show_login()
        return
    
    # Check if user exists and is approved
    if st.session_state.user not in st.session_state.users:
        st.error("Your account has been deleted or is no longer active.")
        st.session_state.user = None
        time.sleep(2)
        st.rerun()
    
    user_data = st.session_state.users[st.session_state.user]
    if not user_data['approved']:
        st.error("Your account is pending admin approval. Please contact administrator.")
        st.session_state.user = None
        time.sleep(2)
        st.rerun()

    # Initialize data manager
    DataManager.initialize_session_state()

    # Apply dark mode
    apply_dark_mode()

    # Initialize stock manager
    stock_manager = StockManager()
    
    # Header with user info and dark mode toggle
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown('<h1 class="main-header">🏪 TY PASAR RAYA JIMAT SDN BHD</h1>', unsafe_allow_html=True)
        st.markdown("### Stock Management & Purchase Order System")
    with col2:
        user_role = user_data['role']
        role_badge = "👑 Admin" if user_role == 'admin' else "👤 User"
        st.markdown(f'<div class="user-status">{role_badge} | {st.session_state.user}</div>', unsafe_allow_html=True)
    with col3:
        if st.button("🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.login_time = None
            st.rerun()
    
    # Sidebar with Navigation
    st.sidebar.title("Navigation")
    
    # Admin panel in sidebar for admin users
    if user_role == 'admin':
        if st.sidebar.button("👨‍💼 Admin Panel", use_container_width=True):
            st.session_state.admin_panel = True
        
        if st.session_state.get('admin_panel', False):
            show_admin_panel()
            if st.sidebar.button("← Back to Main", use_container_width=True):
                st.session_state.admin_panel = False
            return
    
    app_mode = st.sidebar.selectbox(
        "Choose a feature",
        ["📊 Dashboard", "🔍 Check Stock", "📍 Find Locations", "🏪 Store Inventory", 
         "📦 All Products", "➕ Add Products/Stores", "✏️ Edit/Merge Products", "💰 Manage Prices", 
         "📋 Generate PO", "💾 Saved POs"]
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
                           'product_suppliers.json', 'product_categories.json', 'saved_pos.json', 'pending_changes.json']:
                    try:
                        if os.path.exists(file):
                            os.remove(file)
                    except:
                        pass
                st.session_state.initialized = False
                st.sidebar.success("✅ Data reset! Refresh the page.")
                time.sleep(2)
                st.rerun()
    
    # Show pending approval message for non-admin users
    if user_role != 'admin' and stock_manager.pending_changes:
        pending_count = len([c for c in stock_manager.pending_changes if c['requested_by'] == st.session_state.user])
        if pending_count > 0:
            st.markdown(f'<div class="pending-approval">⚠️ You have {pending_count} change(s) pending admin approval</div>', unsafe_allow_html=True)
    
    # Main application logic based on selected mode
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
    elif app_mode == "💾 Saved POs":
        show_saved_pos(stock_manager)
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">Deployed by "xtremrakib"</div>', unsafe_allow_html=True)

# All the remaining functions (auto_fix_products, update_all_prices, show_dashboard, etc.)
# remain the same as before, but I'll add the new generate_po and show_saved_pos functions

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
        
        # Show current stock information
        if new_product:
            stock_count = stock_manager.get_stock_count(new_product)
            stock_locations = stock_manager.find_product_locations(new_product)
            st.markdown(f'''
            <div class="stock-info">
                <strong>Current Stock:</strong> Available in {stock_count} stores<br>
                <strong>Available at:</strong> {", ".join(stock_locations) if stock_locations else "No stores"}
            </div>
            ''', unsafe_allow_html=True)
            
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
        st.subheader("Current Purchase Order Items (Category-wise)")
        
        # Group PO items by category
        po_categories = {}
        for i, (product, qty, price) in enumerate(zip(st.session_state.po_products, st.session_state.po_quantities, st.session_state.po_prices)):
            category = stock_manager.product_categories.get(product, "Uncategorized")
            if category not in po_categories:
                po_categories[category] = []
            po_categories[category].append({
                'product': product,
                'quantity': qty,
                'price': price,
                'index': i
            })
        
        total_amount = 0
        
        # Display by category
        for category, items in po_categories.items():
            with st.expander(f"{category} ({len(items)} items)"):
                for item in items:
                    total = item['price'] * item['quantity']
                    total_amount += total
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
                    with col1:
                        st.write(f"**{item['product']}**")
                    with col2:
                        st.write(f"**Qty:** {item['quantity']}")
                    with col3:
                        # Editable price field
                        new_price = st.number_input(f"Price", value=float(item['price']), min_value=0.0, step=0.1, key=f"price_{item['index']}")
                        if new_price != item['price']:
                            st.session_state.po_prices[item['index']] = new_price
                            st.rerun()
                    with col4:
                        item_total = st.session_state.po_prices[item['index']] * item['quantity']
                        st.write(f"**Total:** RM{item_total:.2f}")
                    with col5:
                        st.write("")  # Spacer
                    with col6:
                        if st.button("❌ Remove", key=f"remove_{item['index']}"):
                            st.session_state.po_products.pop(item['index'])
                            st.session_state.po_quantities.pop(item['index'])
                            st.session_state.po_prices.pop(item['index'])
                            st.rerun()
        
        st.markdown(f"**Grand Total: RM{total_amount:.2f}**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📄 Generate PO Document", type="primary", use_container_width=True):
                generate_po_document(stock_manager, st.session_state.po_products, 
                                   st.session_state.po_quantities, st.session_state.po_prices, 
                                   supplier, delivery_date, company_name, delivery_address)
        with col2:
            if st.button("💾 Save PO", use_container_width=True):
                po_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                po_data = {
                    'po_number': po_number,
                    'timestamp': datetime.now().isoformat(),
                    'supplier': supplier,
                    'delivery_date': delivery_date.isoformat(),
                    'company_name': company_name,
                    'delivery_address': delivery_address,
                    'items': [
                        {
                            'product': product,
                            'quantity': qty,
                            'price': price,
                            'total': price * qty
                        }
                        for product, qty, price in zip(st.session_state.po_products, st.session_state.po_quantities, st.session_state.po_prices)
                    ],
                    'total_amount': total_amount,
                    'created_by': st.session_state.user
                }
                if stock_manager.save_po(po_data):
                    st.success(f"✅ PO {po_number} saved successfully!")
        with col3:
            if st.button("🖨️ Print PO", use_container_width=True):
                st.info("PO ready for printing - Use browser print function (Ctrl+P)")
        with col4:
            if st.button("🗑️ Clear PO", use_container_width=True):
                st.session_state.po_products = []
                st.session_state.po_quantities = []
                st.session_state.po_prices = []
                st.rerun()
    else:
        st.info("No products added to purchase order yet.")

def show_saved_pos(stock_manager):
    st.header("💾 Saved Purchase Orders")
    
    if not stock_manager.saved_pos:
        st.info("No saved purchase orders found.")
        return
    
    for po_number, po_data in sorted(stock_manager.saved_pos.items(), reverse=True):
        with st.expander(f"📋 {po_number} - {po_data['timestamp'][:10]} - RM{po_data['total_amount']:.2f}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Supplier:** {po_data['supplier']}")
                st.write(f"**Delivery Date:** {po_data['delivery_date'][:10]}")
                st.write(f"**Created by:** {po_data['created_by']}")
            with col2:
                st.write(f"**Company:** {po_data['company_name']}")
                st.write(f"**Total Amount:** RM{po_data['total_amount']:.2f}")
                st.write(f"**Items:** {len(po_data['items'])}")
            
            st.subheader("PO Items")
            
            # Group items by category
            categories = {}
            for item in po_data['items']:
                category = stock_manager.product_categories.get(item['product'], "Uncategorized")
                if category not in categories:
                    categories[category] = []
                categories[category].append(item)
            
            for category, items in categories.items():
                with st.expander(f"{category} ({len(items)} items)"):
                    for item in items:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        with col1:
                            st.write(item['product'])
                        with col2:
                            st.write(f"Qty: {item['quantity']}")
                        with col3:
                            st.write(f"Price: RM{item['price']:.2f}")
                        with col4:
                            st.write(f"Total: RM{item['total']:.2f}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📄 View/Print {po_number}", key=f"view_{po_number}"):
                    # Regenerate the PO document
                    products = [item['product'] for item in po_data['items']]
                    quantities = [item['quantity'] for item in po_data['items']]
                    prices = [item['price'] for item in po_data['items']]
                    
                    generate_po_document(
                        stock_manager, products, quantities, prices,
                        po_data['supplier'], 
                        datetime.fromisoformat(po_data['delivery_date']),
                        po_data['company_name'],
                        po_data['delivery_address'],
                        po_data['po_number']
                    )
            with col2:
                if st.button(f"📥 Download {po_number}", key=f"download_{po_number}"):
                    # Create download link
                    products = [item['product'] for item in po_data['items']]
                    quantities = [item['quantity'] for item in po_data['items']]
                    prices = [item['price'] for item in po_data['items']]
                    
                    generate_po_download(
                        stock_manager, products, quantities, prices,
                        po_data['supplier'], 
                        datetime.fromisoformat(po_data['delivery_date']),
                        po_data['company_name'],
                        po_data['delivery_address'],
                        po_data['po_number']
                    )
            with col3:
                if st.button(f"🗑️ Delete {po_number}", key=f"delete_{po_number}"):
                    if st.session_state.users[st.session_state.user]['role'] == 'admin':
                        del stock_manager.saved_pos[po_number]
                        stock_manager.save_all_data()
                        st.success(f"PO {po_number} deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Only admin users can delete POs")

def generate_po_document(stock_manager, products, quantities, prices, supplier, delivery_date, company_name, delivery_address, po_number=None):
    if po_number is None:
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
    <!DOCTYPE html>
    <html>
    <head>
        <title>Purchase Order - {po_number}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                color: #333;
            }}
            .header {{
                text-align: center;
                color: #2E86AB;
                border-bottom: 2px solid #2E86AB;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #2E86AB;
                color: white;
            }}
            .total-row {{
                background-color: #f8f9fa;
                font-weight: bold;
                font-size: 1.1em;
            }}
            .signature-section {{
                margin-top: 40px;
                border-top: 2px solid #2E86AB;
                padding-top: 20px;
            }}
            .signature-box {{
                float: left;
                width: 45%;
            }}
            .clear {{
                clear: both;
            }}
            @media print {{
                body {{
                    margin: 0;
                    padding: 20px;
                }}
                .no-print {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>PURCHASE ORDER</h1>
        </div>
        
        <table>
            <tr>
                <td><strong>PO Number:</strong> {po_number}</td>
                <td><strong>Date:</strong> {timestamp}</td>
            </tr>
            <tr>
                <td><strong>Supplier:</strong> {supplier}</td>
                <td><strong>Delivery Date:</strong> {delivery_date}</td>
            </tr>
            <tr>
                <td colspan="2"><strong>Company:</strong> {company_name}</td>
            </tr>
            <tr>
                <td colspan="2"><strong>Delivery Address:</strong> {delivery_address}</td>
            </tr>
        </table>
        
        <table>
            <tr>
                <th>Item No.</th>
                <th>Product Description</th>
                <th style="text-align: center;">Quantity</th>
                <th style="text-align: right;">Unit Price (RM)</th>
                <th style="text-align: right;">Total (RM)</th>
            </tr>
    """
    
    for item in po_data:
        po_html += f"""
            <tr>
                <td>{item[0]}</td>
                <td>{item[1]}</td>
                <td style="text-align: center;">{item[2]}</td>
                <td style="text-align: right;">{item[3]}</td>
                <td style="text-align: right;">{item[4]}</td>
            </tr>
        """
    
    po_html += f"""
            <tr class="total-row">
                <td colspan="4" style="text-align: right;">GRAND TOTAL</td>
                <td style="text-align: right;">RM{total_amount:.2f}</td>
            </tr>
        </table>
        
        <div class="signature-section">
            <div class="signature-box">
                <p><strong>Prepared By:</strong></p>
                <p>_________________________</p>
                <p>Name: {st.session_state.user}</p>
                <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
            </div>
            <div class="signature-box" style="float: right;">
                <p><strong>Authorized Signature:</strong></p>
                <p>_________________________</p>
                <p>Name: ___________________</p>
                <p>Date: ___________________</p>
            </div>
            <div class="clear"></div>
        </div>
        
        <div class="no-print" style="margin-top: 20px; text-align: center;">
            <button onclick="window.print()" style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">🖨️ Print Purchase Order</button>
        </div>
        
        <script>
            function printPO() {{
                window.print();
            }}
        </script>
    </body>
    </html>
    """
    
    # Display the PO
    st.components.v1.html(po_html, height=800, scrolling=True)
    
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
        # Download as HTML (for printing)
        html_b64 = base64.b64encode(po_html.encode()).decode()
        href_html = f'<a href="data:text/html;base64,{html_b64}" download="{po_number}.html" style="background-color: #008CBA; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">📄 Download as HTML</a>'
        st.markdown(href_html, unsafe_allow_html=True)

def generate_po_download(stock_manager, products, quantities, prices, supplier, delivery_date, company_name, delivery_address, po_number):
    """Generate PO for download without displaying"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    po_data = []
    total_amount = 0
    
    for i, (product, qty, price) in enumerate(zip(products, quantities, prices)):
        total = price * qty
        total_amount += total
        po_data.append([i + 1, product, qty, f"RM{price:.2f}", f"RM{total:.2f}"])
    
    # Create a printable PO document
    po_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Purchase Order - {po_number}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                color: #333;
            }}
            .header {{
                text-align: center;
                color: #2E86AB;
                border-bottom: 2px solid #2E86AB;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #2E86AB;
                color: white;
            }}
            .total-row {{
                background-color: #f8f9fa;
                font-weight: bold;
                font-size: 1.1em;
            }}
            .signature-section {{
                margin-top: 40px;
                border-top: 2px solid #2E86AB;
                padding-top: 20px;
            }}
            .signature-box {{
                float: left;
                width: 45%;
            }}
            .clear {{
                clear: both;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>PURCHASE ORDER</h1>
        </div>
        
        <table>
            <tr>
                <td><strong>PO Number:</strong> {po_number}</td>
                <td><strong>Date:</strong> {timestamp}</td>
            </tr>
            <tr>
                <td><strong>Supplier:</strong> {supplier}</td>
                <td><strong>Delivery Date:</strong> {delivery_date}</td>
            </tr>
            <tr>
                <td colspan="2"><strong>Company:</strong> {company_name}</td>
            </tr>
            <tr>
                <td colspan="2"><strong>Delivery Address:</strong> {delivery_address}</td>
            </tr>
        </table>
        
        <table>
            <tr>
                <th>Item No.</th>
                <th>Product Description</th>
                <th style="text-align: center;">Quantity</th>
                <th style="text-align: right;">Unit Price (RM)</th>
                <th style="text-align: right;">Total (RM)</th>
            </tr>
    """
    
    for item in po_data:
        po_html += f"""
            <tr>
                <td>{item[0]}</td>
                <td>{item[1]}</td>
                <td style="text-align: center;">{item[2]}</td>
                <td style="text-align: right;">{item[3]}</td>
                <td style="text-align: right;">{item[4]}</td>
            </tr>
        """
    
    po_html += f"""
            <tr class="total-row">
                <td colspan="4" style="text-align: right;">GRAND TOTAL</td>
                <td style="text-align: right;">RM{total_amount:.2f}</td>
            </tr>
        </table>
        
        <div class="signature-section">
            <div class="signature-box">
                <p><strong>Prepared By:</strong></p>
                <p>_________________________</p>
                <p>Name: {st.session_state.user}</p>
                <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
            </div>
            <div class="signature-box" style="float: right;">
                <p><strong>Authorized Signature:</strong></p>
                <p>_________________________</p>
                <p>Name: ___________________</p>
                <p>Date: ___________________</p>
            </div>
            <div class="clear"></div>
        </div>
    </body>
    </html>
    """
    
    # Create download link
    html_b64 = base64.b64encode(po_html.encode()).decode()
    href = f'<a href="data:text/html;base64,{html_b64}" download="{po_number}.html" style="background-color: #008CBA; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; margin: 10px;">📄 Download {po_number} as HTML</a>'
    st.markdown(href, unsafe_allow_html=True)

# [The rest of the functions remain the same - auto_fix_products, update_all_prices, add_products_stores, 
# show_dashboard, check_stock, find_locations, store_inventory, all_products, edit_merge_products, manage_prices]

def auto_fix_products(stock_manager):
    """Automatically fix product names and merges"""
    # Check if user is admin
    if st.session_state.users[st.session_state.user]['role'] != 'admin':
        st.error("Only admin users can run auto-fix")
        return
    
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
    # Check if user is admin
    if st.session_state.users[st.session_state.user]['role'] != 'admin':
        st.error("Only admin users can update all prices")
        return
    
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
        'PRAN SWEETENED CREAMER 500GM EASY OPEN': 2.92,
        'PRAN CHOCO STICK': 0.70,
        'PRAN SWEETENED CREAMER 500GM': 2.75,
        'BOMBAY BRIYANI MASALA': 2.92,
        'PRAN POTATA BISCUITS 100GM': 1.60,
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

# [The rest of the functions remain the same but with admin checks added where appropriate]

if __name__ == "__main__":
    main()
