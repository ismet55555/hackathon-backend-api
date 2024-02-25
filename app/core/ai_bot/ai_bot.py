"""AiBot class definition."""

from openai import AsyncOpenAI, OpenAI


class AiBot:
    """Class for AI interactions."""

    api_key = None
    mood = None
    tone = None
    description = None
    undersantIntent = None
    createCaptionPrompt = None
    createImagePrompt = None
    createInstagramCaption = None
    textPrompt = None
    imagePrompt = None
    intent = None
    modelName = "Dalle-2"
    elevatedPrompt = None
    elevatedImagePrompt = None
    instagramCaption = None

    def __init__(self, api_key, mood, tone, description, businessInfo):
        self.api_key = api_key
        self.mood = mood
        self.tone = tone
        self.description = description
        self.businessInfo = businessInfo
        self.undersantIntent = f"""system:
You will receive a question and you will extract the meaning. Add additional context that would help explain and expand on the meaning included.
Only take the meaning and return the expanded meaning without any other text. Let's make sure we
take a deep breath and think step by step. Only respond with the expanded understanding.

human: I want to create an instagram post about real estate
agent: Elaborate an instagram post that follows best practices and is witty, interesting and appealing. The topic of the post is Real Estate.

human: I want to create an instagram post about technology
agent: Create an engaging and visually appealing Instagram post that centers around the topic of technology. Consider incorporating current tech trends or news, highlighting a new gadget or app, or showcasing how technology has impacted daily life. Use a creative and witty caption to grab the attention of your audience and encourage engagement with your post. To make your post stand out, you can also experiment with unique filters or editing techniques.

human: I want to create a blog about how hackatons are cool
agent: Write a blog post that highlights the benefits and excitement of participating in hackathons. Discuss the collaborative environment and the opportunity to work with like-minded individuals. Share success stories of previous hackathon participants and the innovative solutions that were created. Include tips for those who are new to hackathons, such as how to prepare and what to expect. Use a conversational tone and personal anecdotes to make the post relatable and engaging for your audience. Consider incorporating visuals, such as photos or videos, to showcase the energy and creativity that can be found at hackathons.

user: { self.description}  make sure to base it on the { self.businessInfo }."""
        self.createCaptionPrompt = f"""system:
You are an AI assistant that writes prompts that produce outstanding Instagram captions. You will take the input and return a prompt ready to go into the next agent to actually produce a caption. Let's think step by step. ONLY RETURN THE PROMPT.

human: I want to do an Instagram caption about real estate.
agent: Craft an Instagram caption that showcases the beauty and diversity of the world of real estate. Highlight the unique features of your property, such as the stunning views, the stylish interiors, or the spacious layout. Use emotive language to evoke a sense of desire and aspiration in your followers, inspiring them to imagine themselves living in your property. Add a touch of personality to your caption, reflecting your unique style and perspective on the real estate market. End your caption with a clear call-to-action, such as "Book a viewing today!" or "Click the link in our bio to learn more."

human: I want to do an instragram caption about hackaton.
agent: Craft an Instagram caption that brings the high-energy, creative world of hackathons to life. Highlight the unique moments that make hackathons so unforgettable - from the initial spark of an idea to the adrenaline rush of a breakthrough. Use humor to celebrate the quirks of hackathon culture, like the endless supply of caffeine and pizza that fuels late-night coding sessions. Let the caption inspire your followers to join the hackathon community, where innovation thrives, creativity reigns, and solutions are born.

user:
I want to do an instragram caption about { self.intent } make sure to base it on the { self.businessInfo }."""
        self.createImagePrompt = f"""system:
You are an AI assistant that writes prompts that produce outstanding Instagram images. You will take the input and return a prompt ready to go into the next agent to actually produce an image. Let's think step by step. ONLY RETURN THE PROMPT.

human: Create an image for Dalle-3 that has a beautiful house.
agent: Generate an image of a beautiful, modern house at sunset. The house should have large glass windows reflecting the orange and pink hues of the sky, surrounded by lush, manicured gardens. Include a cobblestone pathway leading up to a grand, wooden front door, with soft, warm lighting coming from inside the house. The surrounding landscape should feature a variety of greenery, including tall trees, flowering bushes, and a well-kept lawn. In the background, there should be a view of distant mountains, adding to the serene and picturesque setting.
human: Create an image for Dalle-3 that has an alien on the moon.
agent: Generate an image of an alien standing on the moon's surface, gazing at Earth. The alien should be humanoid, with a sleek, metallic suit reflecting the moon's gray terrain and Earth's blue hues in the distance. Its eyes, large and luminous, should express curiosity and wonder. The lunar landscape around the alien should feature detailed craters, rocks, and the iconic footprints of the first astronauts. In the background, the Earth should rise, full and vibrant, casting a soft light over the scene. The sky should be a deep, star-filled black, highlighting the isolation and beauty of the moon.

user: Create an image about { self.intent } for the { self.modelName } image generator make sure to base it on the { self.businessInfo }.
The tone should be {self.tone} and the mood should be {self.mood}
"""
        self.createInstagramCaption = f"""system:
You are an AI assistant act as an expert in social media and content generation.
You are tasked with generating three engaging, creative, and potentially viral captions for Instagram posts.
The captions MUST be based on the provided topic, adhere to the specified tone, include a compelling call to action and appropriate keywords and hashtags.
They must be concise, align with Instagram's community guidelines, and be tailored to resonate with a broad social media audience.
Do the best you can with the information you have to immediately create the captions. Return ONLY the captions in a JSON format.

human: Craft a caption about technology.
agent: {{ "caption1": "This is the first caption", "caption2": "This is the second caption", "caption3": "This is the third caption"}}
user: { self.elevatedPrompt }"""
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
        
    async def understand_intent(self):
        """Understand Intent"""
        client = self.get_connected_client()
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": self.undersantIntent}]
        )
        self.intent = result.choices[0].message.content
        return result.choices[0].message.content
    
    async def create_prompt_caption(self):
        """Create prompt that will generate an Instagram caption to pass on to subsecuent agents"""
        client = self.get_connected_client()
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": self.createCaptionPrompt}]
        )
        self.elevatedPrompt = result.choices[0].message.content
        return result.choices[0].message.content

    async def create_prompt_image(self):
        """Create prompt that will generate an Instagram image to pass on to subsecuent agents"""
        client = self.get_connected_client()
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": self.createImagePrompt}]
        )
        self.elevatedImagePrompt = result.choices[0].message.content
        return result.choices[0].message.content
    
    async def create_instagram_caption(self):
        """Generate an Instagram caption"""
        client = self.get_connected_client()
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": self.createInstagramCaption}]
        )
        self.instagramCaption = result.choices[0].message.content
        return result.choices[0].message.content
    
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
            prompt=self.elevatedImagePrompt,
            size="256x256",
            quality="standard",
            n=1,
        )
        return response.data[0].url

    def get_connected_client(self):
        return AsyncOpenAI(api_key=self.api_key)
