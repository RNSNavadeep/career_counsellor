def build_response(career):
    """
    Build a formatted career recommendation text block.
    Used by app.py for CLI display.
    """
    salary = career.get("salary", {})
    matched = career.get("matched_keywords", [])
    matched_text = ", ".join(str(k) for k in matched if k) or "N/A"
    confidence = career.get("confidence", 0)

    text = f"""
╔══════════════════════════════════════════════╗
  🤖  AI Career Counsellor — Recommendation
╚══════════════════════════════════════════════╝

  🎯  Career    : {career['career']}
  📈  Confidence: {confidence:.0f}%
  ✅  Matched   : {matched_text}

  📖  Description:
      {career['description']}

  💰  Salary (Entry): {salary.get('entry', 'N/A')}
"""
    return text