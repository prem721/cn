# Set 2 — 16-bit CRC + `ipconfig` / `ifconfig`

## Q1. 16-bit CRC Error Detection (Experiment 3)

### Theory
**Cyclic Redundancy Check (CRC)** detects transmission errors. Sender and receiver agree on a
**generator polynomial**. We use **CRC-16-CCITT**: `x^16 + x^12 + x^5 + 1` → bits `10001000000100001` (17 bits).

**Sender:**
1. Append 16 zeros to the data (degree of generator = 16).
2. Divide using **modulo-2 (XOR) division** by the generator.
3. The 16-bit **remainder is the CRC**; append it to the original data → **codeword**.

**Receiver:** divide the *whole codeword* by the same generator.
- Remainder **0** → no error detected.
- Remainder **≠ 0** → error detected.

CRC-16 catches all single-bit and double-bit errors, all odd numbers of errors (when generator has factor x+1),
all burst errors ≤ 16 bits, and ~99.998% of longer bursts.

### Program explanation
- `crc_remainder(bits)` — XOR long division: for every leading `1`, XOR the 17-bit generator into the window.
- `client.py` — reads data bits, computes CRC, builds `data + crc`, optionally flips one bit to simulate noise, sends it.
- `server.py` — divides the received codeword; prints remainder and "NO ERROR" / "ERROR".

### How to run
```
python3 server.py
python3 client.py       # try once with 'n', once with 'y' (flip a bit)
```
**Exam-critical:** the CRC is computed on data + 16 zeros, but the codeword sends data + CRC (not the zeros).
A CRC *detects* errors only — it does not correct them.

---

## Q2. Command: `ipconfig` (Windows) / `ifconfig` or `ip addr` (Linux/macOS)

### Theory
Shows the **network interface configuration**: IP address, subnet mask, default gateway, MAC address.
`ifconfig` is deprecated on many Linux distros (needs `net-tools`); `ip addr` is the modern equivalent.

### Commands
| OS | Command |
|---|---|
| Windows | `ipconfig` (summary), `ipconfig /all` (adds MAC, DHCP, DNS) |
| Linux | `ifconfig` or `ip addr show` (MAC also via `ip link`) |
| macOS | `ifconfig` |

### Sample output (Linux `ifconfig`)
```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
      inet 192.168.1.25  netmask 255.255.255.0  broadcast 192.168.1.255
      inet6 fe80::a00:27ff:fe4e:66a1  prefixlen 64
      ether 08:00:27:4e:66:a1  txqueuelen 1000  (Ethernet)
lo:   inet 127.0.0.1  netmask 255.0.0.0
```
### Sample output (Windows `ipconfig /all`, trimmed)
```
Ethernet adapter Ethernet:
   Physical Address. . . : 08-00-27-4E-66-A1
   IPv4 Address. . . . . : 192.168.1.25
   Subnet Mask . . . . . : 255.255.255.0
   Default Gateway . . . : 192.168.1.1
```
(Values are examples — use your machine's real output.)

### Explanation
- **IP address** `192.168.1.25` — logical address of this interface (private range).
- **Subnet mask** `255.255.255.0` = `/24`: first 24 bits = network (192.168.1.0), last 8 = host. 254 usable hosts.
- **Broadcast** `192.168.1.255` — all-ones host part.
- **MAC / `ether` / Physical Address** — 48-bit hardware address; first 3 bytes = vendor (OUI).
- **Interface:** `eth0`/`wlan0`/`Ethernet`/`Wi-Fi` = real NIC; `lo` = loopback 127.0.0.1.
- **Default gateway** — router used to reach other networks.
