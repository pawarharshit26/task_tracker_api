class Phase(CreateUpdateDeleteModel):
    """
    Time-Boxed Focus
    Examples:
	•	“DSA Foundation – 8 weeks”
	•	“Flute basics – breath control”

    Why
    •	Humans need short horizons
    •	Prevents endless vague goals

    Rules
    •	Phase has start & end dates
    •	Only 1 active phase per goal (constraint)
    """
    __tablename__ = "phase"