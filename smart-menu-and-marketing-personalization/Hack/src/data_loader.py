import os
import django
import pandas as pd
from datetime import datetime
from typing import Tuple, Optional
from django.conf import settings
from django.db import connection
import json
import logging
from sqlalchemy import create_engine
import warnings

logger = logging.getLogger(__name__)

# Suppress the pandas SQLAlchemy warnings
warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy connectable')

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hack.settings")

try:
    django.setup()
    logger.info("Django setup successful")
except Exception as e:
    logger.error(f"Django setup failed: {e}")
    raise


def get_db_engine():
    """Create SQLAlchemy engine from Django database settings"""
    try:
        from django.conf import settings
        db_settings = settings.DATABASES['default']
        
        # Build database URL based on engine type
        if db_settings['ENGINE'] == 'django.db.backends.postgresql':
            # Handle PostgreSQL with proper driver
            driver = 'psycopg2' if 'psycopg2' in str(db_settings.get('OPTIONS', {})) else 'psycopg2'
            db_url = f"postgresql+{driver}://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
        elif db_settings['ENGINE'] == 'django.db.backends.mysql':
            # Handle MySQL with proper driver
            driver = 'pymysql' if 'pymysql' in str(db_settings.get('OPTIONS', {})) else 'pymysql'
            db_url = f"mysql+{driver}://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
        elif db_settings['ENGINE'] == 'django.db.backends.sqlite3':
            db_url = f"sqlite:///{db_settings['NAME']}"
        else:
            # Fallback to Django connection
            logger.warning(f"Unsupported database engine: {db_settings['ENGINE']}. Using Django connection.")
            return connection
            
        from sqlalchemy import create_engine
        # Create engine with proper configuration
        engine = create_engine(
            db_url,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections every 5 minutes
            echo=False           # Set to True for SQL debugging
        )
        logger.info(f"Created SQLAlchemy engine for {db_settings['ENGINE']}")
        return engine
    except Exception as e:
        logger.warning(f"Could not create SQLAlchemy engine: {e}. Using Django connection.")
        return connection


def safe_read_sql(query, params=None):
    """Safely execute SQL query with proper parameter handling"""
    try:
        engine = get_db_engine()
        
        # Ensure params is properly formatted
        if params is not None:
            # Convert single values to proper format
            if not isinstance(params, (list, tuple, dict)):
                params = [params]
            elif isinstance(params, (list, tuple)):
                # Ensure all params are scalars
                cleaned_params = []
                for p in params:
                    if isinstance(p, (list, tuple)) and len(p) > 0:
                        cleaned_params.append(p[0])  # Take first element
                    else:
                        cleaned_params.append(p)
                params = tuple(cleaned_params)  # Convert to tuple for database compatibility
        
        logger.debug(f"Executing query with params: {params}")
        
        # Check if we have a SQLAlchemy engine
        if hasattr(engine, 'execute') and hasattr(engine, 'connect'):
            # Use SQLAlchemy engine
            return pd.read_sql(query, engine, params=params)
        else:
            # Fallback to Django connection - suppress warnings
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy connectable')
                return pd.read_sql(query, engine, params=params)
        
    except Exception as e:
        logger.error(f"Error executing SQL query: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        raise


def validate_user_exists(user_id: int) -> bool:
    """Check if user exists in database"""
    try:
        # Ensure user_id is a scalar integer
        if isinstance(user_id, (list, tuple)):
            user_id = user_id[0] if len(user_id) > 0 else 0
        user_id = int(user_id)
        
        query = "SELECT COUNT(*) as count FROM slice_user WHERE uid = %s"
        result = safe_read_sql(query, (user_id,))  # Pass as tuple
        return result['count'].iloc[0] > 0
    except Exception as e:
        logger.error(f"Error checking user existence: {e}")
        return False


def validate_store_exists(store_id: int) -> bool:
    """Check if store exists in database"""
    try:
        # Ensure store_id is a scalar integer
        if isinstance(store_id, (list, tuple)):
            store_id = store_id[0] if len(store_id) > 0 else 0
        store_id = int(store_id)
        
        query = "SELECT COUNT(*) as count FROM slice_menu WHERE store_id = %s"
        result = safe_read_sql(query, (store_id,))  # Pass as tuple
        return result['count'].iloc[0] > 0
    except Exception as e:
        logger.error(f"Error checking store existence: {e}")
        return False


def load_users(user_id: Optional[int] = None) -> pd.DataFrame:
    """Load users from PostgreSQL database with proper validation"""
    
    # Normalize user_id parameter
    if isinstance(user_id, (list, tuple)):
        user_id = user_id[0] if len(user_id) > 0 else None
    if user_id is not None:
        try:
            user_id = int(user_id)
            if user_id <= 0:
                user_id = None
        except (ValueError, TypeError):
            user_id = None
    
    # If specific user requested, validate first
    if user_id and not validate_user_exists(user_id):
        logger.warning(f"User {user_id} does not exist in database")
        return pd.DataFrame(columns=[
            'user_id', 'username', 'first_name', 'last_name', 'email', 'role',
            'phone', 'address', 'city', 'nexo_coins', 'xp', 'level', 'prefs',
            'favorite_categories', 'diet', 'favorites', 'allergies', 
            'time_preferences', 'budget_sensitivity'
        ])
    
    query = """
        SELECT 
            uid as user_id,
            username,
            first_name,
            last_name,
            email,
            role,
            phone,
            address,
            city,
            nexo_coins,
            xp,
            level,
            prefs
        FROM slice_user
    """
    params = None
    if user_id:
        query += " WHERE uid = %s"
        params = (user_id,)  # Pass as tuple
    
    try:
        users = safe_read_sql(query, params)
        logger.info(f"Loaded {len(users)} users from database")
    except Exception as e:
        logger.error(f"Error loading users: {e}")
        return pd.DataFrame()
    
    if users.empty:
        logger.warning("No users found in database")
        return pd.DataFrame()

    # Parse JSON preferences field
    def parse_prefs(prefs_json):
        if pd.isna(prefs_json) or prefs_json == '{}':
            return {
                'cuisine': [],
                'diet': None,
                'favorites': [],
                'allergies': [],
                'time_preferences': []
            }
        try:
            prefs = json.loads(prefs_json) if isinstance(prefs_json, str) else prefs_json
            return prefs if isinstance(prefs, dict) else {}
        except Exception as e:
            logger.warning(f"Error parsing preferences: {e}")
            return {'cuisine': [], 'diet': None, 'favorites': [], 'allergies': [], 'time_preferences': []}
    
    prefs_parsed = users['prefs'].apply(parse_prefs)
    users['favorite_categories'] = prefs_parsed.apply(lambda x: x.get('cuisine', []))
    users['diet'] = prefs_parsed.apply(lambda x: x.get('diet'))
    users['favorites'] = prefs_parsed.apply(lambda x: x.get('favorites', []))
    users['allergies'] = prefs_parsed.apply(lambda x: x.get('allergies', []))
    users['time_preferences'] = prefs_parsed.apply(lambda x: x.get('time_preferences', []))
    
    # Add budget sensitivity based on order history (will be computed later)
    users['budget_sensitivity'] = 'medium'  # Default
    
    return users


def load_items(store_id: Optional[int] = None) -> pd.DataFrame:
    """Load menu items from PostgreSQL database with proper validation"""
    
    # Normalize store_id parameter
    if isinstance(store_id, (list, tuple)):
        store_id = store_id[0] if len(store_id) > 0 else None
    if store_id is not None:
        try:
            store_id = int(store_id)
            if store_id <= 0:
                store_id = None
        except (ValueError, TypeError):
            store_id = None
    
    query = """
        SELECT 
            mi.item_id,
            mi.name,
            mi.category,
            mi.description,
            mi.price,
            mi.recipe,
            mi.display_type,
            mi.available,
            mi.menu_id,
            m.store_id
        FROM slice_menuitem mi
        JOIN slice_menu m ON mi.menu_id = m.menu_id
    """
    params = None
    if store_id:
        query += " WHERE m.store_id = %s"
        params = (store_id,)  # Pass as tuple
    
    try:
        items = safe_read_sql(query, params)
        logger.info(f"Loaded {len(items)} items from database")
    except Exception as e:
        logger.error(f"Error loading items: {e}")
        return pd.DataFrame()
    
    if items.empty:
        logger.warning("No items found in database")
        return pd.DataFrame()

    # Parse multilingual name field (JSON)
    def get_name(name_json):
        if pd.isna(name_json):
            return "Unknown Item"
        try:
            if isinstance(name_json, str):
                names = json.loads(name_json)
            else:
                names = name_json
            if isinstance(names, dict):
                return names.get('en', list(names.values())[0] if names else 'Unknown Item')
            return str(names)
        except Exception as e:
            logger.warning(f"Error parsing name: {e}")
            return str(name_json) if name_json else "Unknown Item"
    
    items['name'] = items['name'].apply(get_name)
    
    # Parse description
    def get_description(desc_json):
        if pd.isna(desc_json):
            return ""
        try:
            if isinstance(desc_json, str):
                descs = json.loads(desc_json)
            else:
                descs = desc_json
            if isinstance(descs, dict):
                return descs.get('en', list(descs.values())[0] if descs else '')
            return str(descs)
        except Exception as e:
            logger.warning(f"Error parsing description: {e}")
            return str(desc_json) if desc_json else ""
    
    items['description'] = items['description'].apply(get_description)
    
    # Ensure category is string and lowercase
    items['category'] = items['category'].astype(str).str.lower()
    items['subcategory'] = items['category']  # Simplified for now
    
    # Parse recipe to determine dietary tags - IMPROVED
    def extract_dietary_tags(recipe_json, category, name):
        tags = []
        category_str = str(category).lower()
        name_str = str(name).lower()
        
        # Category-based tags
        if category_str in ['salad', 'juice', 'smoothie']:
            tags.append('vegetarian')
        elif category_str in ['pizza']:
            # Check pizza name for vegetarian indicators
            if any(word in name_str for word in ['vegetarian', 'veggie', 'mushroom', 'cheese']):
                tags.append('vegetarian')
            if any(word in name_str for word in ['meat', 'chicken', 'beef', 'pepperoni', 'sausage']):
                tags.append('meat')
        elif category_str in ['dessert']:
            # Most desserts are vegetarian
            tags.append('vegetarian')
            if any(word in name_str for word in ['cheese', 'cream', 'milk']):
                tags.append('dairy')
        elif category_str in ['cold drink', 'hot drink']:
            tags.append('vegetarian')
        
        return tags
    
    items['dietary_tags'] = items.apply(lambda x: extract_dietary_tags(x['recipe'], x['category'], x['name']), axis=1)
    
    # Determine time preference based on category
    def get_time_preference(category):
        morning_items = ['juice', 'smoothie', 'coffee', 'breakfast']
        lunch_items = ['salad', 'sandwich', 'soup']
        dinner_items = ['pizza', 'pasta', 'steak', 'burger']
        
        cat_lower = str(category).lower()
        if any(item in cat_lower for item in morning_items):
            return 'morning'
        elif any(item in cat_lower for item in lunch_items):
            return 'lunch'
        elif any(item in cat_lower for item in dinner_items):
            return 'dinner'
        return 'any'
    
    items['time_preference'] = items['category'].apply(get_time_preference)
    
    # Determine budget category based on price
    def get_budget_category(price):
        if pd.isna(price) or price <= 0:
            return 'mid'
        try:
            price_float = float(price)
            if price_float < 1000:
                return 'low'
            elif price_float > 3000:
                return 'high'
            return 'mid'
        except (ValueError, TypeError):
            return 'mid'
    
    items['budget_category'] = items['price'].apply(get_budget_category)
    
    # Add popularity score (will be calculated from orders)
    items['popularity_score'] = 0.5  # Default
    
    # Add seasonal field
    items['seasonal'] = 'all'  # Default to all seasons
    
    return items


def load_orders(user_id: Optional[int] = None, store_id: Optional[int] = None) -> pd.DataFrame:
    """Load orders with their items from PostgreSQL database with proper validation"""
    
    # Normalize parameters - CRITICAL: ensure these are scalars
    if isinstance(user_id, (list, tuple)):
        user_id = user_id[0] if len(user_id) > 0 else None
    if isinstance(store_id, (list, tuple)):
        store_id = store_id[0] if len(store_id) > 0 else None
        
    if user_id is not None:
        try:
            user_id = int(user_id)
            if user_id <= 0:
                user_id = None
        except (ValueError, TypeError):
            logger.warning(f"Invalid user_id: {user_id}")
            user_id = None
            
    if store_id is not None:
        try:
            store_id = int(store_id)
            if store_id <= 0:
                store_id = None
        except (ValueError, TypeError):
            logger.warning(f"Invalid store_id: {store_id}")
            store_id = None
    
    # Debug: Check if orders table has data
    try:
        count_query = "SELECT COUNT(*) as total FROM slice_order"
        count_result = safe_read_sql(count_query)
        total_orders = count_result['total'].iloc[0]
        logger.info(f"Total orders in database: {total_orders}")
        
        if total_orders == 0:
            logger.warning("slice_order table is empty")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error checking order count: {e}")
    
    query = """
        SELECT 
            o.id as order_id,
            o.store_id,
            o.user_id,
            o.display_id,
            o.created_at as timestamp,
            o.pickup_type,
            o.status,
            o.total as total_amount,
            o.payment,
            o.source,
            o.meta,
            o.items as items_json
        FROM slice_order o
        WHERE o.user_id IS NOT NULL
    """
    
    params = []
    conditions = []
    
    if user_id is not None:
        conditions.append("o.user_id = %s")
        params.append(user_id)
        
    if store_id is not None:
        conditions.append("o.store_id = %s")
        params.append(store_id)
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
    
    query += " ORDER BY o.created_at DESC"
    
    logger.info(f"Executing order query with params: {params}")
    
    try:
        orders = safe_read_sql(query, tuple(params) if params else None)
        logger.info(f"Loaded {len(orders)} orders from database")
    except Exception as e:
        logger.error(f"Error loading orders: {e}")
        return pd.DataFrame()
    
    if orders.empty:
        logger.warning("No orders found in database")
        return pd.DataFrame()

    # Continue with the rest of the order processing...
    # [Rest of the function remains the same as before]
    order_items_list = []
    
    for idx, order_row in orders.iterrows():
        try:
            items_data = order_row['items_json']
            
            if pd.isna(items_data) or items_data is None:
                items_data = []
            elif isinstance(items_data, str):
                if items_data.strip() == '' or items_data.strip() == '{}':
                    items_data = []
                else:
                    items_data = json.loads(items_data)
            elif not isinstance(items_data, list):
                items_data = []
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Error parsing items JSON for order {order_row['order_id']}: {e}")
            items_data = []
        except Exception as e:
            logger.warning(f"Unexpected error parsing items JSON for order {order_row['order_id']}: {e}")
            items_data = []
        
        for item in items_data:
            if not isinstance(item, dict):
                continue
                
            try:
                item_id = item.get('itemId') or item.get('item_id') or item.get('id')
                if item_id is None:
                    continue
                    
                item_id = int(item_id)
                quantity = max(1, int(item.get('qty', item.get('quantity', 1))))
                price = max(0, float(item.get('price', 0)))
                
                order_item = {
                    'order_id': order_row['order_id'],
                    'user_id': order_row['user_id'],
                    'timestamp': order_row['timestamp'],
                    'item_id': item_id,
                    'item_name': str(item.get('name', 'Unknown'))[:100],
                    'quantity': quantity,
                    'size': str(item.get('size', 'regular'))[:20],
                    'price': price,
                    'added_ingredients': item.get('addedIngredients', item.get('added_ingredients', [])),
                    'removed_ingredients': item.get('removedIngredients', item.get('removed_ingredients', [])),
                    'total_amount': order_row['total_amount'],
                    'pickup_type': order_row['pickup_type'],
                    'status': order_row['status']
                }
                order_items_list.append(order_item)
                
            except Exception as e:
                logger.warning(f"Error processing item in order {order_row['order_id']}: {e}")
                continue
    
    if not order_items_list:
        logger.warning("No order items found after parsing")
        return pd.DataFrame()

    complete_orders = pd.DataFrame(order_items_list)
    
    # Add time_of_day field
    def _infer_time_of_day(ts) -> str:
        if pd.isna(ts):
            return "dinner"
        try:
            if isinstance(ts, str):
                ts = pd.to_datetime(ts)
            h = ts.hour
            if 6 <= h < 11:
                return "morning"
            elif 11 <= h < 15:
                return "lunch"  
            elif 15 <= h < 18:
                return "afternoon"
            return "dinner"
        except Exception as e:
            logger.warning(f"Error inferring time of day: {e}")
            return "dinner"
    
    complete_orders['time_of_day'] = complete_orders['timestamp'].apply(_infer_time_of_day)
    
    # Ensure lists are properly formatted
    for col in ['added_ingredients', 'removed_ingredients']:
        complete_orders[col] = complete_orders[col].apply(
            lambda x: x if isinstance(x, list) else []
        )
    
    logger.info(f"Successfully processed {len(complete_orders)} order items")
    return complete_orders


def load_all(user_id: Optional[int] = None, store_id: Optional[int] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all data with parameter safety"""
    
    # CRITICAL: Ensure parameters are scalars
    if isinstance(user_id, (list, tuple)):
        user_id = user_id[0] if len(user_id) > 0 else None
    if isinstance(store_id, (list, tuple)):
        store_id = store_id[0] if len(store_id) > 0 else None
    
    if user_id is not None:
        try:
            user_id = int(user_id)
            if user_id <= 0:
                user_id = None
        except (ValueError, TypeError):
            user_id = None
            
    if store_id is not None:
        try:
            store_id = int(store_id)
            if store_id <= 0:
                store_id = None
        except (ValueError, TypeError):
            store_id = None
    
    logger.info(f"Loading data - user_id: {user_id}, store_id: {store_id}")
    
    users = load_users(user_id)
    items = load_items(store_id)
    orders = load_orders(user_id, store_id)
    
    # Update item popularity and user budget sensitivity
    if not orders.empty and not items.empty:
        try:
            popularity = orders.groupby('item_id')['quantity'].sum()
            if not popularity.empty:
                popularity_normalized = (popularity - popularity.min()) / (popularity.max() - popularity.min() + 1e-6)
                items['popularity_score'] = items['item_id'].map(popularity_normalized).fillna(0.1)
        except Exception as e:
            logger.error(f"Error updating item popularity: {e}")
    
    if not orders.empty and not users.empty:
        try:
            avg_order_value = orders.groupby('user_id')['total_amount'].mean()
            def categorize_budget(avg_value):
                if pd.isna(avg_value) or avg_value <= 0:
                    return 'medium'
                if avg_value < 1500:
                    return 'low'
                elif avg_value > 3500:
                    return 'high'
                return 'medium'
            
            budget_map = avg_order_value.apply(categorize_budget)
            users['budget_sensitivity'] = users['user_id'].map(budget_map).fillna('medium')
        except Exception as e:
            logger.error(f"Error updating user budget sensitivity: {e}")
    
    logger.info(f"Data loading complete - Users: {len(users)}, Items: {len(items)}, Orders: {len(orders)}")
    return users, items, orders


def get_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Get sample data for testing"""
    try:
        return load_all()
    except Exception as e:
        logger.error(f"Error loading sample data: {e}")
        return (
            pd.DataFrame(columns=['user_id', 'username', 'budget_sensitivity']),
            pd.DataFrame(columns=['item_id', 'name', 'category', 'price']),
            pd.DataFrame(columns=['order_id', 'user_id', 'item_id', 'quantity'])
        )