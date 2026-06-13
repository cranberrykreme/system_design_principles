from fastapi import Request

def get_rate_limiter(request: Request):
    return request.app.state.rate_limiter