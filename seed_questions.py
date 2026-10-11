"""seed_questions.py
--------------------
Populates the questions table with exactly 20 questions across 4 parameters
(5 questions each) used by the MindSync digital loneliness assessment.

Parameters:
  1. Smartphone Usage          (Q1–Q5)
  2. Relationship / Love Failure (Q6–Q10)
  3. Betrayal / Trust Issues   (Q11–Q15)
  4. Financial Difficulties    (Q16–Q20)

Run from the project root:
    python seed_questions.py
"""

from app import create_app
from app.extensions import db
from app.models.question import Question


QUESTIONS = [

    # ── 1. Smartphone Usage (5) ──────────────────────────────────────────────
    Question(
        question_text="How often do you use your smartphone to avoid feelings of loneliness or boredom?",
        category="Smartphone Usage",
        display_order=1,
    ),
    Question(
        question_text="How often do you feel that excessive smartphone use has reduced the quality of your real-life relationships?",
        category="Smartphone Usage",
        display_order=2,
    ),
    Question(
        question_text="How often do you find yourself scrolling through your phone late at night instead of resting?",
        category="Smartphone Usage",
        display_order=3,
    ),
    Question(
        question_text="How often do you feel disconnected from the people around you because of your smartphone use?",
        category="Smartphone Usage",
        display_order=4,
    ),
    Question(
        question_text="How often do you prefer interacting with your phone over having face-to-face conversations?",
        category="Smartphone Usage",
        display_order=5,
    ),

    # ── 2. Relationship / Love Failure (5) ───────────────────────────────────
    Question(
        question_text="How often do past relationship experiences make you feel hesitant to connect with new people?",
        category="Relationship / Love Failure",
        display_order=6,
    ),
    Question(
        question_text="How often do you feel emotionally isolated as a result of a past relationship ending?",
        category="Relationship / Love Failure",
        display_order=7,
    ),
    Question(
        question_text="How often do you find yourself turning to digital platforms for emotional comfort after a relationship difficulty?",
        category="Relationship / Love Failure",
        display_order=8,
    ),
    Question(
        question_text="How often do you feel that your past relationship experiences have made it harder to form meaningful connections?",
        category="Relationship / Love Failure",
        display_order=9,
    ),
    Question(
        question_text="How often do you feel a sense of loneliness that you associate with unresolved relationship experiences?",
        category="Relationship / Love Failure",
        display_order=10,
    ),

    # ── 3. Betrayal / Trust Issues (5) ───────────────────────────────────────
    Question(
        question_text="How often do past experiences of betrayal make you reluctant to open up to others?",
        category="Betrayal / Trust Issues",
        display_order=11,
    ),
    Question(
        question_text="How often do you find it difficult to trust people you meet online or in person?",
        category="Betrayal / Trust Issues",
        display_order=12,
    ),
    Question(
        question_text="How often do trust-related concerns cause you to withdraw from social interactions?",
        category="Betrayal / Trust Issues",
        display_order=13,
    ),
    Question(
        question_text="How often do you feel that a lack of trust in others contributes to your sense of isolation?",
        category="Betrayal / Trust Issues",
        display_order=14,
    ),
    Question(
        question_text="How often do you prefer keeping to yourself rather than risking being let down by others?",
        category="Betrayal / Trust Issues",
        display_order=15,
    ),

    # ── 4. Financial Difficulties (5) ────────────────────────────────────────
    Question(
        question_text="How often do financial pressures make you feel socially withdrawn or isolated?",
        category="Financial Difficulties",
        display_order=16,
    ),
    Question(
        question_text="How often do you avoid social activities because of financial constraints?",
        category="Financial Difficulties",
        display_order=17,
    ),
    Question(
        question_text="How often does financial stress cause you to rely more heavily on digital interactions instead of in-person ones?",
        category="Financial Difficulties",
        display_order=18,
    ),
    Question(
        question_text="How often do financial worries affect your ability to maintain meaningful relationships?",
        category="Financial Difficulties",
        display_order=19,
    ),
    Question(
        question_text="How often do you feel that financial difficulties have increased your sense of loneliness?",
        category="Financial Difficulties",
        display_order=20,
    ),
]


def seed():
    """Clear existing questions and insert the 20-question bank."""
    app = create_app()
    with app.app_context():
        db.session.query(Question).delete()
        db.session.add_all(QUESTIONS)
        db.session.commit()
        print(f"Successfully seeded {len(QUESTIONS)} questions across 4 categories.")
        for cat in ["Smartphone Usage", "Relationship / Love Failure",
                    "Betrayal / Trust Issues", "Financial Difficulties"]:
            count = db.session.query(Question).filter_by(category=cat).count()
            print(f"  {cat}: {count} questions")


if __name__ == "__main__":
    seed()
