import os
import aiofiles
import re

MEMORIES_DIR = "local_data/memories"
BRAIN_FILE = "local_data/brain.md"

memory_cache = {}
discord_to_file = {}
brain_context = ""

def load_all_memories():
    global brain_context
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "r", encoding="utf-8") as f:
            brain_context = f.read()

    if not os.path.exists(MEMORIES_DIR):
        os.makedirs(MEMORIES_DIR, exist_ok=True)

    memory_cache.clear()
    discord_to_file.clear()

    for filename in os.listdir(MEMORIES_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(MEMORIES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                file_key = filename.replace(".md", "").lower()
                memory_cache[file_key] = content

                match = re.search(r"Discord Username:\s*(.+)", content)
                if match:
                    username = match.group(1).strip()
                    if username and username != "[PENDING]":
                        discord_to_file[username] = file_key

def get_user_context(discord_username: str) -> str:
    file_key = discord_to_file.get(discord_username)
    if file_key:
        return memory_cache.get(file_key)
    return None

def get_pending_profiles_context() -> str:
    pending_contexts = []
    for file_key, content in memory_cache.items():
        if "Discord Username: [PENDING]" in content:
            pending_contexts.append(f"--- UNCLAIMED PROFILE ({file_key}.md) ---\n{content}\n")
    return "\n".join(pending_contexts)

async def create_new_user_memory(discord_username: str):
    os.makedirs(MEMORIES_DIR, exist_ok=True)
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
    file_key = target_filename.lower()
    if file_key in memory_cache:
        filepath = os.path.join(MEMORIES_DIR, f"{file_key}.md")
        content = memory_cache[file_key]
        new_content = re.sub(
            r"Discord Username:\s*\[PENDING\]",
            f"Discord Username: {discord_username}",
            content,
            count=1,
            flags=re.IGNORECASE
        )
        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            await f.write(new_content)

        old_temp_file = os.path.join(MEMORIES_DIR, f"{discord_username.lower()}.md")
        if os.path.exists(old_temp_file) and file_key != discord_username.lower():
            os.remove(old_temp_file)

        load_all_memories()

async def add_memory(discord_username: str, fact: str):
    file_key = discord_to_file.get(discord_username)
    if not file_key:
        return
    filepath = os.path.join(MEMORIES_DIR, f"{file_key}.md")
    async with aiofiles.open(filepath, "a", encoding="utf-8") as f:
        await f.write(f"\n- {fact}")
    load_all_memories()