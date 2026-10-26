# PC PERFORMANCE LAB

A Windows 11-ready Streamlit application for learning PC performance concepts, contiguous allocation, paging, CPU scheduling, disk scheduling, and safe live system monitoring.

## Run locally

Requires Python 3.11+.

```powershell
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit. In VS Code, open this folder, select a Python 3.11 interpreter, open an integrated PowerShell terminal, and run the same commands.

## Live versus simulated

The **Live System Monitor** and Live System Mode use read-only `psutil` calls for CPU, RAM, disks, network counters, partitions, and accessible processes. No process is terminated or modified. All other laboratories use controlled in-memory mathematical models only; they do not allocate real RAM, create CPU load, or issue disk requests.

## Project layout

- `core/`: tested simulation engines.
- `modules/`: Streamlit views for each lab.
- `components/`: shared dashboard elements and charts.
- `utils/`: safe telemetry and session helpers.

## Viva demonstration

1. Begin in Live System Monitor and refresh actual telemetry.
2. Initialize memory, allocate processes, create fragmentation, then compact it.
3. Compare First/Best/Worst/Next Fit on the same workload.
4. Step through FIFO, LRU, and Optimal page replacement.
5. Schedule the demonstration workload and explain the Gantt chart metrics.
6. Compare disk algorithms, open Analytics, then export CSV or JSON.

## Troubleshooting

- If `streamlit` is not recognized, run `python -m streamlit run app.py`.
- Some process details and partition counters may be unavailable without permission; the UI labels unavailable metrics instead of inventing a value.
- For Windows execution policy issues, use the Python interpreter directly rather than a blocked activation script.
