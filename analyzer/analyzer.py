import os
import subprocess
import email
import re

def extract_urls_from_eml(path):
    with open(path, 'rb') as f:
        msg = email.message_from_binary_file(f)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    body = part.get_payload(decode=True).decode(errors='ignore')
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')
        return re.findall(r'https?://[^\s"<>]+', body)

def analyze_url(phish_url, scan_id, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"[+] Scanning URL: {phish_url}")
    log = subprocess.getoutput(f"curl -I {phish_url}")
    with open(f"{output_dir}/{scan_id}_log.txt", "w") as f:
        f.write(log)

    subprocess.run(f"timeout 10 tshark -i any -a duration:10 -w {output_dir}/{scan_id}.pcapng", shell=True)
    return f"{scan_id}_log.txt", f"{scan_id}.pcapng"

def analyze_eml_file(eml_path, scan_id, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    log = subprocess.getoutput(f"clamscan {eml_path}")
    with open(f"{output_dir}/{scan_id}_log.txt", "w") as f:
        f.write(log)

    urls = extract_urls_from_eml(eml_path)
    with open(f"{output_dir}/{scan_id}_urls.txt", "w") as f:
        for url in urls:
            f.write(url + "\n")

    subprocess.run(f"timeout 10 tshark -i any -a duration:10 -w {output_dir}/{scan_id}.pcapng", shell=True)
    return f"{scan_id}_log.txt", f"{scan_id}.pcapng", urls
