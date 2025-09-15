import json
import re

def remove_json_tag(json_string: str) -> str:
    # Remove ```json fences or stray "json" prefix
    cleaned = re.sub(r"^```json\s*|\s*```$", "", json_string.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"^json\s*", "", cleaned.strip())  # handle 'json\n{...}'
    return cleaned.strip()


if __name__ == "__main__":
    json_string = '''json
    {
      "question": "Okay, that's helpful! To assist you better, could you please list the ingredients you have on hand and also what is the time you are willing to spend?",
      "user_intent": {
        "ingredients_on_hand": [],
        "time_budget_minutes": null,
        "cuisine_pref": null,
        "dietary_rules": [],
        "equipment": [],
        "skill_level": null,
        "servings": 3,
        "flavor_prefs": [],
        "missing_slots": [
          "ingredients_on_hand",
          "time_budget_minutes"
        ]
      }
    }
    '''

    res = remove_json_tag(json_string)
    print(res)
    data = json.loads(res)
    print(data)

    print(data["user_intent"])
    print(data['question'])
