class Goal(CreateUpdateDeleteModel):
    """
    Outcome-Oriented
    
    Examples:
	•	“Become senior backend engineer”
	•	“Perform flute recital confidently”

    Why
    •	Gives direction to effort
    •	Still abstract, not daily

    Rules
    •	Track can have multiple goals (but few active)
    •	Goals can overlap in time
    """
    __tablename__ = "goal"