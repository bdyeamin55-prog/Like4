from fastapi import FastAPI, Query
import threading
import time
from black9 import ghost_pakcet
# আপনার অন্যান্য মডিউল ইমপোর্ট করুন

app = FastAPI()

# গ্লোবাল ডিকশনারি যেখানে কানেক্টেড আইডিগুলো থাকবে
# (আপনার StarT_SerVer ফাংশন এগুলো পপুলেট করবে)
connected_clients = {} 

@app.get("/")
def read_root():
    return {"status": "API is Running", "connected_accounts": len(connected_clients)}

@app.get("/ghost-join")
def ghost_join_api(
    code: str = Query(..., description="Team Code for the attack"),
    name: str = Query("GHOST_PRO", description="Name of the ghost player"),
    count: int = Query(50, description="Number of packets per account")
):
    """
    এই এন্ডপয়েন্টটি কল করলে ঘোস্ট জয়েন শুরু হবে।
    Example: /ghost-join?code=123456&name=KING&count=100
    """
    active_clients = [c for c in connected_clients.values() if hasattr(c, 'CliEnts2')]
    
    if not active_clients:
        return {"status": "error", "message": "No accounts are currently connected!"}

    def attack_task(client, t_code, g_name, p_count):
        try:
            for _ in range(p_count):
                # বারকেল এরিয়া: প্যাকেট জেনারেট এবং গেট হোম (CliEnts2) দিয়ে সেন্ড
                packet = ghost_pakcet(str(t_code), str(g_name), "1", client.key, client.iv)
                client.CliEnts2.send(packet)
                time.sleep(0.02)
        extra = {} # Error handling
        except Exception as e:
            print(f"Attack failed for {client.id}: {e}")

    # প্রতিটি আইডির জন্য আলাদা থ্রেডে অ্যাটাক শুরু করা
    for client in active_clients:
        threading.Thread(target=attack_task, args=(client, code, name, count)).start()

    return {
        "status": "success",
        "target_code": code,
        "ghost_name": name,
        "accounts_used": len(active_clients),
        "total_packets_estimate": len(active_clients) * count
    }

# --- আপনার একাউন্ট স্টার্ট করার লজিক ---
def background_account_starter():
    # এখানে আপনার StarT_SerVer() লজিক থাকবে যা আইডি কানেক্ট করবে
    pass

@app.on_event("startup")
def startup_event():
    # এপিআই চালু হওয়ার সময় ব্যাকগ্রাউন্ডে আইডি কানেকশন শুরু হবে
    threading.Thread(target=background_account_starter, daemon=True).start()