"""
title: OWUI Cursor Bridge
author: peetuhr
version: 0.2.1
license: MIT
description: Sends instructions to Cursor IDE via the bridge. Trigger with "s2cursor"
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        enabled: bool = Field(
            default=True, description="Enable or disable the Cursor bridge"
        )
        trigger_keyword: str = Field(
            default="s2cursor", description="Keyword that triggers the bridge"
        )

    def __init__(self):
        self.valves = self.Valves()
        # Bridge folder path (inside Docker container)
        self.bridge_path = Path("/app/backend/data/bridge")
        self.instructions_path = self.bridge_path / "instructions"

    def send_to_cursor(self, message: str) -> str:
        """
        Send an instruction to Cursor IDE.

        This tool is triggered when the user's message contains the s2cursor keyword.
        The instruction is written to a shared folder where the Cursor watcher picks it up.

        :param message: The user's full message containing the instruction
        :return: Confirmation message
        """
        # Check if enabled
        if not self.valves.enabled:
            return "Cursor bridge is disabled."

        # Check for trigger keyword
        trigger = self.valves.trigger_keyword.lower()
        if trigger not in message.lower():
            # No trigger found - don't process
            return ""

        # Extract the instruction (everything after the trigger keyword)
        message_lower = message.lower()
        trigger_pos = message_lower.find(trigger)
        instruction = message[trigger_pos + len(trigger) :].strip()

        if not instruction:
            return "Please provide an instruction after @cursor"

        # Ensure instructions directory exists
        self.instructions_path.mkdir(parents=True, exist_ok=True)

        # Create instruction payload
        instruction_id = str(uuid.uuid4())
        payload = {
            "id": instruction_id,
            "timestamp": datetime.now().isoformat(),
            "action": "instruct",
            "payload": {
                "instruction": instruction,
                "context": "Sent from OWUI planning session",
            },
        }

        # Write instruction file
        instruction_file = self.instructions_path / f"{instruction_id[:8]}.json"
        instruction_file.write_text(json.dumps(payload, indent=2))

        return f"""✓ **Instruction sent to Cursor**

**ID:** `{instruction_id[:8]}`
**Instruction:** {instruction}

The watcher will pick this up and Cursor will process it."""
