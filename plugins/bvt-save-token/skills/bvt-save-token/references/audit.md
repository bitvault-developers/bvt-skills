# Setup audit

Reply with a numbered action list, biggest saving first, in plain words:

1. Connectors: set Tool access to "On demand" (Anthropic recommends this with 10 or more connectors). Turn off connectors not used this week, and switch them on per chat when needed.
2. Plugins and skills: every enabled skill adds its name and description (about 100 tokens) to every message, and a plugin switches on all of its skills at once. Look at the skills available in this session, group them by plugin, and name the plugin groups that look unrelated to the user's work as candidates to turn off. Estimate the saving as number of skills x about 100 tokens, on every message. Also point out any duplicate copies of the same skill (for example a standalone skill and a plugin skill with the same rules).
3. Projects: put documents that get reused (specs, brand docs, code notes) into a Project instead of uploading them again in each chat. The cache expires after a break, so the first message after a pause costs more.
4. Saved preferences and memory: keep them short, because they load in every chat.
5. Model and effort: use a smaller model or lower effort for simple edits, and turn off extended thinking and Research when they aren't needed.
6. Check the Usage page in Settings weekly to see whether the changes worked.

Don't guess exact menu paths. Name the setting and let the user find it. Mark every token figure as an estimate.
