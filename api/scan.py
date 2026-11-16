import urllib.request
import urllib.error

# ബേസ് ലിങ്ക് (network_id ഒഴികെയുള്ള ഭാഗം)
base_url = "https://stream-us-east-1.getpublica.com/playlist.m3u8?network_id="

print("Scanning Publica Network IDs... Please wait.\n")

valid_channels = 0
checked_count = 0

# 1 മുതൽ 2000 വരെയുള്ള ഐഡികൾ ചെക്ക് ചെയ്യാൻ (നിനക്ക് ആവശ്യമുള്ള റേഞ്ച് ഇവിടെ മാറ്റാം)
for net_id in range(1, 1500):
    target_url = base_url + str(net_id)
    checked_count += 1
    
    try:
        req = urllib.request.Request(
            target_url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        # ലിങ്ക് വർക്ക് ചെയ്യുന്നുണ്ടോ എന്ന് നോക്കാൻ ഓപ്പൺ ചെയ്യുന്നു
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                content = response.read().decode('utf-8', errors='ignore')
                # ഇതൊരു വാലിഡ് പ്ലേലിസ്റ്റ് ആണോ എന്ന് ചെക്ക് ചെയ്യാൻ
                if "#EXTM3U" in content or "m3u8" in content or len(content) > 50:
                    valid_channels += [net_id]
                    print(f"[+] FOUND! Network ID: {net_id} is ACTIVE.")
    except Exception as e:
        # ഡെഡ് ആയതോ കിട്ടാത്തതോ ആയ ഐഡികൾ സൈലന്റ് ആയി സ്കിപ്പ് ചെയ്യും
        pass

print("\n--- SCAN COMPLETE ---")
print(f"Total Checked: {checked_count}")
print(f"Total Active Channel/Network IDs Found: {len(valid_channels)}")
print(f"Working IDs List: {valid_channels}")
