from agent.decision import make_decision, make_next_decision
from agent.planner import execute_tool, analyze_tool_result
from memory.memory import Memory
from agent.critic import critique_scene
from agent.revision import revise_scene
from agent.formatter import format_final_plan


# ==============================
# INPUT SCENE
# ==============================

scene = input("Enter the scene description:\n\n")


# ==============================
# CREATE MEMORY
# ==============================

memory = Memory()


# ==============================
# SEARCH RELEVANT MEMORIES
# ==============================

previous_memories = memory.search(scene)


# ==============================
# STEP 1: FIRST DECISION
# ==============================

decision = make_decision(
    scene,
    previous_memories
)


if decision is None:
    print("Unable to create a shot plan.")
    exit()


# ==============================
# TRACK USED TOOLS
# ==============================

used_tools = set()

all_tool_results = []


# ==============================
# STEP 2: EXECUTE FIRST TOOL
# ==============================

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


# ==============================
# STEP 3: TOOL DECISION LOOP
# ==============================

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


    # ==============================
    # NO MORE TOOLS
    # ==============================

    if next_tool == "none":
        break


    # ==============================
    # PREVENT REPEATED TOOL
    # ==============================

    if next_tool in used_tools:
        break


    # ==============================
    # EXECUTE NEW TOOL
    # ==============================

    new_tool_result = execute_tool(
        next_decision,
        scene
    )


    # ==============================
    # TRACK TOOL
    # ==============================

    used_tools.add(next_tool)


    # ==============================
    # STORE TOOL RESULT
    # ==============================

    all_tool_results.append({
        "tool": next_tool,
        "result": new_tool_result
    })


    tool_call_count += 1


# ==============================
# STEP 4: CINEMATOGRAPHY REASONING
# ==============================

recommendations = analyze_tool_result(
    scene,
    all_tool_results
)


# ==============================
# STEP 5: CRITIC → REVISION LOOP
# ==============================

MAX_REVISIONS = 2

current_plan = recommendations

revision_count = 0

final_critique = None


while revision_count <= MAX_REVISIONS:


    # ==============================
    # RUN CRITIC
    # ==============================

    critique = critique_scene(
        scene,
        current_plan,
        previous_memories
    )


    # ==============================
    # EXTRACT VERDICT
    # ==============================

    verdict = None


    for line in critique.splitlines():

        line = line.strip()


        if line.startswith("VERDICT:"):

            verdict = line.replace(
                "VERDICT:",
                ""
            ).strip().upper()

            break


    # ==============================
    # PASS
    # ==============================

    if verdict == "PASS":

        final_critique = critique

        break


    # ==============================
    # UNKNOWN VERDICT
    # ==============================

    if verdict != "FAIL":

        final_critique = critique

        break


    # ==============================
    # MAX REVISION CHECK
    # ==============================

    if revision_count >= MAX_REVISIONS:

        final_critique = critique

        break


    # ==============================
    # REVISION
    # ==============================

    revision_count += 1


    current_plan = revise_scene(
        scene,
        current_plan,
        critique,
        previous_memories
    )


# ==============================
# FINAL APPROVED PLAN
# ==============================

revised_plan = current_plan


# ==============================
# STEP 6: FORMAT FINAL PLAN
# ==============================

final_plan = format_final_plan(
    scene,
    revised_plan
)


# ==============================
# STEP 7: STORE EXPERIENCE
# ==============================

memory.add({
    "scene": scene,
    "tool_used": list(used_tools),
    "tool_results": all_tool_results,
    "recommendations": recommendations,
    "critique": final_critique,
    "revised_plan": revised_plan,
    "final_plan": final_plan,
    "revision_count": revision_count
})


# ==============================
# STEP 8: FINAL USER OUTPUT
# ==============================

print(final_plan)