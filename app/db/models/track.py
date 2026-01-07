class Track(CreateUpdateDeleteModel):    
    """
    Skill / Focus Area
    Track represents a life domain under a Theme.
    Examples:
	•	Backend Engineering
	•	Flute Practice
	•	Applied AI
	•	System Design Interviews

    Why
	•	Themes are too broad to execute
	•	Tracks are workable lanes

    Rules
    •	Track belongs to ONE Theme
    •	Can be paused
    •	Has its own cadence
    """
    __tablename__ = "track" 