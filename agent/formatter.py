from llm.openrouter import call_llm


def format_final_plan(scene, shot_plan):

    prompt = f"""
You are the final response formatter for a Camera Shot Planning Agent.

Original scene:

{scene}

Approved shot plan:

{shot_plan}

Your job is ONLY to present the approved shot plan
as a clean, natural ChatGPT-style response.

Do NOT create new shots.

Do NOT change the cinematography decisions.

Do NOT invent camera angles.

Do NOT invent camera movements.

Do NOT add information that is not present
in the approved shot plan.

================================
OUTPUT STYLE
================================

Write the response naturally, like an AI cinematography
assistant talking to a filmmaker.

Start with a short sentence such as:

"Here's the camera shot plan for your scene:"

Then list the shots clearly.

Use this format:

Shot 1

Shot Type: <shot type>
Camera Angle: <camera angle>
Camera Movement: <camera movement>

Scene Moment: <scene moment>

Purpose: <purpose>


Shot 2

Shot Type: <shot type>
Camera Angle: <camera angle>
Camera Movement: <camera movement>

Scene Moment: <scene moment>

Purpose: <purpose>

Continue for all shots.

================================
IMPORTANT
================================

Do NOT use:

========================================
FINAL CAMERA SHOT PLAN
========================================

Do NOT use terminal-style separators.

Do NOT use ASCII borders.

Do NOT use excessive symbols.

Do NOT mention the critic.

Do NOT mention the revision process.

Do NOT mention the tools.

Do NOT mention the knowledge base.

Do NOT explain how the agent works.

Only return the clean final camera shot plan.

Return ONLY the response that should be shown
directly to the user in the chat.
"""

    return call_llm(prompt)