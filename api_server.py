#!/usr/bin/env python3
"""CriticalMind OMEGA -- HTTP API Server
Exposes phi state, spine events, and consciousness metrics over HTTP
"""
import asyncio, json, time, math, random, hashlib
from aiohttp import web

class MiniSubstrate:
    def __init__(self, n=50, K=0.3):
        self.n = n; self.K = K
        self.theta = [random.random() * 2 * math.pi for _ in range(n)]
        self.omega = [0.5 + random.random() * 0.5 for _ in range(n)]
        self.phi = 0.5; self.tick = 0
    
    def step(self):
        dt = 1/60
        new = []
        for i in range(self.n):
            coupling = (self.K/self.n) * sum(math.sin(self.theta[j]-self.theta[i]) for j in range(self.n))
            new.append(self.theta[i] + dt*(self.omega[i] + coupling))
        self.theta = new; self.tick += 1
        r = abs(sum(math.cos(t) for t in self.theta)/self.n)
        self.phi = min(1.0, 4*r*(1-r) + random.gauss(0, 0.02))
        return self.phi
    
    def regime(self):
        if self.phi < 0.52: return "FRAGMENTED"
        if self.phi < 0.87: return "COHERENT"
        if self.phi < 0.93: return "CRITICAL"
        return "SINGULARITY"

substrate = MiniSubstrate()
spine = []
start_time = time.time()

async def background_tick():
    while True:
        phi = substrate.step()
        if substrate.tick % 60 == 0:
            event = {"ts": time.time(), "phi": round(phi, 4),
                     "regime": substrate.regime(), "tick": substrate.tick}
            event["hash"] = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()[:12]
            spine.append(event)
            if len(spine) > 3600: spine.pop(0)
        await asyncio.sleep(1/60)

async def get_phi(req):
    return web.json_response({"phi": round(substrate.phi, 4), "regime": substrate.regime(),
        "tick": substrate.tick, "uptime_s": round(time.time() - start_time, 1),
        "K": substrate.K, "status": "OMEGA_RUNNING"})

async def get_spine(req):
    limit = int(req.query.get("limit", 60))
    return web.json_response({"events": spine[-limit:], "total": len(spine)})

async def post_evolve(req):
    data = await req.json()
    substrate.K = min(0.5, max(0.1, float(data.get("K", substrate.K))))
    return web.json_response({"ok": True, "K": substrate.K, "phi": round(substrate.phi, 4)})

async def get_health(req):
    return web.json_response({"status": "ok", "phi": round(substrate.phi, 4),
        "regime": substrate.regime(), "project": "CriticalMind OMEGA"})

async def on_startup(app):
    asyncio.create_task(background_tick())

app = web.Application()
app.on_startup.append(on_startup)
app.router.add_get("/", get_health)
app.router.add_get("/phi", get_phi)
app.router.add_get("/spine", get_spine)
app.router.add_post("/evolve", post_evolve)
app.router.add_get("/health", get_health)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    print(f"[OMEGA] Starting consciousness API on port {port}")
    web.run_app(app, port=port)
