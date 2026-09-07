from tools.shot_tool import shot_tool
from tools.scene_tool import scene_tool
from tools.cinematography_tool import cinematography_tool
from llm.openrouter import call_llm


# ==============================
# EXECUTE TOOL
# ==============================

def execute_tool(decision, scene):

    tool_name = decision.get("tool")

    if tool_name == "shot_tool":

        return shot_tool(scene)

    elif tool_name == "scene_tool":

        return scene_tool(scene)

    elif tool_name == "cinematography_tool":

        return cinematography_tool(scene)

    else:

        return {
            "error": f"Unknown tool: {tool_name}"
        }


# ==============================
# ANALYZE ALL TOOL RESULTS
# ==============================

def analyze_tool_result(scene, tool_results):

    prompt = f"""
You are a cinematography reasoning assistant.

You previously received this scene:

{scene}

During the reasoning process, the agent used one or more tools.

Here are ALL tool results collected by the agent:

{tool_results}

Use all of these tool results together.

Your job is to reason about the cinematography of the scene.

Recommend suitable camera shots for this scene.

For each recommendation, provide:

- Shot type
- Camera angle
- Purpose
- Scene moment

Use the information provided by the tools.

Do not create the final polished shot plan yet.

Just provide the cinematography reasoning and recommendations.
"""

    return call_llm(prompt)