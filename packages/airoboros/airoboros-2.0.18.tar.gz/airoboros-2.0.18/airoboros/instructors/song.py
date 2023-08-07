from airoboros.instructors.simple_task import generate as generate_simple_task


async def generate(instructor):
    """Generator for song training data."""
    async for item in generate_simple_task(instructor, "song"):
        yield item
