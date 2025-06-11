import g4f
import json

def generate_ai_roadmap(language_name, level):
    """
    Uses g4f to generate a roadmap for a given programming language and skill level.
    Returns a JSON-formatted study plan.
    """
    prompt = f"""
    Generate a structured 7-week study plan for learning {language_name} at the {level} level. 
    Format the output as a JSON list with each week having a 'week' key (1-7) and a 'topic' key (brief topic name).
    """
    
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract response text
    roadmap_content = response if isinstance(response, str) else response['choices'][0]['message']['content']
    
    try:
        roadmap_json = json.loads(roadmap_content)  # Ensure it is valid JSON
        return json.dumps(roadmap_json)
    except json.JSONDecodeError:
        return json.dumps([])  # Return empty if there's an error
