STAGES = {
    0: "audio",
    1: "360p",
    2: "480p",
    3: "720p",
    4: "1080p",
    5: "best",
}


def parse(expression):
    if not isinstance(expression, dict):
        raise ValueError("Easyder syntax must be a dictionary")

    result = {
        "url": None,
        "blocks": []
    }

    for key, variable in expression.items():
        key = str(key).strip()
        variable = str(variable).strip()

        if key.startswith("video[") and key.endswith("]"):
            stage_text = key[6:-1]

            try:
                stage = int(stage_text)
            except ValueError:
                raise ValueError(f"Invalid video stage: {stage_text}")

            if stage not in STAGES:
                raise ValueError(f"Unknown video stage: {stage}")

            result["blocks"].append({
                "type": "video",
                "stage": stage,
                "variable": variable
            })
            continue

        if key == "playlist":
            parts = variable.split(":")

            if len(parts) != 3:
                raise ValueError(
                    "Playlist syntax: QUALITY:SKIP:COUNT"
                )

            try:
                quality = int(parts[0])
                skip = int(parts[1])
                count = int(parts[2])
            except ValueError:
                raise ValueError(
                    "Playlist values must be numbers"
                )

            if quality not in STAGES:
                raise ValueError(
                    f"Unknown playlist quality: {quality}"
                )

            if skip < 0:
                raise ValueError(
                    "Playlist skip cannot be negative"
                )

            if count <= 0:
                raise ValueError(
                    "Playlist count must be greater than 0"
                )

            result["blocks"].append({
                "type": "playlist",
                "quality": quality,
                "skip": skip,
                "count": count,
                "variable": None
            })
            continue

        result["blocks"].append({
            "type": key,
            "variable": variable
        })

    return result
