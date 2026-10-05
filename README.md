# Computer Networks Lab — Exam Kit (Sets 1–10)

Each `SetNN_*` folder has:

| File | What it is |
|---|---|
| `server.py` | server / receiver (start this first) |
| `client.py` | client / sender (start in a second terminal) |
| `theory.md` | theory of the program + the Experiment-1 command (commands, sample output, explanation) |

Requirements: Python 3 only (standard library). Everything runs on `127.0.0.1`.

## Quick start
```
cd Set01_BitStuffing_ping
python3 server.py          # terminal 1
python3 client.py          # terminal 2
```

| Set | Program (ports) | Command |
|---|---|---|
| 1 | Bit stuffing (5001) | ping |
| 2 | 16-bit CRC (5002) | ipconfig / ifconfig |
| 3 | Sliding window / Go-Back-N (5003) | arp |
| 4 | Dijkstra (5004) | netstat |
| 5 | TCP echo, single message (5005) | nslookup |
| 6 | Byte stuffing (5006) | ftp |
| 7 | 16-bit CRC, correct + corrupted (5007) | dig |
| 8 | Sliding window / Go-Back-N, window 3 (5008) | telnet |
| 9 | Distance vector (5009) | tftp |
| 10 | TCP echo, multiple messages (5010) | ping |

If you see "Address already in use", wait a few seconds or stop the old server (Ctrl+C).
On Windows use `python` instead of `python3` if needed.
