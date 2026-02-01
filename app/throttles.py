# app/throttles.py
# Fixed Window Rate Limiting
from rest_framework.throttling import UserRateThrottle

class PurchaseRateThrottle(UserRateThrottle):
    scope = 'purchase'


# Custom Token Bucket Throttle

# import time
# from django.core.cache import cache
# from rest_framework.throttling import BaseThrottle


# class TokenBucketThrottle(BaseThrottle):
#     rate = 5          # max tokens
#     per = 60          # per 60 seconds

#     def get_cache_key(self, request, view):
#         if request.user.is_authenticated:
#             return f"token_bucket_{request.user.id}"
#         return f"token_bucket_{self.get_ident(request)}"

#     def allow_request(self, request, view):
#         key = self.get_cache_key(request, view)
#         now = time.time()

#         data = cache.get(key)

#         if data is None:
#             # bucket full
#             cache.set(key, {
#                 "tokens": self.rate - 1,
#                 "last": now
#             }, timeout=self.per)
#             return True

#         tokens = data["tokens"]
#         last = data["last"]

#         # refill logic
#         elapsed = now - last
#         refill = int(elapsed * (self.rate / self.per))
#         tokens = min(self.rate, tokens + refill)

#         if tokens <= 0:
#             self.wait_time = int(self.per / self.rate)
#             return False

#         tokens -= 1
#         cache.set(key, {
#             "tokens": tokens,
#             "last": now
#         }, timeout=self.per)

#         return True

#     def wait(self):
#         return getattr(self, "wait_time", None)
