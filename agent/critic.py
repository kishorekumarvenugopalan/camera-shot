from llm.openrouter import call_llm
import json


# ==============================
# LOAD CINEMATOGRAPHY KNOWLEDGE
# ==============================

def load_cinematography_knowledge():

    with open("data/cinematography.json", "r") as file:
        return json.load(file)


# ==============================
# CRITIC
# ==============================

def critique_scene(scene, recommendations, memories=None):

    knowledge = load_cinematography_knowledge()

    valid_shot_types = list(
        knowledge["shot_types"].keys()
    )

    valid_camera_angles = list(
        knowledge["camera_angles"].keys()
    )

    valid_camera_movements = list(
        knowledge["camera_movements"].keys()
    )

    prompt = f"""
You are a strict cinematography critic.

Analyze the following scene:

{scene}

The Camera Shot Planning Agent produced:

{recommendations}

Previous relevant experiences from memory:

{memories}

================================
AUTHORITATIVE KNOWLEDGE BASE
================================

Valid shot types:

{valid_shot_types}

Valid camera angles:

{valid_camera_angles}

Valid camera movements:

{valid_camera_movements}

================================
STRICT VALIDATION RULES
================================

You MUST treat the knowledge base above as authoritative.

1. A shot type is valid ONLY if it exactly matches one of the
   valid shot types.

2. A camera angle is valid ONLY if it exactly matches one of the
   valid camera angles.

3. A camera movement is valid ONLY if it exactly matches one of
   the valid camera movements.

4. Do NOT accept synonyms or approximate descriptions.

For example:

"Overhead Shot" is NOT a valid shot type.

"Straight-on" is NOT a valid camera angle.

"Slightly above eye level" is NOT a valid camera angle.

"Tracking Shot" should NOT be treated as a shot type.
Tracking is a camera movement.

5. If an invalid term is found, identify it as an issue and
   recommend replacing it with a valid term from the knowledge base.

6. Check whether every shot actually matches the scene.

7. Check whether every shot has a clear cinematic purpose.

8. Check whether the camera angle contributes to the storytelling.

9. Check whether the sequence of shots is useful for filming.

10. Check whether previous memories contain lessons or mistakes
    that should be considered.

================================
VERDICT
================================

Return:

VERDICT: PASS

only if there are NO important problems.

Otherwise return:

VERDICT: FAIL

================================
RESPONSE FORMAT
================================

Return ONLY this format:

VERDICT: PASS or FAIL

ISSUES:
- issue 1
- issue 2
- issue 3

SUGGESTIONS:
- suggestion 1
- suggestion 2
- suggestion 3
"""

    return call_llm(prompt)