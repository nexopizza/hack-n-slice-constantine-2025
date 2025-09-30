from __future__ import annotations

import math
import pandas as pd
from typing import List, Dict
from src.data_loader import load_all
from .contextual import Context
from .collaborative import cf_scores_for_user
from src.utils import season_of
import logging

logger = logging.getLogger(__name__)


def compute_user_favorites(orders: pd.DataFrame) -> pd.Series:
    """Compute user favorites with proper error handling"""
    if orders.empty:
        return pd.Series(dtype=float)
    
    try:
        return orders.groupby(["user_id", "item_id"]).size().groupby(level=0).apply(
            lambda s: (s - s.min()) / (s.max() - s.min() + 1e-6)
        )
    except Exception as e:
        logger.error(f"Error computing user favorites: {e}")
        return pd.Series(dtype=float)


def score_items(user_id: int, ctx: Context, users: pd.DataFrame, items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """Score items with comprehensive validation and error handling"""
    ctx.ensure()

    if items.empty:
        logger.warning("No items available for scoring")
        return pd.DataFrame()

    # Validate user exists
    user_exists = not users.empty and user_id in users['user_id'].values
    if not user_exists:
        logger.warning(f"User {user_id} not found in database. Using default preferences.")
        user = {
            "diet": "none", 
            "budget_sensitivity": "medium",
            "favorite_categories": [],
            "allergies": [],
            "time_preferences": []
        }
    else:
        user_row = users.loc[users.user_id == user_id].iloc[0]
        user = {
            "diet": user_row.get("diet", "none"),
            "budget_sensitivity": user_row.get("budget_sensitivity", "medium"),
            "favorite_categories": user_row.get("favorite_categories", []),
            "allergies": user_row.get("allergies", []),
            "time_preferences": user_row.get("time_preferences", [])
        }

    # Base score: recency-decayed popularity
    if orders.empty:
        logger.warning("No orders available for popularity calculation. Using default scores.")
        popularity = pd.Series(0.5, index=items['item_id'])
    else:
        try:
            now = ctx.now if hasattr(ctx.now, 'tz') and ctx.now.tz is not None else pd.Timestamp.now()
            
            # Handle timezone compatibility
            orders_ts = orders["timestamp"]
            if hasattr(now, 'tz') and now.tz is not None:
                if not hasattr(orders_ts.dtype, 'tz') or orders_ts.dt.tz is None:
                    orders_ts = pd.to_datetime(orders_ts, utc=True)
            else:
                if hasattr(orders_ts.dtype, 'tz') and orders_ts.dt.tz is not None:
                    orders_ts = orders_ts.dt.tz_localize(None)
            
            orders = orders.assign(_age_days=(now - orders_ts).dt.days.clip(lower=0))
            decay = 0.5 ** (orders["_age_days"] / 30.0)  # half-life ~30 days
            popularity = orders.groupby("item_id").apply(lambda g: (0.2 + decay.loc[g.index]).sum())
            
            if not popularity.empty:
                popularity = (popularity - popularity.min()) / (popularity.max() - popularity.min() + 1e-6)
            else:
                popularity = pd.Series(0.5, index=items['item_id'])
        except Exception as e:
            logger.error(f"Error calculating popularity scores: {e}")
            popularity = pd.Series(0.5, index=items['item_id'])

    df = items.copy()
    # Ensure popularity is a proper Series with correct index
    if isinstance(popularity, pd.Series):
        # Convert to dict to avoid pandas map issues
        popularity_dict = popularity.to_dict()
        df["base"] = df["item_id"].map(popularity_dict).fillna(0.2)
    else:
        df["base"] = 0.2

    # Diet filter/boost - IMPROVED
    diet = str(user.get("diet", "none")).lower()
    def diet_ok(tags: List[str]) -> float:
        if not isinstance(tags, list):
            tags = []
        tags = set(str(tag).lower() for tag in tags)
        
        # Handle different diet types from the database
        if diet in ["végétarien", "vegetarian"]:
            if "meat" in tags or "chicken" in tags or "beef" in tags or "pork" in tags:
                return 0.0
            # Boost vegetarian items
            if "vegetarian" in tags or "veggie" in tags:
                return 1.2
        elif diet in ["vegan"]:
            if any(t in tags for t in ["meat", "chicken", "beef", "pork", "dairy", "cheese", "milk", "egg"]):
                return 0.0
            # Boost vegan items
            if "vegan" in tags:
                return 1.3
        elif diet in ["aucun", "none", "no"]:
            # No dietary restrictions - slight boost for all items
            return 1.0
        else:
            # Unknown diet - no filtering
            return 1.0
        
        # Check for user allergies
        allergies = user.get("allergies", [])
        if isinstance(allergies, list):
            allergy_set = set(str(a).lower() for a in allergies)
            if any(allergy in tags for allergy in allergy_set):
                return 0.0
        
        return 1.0

    # Handle dietary_tags properly - ensure it's a list
    def safe_diet_ok(tags):
        try:
            if tags is None or (hasattr(tags, '__len__') and len(tags) == 0):
                return diet_ok([])
            if isinstance(tags, list):
                return diet_ok(tags)
            return diet_ok([])
        except Exception:
            return diet_ok([])
    
    df["diet_multiplier"] = df["dietary_tags"].apply(safe_diet_ok)

    # Time-of-day boosts
    df["time_multiplier"] = (df["time_preference"].fillna("any").apply(
        lambda t: 1.2 if t == ctx.time_of_day else (1.05 if t in ["any", "all"] else 1.0)
    ))

    # Seasonality boost
    current_season = season_of(ctx.now)
    if "seasonal" in df.columns:
        df["season_multiplier"] = df["seasonal"].fillna("all").apply(
            lambda s: 1.15 if s == current_season or s in ["all", "any"] else 1.0
        )
    else:
        df["season_multiplier"] = 1.0

    # Budget sensitivity
    budget = ctx.budget_level or str(user.get("budget_sensitivity", "medium"))
    def budget_mult(cat: str) -> float:
        if pd.isna(cat):
            cat = "mid"
        cat = str(cat).lower()
        
        budget_lower = str(budget).lower()
        if budget_lower in ["low", "high", "mid", "medium"]:
            mapping = {
                "low": {"low": 1.2, "mid": 1.0, "high": 0.8},
                "medium": {"low": 1.1, "mid": 1.1, "high": 0.95},
                "mid": {"low": 1.1, "mid": 1.1, "high": 0.95},
                "high": {"low": 0.9, "mid": 1.0, "high": 1.2},
            }
            budget_key = "medium" if budget_lower == "mid" else budget_lower
            return mapping[budget_key].get(cat, 1.0)
        return 1.0
    
    df["budget_multiplier"] = df["budget_category"].fillna("mid").apply(budget_mult)

    # User favorites from orders
    try:
        if orders.empty or not user_exists:
            df["favorite_boost"] = 1.0
        else:
            fav_series = compute_user_favorites(orders)
            if user_id in fav_series.index.get_level_values(0):
                user_favs = fav_series.xs(user_id, level=0)
                if isinstance(user_favs, pd.Series):
                    # Convert to dict to avoid pandas map issues
                    user_favs_dict = user_favs.to_dict()
                    df["favorite_boost"] = df["item_id"].map(user_favs_dict).fillna(0.0) * 0.6 + 1.0
                else:
                    df["favorite_boost"] = 1.0
            else:
                df["favorite_boost"] = 1.0
    except (KeyError, IndexError, Exception) as e:
        logger.warning(f"Error calculating favorite boost: {e}")
        df["favorite_boost"] = 1.0

    # Price alignment to user's historical spend
    try:
        if orders.empty or not user_exists:
            df["price_align"] = 1.0
        else:
            user_spend = orders.loc[orders.user_id == user_id]
            if not user_spend.empty and "price" in df.columns:
                # Join with items to get prices
                joined = user_spend.merge(df[["item_id", "price"]], on="item_id", how="left")
                price_col = "price_y" if "price_y" in joined.columns else "price"
                
                if price_col in joined.columns:
                    valid_prices = joined[price_col].dropna()
                    if not valid_prices.empty:
                        target = valid_prices.mean()
                        df["price_align"] = (1.0 - (df["price"] - target).abs() / (target + 1e-6)).clip(0.8, 1.2)
                    else:
                        df["price_align"] = 1.0
                else:
                    df["price_align"] = 1.0
            else:
                df["price_align"] = 1.0
    except Exception as e:
        logger.warning(f"Error calculating price alignment: {e}")
        df["price_align"] = 1.0

    # Recent-purchase penalty
    try:
        if orders.empty or not user_exists:
            df["recent_penalty"] = 1.0
        else:
            recent = orders.sort_values("timestamp").groupby("user_id").tail(3)
            recent_ids = set(recent.loc[recent.user_id == user_id, "item_id"].tolist())
            df["recent_penalty"] = df["item_id"].apply(lambda x: 0.85 if x in recent_ids else 1.0)
    except Exception as e:
        logger.warning(f"Error calculating recent penalty: {e}")
        df["recent_penalty"] = 1.0

    # Category preference boost - IMPROVED
    try:
        favorite_categories = user.get("favorite_categories", [])
        if isinstance(favorite_categories, list) and favorite_categories:
            # Create a mapping of category names to boost values
            category_boosts = {}
            for fc in favorite_categories:
                fc_lower = str(fc).lower()
                # Map different category names to actual item categories
                if fc_lower in ['italienne', 'italian']:
                    category_boosts.update({'pizza': 1.3, 'pasta': 1.2, 'dessert': 1.1})
                elif fc_lower in ['algérienne', 'algerian']:
                    category_boosts.update({'pizza': 1.2, 'dessert': 1.1, 'cold drink': 1.1})
                elif fc_lower in ['végétarienne', 'vegetarian']:
                    category_boosts.update({'pizza': 1.2, 'dessert': 1.1, 'salad': 1.3})
                else:
                    # Generic boost for any category match
                    category_boosts[fc_lower] = 1.2
            
            def get_category_boost(cat):
                cat_lower = str(cat).lower()
                return category_boosts.get(cat_lower, 1.0)
            
            df["category_boost"] = df["category"].apply(get_category_boost)
        else:
            df["category_boost"] = 1.0
    except Exception as e:
        logger.warning(f"Error calculating category boost: {e}")
        df["category_boost"] = 1.0

    # Final score (content/context)
    df["score"] = (
        df["base"]
        * df["diet_multiplier"]
        * df["time_multiplier"]
        * df["season_multiplier"]
        * df["budget_multiplier"]
        * df["favorite_boost"]
        * df["price_align"]
        * df["recent_penalty"]
        * df["category_boost"]
    )
    
    # Add small randomization to break ties and provide variety
    import numpy as np
    np.random.seed(user_id)  # Consistent randomization per user
    df["tie_breaker"] = np.random.uniform(0.95, 1.05, len(df))
    df["final_score"] = df["score"] * df["tie_breaker"]
    
    return df.sort_values("final_score", ascending=False)


def recommend_hybrid(user_id: int, top_k: int = 10, ctx: Context | None = None) -> pd.DataFrame:
    """Generate hybrid recommendations with comprehensive error handling and validation"""
    logger.info(f"Generating recommendations for user_id: {user_id}, top_k: {top_k}")
    
    try:
        # Load data with validation
        users, items, orders = load_all(user_id=user_id)
        
        # Check if we have data
        if items.empty:
            logger.warning("No items available in database")
            return _create_empty_recommendation_df()
        
        # Create context
        ctx = ctx or Context(user_id=user_id, now=pd.Timestamp.now()).ensure()
        
        # Validate user exists
        user_exists = not users.empty and user_id in users['user_id'].values
        if not user_exists:
            logger.warning(f"User {user_id} not found in database. Generating content-based recommendations.")
        
        # Score items using content-based approach
        content_scored = score_items(user_id, ctx, users, items, orders)
        
        if content_scored.empty:
            logger.warning("No items could be scored")
            return _create_empty_recommendation_df()

        # Collaborative filtering scores
        try:
            if user_exists and not orders.empty:
                cf = cf_scores_for_user(user_id)
                if not cf.empty and isinstance(cf, pd.Series):
                    # Normalize CF to 0..1
                    cf_norm = (cf - cf.min()) / (cf.max() - cf.min() + 1e-6)
                    # Convert to dict to avoid pandas map issues
                    cf_norm_dict = cf_norm.to_dict()
                    content_scored["cf_score"] = content_scored["item_id"].map(cf_norm_dict).fillna(0.0)
                else:
                    content_scored["cf_score"] = 0.0
            else:
                content_scored["cf_score"] = 0.0
        except Exception as e:
            logger.warning(f"Collaborative filtering failed: {e}. Using content-based only.")
            content_scored["cf_score"] = 0.0

        # Hybrid combine: weighted geometric mean with content/context dominant
        content_scored["hybrid_score"] = (
            (content_scored["score"] + 1e-6) ** 0.7 * (content_scored["cf_score"] + 1e-6) ** 0.3
        )
        scored = content_scored.sort_values("hybrid_score", ascending=False)

        # Simple diversity re-ranking: limit top-N per category
        max_per_category = max(1, top_k // 3)
        seen = {}
        diversified = []
        for _, row in scored.iterrows():
            cat = row.get("category", "unknown")
            count = seen.get(cat, 0)
            if count < max_per_category or len(diversified) < top_k:
                diversified.append(row)
                seen[cat] = count + 1
            if len(diversified) >= top_k * 2:  # Limit processing
                break
        
        scored = pd.DataFrame(diversified) if diversified else scored.head(top_k * 2)
        
        # Ensure required columns exist and select them
        required_cols = [
            "item_id", "name", "category", "subcategory", "price", 
            "dietary_tags", "time_preference", "budget_category", 
            "score", "cf_score", "hybrid_score"
        ]
        
        for col in required_cols:
            if col not in scored.columns:
                scored[col] = None
        
        final_result = scored[required_cols].head(top_k)
        logger.info(f"Generated {len(final_result)} recommendations for user {user_id}")
        return final_result
        
    except Exception as e:
        logger.error(f"Error in recommend_hybrid: {e}")
        return _create_empty_recommendation_df()


def _create_empty_recommendation_df() -> pd.DataFrame:
    """Create empty DataFrame with proper structure for recommendations"""
    return pd.DataFrame(columns=[
        "item_id", "name", "category", "subcategory", "price", 
        "dietary_tags", "time_preference", "budget_category", 
        "score", "cf_score", "hybrid_score"
    ])