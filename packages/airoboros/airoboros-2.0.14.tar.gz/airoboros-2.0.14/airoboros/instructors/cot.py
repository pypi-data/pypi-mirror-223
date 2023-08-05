from airoboros.instructors.simple_task import generate as generate_simple


async def generate(instructor):
    """Generator for chain-of-thought training data."""
    async for item in generate_simple(instructor, "cot", filter_response=False):
        yield item
