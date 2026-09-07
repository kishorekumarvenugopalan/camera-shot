def shot_tool(scene):
    """
    Provides basic camera shot recommendations
    based on the scene.
    """

    return {
        "available_shots": [
            "Extreme Wide Shot",
            "Wide Shot",
            "Medium Shot",
            "Medium Close-Up",
            "Close-Up",
            "Extreme Close-Up",
            "Over-the-Shoulder Shot",
            "Point-of-View Shot"
        ],
        "scene": scene
    }