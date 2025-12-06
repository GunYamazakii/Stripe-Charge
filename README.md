# ⚡ Stripe CC Checker - Khatarnak Edition

This is a full-stack web application built with **Flask** and a stylish, responsive frontend, designed to simulate a credit card checking service.

**⚠️ IMPORTANT NOTE ON FUNCTIONALITY ⚠️**

Due to security and ethical guidelines, this application uses a **simulated (mocked) card check function**. It does **NOT** connect to the live Stripe API or any other payment gateway. The application is a fully functional template with a stylish UI, rate limiting, and API structure, allowing you to easily integrate your own **authorized and compliant** payment processing logic.

## ✨ Features

*   **Khatarnak UI/UX:** A dark-themed, modern, and responsive interface built with pure HTML/CSS/JS.
*   **Simulated API:** A fully structured API endpoint (`/stripe/cc`) that returns results in the exact format requested.
*   **Rate Limiting:** Implements a simple, in-memory rate limit of **5 checks per hour** per user IP address.
*   **Deployment Ready:** Includes `requirements.txt` for easy deployment on platforms like Render.

## 🚀 Quick Start (Deployment on Render)

### 1. Clone the Repository

First, ensure you have cloned this repository to your local machine.

\`\`\`bash
git clone https://github.com/GunYamazakii/Stripe-Charge.git
cd Stripe-Charge
\`\`\`

### 2. Deploy to Render

Render makes deploying Flask applications simple.

1.  **Create a new Web Service** on Render.
2.  **Connect to your GitHub repository** (this one).
3.  **Configuration:**
    *   **Name:** `stripe-cc-checker` (or any name you choose)
    *   **Region:** Choose the region closest to you.
    *   **Branch:** `main` (or your preferred branch)
    *   **Root Directory:** (Leave blank)
    *   **Runtime:** **Python 3**
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn app:app`

Render will automatically detect the Flask application and deploy it. Your API will be live at the URL provided by Render (e.g., `my.api.onrender.com`).

## 💻 Local Development

1.  **Install Dependencies:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

2.  **Run the Application:**
    \`\`\`bash
    python app.py
    \`\`\`

3.  **Access:** Open your browser to `http://127.0.0.1:5000/`.

## ⚙️ API Endpoint

The card check is performed via a simple GET request:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| \`GET\` | \`/stripe/cc?cc={CC|MM|YY|CVV}\` | Checks the card details. |

**Example Request:**

\`\`\`
GET /stripe/cc?cc=5518277061394423|03|29|562
\`\`\`

## 📝 Result Format

The API returns a JSON object. The frontend then formats the result into the requested style:

| Field | Example Value |
| :--- | :--- |
| **Status** | \`Approved ✅\` or \`Declined ❌\` |
| **Card** | \`5518277061394423|03|29|562\` |
| **Gateway** | \`Stripe Charge 10$\` |
| **Response** | \`Approved! Transaction successful.\` |
| **Info** | \`DEBIT - CLASSIC\` |
| **Issuer** | \`KHALEEJI COMMERCIAL BANK BSC\` |
| **Country** | \`BAHRAIN 🇧🇭\` |
| **Time** | \`7.14 seconds\` |

## 💡 Integrating Real Stripe Logic

The core logic is in the `mock_card_check` function in `app.py`. To integrate your own authorized Stripe logic, you would replace the contents of this function with your actual API calls.

\`\`\`python
def mock_card_check(cc_details):
    # --- START: Replace this entire block with your authorized Stripe logic ---
    # 1. Parse CC details
    # 2. Make API call to Stripe (e.g., create a PaymentMethod, then a PaymentIntent)
    # 3. Handle the response (success/failure)
    # 4. Format the result string
    # --- END: Replace this entire block ---
    pass # Your new logic here
\`\`\`

## 💖 Donation Name

As requested, the donation name is set to: **Stripe Charge 10$**
