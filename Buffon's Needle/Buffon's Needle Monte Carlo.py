import numpy as np
import multiprocessing
import time
 
 
def simulate_chunk(trials):
    """Runs one chunk of trials in its own process. Returns the raw
    crossing count for this chunk (not a pi estimate) so the caller can
    correctly combine counts across all chunks before dividing."""
    point_one = np.random.random(trials)
 
    vector_verical = np.random.uniform(-1, 1, int(trials * 1.3))
    vector_horizontal = np.random.uniform(-1, 1, int(trials * 1.3))
    mask = vector_verical**2 + vector_horizontal**2 <= 1
    vector_verical, vector_horizontal = vector_verical[mask], vector_horizontal[mask]
 
    while len(vector_verical) < trials:
        extra = trials - len(vector_verical)
        vv_more = np.random.uniform(-1, 1, extra * 2)
        vh_more = np.random.uniform(-1, 1, extra * 2)
        mask_more = vv_more**2 + vh_more**2 <= 1
        vector_verical = np.concatenate([vector_verical, vv_more[mask_more]])
        vector_horizontal = np.concatenate([vector_horizontal, vh_more[mask_more]])
 
    vector_verical, vector_horizontal = vector_verical[:trials], vector_horizontal[:trials]
    radius = np.sqrt(vector_verical**2 + vector_horizontal**2)
    sin_theta = vector_verical / radius
 
    point_two = point_one + sin_theta
    crossed = np.count_nonzero((point_two > 1) | (point_two < 0))
    return crossed
 
 
def run_simulation(total_trials, n_workers=None):
    if n_workers is None:
        n_workers = multiprocessing.cpu_count()
 
    chunk_size = total_trials // n_workers
    chunks = [chunk_size] * n_workers
 
    with multiprocessing.Pool(n_workers) as pool:
        crossed_counts = pool.map(simulate_chunk, chunks)
 
    total_crossed = sum(crossed_counts)
    total_run = chunk_size * n_workers   # note: may be slightly less than
                                          # total_trials due to integer division
    return 2 / (total_crossed / total_run)
 
 
if __name__ == "__main__":
    N = 100_000_000
    print(f"cores available: {multiprocessing.cpu_count()}")
 
    t0 = time.time()
    pi_estimate = run_simulation(N)
    t1 = time.time()
    print(f"The derived value of pi is equal to {pi_estimate}.")
    print(f"time: {t1 - t0:.2f}s")