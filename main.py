from ta.momentum import RSIIndicator
import yfinance as yf
import matplotlib.pyplot as plt

stock = yf.Ticker("TCS.NS")

data = stock.history(period="6mo")

data["Daily_Return"] = data["Close"].pct_change() * 100

volatility = data["Daily_Return"].std()

average_volume = data["Volume"].mean()

latest_volume = data["Volume"].iloc[-1]

volume_ratio = latest_volume / average_volume

if volume_ratio >= 2:
    print("🚨 ALERT: Unusual Volume Detected!")
else:
    print("🟢 Normal Volume")

latest_return = data["Daily_Return"].iloc[-1]

if latest_return >= 3:
    print("🚨 ALERT: Strong Upward Price Movement!")
elif latest_return <= -3:
    print("🚨 ALERT: Strong Downward Price Movement!")
else:
    print("🟢 Normal Price Movement")

if abs(latest_return) >= 3 and volume_ratio >= 2:
    print("\n🚨 HIGH IMPACT CONDITION DETECTED!")
    print("Reason: Strong price movement + unusual volume")

elif abs(latest_return) >= 3:
    print("\n🟡 PRICE MOVEMENT ALERT")
    print("Reason: Strong price movement")

elif volume_ratio >= 2:
    print("\n🟡 VOLUME ALERT")
    print("Reason: Unusual trading volume")

else:
    print("\n🟢 STOCK CONDITION: NORMAL")

data["RSI"] = RSIIndicator(
    close=data["Close"],
    window=14
).rsi()

latest_rsi = data["RSI"].iloc[-1]

print("\nLatest RSI:", latest_rsi)

reasons = []

condition_score = 0

if latest_rsi < 30:
    condition_score += 1
    reasons.append("RSI is in oversold zone")
elif latest_rsi > 70:
    condition_score -= 1
    reasons.append("RSI is in overbought zone")

if latest_return >= 3:
    condition_score += 1
elif latest_return <= -3:
    condition_score -= 1

if volume_ratio >= 2:
    condition_score += 1
    reasons.append("Unusual trading volume detected")


if condition_score >= 2:
    print("🟢 POSITIVE STOCK CONDITION")
elif condition_score <= -2:
    print("🔴 NEGATIVE STOCK CONDITION")
else:
    print("🟡 NORMAL / WATCH CONDITION")

data["MA20"] = data["Close"].rolling(window=20).mean()

latest_price = data["Close"].iloc[-1]
latest_ma20 = data["MA20"].iloc[-1]

print("\nLatest Price:", latest_price)
print("20-Day Moving Average:", latest_ma20)

if latest_price > latest_ma20:
    print("🟢 Price is above 20-Day MA")
else:
    print("🔴 Price is below 20-Day MA")

if latest_price > latest_ma20:
    condition_score += 1
elif latest_price < latest_ma20:
    condition_score -= 1
    reasons.append("Price is below 20-Day MA")

if condition_score >= 2:
    print("🟢 POSITIVE STOCK CONDITION")
elif condition_score <= -2:
    print("🔴 NEGATIVE STOCK CONDITION")
else:
    print("🟡 NORMAL / WATCH CONDITION")

data["MA50"] = data["Close"].rolling(window=50).mean()

latest_ma50 = data["MA50"].iloc[-1]

print("\n50-Day Moving Average:", latest_ma50)


if latest_price > latest_ma50:
    print("🟢 Price is above 50-Day MA")
else:
    print("🔴 Price is below 50-Day MA")
    reasons.append("Price is below 50-Day MA")


if latest_price > latest_ma20 and latest_price > latest_ma50:
    trend = "UPTREND"
elif latest_price < latest_ma20 and latest_price < latest_ma50:
    trend = "DOWNTREND"
else:
    trend = "SIDEWAYS"

print("\nCurrent Trend:", trend)

if trend == "UPTREND":
    condition_score += 1
elif trend == "DOWNTREND":
    condition_score -= 1
    reasons.append("Current trend is DOWNTREND")

if condition_score >= 2:
    print("🟢 POSITIVE STOCK CONDITION")
elif condition_score <= -2:
    print("🔴 NEGATIVE STOCK CONDITION")
else:
    print("🟡 NORMAL / WATCH CONDITION")

if condition_score <= -3:
    strength = "STRONG NEGATIVE"
elif condition_score == -2:
    strength = "MODERATE NEGATIVE"
elif condition_score == -1:
    strength = "WEAK NEGATIVE"
elif condition_score == 0:
    strength = "NEUTRAL"
elif condition_score == 1:
    strength = "WEAK POSITIVE"
elif condition_score == 2:
    strength = "MODERATE POSITIVE"
else:
    strength = "STRONG POSITIVE"


if latest_price > latest_ma50:
    ma50_signal = 1
else:
    ma50_signal = -1


print("\n========== STOCKSENSE AI REPORT ==========")

print("Stock: TCS")
print("Price:", latest_price)
print("Trend:", trend)
print("Condition Score:", condition_score)
print("Volatility:", round(volatility, 2), "%")

print("\nReasons:")
for reason in reasons:
    print("-", reason)
if condition_score >= 2:
    condition = "POSITIVE"
elif condition_score <= -2:
    condition = "NEGATIVE"
else:
    condition = "NORMAL / WATCH"

print("\nCondition:", condition)
print("==========================================")