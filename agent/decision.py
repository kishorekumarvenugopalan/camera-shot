import json
from llm.openrouter import call_llm


# ==============================
# FIRST DECISION
# ==============================

def make_decision(scene, memories=None):

    prompt = f"""
You are the decision-making component of a Camera Shot Planning Agent.

Your job is NOT to create the final shot plan.

You must analyze the scene and decide what tool the agent should use.

Previous memories from earlier scenes:

{memories}

Available tools:

1. cinematography_tool
   - Provides cinematography principles.
   - Provides valid shot types.
   - Provides valid camera angles.
   - Provides valid camera movements.

2. shot_tool
   - Provides available camera shot types.

3. scene_tool
   - Analyzes scene elements such as characters, location, objects,
     time, actions, mood, and important details.

Scene:

{scene}

Choose the tool that provides the most useful missing information.

Return ONLY valid JSON in this exact format:

{{
    "tool": "tool_name",
    "reason": "short explanation"
}}
"""

    response = call_llm(prompt)

    try:

        return json.loads(response)

    except json.JSONDecodeError:

        print("Invalid decision returned by LLM:")
        print(response)

        return None


# ==============================
# NEXT TOOL DECISION
# ==============================

def make_next_decision(
    scene,
    tool_results,
    memories=None
):

    prompt = f"""
You are the decision-making component of a Camera Shot Planning Agent.

The original scene is:

{scene}

Previous relevant memories from earlier scenes:

{memories}

The agent has already used the following tools:

{tool_results}

You must now decide what the agent should do next.

================================
IMPORTANT
================================

Look carefully at ALL information already collected.

The previous tool results may contain detailed scene analysis.

Use that information when deciding what information is still missing.

Do NOT ignore the previous tool results.

================================
AVAILABLE TOOLS
================================

1. cinematography_tool

Provides:

- Cinematography principles
- Valid shot types
- Valid camera angles
- Valid camera movements

2. shot_tool

Provides:

- Available camera shot types

3. scene_tool

Provides:

- Characters
- Location
- Time
- Objects
- Actions
- Mood
- Important scene details

4. none

Use "none" when enough information has been collected.

================================
DECISION RULES
================================

1. Examine the original scene.

2. Examine the previous memories.

3. Examine ALL previous tool results.

4. Identify what information has already been collected.

5. Identify what useful information is still missing.

6. Choose the tool that provides the most useful missing information.

7. Do NOT repeatedly call a tool when its information has already
   been sufficiently collected.

8. If enough information exists for cinematography reasoning,
   choose "none".

================================
EXAMPLE
================================

If scene_tool has already provided:

- characters
- location
- time
- actions
- mood

then there may be no reason to call scene_tool again.

The agent may instead choose:

shot_tool

or:

cinematography_tool

If the available information is already sufficient, choose:

none

================================
OUTPUT
================================

Return ONLY valid JSON in this exact format:

{{
    "tool": "tool_name",
    "reason": "short explanation"
}}
"""

    response = call_llm(prompt)

    try:

        return json.loads(response)

    except json.JSONDecodeError:

        print("Invalid next decision returned by LLM:")
        print(response)

        return None