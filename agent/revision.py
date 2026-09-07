from llm.openrouter import call_llm
import json


# ==============================
# LOAD CINEMATOGRAPHY KNOWLEDGE
# ==============================

def load_cinematography_knowledge():

    with open("data/cinematography.json", "r") as file:
        return json.load(file)


# ==============================
# REVISION
# ==============================

def revise_scene(
    scene,
    recommendations,
    critique,
    memories=None
):

    knowledge = load_cinematography_knowledge()


    # ==============================
    # EXTRACT VALID OPTIONS
    # ==============================

    valid_shot_types = list(
        knowledge["shot_types"].keys()
    )

    valid_camera_angles = list(
        knowledge["camera_angles"].keys()
    )

    valid_camera_movements = list(
        knowledge["camera_movements"].keys()
    )


    # ==============================
    # REVISION PROMPT
    # ==============================

    prompt = f"""
You are the revision component of a Camera Shot Planning Agent.

The original scene is:

{scene}

The current shot plan is:

{recommendations}

The cinematography critic provided this feedback:

{critique}

Previous relevant experiences from memory:

{memories}


================================
AUTHORITATIVE KNOWLEDGE BASE
================================

You MUST use ONLY the following valid options.

VALID SHOT TYPES:

{valid_shot_types}


VALID CAMERA ANGLES:

{valid_camera_angles}


VALID CAMERA MOVEMENTS:

{valid_camera_movements}


================================
REVISION RULES
================================

1. Fix the problems identified by the critic.

2. Keep good recommendations when appropriate.

3. Remove unnecessary shots.

4. Make every shot relevant to the scene.

5. Give every shot a clear cinematic purpose.

6. Make sure the camera angle contributes to the storytelling.

7. Make sure the camera movement is practical.

8. Apply useful lessons from previous memories.

9. Do NOT invent new shot types.

10. Do NOT invent new camera angles.

11. Do NOT invent new camera movements.

12. Use the EXACT names from the knowledge base.

For example, if the knowledge base contains:

"High Angle"

you must write:

"High Angle"

Do not write:

"High-Angle Shot"

"Overhead Angle"

"Slightly High Angle"

or any other variation.

The same rule applies to shot types and camera movements.


================================
FINAL VALIDATION
================================

Before returning the answer, check every shot.

Every:

- Shot type

must exist in VALID SHOT TYPES.

Every:

- Camera angle

must exist in VALID CAMERA ANGLES.

Every:

- Camera movement

must exist in VALID CAMERA MOVEMENTS.


================================
OUTPUT FORMAT
================================

Return ONLY the improved shot plan.

For each shot provide:

Shot:
- Shot type:
- Camera angle:
- Camera movement:
- Purpose:
- Scene moment:

Do not explain the revision process.
Do not mention the critic.
Do not mention the knowledge base.

Only provide the final improved shot plan.
"""


    # ==============================
    # CALL LLM
    # ==============================

    return call_llm(prompt)