from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        base_url = "https://stream-us-east-1.getpublica.com/playlist.m3u8?network_id="
        valid_channels = []
        checked_count = 0

        # ആവശ്യാനുസരണം റേഞ്ച് കൂട്ടുകയോ കുറയ്ക്കുകയോ ചെയ്യാം (ഉദാഹരണത്തിന് 1 മുതൽ 150 വരെ)
        for net_id in range(1, 150):
            target_url = base_url + str(net_id)
            checked_count += 1
            try:
                req = urllib.request.Request(
                    target_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=2) as response:
                    if response.status == 200:
                        content = response.read().decode('utf-8', errors='ignore')
                        if "#EXTM3U" in content or len(content) > 50:
                            valid_channels.append(net_id)
            except Exception:
                pass

        # റെസ്‍പോൺസ് JSON ഫോർമാറ്റിൽ വെർസലിലേക്ക് അയക്കുന്നു
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": "success",
            "total_checked": checked_count,
            "active_network_ids": valid_channels
        }
        
        self.wfile.write(json.dumps(response_data, indent=4).encode('utf-8'))
        return
