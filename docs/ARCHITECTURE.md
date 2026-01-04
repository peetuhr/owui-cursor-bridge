```markdown
# OWUI-Cursor Bridge

## What Is This?

A tool that connects Open WebUI (OWUI) and Cursor IDE, letting you:

- **Plan** features in OWUI with a long-context model (like Opus)
- **Execute** those plans directly in Cursor
- **Iterate** as OWUI receives feedback from Cursor

Think of it as giving your AI architect hands.

---

## The Problem

When coding with AI assistants:

1. **Context fragmentation**: You plan in one window, code in another, copy-paste between them
2. **Cursor's chat is tactical**: Great for "fix this function," less great for "let's design this system"
3. **No memory between tools**: Cursor doesn't know what you discussed in OWUI
4. **Manual handoff breaks flow**: Every copy-paste is a context switch

---

## The Solution

An OWUI Tool (Python function) that:

1. Takes structured instructions from your OWUI conversation
2. Writes them to a location Cursor can see
3. A watcher script in Cursor picks them up
4. Executes the instruction (create file, edit file, run command)
5. Writes the result back
6. OWUI reads the result and continues the conversation

---

## Architecture
```

┌─────────────────────────────────────────────────────────────┐
│ OWUI (Docker) │
│ │
│ User ←→ Planning Agent (Opus) │
│ │ │
│ ▼ │
│ bridge_execute() tool │
│ │ │
└────────────────────┼────────────────────────────────────────┘
│
▼
┌─────────────────┐
│ Shared Volume │
│ │
│ instructions/ │
│ responses/ │
└─────────────────┘
│
┌────────────────────┼────────────────────────────────────────┐
│ ▼ │
│ watcher.py (always running) │
│ │ │
│ ▼ │
│ Cursor IDE │
│ │
│ WSL / Ubuntu │
└─────────────────────────────────────────────────────────────┘

````

---

## Instruction Format

OWUI sends (JSON):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-15T10:30:00Z",
  "action": "create_file",
  "payload": {
    "path": "src/utils/helpers.py",
    "content": "def greet(name):\n    return f'Hello, {name}!'"
  },
  "context": "Creating a simple greeting utility"
}
````

Cursor responds (JSON):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-15T10:30:01Z",
  "status": "success",
  "result": {
    "files_changed": ["src/utils/helpers.py"],
    "output": "File created successfully"
  }
}
```

---

## Supported Actions

| Action        | Description              | Payload                     |
| ------------- | ------------------------ | --------------------------- |
| `create_file` | Create a new file        | `path`, `content`           |
| `edit_file`   | Modify existing file     | `path`, `find`, `replace`   |
| `read_file`   | Get file contents        | `path`                      |
| `run_command` | Execute terminal command | `command`, `cwd` (optional) |
| `list_files`  | List directory contents  | `path`                      |

---

## Project Phases

### Phase 1: Fire and Forget (MVP) ✅ COMPLETE

- [x] Watcher script monitors instructions folder
- [x] OWUI tool writes instruction files (triggered by `s2cursor`)
- [x] Watcher processes JSON and writes `CURSOR_INSTRUCTION.md`
- [x] Instruction history maintained (last 5)
- [x] JSON files cleaned up after processing

### Phase 2: Bidirectional Communication

- [ ] Watcher writes response files
- [ ] OWUI tool waits for and reads responses
- [ ] Agent can see results and continue

### Phase 3: Agentic Workflows

- [ ] Multi-step execution plans
- [ ] Error recovery and retry logic
- [ ] Git operations (commit, branch, etc.)

---

## Technical Details

### Communication Method

Using a **shared volume** mounted in both Docker (OWUI) and accessible from WSL:

```
/path/to/bridge/
├── instructions/     # OWUI writes here
│   └── {uuid}.json
├── responses/        # Watcher writes here
│   └── {uuid}.json
└── logs/             # Debug logs
    └── watcher.log
```

### Why Not HTTP/WebSocket?

Simpler. Files work. No ports to manage. No auth to configure. We can upgrade later if needed.

### Security Considerations

This tool executes arbitrary code. Acceptable for personal use. For public distribution:

- Whitelist allowed actions
- Require confirmation for destructive operations
- Sandbox command execution
- Never expose the shared folder to the network

---

## File Structure

```
owui-cursor-bridge/
├── docs/
│   └── ARCHITECTURE.md      # This file
├── owui/
│   ├── tool.py              # OWUI function definition
│   └── prompts/
│       └── bridge-agent.md  # System prompt for planning agent
├── cursor/
│   └── watcher.py           # File watcher script
├── shared/
│   └── protocol.py          # Shared instruction/response schemas
├── examples/
│   └── walkthrough.md       # Tutorial for first-time users
└── .github/
    └── CONTRIBUTING.md
```

---

## Success Criteria

**Phase 1 is done when:**

1. I can describe a file in OWUI
2. Say "create it"
3. The file appears in my Cursor workspace
4. Without touching Cursor myself

---

## Open Questions

1. ~~Where should the shared volume live?~~ → `F:\AI\owui-bridge` (Windows) / `/mnt/f/AI/owui-bridge` (WSL)
2. How to handle Cursor not being open? → Currently manual; user opens `CURSOR_INSTRUCTION.md`
3. Should watcher auto-start with WSL? → Future enhancement
4. How to surface errors clearly in OWUI? → Phase 2 (response files)

---

## References

- [Open WebUI Tools Documentation](https://docs.openwebui.com/features/plugin/tools/)
- [Python watchdog library](https://python-watchdog.readthedocs.io/)
- [Cursor CLI](https://docs.cursor.com/context/codebase-indexing#cli)

```

```
