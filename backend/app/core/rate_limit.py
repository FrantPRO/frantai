"""
Rate limiting utilities using slowapi.
"""

import hashlib

from slowapi import Limiter
from slowapi.util import get_remote_address


def get_rate_limiter() -> Limiter:
    """Get rate limiter instance"""
    return Limiter(key_func=get_remote_address)


def hash_ip(ip: str) -> str:
    """Hash IP address for privacy"""
    return hashlib.sha256(ip.encode()).hexdigest()
