import sys
import os
import threading
import time
from fastapi import FastAPI, Query

# ফাইল পাথ ফিক্স করা যাতে black9 খুঁজে পায়
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from black9 import ghost_pakcet
except ImportError:
    ghost_pakcet = None

app = FastAPI()

# আপনার একাউন্ট লিস্ট এবং কানেক্টেড ক্লায়েন্ট
ACCOUNTS = [] # এখানে আপনার আইডি পাসওয়ার্ড এর ডিকশনারি থাকবে
connected_clients = {}

@app.get("/")
def home():
    return {"status": "Gateway Online", "accounts_connected": len(connected_clients)}

@app.get("/ghost-join")
async def ghost_join_api(
    code: str = Query(..., description="Team Code"),
    name: str = Query("yeamin", description="Ghost Name")
):
    if not ghost_pakcet:
        return {"error": "black9.py module not found or failed to load"}

    active_clients = [c for c in connected_clients.values() if hasattr(c, 'CliEnts2')]
    
    if not active_clients:
        # টেস্ট করার জন্য যদি একাউন্ট কানেক্ট না থাকে
        return {"status": "warning", "message": "No accounts connected to gateway", "team": code, "name": name}

    def attack(client, t_code, g_name):
        try:
            for _ in range(30):
                packet = ghost_pakcet(str(t_code), str(g_name), "1", client.key, client.iv)
                client.CliEnts2.send(packet)
                time.sleep(0.05)
        except:
            pass

    for client in active_clients:
        threading.Thread(target=attack, args=(client, code, name), daemon=True).start()

    return {"status": "Attack Sent", "team": code, "ghost": name}

# সার্ভার স্টার্ট হলে আইডি কানেক্ট করার চেষ্টা করবে (Vercel-এ এটি লিমিটেড)
@app.on_event("startup")
def startup():
    # এখানে আপনার আইডি কানেকশন লজিক বা StarT_SerVer() কল করতে পারেন
    pass
