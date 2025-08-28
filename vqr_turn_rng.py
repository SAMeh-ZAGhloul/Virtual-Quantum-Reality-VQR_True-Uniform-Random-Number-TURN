# Let's create a conceptual VQR/TURN-like RNG in a single Python module and run a quick demo.
# The design:
# - Gather entropy from multiple "virtual-physical" sources (os.urandom + timing jitter loops).
# - Apply a Von Neumann extractor on raw bits to debias.
# - Mix with SHA3-256.
# - Feed into a simplified HMAC-DRBG (per NIST SP800-90A style) with periodic reseeding.
# - Include simple health tests (repetition and adaptive proportion on raw entropy) and basic statistical sanity checks on output.
#
# Note: This is a teaching/demo implementation, NOT a certified RNG.

import os, time, hmac, hashlib, struct, math, statistics, random
from typing import Tuple

def _timing_jitter_bytes(n_bytes: int = 64) -> bytes:
    """Harvest timing jitter by tight-loop sampling of perf_counter_ns.
    We compress deltas with SHA3 to avoid exposing structure."""
    h = hashlib.sha3_256()
    last = time.perf_counter_ns()
    # loop more than needed to gather noise
    loops = max(2000, n_bytes * 200)
    for i in range(loops):
        now = time.perf_counter_ns()
        delta = now - last
        last = now
        # Incorporate low-entropy deltas; mixing happens via hash.
        h.update(struct.pack("!Q", delta & ((1<<48)-1)))
    return h.digest()[:n_bytes]


def _von_neumann(bits: bytes) -> bytes:
    """Von Neumann extractor on a bitstream given as bytes.
    Converts biased bits to unbiased (at cost of throughput)."""
    out = bytearray()
    acc = 0
    acc_len = 0
    # read bit pairs
    total_bits = len(bits) * 8
    # iterate in steps of 2 bits
    for i in range(0, total_bits - 1, 2):
        b1 = (bits[i // 8] >> (7 - (i % 8))) & 1
        b2 = (bits[(i+1) // 8] >> (7 - ((i+1) % 8))) & 1
        if b1 == b2:
            continue
        bit = 0 if (b1, b2) == (0, 1) else 1
        acc = (acc << 1) | bit
        acc_len += 1
        if acc_len == 8:
            out.append(acc)
            acc = 0
            acc_len = 0
    if acc_len:
        out.append(acc << (8 - acc_len))
    return bytes(out)


def _health_checks(raw: bytes) -> Tuple[bool, str]:
    """Basic online health checks on raw entropy.
    - Repetition Count Test (fail if > 100 identical consecutive bits).
    - Adaptive Proportion Test over windows of 1024 bits (fail if too biased).
    """
    bits = []
    for b in raw:
        for k in range(8):
            bits.append((b >> (7-k)) & 1)
    # Repetition count
    max_run = 1
    cur = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            cur += 1
            if cur > max_run:
                max_run = cur
        else:
            cur = 1
    if max_run > 100:
        return False, f"Repetition count too high: {max_run}"
    # Adaptive proportion
    window = 1024
    if len(bits) >= window:
        for s in range(0, len(bits)-window+1, window):
            w = bits[s:s+window]
            ones = sum(w)
            # 3-sigma bounds around 512 for fair coin: ~[448,576]
            if ones < 448 or ones > 576:
                return False, f"Adaptive proportion out of range ({ones}/1024)"
    return True, "ok"


class HMAC_DRBG:
    """Simplified HMAC-DRBG (SHA256) per SP800-90A style."""
    def __init__(self, seed_material: bytes):
        self.K = b'\x00' * 32
        self.V = b'\x01' * 32
        self._update(seed_material)

    def _hmac(self, key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, hashlib.sha256).digest()

    def _update(self, provided_data: bytes = b""):
        self.K = self._hmac(self.K, self.V + b"\x00" + provided_data)
        self.V = self._hmac(self.K, self.V)
        if provided_data:
            self.K = self._hmac(self.K, self.V + b"\x01" + provided_data)
            self.V = self._hmac(self.K, self.V)

    def reseed(self, seed_material: bytes):
        self._update(seed_material)

    def generate(self, n_bytes: int) -> bytes:
        out = bytearray()
        while len(out) < n_bytes:
            self.V = self._hmac(self.K, self.V)
            out += self.V
        self._update()
        return bytes(out[:n_bytes])


class VQRTurnRNG:
    """Conceptual VQR/TURN RNG with continuous entropy harvesting and DRBG expansion."""
    def __init__(self, reseed_interval_bytes: int = 1<<20):
        self.reseed_interval_bytes = reseed_interval_bytes
        seed = self._collect_entropy()
        self.drbg = HMAC_DRBG(seed)
        self.bytes_generated = 0

    def _collect_entropy(self, target_bytes: int = 64) -> bytes:
        # Collect from multiple sources
        e1 = os.urandom(target_bytes)
        e2 = _timing_jitter_bytes(target_bytes)
        # Mix and debias: Von Neumann on concatenated bits
        raw = e1 + e2
        ok, msg = _health_checks(raw)
        if not ok:
            # if health test fails, add more OS entropy
            raw += os.urandom(target_bytes)
        debiased = _von_neumann(raw)
        # Hash to fixed size seed (SHA3-256)
        seed = hashlib.sha3_256(debiased or raw).digest()
        # Add a counter/time to differentiate sessions
        meta = struct.pack("!QQ", int(time.time_ns()), self.bytes_generated)
        return hashlib.sha3_256(seed + meta).digest()

    def reseed(self):
        seed = self._collect_entropy()
        self.drbg.reseed(seed)

    def random_bytes(self, n: int) -> bytes:
        out = bytearray()
        while n > 0:
            if self.bytes_generated >= self.reseed_interval_bytes:
                self.reseed()
                self.bytes_generated = 0
            take = min(n, 4096)
            block = self.drbg.generate(take)
            out += block
            n -= take
            self.bytes_generated += take
        return bytes(out)

    def random_u64(self) -> int:
        return struct.unpack("!Q", self.random_bytes(8))[0]

    def random(self) -> float:
        # Uniform [0,1)
        return self.random_u64() / 2**64


# --- Basic statistical sanity checks on output ---

def monobit_frequency_test(bits: bytes) -> Tuple[float, float]:
    """Return (proportion_ones, p_value) using normal approximation."""
    n = len(bits)*8
    ones = sum(bin(b).count("1") for b in bits)
    s = (ones - (n-ones))  # difference
    s_obs = abs(s) / math.sqrt(n)
    # p-value ~ erfc(s_obs/sqrt(2))
    p = math.erfc(s_obs / math.sqrt(2))
    return ones/n, p


def chi_square_bytes_uniformity(bytes_seq: bytes) -> Tuple[float, float]:
    """Chi-square test for uniformity over 256 bins."""
    n = len(bytes_seq)
    if n == 0:
        return 0.0, 1.0
    expected = n / 256.0
    counts = [0]*256
    for b in bytes_seq:
        counts[b] += 1
    chisq = sum((c - expected)**2 / expected for c in counts)
    # df = 255
    # p-value from upper tail using survival function approximation
    # We'll use incomplete gamma via scipy normally; here rough normal approx:
    # Convert to z using (chisq - df)/sqrt(2*df)
    df = 255
    z = (chisq - df) / math.sqrt(2*df)
    # normal tail approx
    p = 0.5*math.erfc(z/math.sqrt(2))
    return chisq, p

