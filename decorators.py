from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar
import logging
import asyncio
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Callable)

def with_cache(ttl_seconds: int = 300):
    """Cache function results for specified duration"""
    def decorator(func: T) -> T:
        cache: Dict[str, Any] = {}
        cache_ttl: Dict[str, datetime] = {}
        
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check cache
            if cache_key in cache and datetime.now() < cache_ttl[cache_key]:
                logger.debug(f"Cache hit for {func.__name__}")
                return cache[cache_key]
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Update cache
            cache[cache_key] = result
            cache_ttl[cache_key] = datetime.now() + timedelta(seconds=ttl_seconds)
            
            return result
        return wrapper
    return decorator

# TODO: Use Redis in a multi-process environment
# def with_cache(ttl_seconds: int = 300):
#     """Cache function results using Redis"""
#     def decorator(func: T) -> T:
#         redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
#         @wraps(func)
#         async def wrapper(*args, **kwargs) -> Any:
#             cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
#             # Check Redis cache
#             cached = redis_client.get(cache_key)
#             if cached:
#                 logger.debug(f"Cache hit for {func.__name__}")
#                 return json.loads(cached)
            
#             # Execute function
#             result = await func(*args, **kwargs)
            
#             # Update Redis cache
#             redis_client.setex(
#                 cache_key,
#                 ttl_seconds,
#                 json.dumps(result)
#             )
            
#             return result
#         return wrapper
#     return decorator

def with_retry(max_retries: int = 3, delay: float = 1.0):
    """Retry function execution on failure"""
    def decorator(func: T) -> T:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        delay_time = delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"Retry {attempt + 1}/{max_retries} for {func.__name__} after {delay_time}s")
                        await asyncio.sleep(delay_time)
            
            logger.error(f"All retries failed for {func.__name__}: {last_error}")
            raise last_error
        return wrapper
    return decorator

def monitor_execution():
    """Monitor function execution time and status"""
    def decorator(func: T) -> T:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = datetime.now()
            try:
                result = await func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"{func.__name__} executed successfully in {execution_time:.2f}s")
                return result
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"{func.__name__} failed after {execution_time:.2f}s: {e}")
                raise
        return wrapper
    return decorator