from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker

import sys
import os

# Add the project root to Python path so we can import our modules
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from recommendation import recommend_career


class ActionRecommendCareer(Action):
    """
    Single Rasa custom action that handles:
      1. Career recommendation  (new user input about interests/skills)
      2. Follow-up questions    (roadmap / salary / skills / companies / projects)

    Both cases are handled inside recommendation.py using intent_router + memory.
    """

    def name(self):
        return "action_recommend_career"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain
    ):
        user_message = tracker.latest_message.get("text", "")

        result = recommend_career(user_message)

        # ── Follow-up or error message (plain string) ────────────────────────
        if isinstance(result, str):
            dispatcher.utter_message(text=result)

        # ── Career Recommendation (dict with full career data) ───────────────
        elif isinstance(result, dict):

            confidence  = result.get("confidence", 0)
            career_domain = result.get("domain", "General")
            matched     = result.get("matched_keywords", [])

            # Filter out None values that spellchecker may produce
            matched = [str(k) for k in matched if k]
            matched_text = ", ".join(matched) if matched else "Not Available"

            response = (
                f"╔══════════════════════════════════════╗\n"
                f"  🤖  Career Recommendation\n"
                f"╚══════════════════════════════════════╝\n\n"
                f"  🎯  Career    : {result['career']}\n"
                f"  🏷️  Domain    : {career_domain}\n"
                f"  📈  Confidence: {confidence:.0f}%\n"
                f"  ✅  Matched   : {matched_text}\n\n"
                f"  📖  {result['description']}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"  💡 You can ask me:\n"
                f"     roadmap  •  salary  •  skills\n"
                f"     companies  •  projects  •  description"
            )

            dispatcher.utter_message(text=response)

        # ── No Career Found ──────────────────────────────────────────────────
        else:
            dispatcher.utter_message(
                text=(
                    "🤔 I couldn't find a matching career for that.\n\n"
                    "Try describing your interests in more detail — for example:\n"
                    "  • 'I love machine learning and Python'\n"
                    "  • 'I enjoy Figma wireframing and UI UX design'\n"
                    "  • 'I like digital marketing and SEO'\n"
                    "  • 'I enjoy financial modeling and valuation'"
                )
            )

        return []
