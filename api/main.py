from fastapi import FastAPI, Query
import threading
import time
import os
from black9 import ghost_pakcet # আপনার বারকেল মডিউল
# অন্যান্য প্রয়োজনীয় মডিউল ইমপোর্ট করুন (যেমন: byte, xHeaders)

app = FastAPI()

# গ্লোবাল ডিকশনারি যেখানে কানেক্টেড আইডিগুলো থাকবে
connected_clients = {} 

@app.get("/")
def read_root():
    return {
        "status": "API is Running", 
        "connected_accounts": len(connected_clients),
        "gateway": "Active"
    }

@app.get("/ghost-join")
def ghost_join_api(
    code: str = Query(..., description="Team Code for ghost attack"),
    name: str = Query("GHOST_PRO", description="Display name of ghost"),
    count: int = Query(50, description="Number of packets per account")
):
    """
    এই লিঙ্কটি কল করলে ঘোস্ট জয়েন শুরু হবে।
    Example: /ghost-join?code=123456&name=KING&count=100
    """
    # গেট হোম (Gateway) চেক করা
    active_clients = [c for c in connected_clients.values() if hasattr(c, 'CliEnts2')]
    
    if not active_clients:
        return {"status": "error", "message": "No accounts connected to the gateway!"}

    def attack_worker(client, t_code, g_name, p_count):
        try:
            for _ in range(p_count):
                # বারকেল এরিয়া: প্যাকেট তৈরি করা
                packet = ghost_pakcet(str(t_code), str(g_name), "1", client.key, client.iv)
                
                # গেট হোম: সকেট দিয়ে প্যাকেট পুশ করা
                if client.CliEnts2:
                    client.CliEnts2.send(packet)
                time.sleep(0.02) # অ্যাটাক স্পিড
        except Exception as e:
            print(f"Attack failed for {client.id}: {e}")

    # প্রতিটি অ্যাকাউন্টের জন্য আলাদা থ্রেডে অ্যাটাক রান করা
    for client in active_clients:
        threading.Thread(target=attack_worker, args=(client, code, name, count), daemon=True).start()

    return {
        "status": "Attack Started",
        "team_code": code,
        "ghost_name": name,
        "total_accounts": len(active_clients)
    }

# --- অ্যাকাউন্ট অটো-কানেক্ট লজিক ---
def auto_loader():
    # এখানে আপনার StarT_SerVer() এর কোডটুকু বসবে যা accs.json থেকে 
    # আইডি নিয়ে connected_clients ডিকশনারিতে সেভ করবে।
    pass

@app.on_event("startup")
def startup_event():
    # এপিআই স্টার্ট হওয়ার সাথে সাথে ব্যাকগ্রাউন্ডে আইডি কানেক্ট হবে
    threading.Thread(target=auto_loader, daemon=True).start()
