import json
import os


class Memory:

    def __init__(self, file_path="memory/memories.json"):

        self.file_path = file_path

        if os.path.exists(self.file_path):

            with open(self.file_path, "r") as file:
                self.memories = json.load(file)

        else:

            self.memories = []


    # ==============================
    # ADD MEMORY
    # ==============================

    def add(self, information):

        self.memories.append(information)

        with open(self.file_path, "w") as file:
            json.dump(
                self.memories,
                file,
                indent=4
            )


    # ==============================
    # GET ALL MEMORIES
    # ==============================

    def get_all(self):

        return self.memories


    # ==============================
    # GET RECENT MEMORIES
    # ==============================

    def get_recent(self, count=3):

        return self.memories[-count:]


    # ==============================
    # SEARCH MEMORY
    # ==============================

    def search(self, scene):

        results = []

        # Common words that are not very useful
        # for scene matching

        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "at",
            "in",
            "on",
            "of",
            "to",
            "and",
            "or",
            "with",
            "for",
            "from",
            "he",
            "she",
            "they",
            "his",
            "her",
            "their",
            "this",
            "that"
        }

        # Convert scene into meaningful words

        scene_words = set(
            word.lower().strip(".,!?")
            for word in scene.split()
            if word.lower().strip(".,!?") not in stop_words
            and len(word.strip(".,!?")) > 3
        )


        # Compare scene with every memory

        for memory in self.memories:

            memory_text = str(memory).lower()

            score = 0

            for word in scene_words:

                if word in memory_text:

                    score += 1


            results.append(
                (score, memory)
            )


        # Highest matching memories first

        results.sort(
            reverse=True,
            key=lambda x: x[0]
        )


        # Return top 3 relevant memories

        return [
            memory
            for score, memory in results[:3]
            if score > 0
        ]