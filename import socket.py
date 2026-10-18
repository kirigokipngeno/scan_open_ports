import socket
from concurrent.futures import ThreadPoolExecutor

target = "127.0.0.1"
common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 1433, 3306, 3389, 8080, 8443]

def scan_port(port):
    """Scans a single port and returns a result string if open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            try:
                service_name = socket.getservbyport(port, "tcp")
            except (OSError, OverflowError):
                service_name = "Unknown Service"
            
            output = f"Port {port} is open ({service_name})"
            print(output)  # Still print to the console so you see progress
            return output
    return None

def main():
    filename = "scan_results.txt"
    print(f"Scanning common ports on {target} for services...")
    
    # We use executor.map to gather the return values from scan_port
    with ThreadPoolExecutor(max_workers=len(common_ports)) as executor:
        results = executor.map(scan_port, common_ports)
    
    # Filter out the None values (closed ports) leaving only open port text strings
    open_ports = [r for r in results if r is not None]
    
    # Write the results to the file
    with open(filename, "w") as f:
        f.write(f"Scan Results for {target}\n")
        f.write("=" * 30 + "\n")
        if open_ports:
            for item in open_ports:
                f.write(item + "\n")
        else:
            f.write("No open ports found.\n")
            
    print(f"\nScan complete. Results successfully saved to {filename}")

if __name__ == "__main__":
    main()
