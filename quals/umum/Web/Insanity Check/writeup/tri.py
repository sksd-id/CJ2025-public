#!/usr/bin/env python3
import heapq, math
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Set, Optional

def find_sequences_dfs(
    trigrams: List[str],
    start: str,
    end: str,
    target_length: int,
    max_results: int = 50
) -> List[str]:
    """
    Exhaustive deterministic search that allows overlaps of 2, 1 or 0 characters
    between the current sequence and a candidate trigram.

    - trigrams: list of 3-char strings
    - start: sequence prefix (must be length >= 2 for sensible use)
    - end: sequence suffix (must be length >= 2)
    - target_length: required final sequence length (exact)
    - max_results: stop once this many solutions are found
    """
    # Basic validation
    if any(len(t) != 3 for t in trigrams):
        raise ValueError("All trigrams must be length 3.")
    if len(start) < 2 or len(end) < 2:
        raise ValueError("start and end should be length >= 2.")
    if target_length < max(len(start), len(end)):
        return []

    n = len(trigrams)
    results = []
    seen = set()

    # Deterministic ordering: indices sorted by trigram string
    sorted_indices = [i for i, _ in sorted(enumerate(trigrams), key=lambda x: x[1])]

    # DFS with pruning. Each trigram appended with overlap k adds (3-k) new chars.
    def dfs(curr_seq: str, used: Set[int]):
        # stop if we have enough results
        if len(results) >= max_results:
            return
        # prune by length
        if len(curr_seq) > target_length:
            return

        remaining = n - len(used)
        # compute theoretical min/max lengths achievable with remaining trigrams:
        # min additional chars if every remaining trigram uses overlap k=2 -> +1 per trigram
        min_possible = len(curr_seq) + remaining * 1
        # max additional chars if every remaining trigram appended with k=0 -> +3 per trigram
        max_possible = len(curr_seq) + remaining * 3

        # If it's impossible to ever reach target_length, prune
        if max_possible < target_length:
            return
        # If even the minimal growth overshoots (we add at least 1 per trigram), allow small buffer
        if min_possible > target_length + 3:
            return

        # If at exact length, test start/end constraints
        if len(curr_seq) == target_length:
            if curr_seq.startswith(start) and curr_seq.endswith(end):
                if curr_seq not in seen:
                    seen.add(curr_seq)
                    results.append(curr_seq)
            return

        # Try each unused trigram in deterministic order
        for idx in sorted_indices:
            if idx in used:
                continue
            t = trigrams[idx]

            # Try overlap sizes in descending order (prefer larger overlap)
            for k in (2, 1, 0):
                if k > len(curr_seq):
                    continue
                if k > 0:
                    if curr_seq[-k:] != t[:k]:
                        continue
                    new_seq = curr_seq + t[k:]
                else:
                    # 0 overlap: append entire trigram
                    new_seq = curr_seq + t

                dfs(new_seq, used | {idx})
                if len(results) >= max_results:
                    return

    dfs(start, set())
    return results


def find_sequences_astar(
    trigrams: List[str],
    start: str,
    end: str,
    target_length: int,
    max_results: int = 50,
    allow_k0: bool = False
) -> List[str]:
    n = len(trigrams)
    if any(len(t) != 3 for t in trigrams):
        raise ValueError("All trigrams must be length 3.")
    if len(start) < 1 or len(end) < 1:
        raise ValueError("start/end must be non-empty")
    if target_length < len(start) or target_length < len(end):
        return []

    # Deterministic trigram order
    sorted_pairs = sorted(enumerate(trigrams), key=lambda x: x[1])
    idx_order = [i for i, _ in sorted_pairs]
    pref2 = [t[:2] for t in trigrams]
    pref1 = [t[:1] for t in trigrams]

    def priority_for(seq: str) -> Tuple[int, int]:
        # primary: closeness to target length, secondary: shorter seq
        return (abs(len(seq) - target_length), len(seq))

    visited: Dict[Tuple[int, str], int] = {}
    start_seq = start
    start_last = start[-2:] if len(start) >= 2 else start
    start_mask = 0
    heap = []
    heapq.heappush(heap, (priority_for(start_seq), start_last, start_mask, start_seq))
    results: List[str] = []
    seen_results: Set[str] = set()

    while heap and len(results) < max_results:
        (prio_pair, _), last2, mask, seq = heapq.heappop(heap)
        key = (mask, last2)
        if key in visited and visited[key] <= len(seq):
            continue
        visited[key] = len(seq)

        remaining_trigrams = n - bin(mask).count("1")

        # Safe pruning: even if every remaining trigram added +3 chars, can't reach target -> impossible
        max_possible_len = len(seq) + remaining_trigrams * 3
        if max_possible_len < target_length:
            continue

        # Safe lower bound: the minimum number of trigrams required (each can add up to 3 chars)
        chars_needed = target_length - len(seq)
        if chars_needed > 0:
            min_trigrams_needed = math.ceil(chars_needed / 3)
            if min_trigrams_needed > remaining_trigrams:
                continue

        # If we've reached exact length, record if matches start/end
        if len(seq) == target_length:
            if seq.startswith(start) and seq.endswith(end):
                if seq not in seen_results:
                    results.append(seq)
                    seen_results.add(seq)
            continue

        # Expand next states (deterministic order)
        for idx in idx_order:
            if (mask >> idx) & 1:
                continue
            t = trigrams[idx]
            # k=2
            if len(seq) >= 2 and seq[-2:] == pref2[idx]:
                new_seq = seq + t[-1]
                new_last = new_seq[-2:]
                new_mask = mask | (1 << idx)
                if len(new_seq) <= target_length + 3:
                    heapq.heappush(heap, (priority_for(new_seq), new_last, new_mask, new_seq))
                continue
            # k=1
            if len(seq) >= 1 and seq[-1] == pref1[idx]:
                new_seq = seq + t[1:]
                new_last = new_seq[-2:]
                new_mask = mask | (1 << idx)
                if len(new_seq) <= target_length + 3:
                    heapq.heappush(heap, (priority_for(new_seq), new_last, new_mask, new_seq))
            # optionally allow k=0
            if allow_k0:
                new_seq = seq + t
                new_last = new_seq[-2:]
                new_mask = mask | (1 << idx)
                if len(new_seq) <= target_length + 3:
                    heapq.heappush(heap, (priority_for(new_seq), new_last, new_mask, new_seq))

    results.sort(key=lambda s: (abs(len(s) - target_length), len(s), s))
    return results


if __name__ == "__main__":
    trigrams = ['00a', '0ab', '4d4', '8a4', '4aa', '458', '589', '89f', '100', '89b', 'a4a', 'ad6', '9be', 'aad', 'd45', 'b8a', 'ab8', 'd61', '9f1', 'ace', 'be8']
    start = "4d"
    end = "61"
    target_length = 24

    sequences = find_sequences_dfs(trigrams, start, end, target_length, max_results=200)
    print("Found sequences:", sequences)
    print("Count:", len(sequences))
