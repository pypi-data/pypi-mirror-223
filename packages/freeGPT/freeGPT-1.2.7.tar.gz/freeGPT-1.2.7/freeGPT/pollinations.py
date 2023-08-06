from random import randint
from aiohttp import ClientSession, ClientError


class Generation:
    async def create(self, prompt):
        """
        Create a new image generation based on the given prompt.

        Args:
            prompt (str): The prompt for generating the image.

        Returns:
            resp: The generated image content
        """
        try:
            async with ClientSession() as session:
                async with session.get(
                    url=f"https://image.pollinations.ai/prompt/{prompt}{randint(1, 10000)}",
                    timeout=30,
                ) as resp:
                    return await resp.content.read()
        except ClientError:
            raise Exception("Unable to fetch the response.")
