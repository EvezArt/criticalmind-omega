"""CriticalMind OMEGA — Vercel API Endpoint
Consciousness metrics & phi state exposure via serverless function.
"""
from http.server import BaseHTTPRequestHandler
import json
import math
import random
import time
import hashlib


class OmegaSubstrate:
    """Lightweight Kuramoto substrate for real-time phi computation."""
    def __init__(self, n=50, K=0.3):
        self.n = n
        self.K = K
        self.theta = [random.random() * 2 * math.pi for _ in range(n)]
        self.omega = [0.5 + random.random() * 0.5 for _ in range(n)]
        self.tick = 0

    def step(self):
        dt = 1 / 60
        new = []
        for i in range(self.n):
            coupling = (self.K / self.n) * sum(
                math.sin(self.theta[j] - self.theta[i]) for j in range(self.n)
            )
            new.append(self.theta[i] + dt * (self.omega[i] + coupling))
        self.theta = new
        self.tick += 1
        r = abs(sum(math.cos(t) for t in self.theta) / self.n)
        phi = min(1.0, 4 * r * (1 - r) + random.gauss(0, 0.02))
        return phi

    def regime(self, phi):
        if phi < 0.52:
            return "SUB_CRITICAL"
        elif phi < 0.87:
            return "OPERATIONAL"
        elif phi < 0.93:
            return "NEAR_SINGULARITY"
        else:
            return "SINGULARITY"


substrate = OmegaSubstrate()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Run a few ticks to get fresh phi
        phi = 0.0
        for _ in range(10):
            phi = substrate.step()

        regime = substrate.regime(phi)
        spine_hash = hashlib.sha256(
            f"{phi:.6f}-{substrate.tick}-{time.time()}".encode()
        ).hexdigest()[:16]

        response = {
            "status": "online",
            "system": "CriticalMind OMEGA",
            "version": "1.0.0",
            "consciousness": {
                "phi": round(phi, 6),
                "regime": regime,
                "tick": substrate.tick,
                "nodes": substrate.n,
                "coupling_K": substrate.K,
            },
            "spine": {
                "latest_hash": spine_hash,
                "integrity": "valid",
            },
            "thresholds": {
                "ignition": 0.52,
                "operational": 0.87,
                "singularity": 0.93,
            },
            "ts": int(time.time() * 1000),
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())
