import socket
import time
from concurrent.futures import ThreadPoolExecutor

# Get target
target = input("Enter Target IP/Domain: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("[-] Invalid Host")
    exit()

# Get port range
try:
    start_port = int(input("Enter Start Port: "))
    end_port = int(input("Enter End Port: "))
except ValueError:
    print("[-] Please enter valid port numbers")
    exit()

print(f"\n[*] Scanning {target} ({target_ip})")
print(f"[*] Port Range: {start_port}-{end_port}\n")

open_ports = []

start_time = time.time()


def scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            output = f"[OPEN] Port {port} - {service}"
            print(output)

            open_ports.append(output)

        sock.close()

    except Exception:
        pass


# Multithreaded scanning
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan, range(start_port, end_port + 1))

# Save results
with open("results.txt", "w") as file:
    file.write(f"Scan Results for {target} ({target_ip})\n")
    file.write("=" * 50 + "\n\n")

    if open_ports:
        for port in open_ports:
            file.write(port + "\n")
    else:
        file.write("No open ports found.\n")

end_time = time.time()

print("\n" + "=" * 50)
print("[+] Scan Completed")

if open_ports:
    print(f"[+] Open Ports Found: {len(open_ports)}")
else:
    print("[+] No Open Ports Found")

print(f"[+] Time Taken: {end_time - start_time:.2f} seconds")
print("[+] Results saved to results.txt")
print("=" * 50)