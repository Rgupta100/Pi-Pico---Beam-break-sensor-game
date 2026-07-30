# Pico Beam-Break Cup Pong Tracker

An automated beer-pong scoreboard. Six IR beam-break sensors sit in the cups; a
Raspberry Pi Pico watches them and reports over USB serial, and a browser page
reads that serial stream directly with the Web Serial API and counts up.

No server, no driver, no install — the Pico plugs in and a local HTML file
becomes the scoreboard.

## Hardware

| Part | Pico pin |
|---|---|
| Beam-break sensor 1–6 | GP2, GP3, GP4, GP5, GP6, GP7 |

Each sensor output goes to its pin, configured `Pin.IN, Pin.PULL_UP`. The
sensors pull the line **low** when the beam is broken, so idle is high and no
external resistors are needed.

## How it works

**Pico** (`Raspberry Pi/Cup Pong Game.py`, MicroPython)

Polls all six pins every 50 ms. On a falling edge it prints `1` over USB serial
and latches that sensor in a `broken_status` array so it never reports twice — a
ball resting in a cup holds the beam broken, which would otherwise spam the
stream continuously.

**Browser** (`HTML/index.html`)

Click anywhere to trigger `navigator.serial.requestPort()` — the port picker
must be opened from a user gesture, which is why the whole page body is the
click target. Opens at **115200 baud**, pipes the stream through
`TextDecoderStream`, and increments the on-screen counter for each chunk
containing `1`.

## Running

1. Flash MicroPython to the Pico, then copy `Cup Pong Game.py` onto it as
   `main.py` so it runs at power-on.
2. Open `HTML/index.html` in Chrome or Edge.
3. Click the page, pick the Pico's serial port, and start playing.

## Notes and limitations

- **Web Serial is Chromium-only.** Firefox and Safari don't implement it. The
  page also needs `https://` or `file://` — not plain `http://`.
- **Sensors never un-latch.** Once a cup registers, it's counted for the rest of
  the session; removing the ball won't reset it and there's no way to undo a
  miscount short of resetting the Pico and reloading the page.
- **The count is per-chunk, not per-event.** The reader checks
  `value.includes("1")`, so if two `1`s arrive in one serial chunk they score
  once — and because the payload is literally the digit `1`, there's no way to
  tell which cup fired.
- No debouncing beyond the 50 ms poll interval.
- The counter lives only in page memory; a refresh zeroes it.

Sending the sensor index instead of a bare `1` would fix both the
which-cup and the coalescing problems, and would let the page draw a cup layout.

## Files

```
Raspberry Pi/Cup Pong Game.py   MicroPython firmware
HTML/index.html                 Web Serial scoreboard
```
