import json


def cinematography_tool(scene):

    with open("data/cinematography.json", "r") as file:
        knowledge = json.load(file)

    return {
        "scene": scene,
        "cinematography_knowledge": knowledge
    }