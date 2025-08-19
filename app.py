# test_openbb.py - sprawdź czy OpenBB działa
from openbb import obb

# Ustaw domyślny provider na yfinance (darmowy)
obb.user.preferences.output_type = "dataframe"
obb.user.preferences.provider = "yfinance"

# Test - pobierz dane Apple
data = obb.equity.price.historical("AAPL", provider="yfinance")
print(data)