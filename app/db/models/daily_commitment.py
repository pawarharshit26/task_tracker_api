class DailyCommitment(CreateUpdateDeleteModel):
    """
    Intent for a Day
    A promise you make before execution.

    Examples:
	•	“Practice flute 30 min”
	•	“Solve 2 DSA problems”

    Why it exists
    •	Separates intention from reality
    •	Without this, reflection is meaningless

    Rules
    •	Created at start of day (or day before)
	•	One commitment belongs to one Phase
	•	Can be skipped (but logged)
    """
    __tablename__ = "daily_commitment"