````markdown
# owui-cursor-bridge

Bidirectional bridge between Open WebUI and Cursor IDE.

## What It Does

Plan features in OWUI with a long-context model (like Opus), then send instructions directly to Cursor - without copy-pasting between windows.

## Current Status: Phase 1 Complete ✅

OWUI can send instructions to Cursor via a shared folder bridge.

| Component      | Status        | Description                                                   |
| -------------- | ------------- | ------------------------------------------------------------- |
| Watcher Script | ✅ Working    | Monitors for instructions, writes to `CURSOR_INSTRUCTION.md`  |
| OWUI Tool      | ✅ Working    | Triggered by `s2cursor`, sends instructions to bridge         |
| Shared Folder  | ✅ Configured | `F:\AI\owui-bridge` (Windows) ↔ `/mnt/f/AI/owui-bridge` (WSL) |

## Quick Start

### 1. Start the Watcher (WSL Terminal)

```bash
cd ~/projects/owui-cursor-bridge
python3 cursor/watcher.py
```
````

### 2. Send an Instruction (OWUI)

In any OWUI chat with the bridge tool enabled:

```
s2cursor Create a utility function that validates email addresses
```

### 3. Use in Cursor

Open `/mnt/f/AI/owui-bridge/CURSOR_INSTRUCTION.md` in Cursor, copy the instruction to Cursor's AI chat (Ctrl+L).

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for full details.

```
OWUI (Docker)                    Cursor (WSL)
     │                                │
     │  s2cursor <instruction>        │
     ▼                                │
┌─────────────┐                       │
│ Bridge Tool │                       │
└─────────────┘                       │
     │                                │
     │ writes JSON                    │
     ▼                                ▼
┌─────────────────────────────────────────┐
│     Shared Folder (F:\AI\owui-bridge)   │
│                                         │
│  instructions/*.json → watcher.py       │
│                    ↓                    │
│           CURSOR_INSTRUCTION.md         │
└─────────────────────────────────────────┘
```

## Project Structure

```
owui-cursor-bridge/
├── cursor/
│   └── watcher.py          # Monitors for instructions
├── owui/
│   └── tool.py             # OWUI tool (copy to OWUI admin)
├── docs/
│   └── ARCHITECTURE.md     # Detailed architecture
└── README.md               # You are here
```

## Roadmap

- [x] **Phase 1**: OWUI → Cursor (one-way instructions)
- [ ] **Phase 2**: Cursor → OWUI (bidirectional responses)
- [ ] **Phase 3**: Agentic workflows (multi-step, error recovery)

## License

MIT

```

```
