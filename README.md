# Enhanced SUMO Route Finder

A Python-based tool to determine all possible routes between two specified edges in a SUMO network. This tool uses an efficient Breadth-First Search (BFS) algorithm with a global visited set to prevent cycles, ensuring that the search space is pruned effectively and only the first (often shortest) route per node is output.

---

## Overview

This project implements a custom route finder that overcomes several limitations of the standard SUMO `FindAllTrips` tool. Key improvements include:

- **Iteration Limits:** Prevents endless loops by enforcing a maximum number of iterations, unlike SUMO’s tool that may run indefinitely.
- **Edge ID Compatibility:** Handles edge IDs starting with a '-' sign. The regular SUMO tool may encounter problems with such IDs due to limitations in its argument parser.
- **Speed & Efficiency:** Utilizes a BFS algorithm with a global visited set and an efficient `deque` data structure to reduce redundancy in the search process and speed up the route discovery.
- **Cycle Prevention:** Global cycle prevention minimizes redundant explorations, significantly lowering the overall computational load.

---

## Key Features

- **Efficient Route Discovery:** Uses BFS to explore possible routes, ensuring that the first discovered route (often the shortest) is output per node.
- **Controlled Search:** Iteration count is capped with a user-defined maximum (`MAX_ITERATIONS`), so the search won’t run indefinitely.
- **Compatibility with Special Edge IDs:** Successfully processes SUMO edge IDs that begin with a '-' character.
- **Clear and Informative Output:** Provides real-time logging of the search process and writes discovered routes directly into a SUMO-compliant routes XML file.

---

## How It Works

1. **Network Loading:**  
   The SUMO network is loaded from a specified file (`map.net.xml`). The tool verifies that both the source and target edges exist and that they allow passenger vehicles.

2. **Route Search via BFS:**  
   - **Initialization:** The BFS queue is initialized with the source edge.
   - **Cycle Prevention:** A global visited set prevents re-exploration of nodes, dramatically reducing unnecessary computations.
   - **Iteration Limit:** An iteration counter halts the process if it exceeds a predefined maximum (to avoid infinite loops).
   - **Route Output:** Whenever the target edge is reached, the tool prints the route and writes it to an output XML file (`routes.rou.xml`).

3. **Performance Monitoring:**  
   The script logs the number of iterations, total routes discovered, and the overall execution time.

---

## Installation

1. **Prerequisites:**
   - **Python 3:** Make sure you have Python 3.x installed.
   - **SUMO Tools:** The script relies on SUMO's libraries (e.g., `sumolib`), so ensure you have SUMO installed and configured correctly.
   - **Other Dependencies:** Standard Python libraries such as `time` and `collections` are required.

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/Harshit2k1/Enhanced-SUMO-Route-Finder.git
   cd enhanced-sumo-route-finder
   ```

3. **Set Up Your Environment:**

   It’s a good idea to use a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install sumolib
   ```

---

## Usage

1. **Prepare Your Network Files:**
   - Replace `map.net.xml` with the path to your SUMO network file.
   - Specify the correct source (`SOURCE_EDGE`) and target (`TARGET_EDGE`) edge IDs in the script.

2. **Run the Script:**

   ```bash
   python routeFinder.py
   ```

   The script will start the BFS search, log its progress to the console, and write the found routes to `routes.rou.xml`.

---

## Advantages Over Regular SUMO's findAllRoutes

- **Controlled Execution:**  
  With a hard limit on iterations, this tool prevents scenarios where the search runs indefinitely, a common issue with SUMO’s `FindAllTrips`.

- **Robust Edge Handling:**  
  The tool does not fail when encountering edge IDs that start with a '-' sign, whereas SUMO's tool may misinterpret them due to its argument parser limitations.

- **Optimized for Speed:**  
  The route finder reduces redundant computations through efficient data structures and global cycle prevention, leading to faster route discovery.

- **Effective Pruning:**  
  The BFS algorithm and a global visited set minimizes the number of paths that need to be explored, ensuring that performance is maintained even in large networks.

---

## Limitations and Tradeoffs Compared to SUMO's findAllRoutes

While this enhanced route finder offers significant performance improvements and addresses known issues with SUMO's original `findAllRoutes.py` tool, it has a few limitations. These tradeoffs were deliberately chosen to ensure faster performance, resource efficiency, and robustness in challenging network scenarios. Below are the primary limitations, along with explanations of why these design decisions were made:

### 1. Limited Route Variability
The tool outputs only the first discovered route per node (often the shortest) rather than exploring all possible routes. This design choice was made to reduce computational overhead and speed up processing. By selecting the first encountered route, the algorithm avoids the exponential growth of alternative paths, ensuring rapid termination and efficient resource utilization.

### 2. Aggressive Pruning via Global Visited Set
The use of a global visited set to prevent cycles may inadvertently filter out some valid routes that require revisiting nodes through alternative paths. Aggressive pruning is essential to prevent infinite loops and reduce the search space significantly. This tradeoff prioritizes reliability and performance, accepting that a few potential routes might be missed in exchange for dramatically faster execution.

### 3. Hard Iteration Cap
A maximum iteration limit is imposed, which might stop the exploration before discovering all possible routes in very large or highly connected networks. The iteration cap prevents the algorithm from running indefinitely, ensuring that the tool remains responsive even in complex networks. This safeguard is crucial for maintaining predictable and stable execution times.

### 4. Characteristics of BFS Search
The use of Breadth-First Search (BFS) naturally biases the tool towards finding the shortest routes (in terms of edge count), potentially overlooking longer routes that might be optimal under different metrics (such as distance or travel time).  BFS was chosen for its simplicity and efficiency in finding routes quickly. While it may not provide exhaustive alternative paths, it aligns with the tool’s goal of delivering fast and practical results for common routing scenarios.

---

Overall, these tradeoffs were intentionally chosen to strike a balance between efficiency, safety, and practical usability. The enhancements address key issues such as indefinite execution and problematic edge ID parsing found in the original tool, making this solution a robust option for many applications despite the noted limitations.


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests if you have improvements or bug fixes.
---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgements

Special thanks to the SUMO community and developers whose tools and documentation have been invaluable in creating and enhancing this route finder tool.
```
