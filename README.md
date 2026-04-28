# 🧩 ESP32 Multi-Game System: Number Puzzle + R to G

A dual-game embedded system built on **ESP32** with an **SSD1306 OLED display** (I2C) and **4-button control interface**. Written in **MicroPython**, this project features a classic sliding number puzzle and a character navigation game — all running on bare-metal hardware.

---

## 🎮 Games Included

| # | Game Name | Description |
|---|-----------|-------------|
| 1 | **Number Puzzle** | Classic 3x3 sliding puzzle (1-8 with empty space). Rearrange numbers to win! |
| 2 | **R to G** | Navigate 'R' to reach 'G' on a 3x3 grid using button controls |
| 3 | **Exit** | Safely exits the game with a fun animation |
| 4 | **Suspense** | Easter egg mode — surprise animation! 🎭 |

---

## 🔧 Hardware Required

| Component | Quantity |
|-----------|----------|
| ESP32 development board | 1 |
| SSD1306 OLED display (I2C, 128x64) | 1 |
| Tactile push buttons | 4 |
| 10kΩ resistors (optional, for pull-down) | 4 |
| Breadboard | 1 |
| Jumper wires (M-M, M-F) | as needed |

---

## 🔌 Wiring Diagram

### I2C Connections (SSD1306 OLED)

| ESP32 Pin | SSD1306 Pin |
|-----------|-------------|
| 3.3V      | VCC         |
| GND       | GND         |
| GPIO 21   | SDA         |
| GPIO 22   | SCL         |

### Button Connections (with internal PULL_UP)

| Button | ESP32 GPIO | Function |
|--------|------------|----------|
| UP     | GPIO 27    | Move up / Navigate menu |
| DOWN   | GPIO 14    | Move down / Select game |
| LEFT   | GPIO 18    | Move left / Navigate |
| RIGHT  | GPIO 19    | Move right / Select |

> **Note:** Internal pull-up resistors are enabled in code, so buttons connect directly between GPIO and GND. No external resistors needed.

