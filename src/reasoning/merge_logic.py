def merge_observations(inspection, thermal):

    merged = []

    for ins in inspection:
        area = ins.get("area","Not Available")

        related_thermal = [
            t for t in thermal if t.get("area") == area
        ]

        conflict = False

        if related_thermal:
            t_obs = related_thermal[0]["thermal_observation"]

            # simple conflict heuristic
            if "high" in t_obs.lower() and "minor" in ins["issue"].lower():
                conflict = True

            merged.append({
                "area": area,
                "inspection_issue": ins["issue"],
                "thermal_finding": t_obs,
                "conflict": conflict,
                "evidence": ins["evidence"]
            })

        else:
            merged.append({
                "area": area,
                "inspection_issue": ins["issue"],
                "thermal_finding": "Not Available",
                "conflict": False,
                "evidence": ins["evidence"]
            })

    return merged
