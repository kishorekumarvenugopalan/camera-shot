from llm.openrouter import call_llm
import json


def scene_tool(scene):
    """
    Uses the LLM to analyze the user's scene.
    """

    prompt = f"""
You are a scene analysis tool for a Camera Shot Planning Agent.

Analyze the following scene:

{scene}

Extract the important information needed for cinematography planning.

Return ONLY valid JSON in this exact format:

{{
    "characters": [],
    "location": "",
    "time": "",
    "objects": [],
    "actions": [],
    "mood": "",
    "important_details": []
}}

Rules:

1. Identify all important characters.
2. Identify the location.
3. Identify the time of day or setting if mentioned.
4. Identify important objects.
5. Identify the important actions happening in the scene.
6. Identify the mood or emotional atmosphere.
7. Identify details that could affect camera shot decisions.
8. Do not invent unnecessary information.
9. If something is not mentioned, use an empty value.

Return ONLY JSON.
"""

    response = call_llm(prompt)

    try:

        return json.loads(response)

    except json.JSONDecodeError:

        print("Invalid scene analysis returned by LLM:")
        print(response)

        return {
            "error": "Scene analysis failed",
            "raw_response": response
        }