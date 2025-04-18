import os
import uuid
import json
import re
import email
from flask import Flask, request, render_template
from dotenv import load_dotenv
from analyzer import analyze_url, analyze_eml_file
from vt import scan_url
from db import init_db, log_scan_result, get_history

load_dotenv()

UPLOAD_DIR = "static/results"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


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


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    vt_link = []
    scan_logs = []
    pcap_files = []

    if request.method == "POST":
        analysis_id = str(uuid.uuid4())
        file = request.files.get("file")
        url = request.form.get("url")
        run_virustotal = request.form.get("vt")

        # --------------------------------
        # 📎 .eml File Upload
        # --------------------------------
        if file:
            filename = f"{analysis_id}.eml"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Analyze eml file itself
            eml_log, eml_pcap, extracted_urls = analyze_eml_file(file_path, analysis_id, UPLOAD_DIR)
            scan_logs.append(eml_log)
            if eml_pcap:
                pcap_files.append(eml_pcap)
            log_scan_result(analysis_id, filename, eml_log, eml_pcap, "", "")

            # Extract and analyze embedded URLs
            output += f"[+] Extracted {len(extracted_urls)} URLs:\n"
            for link in extracted_urls:
                output += f"   - {link}\n"

            for idx, link in enumerate(extracted_urls):
                sub_id = f"{analysis_id}_{idx}"
                log_name, pcap_name = analyze_url(link, sub_id, UPLOAD_DIR)

                # VirusTotal
                vt_json = None
                if run_virustotal:
                    try:
                        vt_json = scan_url(link)
                        vt_id = vt_json['data']['id'].removeprefix('u-').split('-')[0]
                        vt_link.append(f"https://www.virustotal.com/gui/url/{vt_id}/detection")
                    except Exception as e:
                        vt_link.append(f"[VirusTotal error] {e}")

                # Save metadata
                log_scan_result(
                    sub_id,
                    link,
                    log_name,
                    pcap_name,
                    json.dumps(vt_json) if vt_json else "",
                    vt_link[-1] if vt_link else None
                )

                scan_logs.append(log_name)
                if pcap_name:
                    pcap_files.append(pcap_name)

                # Read scan result into output
                log_path = os.path.join(UPLOAD_DIR, log_name)
                if os.path.exists(log_path):
                    with open(log_path) as f:
                        output += f"\n--- {link} ---\n" + f.read()

        # --------------------------------
        # 🔗 URL Paste
        # --------------------------------
        elif url:
            log_name, pcap_name = analyze_url(url, analysis_id, UPLOAD_DIR)

            vt_json = None
            if run_virustotal:
                try:
                    vt_json = scan_url(url)
                    vt_id = vt_json['data']['id'].removeprefix('u-').split('-')[0]
                    vt_link = [f"https://www.virustotal.com/gui/url/{vt_id}/detection"]
                except Exception as e:
                    vt_link = [f"[VirusTotal error] {e}"]

            log_scan_result(
                analysis_id,
                url,
                log_name,
                pcap_name,
                json.dumps(vt_json) if vt_json else "",
                vt_link[0] if vt_link else None
            )

            log_path = os.path.join(UPLOAD_DIR, log_name)
            if os.path.exists(log_path):
                with open(log_path) as f:
                    output = f.read()

            scan_logs.append(log_name)
            if pcap_name:
                pcap_files.append(pcap_name)

        # --------------------------------
        # 🚫 No Input
        # --------------------------------
        else:
            output = "[-] No input provided."

    return render_template(
        "index.html",
        output=output,
        vt_result="",  # Optional if removed from HTML
        vt_link=vt_link,
        scan_logs=scan_logs,
        pcap_files=pcap_files
    )


@app.route("/history")
def history():
    results = get_history()
    return render_template("history.html", results=results)


if __name__ == "__main__":
    print("✅ Flask app is starting...")
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
