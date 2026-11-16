from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        base_url = "https://stream-us-east-1.getpublica.com/playlist.m3u8?network_id="
        channels_info = []
        checked_count = 0

        # വെർസൽ ടൈംഔട്ട് ഒഴിവാക്കാൻ റേഞ്ച് ഒപ്റ്റിമൈസ് ചെയ്തു (ആവശ്യമെങ്കിൽ ഇത് കൂട്ടാം)
        for net_id in range(1, 1000):
            target_url = base_url + str(net_id)
            checked_count += 1
            try:
                req = urllib.request.Request(
                    target_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=1.5) as response:
                    if response.status == 200:
                        content = response.read().decode('utf-8', errors='ignore')
                        if "#EXTM3U" in content or len(content) > 50:
                            # ചാനലിന്റെ പേര് കണ്ടെത്താൻ ശ്രമിക്കുന്നു
                            channel_name = f"Publica Channel {net_id}"
                            for line in content.splitlines():
                                if "#EXTINF:" in line:
                                    parts = line.split(',')
                                    if len(parts) > 1:
                                        channel_name = parts[-1].strip()
                                        break
                            
                            channels_info.append({
                                "network_id": net_id,
                                "name": channel_name,
                                "stream_url": target_url
                            })
            except Exception:
                pass

        # റെസ്‌പോൺസ് അയക്കുന്നു
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": "success",
            "total_checked": checked_count,
            "active_channels_count": len(channels_info),
            "channels": channels_info
        }
        
        self.wfile.write(json.dumps(response_data, indent=4).encode('utf-8'))
        return
