"""AiBot class definition."""

from openai import AsyncOpenAI, OpenAI


class AiBot:
    """Class for AI interactions."""

    api_key = None
    mood = None
    tone = None
    description = None
    textPrompt = None
    imagePrompt = (None,)

    def __init__(self, api_key, mood, tone, description):
        self.api_key = api_key
        self.mood = mood
        self.tone = tone
        self.description = description
        self.textPrompt = f"""Create an Instagram post given the following information.
    Use the description as a general guideline about the topic.
    The post should have the goal of becoming as viral as possible.
    Aim to avoid extreme views and or activism.
    Mood: {mood} Tone: {tone} Description: {description}"""
        self.imagePrompt = f"""Create an image for an Instagram post given the following information.
        Use the description as a general guideline about the topic.
        The post should have the goal of becoming as viral as possible.
        Aim to avoid extreme views and or activism.
    Mood: {mood} Tone: {tone} Description: {description}"""

    async def generate_post_content(self):
        """Generate post content."""
        client = self.get_connected_client()
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": self.textPrompt}]
        )
        return result.choices[0].message.content

    async def generate_post_image(self):
        """Generate post image."""
        client = self.get_connected_client()
        response = await client.images.generate(
            model="dall-e-2",
            prompt="a white siamese cat",
            size="256x256",
            quality="standard",
            n=1,
        )
        return response.data[0].url

    def get_connected_client(self):
        return AsyncOpenAI(api_key=self.api_key)
