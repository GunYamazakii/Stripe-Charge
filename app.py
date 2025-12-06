import time
import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Simple in-memory rate limiting (IP-based)
# Stores {ip_address: [(timestamp, count), ...]}
RATE_LIMIT_WINDOW_SECONDS = 3600 # 1 hour
MAX_REQUESTS_PER_WINDOW = 5
rate_limit_store = {}

def get_client_ip():
    # Use X-Forwarded-For if running behind a proxy (like Render)
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def check_rate_limit(ip):
    current_time = time.time()
    
    # Clean up old entries
    if ip in rate_limit_store:
        rate_limit_store[ip] = [
            (t, c) for t, c in rate_limit_store[ip] 
            if current_time - t < RATE_LIMIT_WINDOW_SECONDS
        ]
    
    # Check current count
    current_count = sum(c for t, c in rate_limit_store.get(ip, []))
    
    if current_count >= MAX_REQUESTS_PER_WINDOW:
        return False, MAX_REQUESTS_PER_WINDOW - current_count
    
    # Add new request
    rate_limit_store.setdefault(ip, []).append((current_time, 1))
    return True, MAX_REQUESTS_PER_WINDOW - (current_count + 1)

def mock_card_check(cc_details):
    """
    Simulates the card check process.
    NOTE: This function is a MOCK and does not perform any live transaction or
    external API call to Stripe or any other payment processor.
    """
    start_time = time.time()
    
    # Parse CC details
    try:
        card, month, year, cvv = cc_details.split('|')
    except ValueError:
        return "Invalid CC format. Use CC|MM|YY|CVV.", "error"

    # --- Mock Data Generation ---
    # Randomly decide on status (e.g., 20% Approved, 80% Declined)
    status = random.choices(["Approved", "Declined"], weights=[20, 80], k=1)[0]
    
    # Mock Issuer and Country data
    mock_issuers = ["KHALEEJI COMMERCIAL BANK BSC", "BANK OF AMERICA", "CHASE BANK", "WELLS FARGO"]
    mock_countries = ["BAHRAIN 🇧🇭", "UNITED STATES 🇺🇸", "CANADA 🇨🇦", "UNITED KINGDOM 🇬🇧"]
    mock_info = ["DEBIT - CLASSIC", "CREDIT - GOLD", "PREPAID - PLATINUM"]
    
    issuer = random.choice(mock_issuers)
    country = random.choice(mock_countries)
    info = random.choice(mock_info)
    
    # Mock Response
    if status == "Approved":
        response_text = "Approved! Transaction successful."
        status_emoji = "✅"
    else:
        response_text = random.choice(["Declined by issuer.", "Insufficient funds.", "Card expired.", "Transaction not permitted."])
        status_emoji = "❌"

    end_time = time.time()
    time_taken = end_time - start_time

    # Format the result string as requested by the user
    result_text = f"""
    **{status.upper()} {status_emoji}**

    𝗖𝗮𝗿𝗱: {card}|{month}|{year}|{cvv}
    𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Stripe Charge 10$ 
    𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {response_text}

    𝗜𝗻𝗳𝗼: {info}
    𝐈𝐬𝐬𝐮𝐞𝐫: {issuer}
    𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country}

    𝗧𝗶𝗺𝗲: {time_taken:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
    """
    
    return result_text, status.lower()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stripe/cc', methods=['GET'])
def check_cc():
    cc_details = request.args.get('cc')
    
    if not cc_details:
        return jsonify({"status": "error", "message": "Missing 'cc' parameter."}), 400

    ip = get_client_ip()
    can_check, remaining = check_rate_limit(ip)

    if not can_check:
        return jsonify({
            "status": "rate_limited",
            "message": f"Rate limit exceeded. You can only check {MAX_REQUESTS_PER_WINDOW} cards per hour. Try again later.",
            "remaining": remaining
        }), 429

    result_text, status = mock_card_check(cc_details)
    
    return jsonify({
        "status": status,
        "result": result_text,
        "remaining_checks": remaining
    })

if __name__ == '__main__':
    # Use a port suitable for Render deployment
    app.run(host='0.0.0.0', port=5000)
