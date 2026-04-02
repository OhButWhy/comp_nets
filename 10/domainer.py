import subprocess
import socket
import pandas as pd


def resolve_ips(domain):
    try:
        ips = socket.gethostbyname_ex(domain)[2]
    except socket.gaierror:
        return []

    unique_ips = []
    for ip in ips:
        if ip not in unique_ips:
            unique_ips.append(ip)
    return unique_ips


def get_traceroute(ip):
    result = subprocess.run(f"tracert -d {ip}", shell=True,
                            capture_output=True,
                            text=True, encoding='cp866')
    return result.stdout


def hunt(domains):
    results = []

    for domain in domains:
        ips = resolve_ips(domain)

        if not ips:
            results.append({
                "Domain": domain,
                "IP": None,
                "Traceroute": "DNS query failed"
            })
            continue

        for ip in ips:
            trace = get_traceroute(ip)
            results.append({
                "Domain": domain,
                "IP": ip,
                "Traceroute": trace.replace('\n', ' | ').strip()
            })

    df = pd.DataFrame(results)
    df.to_csv("traceroute_results.csv", index=False)


if __name__ == "__main__":
    with open("domains.txt", "r", encoding="utf-8") as f:
        domains = [line.strip() for line in f if line.strip()]

    hunt(domains)
