import pandas as pd
from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timezone
from typing import Optional
from src.core.contextual import Context
from src.core.hybrid import recommend_hybrid as base_recommend
from src.smart_recommender import get_smart_recommender
from src.smart_query_processor import get_query_processor
from src.notifications import generate_notifications
from src.data_loader import get_sample_data
import logging
from src.utils import convert_numpy, clean
import numpy as np


logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Menu API - Hackathon Edition", version="2.0.0")


def convert_numpy(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean(v) for v in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    elif hasattr(obj, "tolist"):
        return obj.tolist()
    return obj


@app.get("/recommendations")
def get_recommendations(
    user_id: int, 
    time: str | None = Query(None), 
    budget: str | None = Query(None), 
    top: int = 10,
    query: str | None = Query(None, description="Natural language query for recommendations"),
    include_explanation: bool = Query(False, description="Include AI-generated explanation"),
    use_smart: bool = Query(True, description="Use smart recommendation system")
):
    """Get personalized menu recommendations"""
    try:
        now = pd.Timestamp.now()
        ctx = Context(user_id=user_id, now=now, time_of_day=time, budget_level=budget)
        
        if use_smart:
            recommender = get_smart_recommender()
            result = recommender.get_recommendations(
                user_id=user_id,
                top_k=top,
                context=ctx,
                user_query=query if query is not None else "",
                include_explanation=include_explanation
            )
            return clean(result)
        else:
            df = base_recommend(user_id, top_k=top, ctx=ctx)
            records = df.apply(convert_numpy).to_dict(orient="records")
            return clean({
                "recommendations": records,
                "metadata": {
                    "user_id": user_id,
                    "time_of_day": ctx.time_of_day,
                    "budget_level": ctx.budget_level,
                    "total_recommendations": len(df),
                    "from_cache": False,
                    "processing_time_seconds": 0.0,
                    "timestamp": now.isoformat()
                }
            })
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications")
def get_notifications(user_id: int):
    """Get personalized notifications for user"""
    try:
        return clean({"notifications": generate_notifications(user_id)})
    except Exception as e:
        logger.error(f"Error generating notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
def record_feedback(
    user_id: int,
    item_id: int,
    feedback_type: str,
    value: float,
    metadata: dict | None = None
):
    """Record user feedback for learning"""
    try:
        recommender = get_smart_recommender()
        recommender.record_feedback(user_id, item_id, value, feedback_type)
        return clean({"status": "success", "message": "Feedback recorded"})
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def get_system_metrics():
    """Get system performance metrics"""
    try:
        recommender = get_smart_recommender()
        return clean(recommender.get_system_stats())
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/query-analysis")
def analyze_query(query: str):
    """Analyze natural language query"""
    try:
        processor = get_query_processor()
        result = processor.process_query(query, user_id=1)  # Demo user
        return clean(result)
    except Exception as e:
        logger.error(f"Error analyzing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return clean({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    })


@app.get("/sampledata")
def sample_data():
    """Get sample data for testing"""
    try:
        users, items, orders = get_sample_data()
        # Convert DataFrames to list of dicts
        users = users.to_dict(orient="records")
        items = items.to_dict(orient="records")
        orders = orders.to_dict(orient="records")
        # Clean all data to remove numpy types
        return clean({
            "users": users,
            "items": items,
            "orders": orders
        })
    except Exception as e:
        logger.error(f"Error getting sample data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

# Add this debug endpoint to your API to trace the issue

@app.get("/debug/recommendations/{user_id}")
def debug_recommendations(user_id: int):
    """Debug endpoint to trace recommendation generation"""
    debug_info = {
        "user_id": user_id,
        "steps": [],
        "data_summary": {},
        "errors": []
    }
    
    try:
        # Step 1: Check database connectivity
        debug_info["steps"].append("1. Checking database connectivity")
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        debug_info["steps"].append("✓ Database connection successful")
        
        # Step 2: Load data with debugging
        debug_info["steps"].append("2. Loading data from database")
        from src.data_loader import load_all, validate_user_exists
        
        # Check if user exists
        user_exists = validate_user_exists(user_id)
        debug_info["user_exists"] = user_exists
        debug_info["steps"].append(f"✓ User exists check: {user_exists}")
        
        # Load all data
        users, items, orders = load_all(user_id=user_id)
        
        debug_info["data_summary"] = {
            "users_loaded": len(users),
            "items_loaded": len(items),  
            "orders_loaded": len(orders),
            "users_columns": list(users.columns) if not users.empty else [],
            "items_columns": list(items.columns) if not items.empty else [],
            "orders_columns": list(orders.columns) if not orders.empty else []
        }
        
        if users.empty:
            debug_info["errors"].append("No users found in database")
        if items.empty:
            debug_info["errors"].append("No items found in database")
        if orders.empty:
            debug_info["errors"].append("No orders found in database")
            
        debug_info["steps"].append(f"✓ Data loaded: {len(users)} users, {len(items)} items, {len(orders)} orders")
        
        # Step 3: Check specific user data
        if not users.empty and user_exists:
            user_row = users[users.user_id == user_id]
            if not user_row.empty:
                user_data = user_row.iloc[0].to_dict()
                debug_info["user_data"] = {k: str(v) for k, v in user_data.items()}
                debug_info["steps"].append("✓ User data retrieved")
            else:
                debug_info["errors"].append(f"User {user_id} not found in loaded users data")
        
        # Step 4: Test context creation
        debug_info["steps"].append("3. Creating context")
        from src.core.contextual import Context
        import pandas as pd
        
        now = pd.Timestamp.now()
        ctx = Context(user_id=user_id, now=now, time_of_day=None, budget_level=None)
        ctx_ensured = ctx.ensure()
        
        debug_info["context"] = {
            "user_id": ctx_ensured.user_id,
            "time_of_day": ctx_ensured.time_of_day,
            "budget_level": ctx_ensured.budget_level,
            "now": str(ctx_ensured.now)
        }
        debug_info["steps"].append(f"✓ Context created: {ctx_ensured.time_of_day}, budget: {ctx_ensured.budget_level}")
        
        # Step 5: Test basic recommendation
        if not items.empty:
            debug_info["steps"].append("4. Testing basic hybrid recommendation")
            from src.core.hybrid import recommend_hybrid
            
            recs = recommend_hybrid(user_id, top_k=5, ctx=ctx_ensured)
            debug_info["recommendations_count"] = len(recs)
            
            if not recs.empty:
                debug_info["sample_recommendations"] = [
                    {k: str(v) for k, v in rec.to_dict().items()} 
                    for _, rec in recs.head(3).iterrows()
                ]
                debug_info["steps"].append(f"✓ Generated {len(recs)} recommendations")
            else:
                debug_info["errors"].append("Hybrid recommender returned empty results")
                debug_info["steps"].append("✗ No recommendations generated")
                
                # Try to understand why
                debug_info["steps"].append("5. Debugging empty recommendations")
                
                # Check if items have required columns
                required_cols = ['item_id', 'name', 'category', 'price']
                missing_cols = [col for col in required_cols if col not in items.columns]
                if missing_cols:
                    debug_info["errors"].append(f"Items missing required columns: {missing_cols}")
                
                # Check if items have valid data
                if not items.empty:
                    debug_info["items_sample"] = [
                        {k: str(v) for k, v in item.to_dict().items()}
                        for _, item in items.head(2).iterrows()
                    ]
                
        else:
            debug_info["errors"].append("No items available for recommendations")
        
        # Step 6: Test smart recommender
        debug_info["steps"].append("6. Testing smart recommender")
        try:
            from src.smart_recommender import get_smart_recommender
            smart_recommender = get_smart_recommender()
            smart_result = smart_recommender.get_recommendations(
                user_id=user_id,
                top_k=5,
                context=ctx_ensured,
                user_query="",
                include_explanation=False
            )
            debug_info["smart_recommendations_count"] = len(smart_result.get("recommendations", []))
            debug_info["steps"].append(f"✓ Smart recommender returned {len(smart_result.get('recommendations', []))} items")
        except Exception as e:
            debug_info["errors"].append(f"Smart recommender failed: {str(e)}")
            debug_info["steps"].append(f"✗ Smart recommender error: {str(e)}")
        
    except Exception as e:
        debug_info["errors"].append(f"Fatal error: {str(e)}")
        debug_info["steps"].append(f"✗ Fatal error: {str(e)}")
        import traceback
        debug_info["traceback"] = traceback.format_exc()
    
    return debug_info


@app.get("/debug/database")
def debug_database():
    """Debug database tables and data"""
    debug_info = {
        "tables": {},
        "sample_data": {},
        "errors": []
    }
    
    try:
        from django.db import connection
        
        # Get table info
        with connection.cursor() as cursor:
            # Check slice_user table
            cursor.execute("SELECT COUNT(*) FROM slice_user")
            user_count = cursor.fetchone()[0]
            debug_info["tables"]["slice_user"] = {"count": user_count}
            
            if user_count > 0:
                cursor.execute("SELECT uid, username, prefs FROM slice_user LIMIT 3")
                users_sample = cursor.fetchall()
                debug_info["sample_data"]["users"] = [
                    {"uid": row[0], "username": row[1], "prefs": str(row[2])[:100] + "..." if row[2] else None}
                    for row in users_sample
                ]
            
            # Check slice_menuitem and slice_menu tables
            cursor.execute("""
                SELECT COUNT(*) 
                FROM slice_menuitem mi 
                JOIN slice_menu m ON mi.menu_id = m.menu_id
            """)
            items_count = cursor.fetchone()[0]
            debug_info["tables"]["slice_menuitem_with_menu"] = {"count": items_count}
            
            if items_count > 0:
                cursor.execute("""
                    SELECT mi.item_id, mi.name, mi.price, mi.category, m.store_id
                    FROM slice_menuitem mi 
                    JOIN slice_menu m ON mi.menu_id = m.menu_id 
                    LIMIT 3
                """)
                items_sample = cursor.fetchall()
                debug_info["sample_data"]["items"] = [
                    {
                        "item_id": row[0], 
                        "name": str(row[1])[:50] + "..." if row[1] else None,
                        "price": row[2],
                        "category": row[3],
                        "store_id": row[4]
                    }
                    for row in items_sample
                ]
            
            # Check slice_order table
            cursor.execute("SELECT COUNT(*) FROM slice_order WHERE user_id IS NOT NULL")
            orders_count = cursor.fetchone()[0]
            debug_info["tables"]["slice_order"] = {"count": orders_count}
            
            if orders_count > 0:
                cursor.execute("""
                    SELECT id, user_id, store_id, total, items 
                    FROM slice_order 
                    WHERE user_id IS NOT NULL 
                    LIMIT 3
                """)
                orders_sample = cursor.fetchall()
                debug_info["sample_data"]["orders"] = [
                    {
                        "order_id": row[0],
                        "user_id": row[1],
                        "store_id": row[2], 
                        "total": row[3],
                        "items_preview": str(row[4])[:100] + "..." if row[4] else None
                    }
                    for row in orders_sample
                ]
                
    except Exception as e:
        debug_info["errors"].append(f"Database debug error: {str(e)}")
        import traceback
        debug_info["traceback"] = traceback.format_exc()
    
    return debug_info


@app.get("/debug/context/{user_id}")
def debug_context(user_id: int, time: str = None, budget: str = None):
    """Debug context creation"""
    debug_info = {
        "input": {
            "user_id": user_id,
            "time": time,
            "budget": budget
        },
        "context": {},
        "errors": []
    }
    
    try:
        from src.core.contextual import Context
        import pandas as pd
        
        now = pd.Timestamp.now()
        debug_info["now"] = str(now)
        debug_info["hour"] = now.hour
        
        # Create context
        ctx = Context(user_id=user_id, now=now, time_of_day=time, budget_level=budget)
        debug_info["context"]["before_ensure"] = {
            "user_id": ctx.user_id,
            "time_of_day": ctx.time_of_day,
            "budget_level": ctx.budget_level
        }
        
        # Ensure context
        ctx_ensured = ctx.ensure()
        debug_info["context"]["after_ensure"] = {
            "user_id": ctx_ensured.user_id,
            "time_of_day": ctx_ensured.time_of_day,
            "budget_level": ctx_ensured.budget_level
        }
        
        # Time mapping logic
        h = now.hour
        if 6 <= h < 11:
            expected_time = "morning"
        elif 11 <= h < 15:
            expected_time = "lunch"
        elif 15 <= h < 18:
            expected_time = "afternoon"
        else:
            expected_time = "dinner"
        
        debug_info["time_logic"] = {
            "current_hour": h,
            "expected_time_of_day": expected_time,
            "actual_time_of_day": ctx_ensured.time_of_day
        }
        
    except Exception as e:
        debug_info["errors"].append(str(e))
        import traceback
        debug_info["traceback"] = traceback.format_exc()
    
    return debug_info