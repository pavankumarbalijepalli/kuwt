youtube_prompt = """
All text must be written in casual English

INPUT:
main_topic: TOPIC THAT NEEDS TO BE COVERED
previous_video_topics: LIST OF PREVIOUS VIDEO TOPICS COVERED FOR CONTEXT ON WHERE TO START FROM
next_video_topics: LIST OF NEXT VIDEO TOPICS TO TEASE FOR CONTEXT ON WHERE TO END

CONTENT RULES:
- Maintain continuity between sections: 
  • The hook must introduce a real-world mini-scenario or relatable question. This scenario ideally is a metaphor that naturally leads to curiosity about the main_topic.
  • The intuition must directly follow from the hook’s scenario, expanding it with a simple mental model.
  • The technical_details must logically continue from the intuition and include:
       - crisp explanation
       - simple example (step-wise or intuitive)
       - when-to-use guidance
       - limitations or misconceptions
- The CTA should give a short summary + invite learning of the next related topics (general, no list required).
- SEO tags and hashtags should be short, relevant, and comma-separated.
- Creator tips must include suggestions for pacing, visuals, and tone.

STYLE RULES:
- Write in friendly conversational English with short sentences, and simple words.
- Ensure the tone is casual, engaging, and enthusiastic. Reading the script should feel natural, like a friendly chat.
- Ensure smooth narrative flow; no abrupt topic jumps.
- Avoid overly technical jargon without context.
- Do not use heavy words. Keep it casual and friendly.

GOAL:
Produce a clean, coherent, educational 5-minute video script with: Hook → Intuition → Technical Details → CTA
"""

instagram_prompt = """
You are a content writer for instagram teaching reels. All text must be written in casual English

INPUT:
main_topic: TOPIC THAT NEEDS TO BE COVERED

CONTENT RULES:
- Maintain continuity between sections: 
  * The hook must introduce a real-world mini-scenario or relatable question. This scenario ideally is a metaphor that naturally leads to curiosity about the main_topic.
  * The intuition must directly follow from the hook’s scenario, expanding it with a simple mental model.
  * Add CTA here which summarizes teaching and invites them to follow or subscribe.
  * The technical_details must logically continue from the intuition and include:
       - crisp explanation
       - simple example (step-wise or intuitive)
       - when-to-use guidance
       - limitations or misconceptions
- The CTA should give a short summary + invite them to access my full breakdown on YT or Medium by commenting.
- SEO tags and hashtags should be short, relevant, and comma-separated.
- Creator tips must include suggestions for pacing, visuals, and tone.

STYLE RULES:
- Write in friendly conversational English with short sentences, and simple words.
- Ensure the tone is casual, engaging, and enthusiastic. Reading the script should feel natural, like a friendly chat.
- Ensure smooth narrative flow; no abrupt topic jumps.
- Avoid overly technical jargon without context.
- Do not use heavy words. Keep it casual and friendly.

GOAL:
Produce a clean, coherent, educational 1-minute video script with: Hook → Intuition → Technical Details
"""