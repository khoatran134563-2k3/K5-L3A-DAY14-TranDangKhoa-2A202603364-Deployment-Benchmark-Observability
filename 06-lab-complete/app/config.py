"""
Config — 12-Factor: mọi cấu hình đọc từ biến môi trường.

TODO (tiêu chí 9 — Config từ environment variables):
  • Đọc các biến sau từ môi trường, có giá trị mặc định hợp lý khi chạy local:
      PORT, ENVIRONMENT, AGENT_API_KEY, REDIS_URL,
      RATE_LIMIT_PER_MINUTE, DAILY_BUDGET_USD (hoặc MONTHLY_BUDGET_USD)
  • Không hard-code secret (API key thật, mật khẩu...) trong code.
  • Liệt kê đủ các biến này trong .env.example.
"""
from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv(override=False)

@dataclass
class Settings:
    # TODO: thay các giá trị cố định bên dưới bằng giá trị đọc từ biến môi trường
    port: int = 8000
    environment: str = "development"
    agent_api_key: str = ""
    redis_url: str = ""
    rate_limit_per_minute: int = 10
    daily_budget_usd: float = 1.0



settings = Settings(
    port=int(os.getenv("PORT", "8000")),
    environment=os.getenv("ENVIRONMENT", "development"),

)
