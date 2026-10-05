# Set 6 — Byte (Character) Stuffing + `ftp`

## Q1. Byte / Character Stuffing (Experiment 2)

### Theory
**Character-oriented framing** (used in PPP, older BISYNC) delimits frames with a special **FLAG byte**.
If the payload contains a byte equal to FLAG, the receiver would end the frame early. **Byte stuffing** fixes this:

- Choose **FLAG = `~` (0x7E)** and **ESC = `}` (0x7D)**.
- **Sender:** before every FLAG or ESC byte *inside the data*, insert an **ESC**.
- Frame = `FLAG + stuffed data + FLAG`.
- **Receiver:** on ESC, discard it and take the **next byte literally**; an *unescaped* FLAG marks the end of frame.

### Example
| | Value |
|---|---|
| Data | `A~B}C` |
| Frame | `~A}~B}}C~` |

(`~` → `}~`, `}` → `}}`.) De-stuffing gives back `A~B}C`.

### Program explanation
- `client.py` — `stuff()` loops over bytes, adds ESC before FLAG/ESC, wraps with FLAGs; shows ASCII and hex; sends;
  calls `shutdown(SHUT_WR)` so the server knows the frame is finished.
- `server.py` — reads until the client half-closes, `destuff()` verifies leading FLAG, handles ESC sequences, stops at
  the unescaped FLAG, prints the recovered data.

### How to run
```
python3 server.py
python3 client.py       # enter: A~B}C
```
**Exam-critical:** ESC itself must be escaped too. Overhead depends on the data (worst case: all FLAG/ESC → 2×).
Bit stuffing (Set 1) is the bit-oriented counterpart.

---

## Q2. Command: `ftp`

### Theory
**FTP (File Transfer Protocol)** transfers files between client and server over TCP.
- **Two connections:** **control** on port **21** (commands/replies) and **data** on port **20** (active mode) or a
  negotiated high port (passive mode).
- Sends credentials and data in **plain text** (insecure) → use SFTP/FTPS in production.
- Needs login (username/password, or `anonymous`).

### Commands (client side)
```
ftp <host>            # connect (Windows/Linux/macOS)
```
Inside the `ftp>` prompt:

| Command | Purpose |
|---|---|
| `user` / login prompt | authenticate |
| `ls` / `dir` | list remote files |
| `pwd`, `cd <dir>` | remote working directory |
| `get <file>` | download |
| `put <file>` | upload |
| `binary` / `ascii` | transfer mode |
| `lcd <dir>` | change local directory |
| `bye` / `quit` | disconnect |

### Getting a lab server (if none is provided)
```
pip install pyftpdlib
python3 -m pyftpdlib -p 2121 -w       # anonymous server with write access, current folder
ftp localhost 2121                    # in another terminal; user: anonymous
```
Use only servers you are authorised to access.

### Sample session
```
$ ftp localhost 2121
Connected to localhost.
220 pyftpdlib ready.
Name: anonymous
230 Login successful.
ftp> ls
-rw-r--r--   1 user  group    120 Oct 05 09:00 notes.txt
ftp> get notes.txt
226 Transfer complete.
ftp> bye
221 Goodbye.
```
### Explanation
- **220** ready, **230** login OK, **150** opening data connection, **226** transfer complete, **221** goodbye.
- `ls` triggers a data connection; the listing travels on it, commands stay on the control connection.
- Purpose: reliable upload/download of files (websites, backups, software distribution).
