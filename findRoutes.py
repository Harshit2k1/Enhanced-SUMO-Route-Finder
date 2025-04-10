"""
Determine all possible routes between source and destination edges.

# Algorithm: BFS with a global visited set that prevents revisiting nodes.
# Cycle Prevention: Done globally, which greatly reduces the number of routes explored.
# Data Structure: Efficient deque for queue operations.
# Output: Only the first discovered route per node (often the shortest).
# Speed: Faster due to significant pruning of the search space and efficient data structures.
"""
from __future__ import absolute_import
from __future__ import print_function

import sumolib
import time
from collections import deque

# Hardcoded values
NET_FILE = "map.net.xml"   # Replace with your SUMO net file path
OUTPUT_FILE = "routes.rou.xml"      # Replace with your desired output file path
SOURCE_EDGE = "-1290849347#1"        # Source edge (replace with your ID)
TARGET_EDGE = "-1290819148"          # Target edge (replace with your ID)
MAX_ITERATIONS = 1_000_000_000_000_000_000  # Max iterations limit to prevent infinite loops


def edge_allows_passenger(edge):
    """Check if at least one lane in the edge allows passenger vehicles."""
    for lane in edge.getLanes():
        if lane.allows("passenger"):  # Pass "passenger" as an argument
            return True
    return False



def main():
    start_time = time.time()
    print("[INFO] Loading network...")

    net = sumolib.net.readNet(NET_FILE)

    # Create edge lookup dictionary
    edges = {e.getID(): e for e in net.getEdges()}

    # Validate edges
    if SOURCE_EDGE not in edges or TARGET_EDGE not in edges:
        print(f"[ERROR] One or both edges not found: Source={SOURCE_EDGE}, Target={TARGET_EDGE}")
        return

    source = edges[SOURCE_EDGE]
    target = edges[TARGET_EDGE]

    # Check if source and target edges allow passenger vehicles
    if not edge_allows_passenger(source):
        print(f"[ERROR] Source edge '{SOURCE_EDGE}' does not allow passenger vehicles.")
        return
    
    if not edge_allows_passenger(target):
        print(f"[ERROR] Target edge '{TARGET_EDGE}' does not allow passenger vehicles.")
        return

    print(f"[INFO] Starting route search from '{SOURCE_EDGE}' to '{TARGET_EDGE}'...")

    # BFS queue
    queue = deque([[source]])
    visited = set()
    route_count = 0
    iterations = 0

    # Write output file
    with open(OUTPUT_FILE, 'w') as outf:
        sumolib.xml.writeHeader(outf, root="routes")

        while queue:
            iterations += 1

            # Stop if max iterations reached
            if iterations > MAX_ITERATIONS:
                print(f"[WARNING] Max iterations reached ({MAX_ITERATIONS}), stopping search.")
                break

            if iterations % 100000 == 0:
                print(f"[INFO] Iterations: {iterations}, Routes found: {route_count}")

            path = queue.popleft()
            current = path[-1]

            if current == target:
                # Route found
                route = " ".join([e.getID() for e in path])
                print(f"[ROUTE] {route_count}: {route}")
                print(f'    <route id="{route_count}" edges="{route}"/>', file=outf)
                route_count += 1

            visited.add(current)

            for edge in sorted(current.getOutgoing(), key=lambda e: e.getID()):
                # Only consider edges that allow passenger vehicles
                if edge not in visited and edge_allows_passenger(edge):
                    queue.append(path + [edge])

        outf.write('</routes>\n')

    end_time = time.time()
    duration = end_time - start_time

    print(f"[INFO] Routes saved to {OUTPUT_FILE}")
    print(f"[INFO] Total routes found: {route_count}")
    print(f"[INFO] Execution time: {duration:.2f} seconds")
    print(f"[INFO] Total iterations: {iterations}")


if __name__ == "__main__":
    main()
