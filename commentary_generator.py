# commentary_generator.py

class CommentaryGenerator:
    """
    Generates tailored commentary prompts for an LLM based on game events
    and a user's Qloo-derived taste profile.
    """
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def generate_prompt(self, event: dict, user_taste_profile: dict) -> str:
        """
        Crafts a detailed prompt for the LLM based on the game event
        and the user's preferred commentary style.
        """
        style = user_taste_profile.get("style", "balanced")
        focus_areas = user_taste_profile.get("focus", ["general sports action"])

        base_prompt = f"A sports commentator is covering a live {event['sport']} match."
        event_description = self._get_event_description(event)

        # Tailor the prompt based on the determined style
        if style == "analytical":
            prompt = (
                f"{base_prompt} Provide highly analytical commentary for this event: '{event_description}'. "
                f"Focus on {', '.join(focus_areas)}. Discuss strategy, statistics, efficiency, or historical context. "
                "Keep it concise, professional, and insightful. Use a calm, composed tone."
            )
        elif style == "emotional":
            prompt = (
                f"{base_prompt} Provide passionate and emotional commentary for this event: '{event_description}'. "
                f"Focus on the drama, player narratives, and the impact on the game's momentum. "
                "Convey excitement, tension, or disappointment naturally. Use an enthusiastic, high-energy tone."
            )
        elif style == "humorous":
            prompt = (
                f"{base_prompt} Provide lighthearted and humorous commentary for this event: '{event_description}'. "
                f"Incorporate a playful tone, witty observations, or a relevant, funny analogy. "
                "Keep it entertaining and concise. Use a jovial, slightly cheeky tone."
            )
        else: # Balanced/Default
            prompt = (
                f"{base_prompt} Provide balanced commentary for this event: '{event_description}'. "
                "Focus on the key action, player involvement, and immediate impact. "
                "Keep it engaging and to the point. Use a standard, engaging sports commentary tone."
            )
        return prompt

    def _get_event_description(self, event: dict) -> str:
        """
        Converts raw event data into a natural language description for the LLM.
        Expand this function to handle more diverse event types and metadata.
        """
        event_type = event.get("event_type")
        player = event.get("player")
        team = event.get("team")
        outcome = event.get("outcome")
        fouled_player = event.get("fouled_player")
        metadata = event.get("metadata", {})
        score = event.get("score", "0-0") # Provide score for context

        description = ""
        if event_type == "kick_off":
            description = f"The game kicks off! The score is {score}."
        elif event_type == "shot_on_goal":
            if outcome == "scored":
                description = f"{player} of {team} scores a magnificent goal! The score is now {score}."
                if metadata.get("shot_type"):
                    description += f" It was a brilliant {metadata['shot_type']} shot."
            else:
                description = f"{player} of {team} takes a shot, but it's missed or saved! The score remains {score}."
        elif event_type == "foul":
            description = f"A foul committed by {player} of {team} on {fouled_player}."
            if outcome:
                description += f" The referee issues a {outcome.replace('_', ' ')}."
        elif event_type == "possession_change":
            description = f"Possession changes hands, now with {team}."
        elif event_type == "halftime":
            description = f"It's halftime! The score is {score}."
        elif event_type == "end_game":
            description = f"The game has ended! The final score is {score}."
            # You might add logic here to determine winner/loser for commentary
        elif event_type == "save":
            description = f"Incredible save by the {team} goalkeeper against a shot from {player}! The score remains {score}."
        elif event_type == "penalty":
            description = f"Penalty awarded to {team}! {player} steps up to take it."
        elif event_type == "corner":
            description = f"Corner kick for {team}."
        elif event_type == "substitution":
            description = f"Substitution for {team}: {metadata.get('player_out')} off, {metadata.get('player_in')} on."
        else:
            description = f"A key moment in the game: {event_type}."

        return description

    def get_commentary(self, event: dict, user_taste_profile: dict) -> str:
        """
        Generates commentary text by first creating a prompt and then calling the LLM.
        """
        prompt = self.generate_prompt(event, user_taste_profile)
        commentary_text = self.openai_client.generate_commentary(prompt)
        return commentary_text