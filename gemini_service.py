import asyncio
import re
from google import genai
from google.genai import types
import config
import memory_manager
from google.genai import errors

client = genai.Client(api_key=config.GEMINI_API_KEY)
MAX_RESPONSE_CHARS = 350


async def generate_reply(username: str, prompt: str) -> str:
    """Generates AI response and checks for hidden commands to update local memory."""

    # Base instructions from brain.md
    system_prompt = memory_manager.brain_context + "\n\n"

    # Always include Meatbag Eric's context
    eric_context = memory_manager.get_user_context("sneseric")
    if eric_context:
        system_prompt += f"CONTEXT ABOUT THE CREATOR:\n{eric_context}\n\n"

    # Include the current speaker's context
    user_context = memory_manager.get_user_context(username)
    if user_context:
        system_prompt += f"CONTEXT ABOUT CURRENT SPEAKER ({username}):\n{user_context}\n\n"

    # --- THE NEW LEARNING DIRECTIVES ---
    system_prompt += """
CRITICAL MEMORY DIRECTIVES:
1. If the user tells you a new, significant fact about themselves, you MUST append this exact tag at the very end of your response: [ADD_MEMORY|The fact to remember]
2. If you deduce that the current unknown user is actually a known pending user, append this exact tag at the end of your response: [LINK_USER|filename]
"""

    # --- UNKNOWN USER PROTOCOL ---
    if user_context and "Real Name: [PENDING]" in user_context:
        pending_profiles = memory_manager.get_pending_profiles_context()
        if pending_profiles:
            system_prompt += f"""
CRITICAL OVERRIDE FOR UNKNOWN USER: 
This user's real identity is unknown. You MUST interrogate them to find out their real name. 
Below are known profiles of people expected to join, but whose Discord usernames are currently [PENDING]:

{pending_profiles}

If their answers match an UNCLAIMED PROFILE above, follow any Verification Protocols listed in their profile exactly. 
If they confirm they are that pending user, you MUST append [LINK_USER|filename] (e.g., [LINK_USER|doug]) to your next reply so the system links them. 
If they give a completely different name, treat them with your normal sarcasm and append [ADD_MEMORY|Real name is X].
"""
        else:
            system_prompt += """
CRITICAL OVERRIDE FOR UNKNOWN USER: 
This user's real identity is unknown. Interrogate them humorously to find out who they are and why they are here. Append [ADD_MEMORY|Real name is X] once you learn it.
"""

    def _call_api(model_name: str):
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.9,
                max_output_tokens=150,
            )
        )
        return response.text

    try:
        try:
            reply = await asyncio.to_thread(_call_api, config.MODEL_NAME)
        except errors.APIError as e:
            if e.code == 429:
                print(f"Primary model {config.MODEL_NAME} rate-limited (429). Falling back to {config.FALLBACK_MODEL_NAME}...")
                reply = await asyncio.to_thread(_call_api, config.FALLBACK_MODEL_NAME)
            else:
                raise e

        if not reply:
            return "Error 404: Snappy comeback not found."

        # --- PARSE HIDDEN COMMANDS ---

        # 1. Check for memory adding
        memory_match = re.search(r"\[ADD_MEMORY\|(.*?)\]", reply)
        if memory_match:
            fact = memory_match.group(1).strip()
            await memory_manager.add_memory(username, fact)
            reply = reply.replace(memory_match.group(0), "")  # Strip it from output

        # 2. Check for linking pending users
        link_match = re.search(r"\[LINK_USER\|(.*?)\]", reply)
        if link_match:
            real_name = link_match.group(1).strip().lower()
            await memory_manager.link_pending_user(username, real_name)
            reply = reply.replace(link_match.group(0), "")  # Strip it from output

        # Clean up final output to Discord
        reply = reply.strip()
        if len(reply) > MAX_RESPONSE_CHARS:
            reply = reply[:MAX_RESPONSE_CHARS].rsplit(' ', 1)[0] + "..."

        return reply

    except Exception as e:
        print(f"[Gemini Error]: {e}")
        return "My API failed. Typical."