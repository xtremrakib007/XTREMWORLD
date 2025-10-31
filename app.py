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
import csv

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
    .low-stock {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.2rem 0;
        font-size: 0.8rem;
    }
    .out-of-stock {
        background-color: #f8d7da;
        border: 1px solid #dc3545;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.2rem 0;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

class AddressManager:
    """Manages store addresses"""
    
    @staticmethod
    def get_predefined_addresses():
        """Return predefined store addresses"""
        return {
            'TANJONG RAMBUTAN': "NO21,21A,23,25,27,LORONG SUNGAI CHOH 10,TANJONG PERDANA, 31250 TANJONG RAMBUTAN,PERAK",
            'PERPADUAN': "PT 241350, JALAN PERSIARAN PERPADUAN UTARA 2, 31150 ULU KINTA ,PERAK ,MALAYSIA",
            'AMPANG': "40-48,PERSIARAN HALAMAN AMPANG 2,HALAMAN AMPANG INDAH,31350 IPOH,PERAK",
            'BATU GAJAH': "LOT 492,JALAN PANDAK AKHAT,31000 BATU GAJAH,PERAK ,MALAYSIA",
            'PENGKALAN': "1,PERSIARAN PENGKALAN PERTAMA 1,TAMAN PENGKALAN PERTAMA,31650 IPOH,PERAK",
            'STATION 18': "NO.1 (GF),1(A) & 3(GF),JALAN PENGKALAN 1,PUSAT PERNIAGAAN PENGKALAN ,31650 IPOH,PERAK",
            'TELUK INTAN': "LOT 2522,2523,2526,2527, TAMAN MALAYSIA ,36000 TELUK INTAN ,PERAK ,MALAYSIA",
            'KUALA KANGSAR 1': "NO 4-10 PERSIARAN CHANDAN INDAH 1,TAMAN PANDAN INDAH, 33000 KUALA KANGSAR PERAK",
            'KUALA KANGSAR 2': "NO 8, PERSIARAN MEDAN SURIA ,TAMAN SURIA ,33000 KUALA KANGSAR,PERAK",
            'KAMUNTING': "LOT 34482, JALAN PERUSAHAAN 3, KAMUNTING INDUSTRIAL STATE 34600 KAMUNTING PERAK",
            'SIMPANG': "LOT 5821,JALAN SIMPANG ,TAMAN SIMPANG MAKMUR ,34700 SIMPANG ,PERAK"
        }

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
                        'admin': {
                            'password': UserManager.hash_password('admin123'),
                            'role': 'admin',
                            'approved': True,
                            'created_at': datetime.now().isoformat()
                        }
                    }
                    UserManager.save_users()
            except Exception as e:
                st.error(f"Error loading users: {e}")
                # Create default admin user as fallback
                st.session_state.users = {
                    'admin': {
                        'password': UserManager.hash_password('admin123'),
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
        except Exception as e:
            st.error(f"Error saving users: {e}")
    
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
        # Initialize user session state if not exists
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'login_time' not in st.session_state:
            st.session_state.login_time = None
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
        if 'admin_panel' not in st.session_state:
            st.session_state.admin_panel = False
            
        # Initialize data if not exists
        if 'store_data' not in st.session_state:
            st.session_state.store_data = DataManager.load_store_data()
        if 'product_prices' not in st.session_state:
            st.session_state.product_prices = DataManager.load_prices()
        if 'product_barcodes' not in st.session_state:
            st.session_state.product_barcodes = DataManager.load_barcodes()
        if 'product_suppliers' not in st.session_state:
            st.session_state.product_suppliers = DataManager.load_suppliers()
        if 'product_categories' not in st.session_state:
            st.session_state.product_categories = DataManager.load_categories()
        if 'product_stock' not in st.session_state:
            st.session_state.product_stock = DataManager.load_stock()
        if 'po_products' not in st.session_state:
            st.session_state.po_products = []
        if 'po_quantities' not in st.session_state:
            st.session_state.po_quantities = []
        if 'po_prices' not in st.session_state:
            st.session_state.po_prices = []
        if 'po_discounts' not in st.session_state:
            st.session_state.po_discounts = []
        if 'po_foc_quantities' not in st.session_state:
            st.session_state.po_foc_quantities = []
        if 'saved_pos' not in st.session_state:
            st.session_state.saved_pos = DataManager.load_saved_pos()
        if 'pending_changes' not in st.session_state:
            st.session_state.pending_changes = DataManager.load_pending_changes()
        if 'store_addresses' not in st.session_state:
            st.session_state.store_addresses = DataManager.load_store_addresses()
    
    @staticmethod
    def load_store_data():
        """Load store data from file or use sample data"""
        try:
            if os.path.exists('store_data.json'):
                with open('store_data.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading store data: {e}")
        return DataManager.sample_store_data()
    
    @staticmethod
    def load_prices():
        """Load product prices from file"""
        try:
            if os.path.exists('product_prices.json'):
                with open('product_prices.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading prices: {e}")
        return {}
    
    @staticmethod
    def load_barcodes():
        """Load product barcodes from file"""
        try:
            if os.path.exists('product_barcodes.json'):
                with open('product_barcodes.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading barcodes: {e}")
        return {}
    
    @staticmethod
    def load_suppliers():
        """Load product suppliers from file"""
        try:
            if os.path.exists('product_suppliers.json'):
                with open('product_suppliers.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading suppliers: {e}")
        return {}
    
    @staticmethod
    def load_categories():
        """Load product categories from file"""
        try:
            if os.path.exists('product_categories.json'):
                with open('product_categories.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading categories: {e}")
        return {}
    
    @staticmethod
    def load_stock():
        """Load product stock quantities"""
        try:
            if os.path.exists('product_stock.json'):
                with open('product_stock.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading stock: {e}")
        return {}
    
    @staticmethod
    def load_saved_pos():
        """Load saved purchase orders"""
        try:
            if os.path.exists('saved_pos.json'):
                with open('saved_pos.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading saved POs: {e}")
        return {}
    
    @staticmethod
    def load_pending_changes():
        """Load pending changes waiting for admin approval"""
        try:
            if os.path.exists('pending_changes.json'):
                with open('pending_changes.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading pending changes: {e}")
        return []
    
    @staticmethod
    def load_store_addresses():
        """Load store addresses from file"""
        try:
            if os.path.exists('store_addresses.json'):
                with open('store_addresses.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading store addresses: {e}")
        return AddressManager.get_predefined_addresses()
    
    @staticmethod
    def save_store_data(data):
        """Save store data to file"""
        try:
            with open('store_data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving store data: {e}")
    
    @staticmethod
    def save_prices(data):
        """Save product prices to file"""
        try:
            with open('product_prices.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving prices: {e}")
    
    @staticmethod
    def save_barcodes(data):
        """Save product barcodes to file"""
        try:
            with open('product_barcodes.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving barcodes: {e}")
    
    @staticmethod
    def save_suppliers(data):
        """Save product suppliers to file"""
        try:
            with open('product_suppliers.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving suppliers: {e}")
    
    @staticmethod
    def save_categories(data):
        """Save product categories to file"""
        try:
            with open('product_categories.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving categories: {e}")
    
    @staticmethod
    def save_stock(data):
        """Save product stock to file"""
        try:
            with open('product_stock.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving stock: {e}")
    
    @staticmethod
    def save_pos(data):
        """Save purchase orders to file"""
        try:
            with open('saved_pos.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving POs: {e}")
    
    @staticmethod
    def save_pending_changes(data):
        """Save pending changes to file"""
        try:
            with open('pending_changes.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving pending changes: {e}")
    
    @staticmethod
    def save_store_addresses(data):
        """Save store addresses to file"""
        try:
            with open('store_addresses.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving store addresses: {e}")
    
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
        self.product_stock = st.session_state.product_stock
        self.saved_pos = st.session_state.saved_pos
        self.pending_changes = st.session_state.pending_changes
        self.store_addresses = st.session_state.store_addresses
        
        # Initialize default prices and stock for products that don't have them
        self.initialize_default_prices()
        self.initialize_default_stock()
    
    def initialize_default_prices(self):
        """Initialize default prices for products that don't have prices"""
        changed = False
        for product in self.all_products:
            if product not in self.product_prices:
                self.product_prices[product] = self.estimate_price(product)
                changed = True
        
        if changed:
            self.save_all_data()
    
    def initialize_default_stock(self):
        """Initialize default stock quantities for products"""
        changed = False
        for product in self.all_products:
            if product not in self.product_stock:
                # Initialize with random stock between 10-50
                self.product_stock[product] = np.random.randint(10, 51)
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
        st.session_state.product_stock = self.product_stock
        st.session_state.saved_pos = self.saved_pos
        st.session_state.pending_changes = self.pending_changes
        st.session_state.store_addresses = self.store_addresses
        
        # Save to files
        DataManager.save_store_data(self.data)
        DataManager.save_prices(self.product_prices)
        DataManager.save_barcodes(self.product_barcodes)
        DataManager.save_suppliers(self.product_suppliers)
        DataManager.save_categories(self.product_categories)
        DataManager.save_stock(self.product_stock)
        DataManager.save_pos(self.saved_pos)
        DataManager.save_pending_changes(self.pending_changes)
        DataManager.save_store_addresses(self.store_addresses)
    
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
    
    def get_stock_quantity(self, product_name):
        """Get current stock quantity for a product"""
        return self.product_stock.get(product_name, 0)
    
    def update_stock(self, product_name, new_quantity):
        """Update stock quantity for a product"""
        self.product_stock[product_name] = new_quantity
        self.save_all_data()
        return True
    
    def get_stock_status(self, product_name):
        """Get stock status with color coding"""
        quantity = self.get_stock_quantity(product_name)
        if quantity == 0:
            return "Out of Stock", "out-of-stock"
        elif quantity <= 10:
            return f"Low Stock ({quantity})", "low-stock"
        else:
            return f"In Stock ({quantity})", "stock-info"
    
    def estimate_price(self, product_name):
        """Updated price estimation with new prices per piece"""
        price_mapping = {
            'BARBICAN': 4.38,  # 4.375 rounded
            'BASIL SEED': 2.42,  # 2.41666667 rounded
            'BES MINUMAN': 2.00,
            'HUMPTY DUMPTY': 2.00,
            'POWER ENERGY DRINK': 1.42,  # 1.416667 rounded
            'VEGETABLE GHEE 450G': 10.63,  # 10.625 rounded
            'VEGETABLE GHEE 125G': 4.13,  # 4.125 rounded
            'COCONUT WATER': 1.67,  # 1.666666 rounded
            'AIS LEMON TEH': 1.63,  # 1.625 rounded
            'PREMIO PARADISE': 3.11,
            'CHANACHUR': 3.13,  # 3.125 rounded
            'JUS PET 1000ML': 3.75,
            'JUS 330ML': 1.50,
            'PET 320ML': 1.50,
            'DRINKO FLOAT 250ML': 1.50,
            'DRINKO FLOAT 330ML': 2.00,
            'LASSI 285ML': 1.69,  # 1.6944444 rounded
            'SOYA CAN': 1.00,
            'COOLING TAMARIND': 1.38,  # 1.375 rounded
            'JUS PET VALUE PACK 1.5L': 11.00,
            'MUSTARD OIL 400ML': 5.83,  # 5.833333 rounded
            'MUSTARD OIL 200ML': 3.00,
            'VARIETY LOLLIPOP': 30.00,
            'PUFFED RICE': 2.75,
            'CREAMER 500GM': 2.75,  # New price
            'CREAMER 500GM EASY OPEN': 2.92,  # 2.916666 rounded
            'CHOCO STICK': 0.70,  # New price
            'BOMBAY BRIYANI': 2.92,  # 2.916666 rounded
            'POTATA BISCUITS': 1.60  # 1.6041666 rounded
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
            'Puffed Rice': 2.75,
            'Creamer': 2.75,
            'Biscuits': 1.60,
            'Spices': 2.92
        }
        
        category = self.get_product_category(product_name)
        return category_prices.get(category, 3.00)
    
    def add_product(self, product_name, stores, price=None, barcode=None, supplier="PINNACLE FOODS (M) SDN BHD", category=None, initial_stock=0):
        """Add new product to specified stores"""
        # Check if user is admin
        if st.session_state.user not in st.session_state.users or st.session_state.users[st.session_state.user]['role'] != 'admin':
            # Add to pending changes for admin approval
            change_request = {
                'type': 'add_product',
                'product_name': product_name,
                'stores': stores,
                'price': price,
                'barcode': barcode,
                'supplier': supplier,
                'category': category,
                'initial_stock': initial_stock,
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
        
        # Set initial stock
        self.product_stock[product_name] = initial_stock
        
        # Save all changes
        self.save_all_data()
        return True, f"Product '{product_name}' added successfully!"
    
    def add_store(self, store_name, initial_products=None):
        """Add new store with optional initial products"""
        # Check if user is admin
        if st.session_state.user not in st.session_state.users or st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can add stores"
        
        if store_name not in self.data:
            if initial_products is None:
                initial_products = []
            self.data[store_name] = initial_products
            self.save_all_data()
            return True, f"Store '{store_name}' added successfully!"
        return False, "Store already exists"
    
    def add_products_to_store(self, store_name, products):
        """Add multiple products to a specific store"""
        # Check if user is admin
        if st.session_state.user not in st.session_state.users or st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can add products to stores"
        
        if store_name in self.data:
            for product in products:
                if product not in self.data[store_name]:
                    self.data[store_name].append(product)
            self.save_all_data()
            return True, f"Added {len(products)} products to {store_name}"
        return False, "Store not found"
    
    def delete_product(self, product_name):
        """Delete a product from all stores and product lists"""
        # Check if user is admin
        if st.session_state.user not in st.session_state.users or st.session_state.users[st.session_state.user]['role'] != 'admin':
            return False, "Only admin users can delete products"
        
        # Remove from all stores
        for store in self.data:
            if product_name in self.data[store]:
                self.data[store].remove(product_name)
        
        # Remove from product lists
        if product_name in self.all_products:
            self.all_products.remove(product_name)
        
        # Remove from prices, barcodes, suppliers, and stock
        if product_name in self.product_prices:
            del self.product_prices[product_name]
        if product_name in self.product_barcodes:
            del self.product_barcodes[product_name]
        if product_name in self.product_suppliers:
            del self.product_suppliers[product_name]
        if product_name in self.product_categories:
            del self.product_categories[product_name]
        if product_name in self.product_stock:
            del self.product_stock[product_name]
        
        # Save all changes
        self.save_all_data()
        
        return True, f"Product '{product_name}' deleted successfully"
    
    def merge_products(self, product_to_keep, product_to_remove):
        """Merge two products - keep one and remove the other"""
        # Check if user is admin
        if st.session_state.user not in st.session_state.users or st.session_state.users[st.session_state.user]['role'] != 'admin':
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
        
        # Update prices, barcodes, suppliers, stock
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
            
        if product_to_remove in self.product_stock:
            if product_to_keep not in self.product_stock:
                self.product_stock[product_to_keep] = self.product_stock[product_to_remove]
            del self.product_stock[product_to_remove]
        
        # Save all changes
        self.save_all_data()
            
        return True, f"Successfully merged {product_to_remove} into {product_to_keep}"
    
    def update_product(self, old_name, new_name, price, barcode, supplier, stores, category, stock_quantity):
        """Update product details"""
        # Check if user is admin
        if st.session_state.user not in st.session_state.users or st.session_state.users[st.session_state.user]['role'] != 'admin':
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
            if old_name in self.product_stock:
                self.product_stock[new_name] = self.product_stock.pop(old_name)
        
        # Update product details
        self.product_prices[new_name] = price
        self.product_barcodes[new_name] = barcode
        self.product_suppliers[new_name] = supplier
        self.product_categories[new_name] = category
        self.product_stock[new_name] = stock_quantity
        
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
    
    def get_address_options(self):
        """Get formatted address options for dropdown"""
        options = []
        for store_name, address in self.store_addresses.items():
            options.append(f"{store_name}: {address}")
        return options

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
    
    tab1, tab2, tab3, tab4 = st.tabs(["Pending Approvals", "User Management", "Pending Changes", "Store Addresses"])
    
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
                if username != 'admin':  # Don't allow deleting main admin
                    if st.button(f"Make Admin", key=f"admin_{username}"):
                        st.session_state.users[username]['role'] = 'admin'
                        UserManager.save_users()
                        st.success(f"{username} is now an admin")
                        time.sleep(1)
                        st.rerun()
            with col3:
                if username != 'admin' and not user_data['approved']:
                    if st.button(f"Approve", key=f"app_{username}"):
                        success, message = UserManager.approve_user(username)
                        if success:
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
            with col4:
                if username != 'admin':  # Don't allow deleting main admin
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
                    st.write(f"Initial Stock: {change['initial_stock']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve Change", key=f"approve_change_{i}"):
                        # Apply the change
                        if change['type'] == 'add_product':
                            # Admin can directly add the product
                            if change['product_name'] not in stock_manager.all_products:
                                stock_manager.all_products.append(change['product_name'])
                                stock_manager.all_products.sort()
                            
                            for store in change['stores']:
                                if store in stock_manager.data:
                                    if change['product_name'] not in stock_manager.data[store]:
                                        stock_manager.data[store].append(change['product_name'])
                            
                            # Set price
                            stock_manager.product_prices[change['product_name']] = change['price']
                            
                            if change.get('barcode'):
                                stock_manager.product_barcodes[change['product_name']] = change['barcode']
                                
                            stock_manager.product_suppliers[change['product_name']] = change['supplier']
                            stock_manager.product_categories[change['product_name']] = change['category']
                            stock_manager.product_stock[change['product_name']] = change['initial_stock']
                            
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
    
    with tab4:
        st.subheader("Manage Store Addresses")
        stock_manager = StockManager()
        
        st.info("Edit store addresses below. Changes will be reflected in PO delivery address options.")
        
        for store_name, address in stock_manager.store_addresses.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**{store_name}**")
            with col2:
                new_address = st.text_area(f"Address for {store_name}", value=address, key=f"addr_{store_name}")
                if new_address != address:
                    stock_manager.store_addresses[store_name] = new_address
                    stock_manager.save_all_data()
                    st.success(f"✅ Address updated for {store_name}")
        
        # Add new store address
        st.subheader("Add New Store Address")
        col1, col2 = st.columns(2)
        with col1:
            new_store_name = st.text_input("Store Name")
        with col2:
            new_store_address = st.text_area("Store Address")
        
        if st.button("Add Store Address"):
            if new_store_name and new_store_address:
                if new_store_name not in stock_manager.store_addresses:
                    stock_manager.store_addresses[new_store_name] = new_store_address
                    stock_manager.save_all_data()
                    st.success(f"✅ Address added for {new_store_name}")
                else:
                    st.error("Store name already exists")
            else:
                st.error("Please enter both store name and address")

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
            'Mustard Oil',
            stock_manager.product_stock.get('MUSTARD OIL 200ML', 0)
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
    """Update all prices to the new specified prices per piece"""
    # Check if user is admin
    if st.session_state.users[st.session_state.user]['role'] != 'admin':
        st.error("Only admin users can update all prices")
        return
    
    st.info("💰 Updating all product prices to new per piece prices...")
    
    # Define the new prices per piece (rounded to 2 decimal places)
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
        
        # Creamer
        'PRAN CREAMER 500GM': 2.75,
        'PRAN CREAMER 500GM EASY OPEN': 2.92,
        
        # Choco Stick
        'PRAN CHOCO STICK': 0.70,
        
        # Bombay Briyani
        'BOMBAY BRIYANI MASALA': 2.92,
        
        # Potata Biscuits
        'PRAN POTATA BISCUITS 100GM': 1.60,
        
        # Other products
        'PRAN SWEETENED CREAMER 500GM': 5.00,
    }
    
    updated_count = 0
    for product in stock_manager.all_products:
        for key, price in new_prices.items():
            if key in product.upper():
                stock_manager.product_prices[product] = price
                updated_count += 1
                break
    
    stock_manager.save_all_data()
    st.success(f"✅ Updated prices for {updated_count} products to new per piece prices!")
    st.rerun()

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
        
        # Show stock quantity and status
        stock_status, status_class = stock_manager.get_stock_status(product_name)
        st.markdown(f'<div class="{status_class}"><strong>Stock Status:</strong> {stock_status}</div>', unsafe_allow_html=True)
        
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
        
        # Show stock quantity and status
        stock_status, status_class = stock_manager.get_stock_status(product_name)
        st.markdown(f'<div class="{status_class}"><strong>Stock Status:</strong> {stock_status}</div>', unsafe_allow_html=True)
        
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
                            stock_status, status_class = stock_manager.get_stock_status(product)
                            
                            st.markdown(f'''
                            <div class="{product_class}">
                                <strong>{product}</strong><br>
                                <small>Price: RM{price:.2f} | Supplier: {supplier}</small><br>
                                <small>Barcode: {barcode}</small><br>
                                <div class="{status_class}"><small>{stock_status}</small></div>
                            </div>
                            ''', unsafe_allow_html=True)

def all_products(stock_manager):
    st.header("📦 All Products")
    st.write(f"**Total Unique Products:** {len(stock_manager.all_products)}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Search products...")
    with col2:
        # Get all unique categories
        all_categories = sorted(list(set(stock_manager.product_categories.values())))
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
            if category_filter != "All Categories" and category != category_filter:
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
    
    for category, products in sorted(products_by_category.items()):
        with st.expander(f"{category} ({len(products)} products)"):
            cols = st.columns(2)
            for i, product in enumerate(products):
                with cols[i % 2]:
                    store_count = len(stock_manager.find_product_locations(product))
                    price = stock_manager.product_prices.get(product, stock_manager.estimate_price(product))
                    barcode = stock_manager.product_barcodes.get(product, "No barcode")
                    supplier = stock_manager.product_suppliers.get(product, "PINNACLE FOODS (M) SDN BHD")
                    stock_status, status_class = stock_manager.get_stock_status(product)
                    
                    st.markdown(f'''
                    <div class="{product_class}">
                        <strong>{product}</strong><br>
                        <small>Stores: {store_count} | Price: RM{price:.2f}</small><br>
                        <small>Supplier: {supplier}</small><br>
                        <small>Barcode: {barcode}</small><br>
                        <div class="{status_class}"><small>{stock_status}</small></div>
                    </div>
                    ''', unsafe_allow_html=True)

def add_products_stores(stock_manager):
    st.header("➕ Add Products & Stores")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add Product", "Add Store", "Add Products to Store", "Manage Barcodes", "Manage Stock"])
    
    with tab1:
        st.subheader("Add New Product")
        
        col1, col2 = st.columns(2)
        with col1:
            new_product_name = st.text_input("Product Name")
            product_price = st.number_input("Price (RM)", min_value=0.0, value=3.0, step=0.1)
            initial_stock = st.number_input("Initial Stock Quantity", min_value=0, value=10, step=1)
        with col2:
            barcode = st.text_input("Barcode (Optional)")
            available_stores = st.multiselect("Available in Stores", list(stock_manager.data.keys()))
            supplier = st.selectbox("Supplier", ["PINNACLE FOODS (M) SDN BHD", "PRAN", "BARBICAN", "DRINKO", "OTHER"])
        
        # Category selection
        all_categories = sorted(list(set(stock_manager.product_categories.values())))
        category = st.selectbox("Category", all_categories + ["Auto-detect from name"])
        
        if st.button("Add Product"):
            if new_product_name and available_stores:
                final_category = None if category == "Auto-detect from name" else category
                success, message = stock_manager.add_product(new_product_name, available_stores, product_price, barcode, supplier, final_category, initial_stock)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.info(message)  # This will show the approval pending message for non-admin users
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
                success, message = stock_manager.add_store(new_store_name, initial_products)
                if success:
                    if initial_products:
                        st.success(f"✅ Store '{new_store_name}' added successfully with {len(initial_products)} products!")
                    else:
                        st.success(f"✅ Store '{new_store_name}' added successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
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
                success, message = stock_manager.add_products_to_store(selected_store, products_to_add)
                if success:
                    st.success(f"✅ Added {len(products_to_add)} products to {selected_store}!")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
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
    
    with tab5:
        st.subheader("Manage Product Stock")
        
        selected_product = st.selectbox("Select Product", stock_manager.all_products, key="stock_product")
        current_stock = stock_manager.get_stock_quantity(selected_product)
        stock_status, status_class = stock_manager.get_stock_status(selected_product)
        
        st.markdown(f'<div class="{status_class}"><strong>Current Stock Status:</strong> {stock_status}</div>', unsafe_allow_html=True)
        
        new_stock = st.number_input("Update Stock Quantity", min_value=0, value=current_stock, step=1)
        
        if st.button("Update Stock"):
            if selected_product:
                stock_manager.update_stock(selected_product, new_stock)
                st.success(f"✅ Stock updated for '{selected_product}' to {new_stock} units")
                st.rerun()

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
                current_stock = stock_manager.get_stock_quantity(product_to_edit)
                new_stock = st.number_input("Stock Quantity", min_value=0, value=current_stock, step=1)
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
            
            # Category selection
            all_categories = sorted(list(set(stock_manager.product_categories.values())))
            current_category = stock_manager.product_categories.get(product_to_edit, "Uncategorized")
            new_category = st.selectbox("Category", all_categories, index=all_categories.index(current_category) if current_category in all_categories else 0)
            
            current_stores = [store for store in stock_manager.data if product_to_edit in stock_manager.data[store]]
            new_stores = st.multiselect("Available in Stores", 
                                      list(stock_manager.data.keys()),
                                      default=current_stores)
            
            if st.button("Update Product"):
                if new_name:
                    success, message = stock_manager.update_product(
                        product_to_edit, new_name, new_price, new_barcode, new_supplier, new_stores, new_category, new_stock
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
            current_stock = stock_manager.get_stock_quantity(product_to_delete)
            store_count = len(stock_manager.find_product_locations(product_to_delete))
            
            st.write(f"**Product Details:**")
            st.write(f"- **Name:** {product_to_delete}")
            st.write(f"- **Category:** {current_category}")
            st.write(f"- **Price:** RM{current_price:.2f}")
            st.write(f"- **Stock:** {current_stock} units")
            st.write(f"- **Barcode:** {current_barcode}")
            st.write(f"- **Supplier:** {current_supplier}")
            st.write(f"- **Available in:** {store_count} stores")
            
            # Confirmation before deletion
            confirm_delete = st.checkbox("I understand this action cannot be undone")
            
            if st.button("🗑️ Delete Product", type="primary", disabled=not confirm_delete):
                success, message = stock_manager.delete_product(product_to_delete)
                if success:
                    st.success(f"✅ Product '{product_to_delete}' deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

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
        
        # Get all unique categories
        all_categories = sorted(list(set(stock_manager.product_categories.values())))
        
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
            category_products = [p for p in stock_manager.all_products if stock_manager.product_categories.get(p) == selected_category]
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
            stock_quantity = stock_manager.get_stock_quantity(product)
            price_data.append({
                'Product': product,
                'Category': category,
                'Stock': stock_quantity,
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

def generate_po_document(stock_manager, products, quantities, prices, discounts, foc_quantities, 
                        supplier, delivery_date, company_name, delivery_address, po_number=None):
    if po_number is None:
        po_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    po_data = []
    total_amount = 0
    total_discount = 0
    total_foc_value = 0
    
    for i, (product, qty, price, discount, foc_qty) in enumerate(zip(products, quantities, prices, discounts, foc_quantities)):
        net_qty = qty - foc_qty
        total = (net_qty * price) - discount
        total_amount += total
        total_discount += discount
        total_foc_value += foc_qty * price
        po_data.append([i + 1, product, qty, foc_qty, net_qty, f"RM{price:.2f}", f"RM{discount:.2f}", f"RM{total:.2f}"])
    
    st.success("✅ Purchase Order Generated Successfully!")
    
    # Create a more compact printable PO document
    po_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Purchase Order - {po_number}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 10px;
                color: #333;
                font-size: 12px;
                line-height: 1.2;
            }}
            .header {{
                text-align: center;
                color: #2E86AB;
                border-bottom: 1px solid #2E86AB;
                padding-bottom: 5px;
                margin-bottom: 10px;
            }}
            .header h1 {{
                font-size: 16px;
                margin: 5px 0;
            }}
            .header h2 {{
                font-size: 14px;
                margin: 3px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 8px 0;
                font-size: 11px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 4px;
                text-align: left;
            }}
            th {{
                background-color: #2E86AB;
                color: white;
                font-weight: bold;
                padding: 5px;
            }}
            .total-row {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            .summary-section {{
                margin-top: 10px;
                padding: 8px;
                background-color: #f8f9fa;
                border-radius: 3px;
                font-size: 11px;
            }}
            .signature-section {{
                margin-top: 15px;
                border-top: 1px solid #2E86AB;
                padding-top: 10px;
                font-size: 11px;
            }}
            .signature-box {{
                float: left;
                width: 45%;
                margin-bottom: 5px;
            }}
            .clear {{
                clear: both;
            }}
            .company-info {{
                font-size: 10px;
                margin-bottom: 8px;
            }}
            .contact-info {{
                font-size: 10px;
                margin: 5px 0;
                text-align: center;
            }}
            @media print {{
                body {{
                    margin: 5px;
                    padding: 5px;
                    font-size: 10px;
                }}
                .no-print {{
                    display: none;
                }}
                table {{
                    font-size: 9px;
                }}
                th, td {{
                    padding: 3px;
                }}
                .header h1 {{
                    font-size: 14px;
                }}
            }}
            .compact-table td, .compact-table th {{
                padding: 2px 3px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>PURCHASE ORDER</h1>
            <h2>TY PASAR RAYA JIMAT SDN BHD</h2>
            <div class="contact-info">
                <strong>Prepared by: MD RAKIBUL ISLAM | 0192699618</strong>
            </div>
        </div>
        
        <table class="compact-table">
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
        
        <table class="compact-table">
            <tr>
                <th style="width: 5%;">No.</th>
                <th style="width: 40%;">Product Description</th>
                <th style="width: 8%; text-align: center;">Qty</th>
                <th style="width: 8%; text-align: center;">FOC</th>
                <th style="width: 8%; text-align: center;">Net</th>
                <th style="width: 10%; text-align: right;">Price (RM)</th>
                <th style="width: 10%; text-align: right;">Disc (RM)</th>
                <th style="width: 11%; text-align: right;">Total (RM)</th>
            </tr>
    """
    
    for item in po_data:
        po_html += f"""
            <tr>
                <td>{item[0]}</td>
                <td style="font-size: 10px;">{item[1]}</td>
                <td style="text-align: center;">{item[2]}</td>
                <td style="text-align: center;">{item[3]}</td>
                <td style="text-align: center;">{item[4]}</td>
                <td style="text-align: right;">{item[5]}</td>
                <td style="text-align: right;">{item[6]}</td>
                <td style="text-align: right;">{item[7]}</td>
            </tr>
        """
    
    po_html += f"""
            <tr class="total-row">
                <td colspan="7" style="text-align: right;"><strong>GRAND TOTAL</strong></td>
                <td style="text-align: right;"><strong>RM{total_amount:.2f}</strong></td>
            </tr>
        </table>
        
        <div class="summary-section">
            <p><strong>Order Summary:</strong> {len(products)} items | Discount: RM{total_discount:.2f} | FOC Value: RM{total_foc_value:.2f} | <strong>Net Payable: RM{total_amount:.2f}</strong></p>
        </div>
        
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
        
        <div class="no-print" style="margin-top: 10px; text-align: center;">
            <button onclick="window.print()" style="background-color: #008CBA; color: white; padding: 6px 12px; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">🖨️ Print Purchase Order</button>
        </div>
        
        <script>
            function printPO() {{
                window.print();
            }}
            // Auto-print when page loads
            window.onload = function() {{
                setTimeout(function() {{
                    window.print();
                }}, 1000);
            }};
        </script>
    </body>
    </html>
    """
    
    # Display the PO
    st.components.v1.html(po_html, height=800, scrolling=True)

def generate_po(stock_manager):
    st.header("📋 Generate Purchase Order")
    
    col1, col2 = st.columns(2)
    with col1:
        supplier = st.selectbox("Supplier", ["PINNACLE FOODS (M) SDN BHD", "PRAN", "BARBICAN", "DRINKO", "OTHER SUPPLIER"])
        company_name = st.text_input("Company Name", "TY PASAR RAYA JIMAT SDN BHD")
    with col2:
        delivery_date = st.date_input("Requested Delivery Date")
        
        # Delivery Address Selection with store names
        address_options = ["Select Address"] + stock_manager.get_address_options() + ["Custom Address"]
        address_option = st.selectbox("Delivery Address", address_options)
        
        if address_option == "Select Address":
            delivery_address = ""
            st.info("Please select a delivery address")
        elif address_option == "Custom Address":
            delivery_address = st.text_area("Enter Custom Delivery Address", "Main Warehouse, Kuala Lumpur")
        else:
            # Extract just the address part (remove store name)
            delivery_address = address_option.split(": ", 1)[1]
            st.success("✅ Store address selected")
    
    # Store selection for outlet-wise products
    st.subheader("Select Store for Products")
    selected_store = st.selectbox("Select Store", list(stock_manager.data.keys()))
    
    if selected_store:
        # Get products available in the selected store
        store_products = stock_manager.data.get(selected_store, [])
        
        # Filter out products already in PO
        available_products = [p for p in store_products if p not in st.session_state.po_products]
        
        st.subheader("Add Products to PO")
        
        # Define all columns first
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            if available_products:
                new_product = st.selectbox("Select Product", available_products, key="po_product_select")
                
                if new_product:
                    # Show current stock information
                    stock_count = stock_manager.get_stock_count(new_product)
                    stock_locations = stock_manager.find_product_locations(new_product)
                    current_price = stock_manager.product_prices.get(new_product, stock_manager.estimate_price(new_product))
                    stock_status, status_class = stock_manager.get_stock_status(new_product)
                    
                    st.markdown(f'''
                    <div class="stock-info">
                        <strong>Current Stock:</strong> Available in {stock_count} stores<br>
                        <strong>Stock Quantity:</strong> <span class="{status_class}">{stock_status}</span><br>
                        <strong>Current Price:</strong> RM{current_price:.2f}<br>
                        <strong>Available at:</strong> {", ".join(stock_locations) if stock_locations else "No stores"}
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.info("No more products available to add from this store")
                new_product = None
            
        with col2:
            new_quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="po_quantity_input")
        
        with col3:
            # Auto-populate price from product database
            if new_product:
                default_price = stock_manager.product_prices.get(new_product, stock_manager.estimate_price(new_product))
                new_price = st.number_input("Unit Price (RM)", min_value=0.0, value=float(default_price), step=0.1, key="po_price_input")
            else:
                new_price = st.number_input("Unit Price (RM)", min_value=0.0, value=0.0, step=0.1, key="po_price_input", disabled=True)
        
        with col4:
            new_discount = st.number_input("Discount (RM)", min_value=0.0, value=0.0, step=0.1, key="po_discount_input")
        
        with col5:
            new_foc_qty = st.number_input("FOC Qty", min_value=0, value=0, step=1, key="po_foc_input")
            
            if st.button("Add to PO", use_container_width=True, key="add_po_button"):
                if new_product:
                    # Initialize session state arrays if they don't exist
                    if 'po_discounts' not in st.session_state:
                        st.session_state.po_discounts = []
                    if 'po_foc_quantities' not in st.session_state:
                        st.session_state.po_foc_quantities = []
                        
                    # Check if product already exists in PO
                    if new_product in st.session_state.po_products:
                        st.error(f"❌ {new_product} is already in the PO. Each product can only be added once.")
                    else:
                        st.session_state.po_products.append(new_product)
                        st.session_state.po_quantities.append(new_quantity)
                        st.session_state.po_prices.append(new_price)
                        st.session_state.po_discounts.append(new_discount)
                        st.session_state.po_foc_quantities.append(new_foc_qty)
                        st.success(f"✅ Added {new_product} to PO!")
                        st.rerun()
                else:
                    st.error("❌ Please select a product to add")
    
    if st.session_state.po_products:
        st.subheader("Current Purchase Order Items")
        
        total_amount = 0
        total_discount = 0
        total_foc_value = 0
        
        # Display PO items
        for i, (product, qty, price, discount, foc_qty) in enumerate(zip(
            st.session_state.po_products, 
            st.session_state.po_quantities, 
            st.session_state.po_prices,
            st.session_state.po_discounts,
            st.session_state.po_foc_quantities
        )):
            # Calculate net quantity (quantity - FOC)
            net_qty = qty - foc_qty
            # Calculate item total (net quantity * price - discount)
            item_total = (net_qty * price) - discount
            total_amount += item_total
            total_discount += discount
            total_foc_value += foc_qty * price
            
            # Define columns for each item
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([3, 1, 1, 1, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{product}**")
                # Show stock status for this product
                stock_status, status_class = stock_manager.get_stock_status(product)
                st.markdown(f'<div class="{status_class}"><small>{stock_status}</small></div>', unsafe_allow_html=True)
            with col2:
                st.write(f"**Qty:** {qty}")
            with col3:
                # Editable price field - auto-update when changed
                new_price = st.number_input(f"Price", value=float(price), min_value=0.0, step=0.1, key=f"price_{i}")
                if new_price != price:
                    st.session_state.po_prices[i] = new_price
                    st.rerun()
            with col4:
                # Editable discount field
                new_discount = st.number_input(f"Discount", value=float(discount), min_value=0.0, step=0.1, key=f"discount_{i}")
                if new_discount != discount:
                    st.session_state.po_discounts[i] = new_discount
                    st.rerun()
            with col5:
                # Editable FOC quantity field
                new_foc_qty = st.number_input(f"FOC Qty", value=foc_qty, min_value=0, step=1, key=f"foc_{i}")
                if new_foc_qty != foc_qty:
                    st.session_state.po_foc_quantities[i] = new_foc_qty
                    st.rerun()
            with col6:
                st.write(f"**Net:** {net_qty}")
            with col7:
                st.write(f"**Total:** RM{item_total:.2f}")
            with col8:
                if st.button("❌ Remove", key=f"remove_{i}"):
                    st.session_state.po_products.pop(i)
                    st.session_state.po_quantities.pop(i)
                    st.session_state.po_prices.pop(i)
                    st.session_state.po_discounts.pop(i)
                    st.session_state.po_foc_quantities.pop(i)
                    st.rerun()
        
        # Summary section
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", len(st.session_state.po_products))
        with col2:
            st.metric("Total Discount", f"RM{total_discount:.2f}")
        with col3:
            st.metric("FOC Value", f"RM{total_foc_value:.2f}")
        with col4:
            st.metric("Grand Total", f"RM{total_amount:.2f}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📄 Generate PO Document", type="primary", use_container_width=True):
                generate_po_document(stock_manager, st.session_state.po_products, 
                                   st.session_state.po_quantities, st.session_state.po_prices, 
                                   st.session_state.po_discounts, st.session_state.po_foc_quantities,
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
                            'discount': discount,
                            'foc_qty': foc_qty,
                            'net_qty': qty - foc_qty,
                            'total': (qty - foc_qty) * price - discount
                        }
                        for product, qty, price, discount, foc_qty in zip(
                            st.session_state.po_products, 
                            st.session_state.po_quantities, 
                            st.session_state.po_prices,
                            st.session_state.po_discounts,
                            st.session_state.po_foc_quantities
                        )
                    ],
                    'total_amount': total_amount,
                    'total_discount': total_discount,
                    'total_foc_value': total_foc_value,
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
                st.session_state.po_discounts = []
                st.session_state.po_foc_quantities = []
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
                st.write(f"**Total Discount:** RM{po_data.get('total_discount', 0):.2f}")
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
                        col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 1, 1, 1, 1, 1, 1])
                        with col1:
                            st.write(item['product'])
                        with col2:
                            st.write(f"Qty: {item['quantity']}")
                        with col3:
                            st.write(f"FOC: {item.get('foc_qty', 0)}")
                        with col4:
                            st.write(f"Net: {item.get('net_qty', item['quantity'])}")
                        with col5:
                            st.write(f"Price: RM{item['price']:.2f}")
                        with col6:
                            st.write(f"Disc: RM{item.get('discount', 0):.2f}")
                        with col7:
                            st.write(f"Total: RM{item['total']:.2f}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📄 View/Print {po_number}", key=f"view_{po_number}"):
                    # Regenerate the PO document
                    products = [item['product'] for item in po_data['items']]
                    quantities = [item['quantity'] for item in po_data['items']]
                    prices = [item['price'] for item in po_data['items']]
                    discounts = [item.get('discount', 0) for item in po_data['items']]
                    foc_quantities = [item.get('foc_qty', 0) for item in po_data['items']]
                    
                    generate_po_document(
                        stock_manager, products, quantities, prices, discounts, foc_quantities,
                        po_data['supplier'], 
                        datetime.fromisoformat(po_data['delivery_date']),
                        po_data['company_name'],
                        po_data['delivery_address'],
                        po_data['po_number']
                    )
            with col2:
                # Create CSV download
                csv_data = "Item,Product,Quantity,FOC Qty,Net Qty,Unit Price (RM),Discount (RM),Total (RM)\n"
                for i, item in enumerate(po_data['items']):
                    net_qty = item.get('net_qty', item['quantity'] - item.get('foc_qty', 0))
                    csv_data += f"{i+1},{item['product']},{item['quantity']},{item.get('foc_qty', 0)},{net_qty},{item['price']},{item.get('discount', 0)},{item['total']}\n"
                
                st.download_button(
                    label=f"📥 Download {po_number}",
                    data=csv_data,
                    file_name=f"{po_number}.csv",
                    mime="text/csv",
                    key=f"download_{po_number}"
                )
            with col3:
                if st.session_state.users[st.session_state.user]['role'] == 'admin':
                    if st.button(f"🗑️ Delete {po_number}", key=f"delete_{po_number}"):
                        del stock_manager.saved_pos[po_number]
                        stock_manager.save_all_data()
                        st.success(f"PO {po_number} deleted successfully!")
                        st.rerun()

def main():
    # Initialize user manager first
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
    try:
        stock_manager = StockManager()
    except Exception as e:
        st.error(f"Error initializing stock manager: {e}")
        st.info("Please try refreshing the page or contact administrator.")
        return
    
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
                           'product_suppliers.json', 'product_categories.json', 'product_stock.json', 'saved_pos.json', 'pending_changes.json']:
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
    try:
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
    except Exception as e:
        st.error(f"Error in {app_mode}: {e}")
        st.info("Please try refreshing the page or contact administrator.")
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">Deployed by "xtremrakib"</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
