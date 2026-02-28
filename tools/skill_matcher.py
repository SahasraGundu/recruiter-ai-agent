# tools/skill_matcher.py

def split_skills(skill_list):
    expanded = []

    for skill in skill_list:
        skill = skill.lower()

        # Replace connectors
        skill = skill.replace(" and ", ",")
        skill = skill.replace(" or ", ",")
        skill = skill.replace("/", ",")
        
        parts = skill.split(",")

        for part in parts:
            cleaned = part.strip()
            if cleaned:
                expanded.append(cleaned)

    return expanded


def normalize(skill):
    skill = skill.lower().strip()

    non_technical = [
        "debugging",
        "fixing software issues",
        "collaborate",
        "testing"
    ]

    if skill in non_technical:
        return None

    # Standard mappings
    mapping = {
        "data structures and algorithms (dsa)": "dsa",
        "data structures and algorithms": "dsa",
        "data structures": "dsa",
        "algorithms": "dsa",
        "object-oriented programming (oop)": "oop",
        "object oriented programming": "oop",
        "version control": "git",
        "git": "git",
        "sql and databases": "sql",
        "databases": "sql",
        "mysql": "sql"
    }

    return mapping.get(skill, skill)


def match_skills(resume_skills, jd_skills):
    # 🔥 Split combined phrases first
    resume_expanded = split_skills(resume_skills)
    jd_expanded = split_skills(jd_skills)

    # 🔥 Normalize after splitting
    resume_set = set(
        normalize(s) for s in resume_expanded
        if normalize(s) is not None
    )

    jd_set = set(
        normalize(s) for s in jd_expanded
        if normalize(s) is not None
    )

    matched = sorted(list(resume_set & jd_set))
    missing = sorted(list(jd_set - resume_set))

    match_percentage = round(
        (len(matched) / len(jd_set)) * 100, 2
    ) if jd_set else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_percentage
    }