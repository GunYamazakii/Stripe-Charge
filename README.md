# 🌌 GatewaysScan: Quantum Web Reconnaissance CLI 🌌

[![PyPI version](https://badge.fury.io/py/gatewaysscan.svg)](https://badge.fury.io/py/gatewaysscan)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

## 🚀 Project Genesis

The **GatewaysScan** CLI is a next-generation tool designed for rapid, non-intrusive web reconnaissance. It leverages advanced pattern matching and HTTP header analysis to instantly identify the underlying server infrastructure and, critically, the presence of major payment gateway integrations on any target URL.

This project transforms the original `Stripe-Charge` repository into a powerful, open-source utility, aligning with the future of digital security and development.

## ✨ Futuristic Feature Matrix

| Feature | Description | Status |
| :--- | :--- | :--- |
| **Server Fingerprinting** | Extracts and reports server software, X-Powered-By headers, and other infrastructure metadata. | ✅ Operational |
| **Payment Gateway Detection** | Scans for known identifiers (API keys, script URLs) for major gateways like Stripe, PayPal, Square, and more. | ✅ Operational |
| **Rich CLI Output** | Utilizes the `rich` library for a visually stunning, futuristic, and color-coded terminal experience. | ✅ Operational |
| **Dependency-Light** | Built on standard Python libraries (`requests`, `click`, `rich`) for fast, reliable execution. | ✅ Operational |

## ⚙️ Installation: Initiating the Module

GatewaysScan is designed to be installed globally via `pip`, making it instantly accessible from any terminal session.

```bash
# Ensure you have Python 3.8+
pip install gatewaysscan
```

## 💻 Usage: Executing the Scan Protocol

To initiate a scan, simply pass the target URL as an argument to the `gatewaysscan` command. The tool automatically handles protocol prefixes (`http://` or `https://`).

```bash
# Scan a target website
gatewaysscan https://www.example.com
```

### 📡 Animated Scan Sequence (Simulated)

The CLI provides a dynamic, real-time feel to the analysis process:

```
[00:00:01] █▒▒▒▒▒▒▒▒▒ Initializing Quantum HTTP Handshake...
[00:00:02] ████▒▒▒▒▒▒ Analyzing Header Signatures...
[00:00:03] ███████▒▒▒ Cross-referencing Gateway Database...
[00:00:04] ██████████ Report Generation Complete.
```

## 📊 Sample Output (Rich CLI)

The output is structured into high-contrast panels for maximum readability and information density.

```
╭──────────────────────────────────────────────────────────────────────────────╮
│                 [bold white on blue]GATEWAY SCAN REPORT[/bold white on blue]                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ [bold cyan]Server Information[/bold cyan]                                     │
│ ╭──────────────────────┬───────────────────────────────────────────────────╮ │
│ │ Attribute            │ Value                                             │ │
│ ├──────────────────────┼───────────────────────────────────────────────────┤ │
│ │ Target URL           │ https://stripe.com                                │ │
│ │ Status Code          │ 200                                               │ │
│ │ Server Software      │ cloudflare                                        │ │
│ │ Content-Type         │ text/html; charset=utf-8                          │ │
│ │ X-Powered-By         │ N/A                                               │ │
│ ╰──────────────────────┴───────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────╮
│             [bold white on green]PAYMENT GATEWAY ANALYSIS[/bold white on green]             │
├──────────────────────────────────────────────────────────────────────────────┤
│        [bold green]GATEWAYS DETECTED:[/bold green] Stripe, PayPal, Braintree        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## 👤 Author and Contribution

This project is maintained and enhanced by the community, with initial development driven by **@diwazz**.

*   **Author:** @diwazz
*   **Repository:** [GunYamazakii/Stripe-Charge](https://github.com/GunYamazakii/Stripe-Charge)

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
