import os
import aiofiles
import re

MEMORIES_DIR = "local-data/memories"
BRAIN_FILE = "local-data/brain.md"

# Cache dictionaries
memory_cache = {}  # Maps filename (e.g., 'user_file') -> File Content
discord_to_file = {}  # Maps Discord Username -> filename
brain_context = ""


def load_all_memories():
    """Loads brain.md and all user profiles into memory dictionaries on startup."""
    global brain_context
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "r", encoding="utf-8") as f:
            brain_context = f.read()

    if not os.path.exists(MEMORIES_DIR):
        os.makedirs(MEMORIES_DIR)

    memory_cache.clear()
    discord_to_file.clear()

    for filename in os.listdir(MEMORIES_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(MEMORIES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                file_key = filename.replace(".md", "").lower()

                # Store the file content by its filename
                memory_cache[file_key] = content

                # Link the Discord username to the file
                match = re.search(r"Discord Username:\s*(.+)", content)
                if match:
                    username = match.group(1).strip()
                    if username and username != "[PENDING]":
                        discord_to_file[username] = file_key


def get_user_context(discord_username: str) -> str:
    """Retrieves user info from the dictionary cache using their Discord name."""
    file_key = discord_to_file.get(discord_username)
    if file_key:
        return memory_cache.get(file_key)
    return None


def get_pending_profiles_context() -> str:
    """Retrieves the contents of all manually created profiles waiting for a Discord user."""
    pending_contexts = []
    for file_key, content in memory_cache.items():
        # Only grab files explicitly waiting for a username link
        if "Discord Username: [PENDING]" in content:
            pending_contexts.append(f"--- UNCLAIMED PROFILE ({file_key}.md) ---\n{content}\n")
    return "\n".join(pending_contexts)


async def create_new_user_memory(discord_username: str):
    """Creates a template memory file for unknown users formatted as [username].md."""
    file_key = discord_username.lower()
    template = f"""Discord Username: {discord_username}
Real Name: [PENDING]

Personality & Traits:
- Needs data.

Past Interactions with Eric:
- Needs data.

Inside Jokes:
- Needs data.

Learned Context:
"""
    filepath = os.path.join(MEMORIES_DIR, f"{file_key}.md")
    async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
        await f.write(template)

    memory_cache[file_key] = template
    discord_to_file[discord_username] = file_key


async def link_pending_user(discord_username: str, target_filename: str):
    """Replaces [PENDING] in a file with the confirmed Discord username."""
    file_key = target_filename.lower()
    if file_key in memory_cache:
        filepath = os.path.join(MEMORIES_DIR, f"{file_key}.md")
        content = memory_cache[file_key]

        # Replace the pending tag with the actual username
        new_content = re.sub(
            r"Discord Username:\s*\[PENDING\]",
            f"Discord Username: {discord_username}",
            content,
            count=1,
            flags=re.IGNORECASE
        )

        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            await f.write(new_content)

        # If this user had a temporary generic file created, delete it
        old_temp_file = os.path.join(MEMORIES_DIR, f"{discord_username.lower()}.md")
        if os.path.exists(old_temp_file) and file_key != discord_username.lower():
            os.remove(old_temp_file)

        # Reload cache so the system immediately recognizes them properly
        load_all_memories()


async def add_memory(discord_username: str, fact: str):
    """Appends newly learned information directly to the bottom of the user's md file."""
    file_key = discord_to_file.get(discord_username)
    if not file_key:
        return

    filepath = os.path.join(MEMORIES_DIR, f"{file_key}.md")
    async with aiofiles.open(filepath, "a", encoding="utf-8") as f:
        await f.write(f"\n- {fact}")

    # Reload cache to update active memory
    load_all_memories()