from flask import Flask, request, jsonify
from flask_cors import CORS

from agent.decision import make_decision, make_next_decision
from agent.planner import execute_tool, analyze_tool_result
from memory.memory import Memory
from agent.critic import critique_scene
from agent.revision import revise_scene
from agent.formatter import format_final_plan


app = Flask(__name__)

CORS(app)


# ==========================================
# GENERATE CAMERA SHOT PLAN
# ==========================================

def generate_shot_plan(scene):

    # Create memory
    memory = Memory()

    # Search previous relevant experiences
    previous_memories = memory.search(scene)


    # ==========================================
    # FIRST DECISION
    # ==========================================

    decision = make_decision(
        scene,
        previous_memories
    )

    if decision is None:
        return None


    # ==========================================
    # TRACK TOOLS
    # ==========================================

    used_tools = set()

    all_tool_results = []


    # ==========================================
    # FIRST TOOL
    # ==========================================

    first_tool = decision.get("tool")


    if first_tool != "none":

        tool_result = execute_tool(
            decision,
            scene
        )

        used_tools.add(first_tool)

        all_tool_results.append({
            "tool": first_tool,
            "result": tool_result
        })


    # ==========================================
    # TOOL DECISION LOOP
    # ==========================================

    MAX_TOOL_CALLS = 3

    tool_call_count = len(used_tools)


    while tool_call_count < MAX_TOOL_CALLS:

        next_decision = make_next_decision(
            scene,
            all_tool_results,
            previous_memories
        )


        if next_decision is None:
            break


        next_tool = next_decision.get("tool")


        if next_tool == "none":
            break


        if next_tool in used_tools:
            break


        new_tool_result = execute_tool(
            next_decision,
            scene
        )


        used_tools.add(next_tool)


        all_tool_results.append({
            "tool": next_tool,
            "result": new_tool_result
        })


        tool_call_count += 1


    # ==========================================
    # CINEMATOGRAPHY REASONING
    # ==========================================

    recommendations = analyze_tool_result(
        scene,
        all_tool_results
    )


    # ==========================================
    # CRITIC + REVISION
    # ==========================================

    MAX_REVISIONS = 2

    current_plan = recommendations

    revision_count = 0

    final_critique = None


    while revision_count <= MAX_REVISIONS:

        critique = critique_scene(
            scene,
            current_plan,
            previous_memories
        )


        verdict = None


        for line in critique.splitlines():

            line = line.strip()


            if line.startswith("VERDICT:"):

                verdict = line.replace(
                    "VERDICT:",
                    ""
                ).strip().upper()

                break


        if verdict == "PASS":

            final_critique = critique

            break


        if verdict != "FAIL":

            final_critique = critique

            break


        if revision_count >= MAX_REVISIONS:

            final_critique = critique

            break


        revision_count += 1


        current_plan = revise_scene(
            scene,
            current_plan,
            critique,
            previous_memories
        )


    # ==========================================
    # FORMAT FINAL PLAN
    # ==========================================

    final_plan = format_final_plan(
        scene,
        current_plan
    )


    # ==========================================
    # SAVE EXPERIENCE TO MEMORY
    # ==========================================

    memory.add({
        "scene": scene,
        "tool_used": list(used_tools),
        "tool_results": all_tool_results,
        "recommendations": recommendations,
        "critique": final_critique,
        "revised_plan": current_plan,
        "final_plan": final_plan,
        "revision_count": revision_count
    })


    return final_plan


# ==========================================
# API ROUTE
# ==========================================

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "No JSON data received"
        }), 400


    scene = data.get("scene")


    if not scene:

        return jsonify({
            "error": "Scene description is required"
        }), 400


    try:

        final_plan = generate_shot_plan(scene)


        if final_plan is None:

            return jsonify({
                "error": "Agent failed to generate a shot plan"
            }), 500


        return jsonify({
            "success": True,
            "scene": scene,
            "final_plan": final_plan
        })


    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )