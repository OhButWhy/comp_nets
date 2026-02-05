import subprocess
import re
import pandas as pd


def hunt(doms):
    results = []
    for domain in doms:
        result = subprocess.run(f"ping -n 4 {domain}", shell=True,
                                capture_output=True,
                                text=True, encoding='cp866')
        output = result.stdout

        ttl_match = re.search(r'TTL=(\d+)', output)
        ttl = int(ttl_match.group(1)) if ttl_match else None

        loss_match = re.search(r'потеряно = (\d+)', output)
        loss = int(loss_match.group(1)) if loss_match else None

        rtt_match = re.search(r'Среднее = (\d+)', output)
        rtt = int(rtt_match.group(1)) if rtt_match else None

        real_match = re.search(r'\[([^\]]+)\]', output)
        real = real_match.group(1) if real_match else None

        results.append({
            "Domain": domain,
            "Adress": real,
            "TTL": ttl,
            "Loss": loss,
            "RTT": rtt
        })

    df = pd.DataFrame(results)
    df.to_csv("domainhunt_results.csv", index=False)


if __name__ == "__main__":
    domains = ["google.com", "youtube.com", "facebook.com", "twitter.com",
               "instagram.com", "wikipedia.org", "vk.com",
               "steamcommunity.com", "scpfoundation.net", "yandex.ru"]
    hunt(domains)
