import sys
import os
import threading
import time
from fastapi import FastAPI, Query
import uvicorn

# ফাইল পাথ ঠিক করা যাতে লোকাল মডিউলগুলো পায়
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# মডিউল ইমপোর্ট করা (black9.py আপনার বারকেল ইঞ্জিন)
try:
    from black9 import ghost_pakcet
except ImportError:
    ghost_pakcet = None

app = FastAPI()

# এখানে আপনার আইডিগুলো কানেক্টেড থাকবে
connected_clients = {} 

@app.get("/")
def home():
    return {
        "status": "Online", 
        "name": "yeamin", 
        "connected_accounts": len(connected_clients),
        "gateway": "Hugging Face Space"
    }

@app.get("/ghost-join")
def ghost_join_api(
    code: str = Query(..., description="টিম কোড দিন"),
    name: str = Query("yeamin", description="ঘোস্ট প্লেয়ারের নাম"),
    count: int = Query(50, description="কতবার প্যাকেট যাবে")
):
    if not ghost_pakcet:
        return {"status": "error", "message": "black9.py ফাইলটি পাওয়া যায়নি!"}

    # চেক করা হচ্ছে গেটওয়ে (CliEnts2) কানেক্টেড কি না
    active_clients = [c for c in connected_clients.values() if hasattr(c, 'CliEnts2')]
    
    if not active_clients:
        return {"status": "warning", "message": "কোনো আইডি গেটওয়েতে কানেক্ট নেই। আগে আইডি লগইন করুন।"}

    def attack_task(client, t_code, g_name, p_count):
        try:
            for _ in range(p_count):
                # বারকেল এরিয়া: প্যাকেট তৈরি
                packet = ghost_pakcet(str(t_code), str(g_name), "1", client.key, client.iv)
                # গেট হোম: সকেট দিয়ে গেমে পাঠানো
                if client.CliEnts2:
                    client.CliEnts2.send(packet)
                time.sleep(0.05)
        except Exception as e:
            print(f"Error: {e}")

    # প্রতিটি আইডির জন্য আলাদা থ্রেডে কাজ শুরু
    for client in active_clients:
        threading.Thread(target=attack_task, args=(client, code, name, count), daemon=True).start()

    return {
        "status": "Attack Started",
        "target_team": code,
        "ghost_name": name,
        "accounts_used": len(active_clients)
    }

if __name__ == "__main__":
    # Hugging Face ডিফল্ট পোর্ট ৭৮৬০ ব্যবহার করে
    uvicorn.run(app, host="0.0.0.0", port=7860)
