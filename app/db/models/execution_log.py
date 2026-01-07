class ExecutionLog(CreateUpdateDeleteModel):
    """
    What Actually Happened
    What actually happened — truth, not intention.

    Examples:
	•	“Practiced 12 minutes, distracted”
	•	“Did 1 problem, got stuck”

    Why it exists
    •	Reality check
    •	Prevents self-deception
    •	Enables learning

    Rules
    •	ExecutionLog belongs to DailyCommitment
    •	Can be empty or partial
    •	Immutable after day ends (later)
    """
    __tablename__ = "execution_log"