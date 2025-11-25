import click
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

# List of common payment gateway identifiers (simplified for illustration)
PAYMENT_GATEWAYS = {
    "Stripe": ["stripe.com/v1", "pk_live_", "pk_test_"],
    "PayPal": ["paypal.com/cgi-bin", "www.paypal.com/webscr"],
    "Square": ["square-api.com", "sq-"],
    "Braintree": ["braintreegateway.com", "braintree.js"],
    "Adyen": ["adyen.com", "adyen.js"],
    "Authorize.Net": ["authorize.net", "anet_"],
}

def scan_website(url):
    """Scans a given URL for server info and payment gateway identifiers."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    console.print(f"\n[bold yellow]Scanning URL:[/bold yellow] {url}")
    
    results = {
        "url": url,
        "server_info": "N/A",
        "status_code": "N/A",
        "headers": {},
        "gateways_found": [],
    }

    try:
        # 1. Fetch the page content and headers
        response = requests.get(url, timeout=10, allow_redirects=True)
        results["status_code"] = response.status_code
        results["headers"] = dict(response.headers)
        
        # 2. Extract Server Information from headers
        results["server_info"] = response.headers.get("Server", "Not Disclosed")

        # 3. Scan for Payment Gateways in headers and content
        content = response.text
        
        # Scan headers
        for gateway, identifiers in PAYMENT_GATEWAYS.items():
            for identifier in identifiers:
                # Check in headers (case-insensitive)
                header_match = any(identifier.lower() in str(v).lower() for v in response.headers.values())
                # Check in content
                content_match = identifier in content
                
                if header_match or content_match:
                    if gateway not in results["gateways_found"]:
                        results["gateways_found"].append(gateway)

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error during request:[/bold red] {e}")
        results["server_info"] = f"Request Error: {type(e).__name__}"
        
    return results

def display_results(results):
    """Displays the scan results in a futuristic, detailed format."""
    
    # --- Server Information Panel ---
    server_table = Table(title="[bold cyan]Server Information[/bold cyan]", show_header=True, header_style="bold magenta")
    server_table.add_column("Attribute", style="dim", width=20)
    server_table.add_column("Value", style="green")
    
    server_table.add_row("Target URL", results["url"])
    server_table.add_row("Status Code", str(results["status_code"]))
    server_table.add_row("Server Software", results["server_info"])
    server_table.add_row("Content-Type", results["headers"].get("Content-Type", "N/A"))
    server_table.add_row("X-Powered-By", results["headers"].get("X-Powered-By", "N/A"))
    
    console.print(Panel(server_table, title="[bold white on blue]GATEWAY SCAN REPORT[/bold white on blue]", border_style="blue"))

    # --- Payment Gateway Scan Panel ---
    gateway_status = "[bold red]NO GATEWAYS DETECTED[/bold red]"
    gateway_style = "red"
    
    if results["gateways_found"]:
        gateway_status = f"[bold green]GATEWAYS DETECTED:[/bold green] {', '.join(results['gateways_found'])}"
        gateway_style = "green"
        
    gateway_text = Text(gateway_status, justify="center")
    
    console.print(Panel(gateway_text, title=f"[bold white on {gateway_style}]PAYMENT GATEWAY ANALYSIS[/bold white on {gateway_style}]", border_style=gateway_style))

    # --- Detailed Headers (Optional) ---
    if results["headers"]:
        header_table = Table(title="[bold yellow]HTTP Response Headers[/bold yellow]", show_header=True, header_style="bold yellow")
        header_table.add_column("Header", style="dim", width=20)
        header_table.add_column("Value", style="white")
        
        for k, v in results["headers"].items():
            header_table.add_row(k, v)
            
        console.print(Panel(header_table, title="[bold white on yellow]RAW DATA LOG[/bold white on yellow]", border_style="yellow"))


@click.command()
@click.argument("url")
def cli(url):
    """
    gatewaysscan: A futuristic tool to scan websites for server and payment gateway information.
    
    Example: gatewaysscan https://example.com
    """
    console.print(Panel(
        Text("GatewaysScan v0.1.0 - Initiating Advanced Web Analysis", justify="center", style="bold bright_white"),
        border_style="bright_white",
        title_align="left",
        subtitle_align="right",
        title="[bold green]START[/bold green]",
        subtitle="[bold red]DIWAZZ[/bold red]"
    ))
    
    results = scan_website(url)
    display_results(results)
    
    console.print(Panel(
        Text("Analysis Complete. Review Report Above.", justify="center", style="bold bright_white"),
        border_style="bright_white",
        title_align="left",
        subtitle_align="right",
        title="[bold red]END[/bold red]",
        subtitle="[bold green]MANUS[/bold green]"
    ))

if __name__ == "__main__":
    cli()
