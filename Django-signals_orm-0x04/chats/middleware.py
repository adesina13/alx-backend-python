# chats/middleware.py
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict

# -------------------------------
# 1. Logging User Requests
# -------------------------------
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("requests.log", "a") as log_file:
            log_file.write(log_message)
        return self.get_response(request)


# -------------------------------
# 2. Restrict Chat Access by Time
# -------------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 6AM (6) and 9PM (21)
        if not (6 <= current_hour < 21):
            return HttpResponseForbidden("Chat access allowed only between 6AM and 9PM.")
        return self.get_response(request)


# -------------------------------
# 3. Limit Chat Messages per IP (Offensive/Spam)
# -------------------------------
class OffensiveLanguageMiddleware:
    # track requests per IP
    ip_requests = defaultdict(list)
    LIMIT = 5       # messages
    WINDOW = 60     # seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chats/"):
            ip = self.get_client_ip(request)
            now = time.time()
            # remove requests older than WINDOW
            self.ip_requests[ip] = [t for t in self.ip_requests[ip] if now - t < self.WINDOW]
            if len(self.ip_requests[ip]) >= self.LIMIT:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")
            self.ip_requests[ip].append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


# -------------------------------
# 4. Role-based Permissions Middleware
# -------------------------------
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: block non-admin/non-moderator users from admin endpoints
        if request.path.startswith("/chats/admin/"):
            if not request.user.is_authenticated or request.user.role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return self.get_response(request)
