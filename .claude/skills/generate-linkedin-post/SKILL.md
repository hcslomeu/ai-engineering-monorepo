---
name: generate-linkedin-post
description: Generate a LinkedIn post about a completed work package with story arc, implementation details, and engagement CTA
user-invocable: true
---

# Skill: Generate LinkedIn Post

Generate a LinkedIn post about a completed work package from the AI Engineering Monorepo project.

## When to Use

- After completing a work package (triggered by the WP Completion Checklist in CLAUDE.md)
- When the user explicitly asks for a LinkedIn post about their progress or interesting concept to be shared

## Inputs

Before generating, read:
- `PROGRESS.md` for WP objectives, dates, and notes
- `.claude/learning-progress.md` for skills learned
- `.claude/learning-context.md` for developer profile and session concepts

## Post Structure (Story Arc)

1. **Hook** (first 150 characters) - compelling opening that makes people click "see more"
2. **Setup** (1-2 sentences) - what project, what phase, what was the goal
3. **Implementation** (3-5 bullet points) - what was built, with specific technologies
4. **Lesson** (2-3 sentences) - key insight or takeaway from the process
5. **CTA** - closing question to drive engagement

## Format Rules

- **Length**: 1,200-1,600 characters (LinkedIn algorithm sweet spot)
- **Line breaks**: Single-line paragraphs with blank lines between (LinkedIn collapses long blocks)
- **Bullet points**: Use arrow symbols (->) for visual scanning
- **Emojis**: Maximum 1-2 strategic emojis, placed at section transitions
- **Hashtags**: 3-5 relevant hashtags on their own line at the end
- **No links in body**: LinkedIn suppresses posts with links; add link in comments instead (note this in the output file)
- **Language**: English

## Tone Guidelines

- First person, professional but approachable
- Frame as **upskilling and staying current**, not "learning from scratch"
- The author is an experienced Python developer expanding into new tools and patterns
- Be specific about technologies and what was built
- Mention challenges faced and how they were overcome
- Mention **Claude Code** as an agentic coding tool being used in the process and that I am better understanding advanced usage skills, like skills, mcps, prompt engineering, Programmatic Tool Calling (PTC) and Tool Search.
- Be transparent about "vibe coding" for TypeScript/UI parts (comfortable with Python, using AI to expand into TypeScript for more robust frontends than Streamlit)
- Avoid buzzwords and generic statements
- No AI-generated feel; write as if sharing with engineering peers
- NEVER use phrases like "I decided to learn X" or "I'm learning X" - instead frame as "building", "expanding into", "updating my stack with"

## Template

```
[Hook - compelling first line that creates curiosity, under 150 chars]

[1-2 sentences of context: what project, what phase, what motivated this]

Here's what I built:

-> [Specific thing 1 with technology name]
-> [Specific thing 2 with technology name]
-> [Specific thing 3 with technology name]
-> [Optional: Specific thing 4]

[Key insight or lesson learned - what surprised you, what you'd do differently, or what clicked]

[CTA question to audience - specific enough to invite real answers]

#hashtag1 #hashtag2 #hashtag3 #hashtag4
```

## Hook Examples (for this project)

- "I just built a CI pipeline that runs 4 checks in parallel. Here's what broke along the way."
- "Most people learn Python from tutorials. I'm building a production monorepo from scratch."
- "13 linting errors. 3 type failures. 1 working pipeline."
- "Building three production AI systems simultaneously. Here's what I'm learning about shared infrastructure."
- "Setting up a Python + TypeScript monorepo taught me more than any course."

## Hashtag Pool

Pick 3-5 from this baseline - identify skills/frameworks from the WP to add as well:
#AIEngineering #Python #DataEngineering #LangChain #LangGraph #MachineLearning #DevOps #CICD #GitHubActions #OpenSource #SoftwareEngineering #MonorepoArchitecture #TypeScript #MLOps #BigQuery #ClaudeCode

## Output Format

Save each post to `.claude/linkedin-posts/WP-XXX-short-title.md` with this structure:

```markdown
# LinkedIn Post: WP-XXX - Title

## Post

[The full post text, ready to copy-paste into LinkedIn]

---

## Notes

**Suggested first comment:** "Project repo: [link]. Built with [key technologies]."

**Diagram suggestion:** Generate a PROMPT to pass to Gemini Banana to generate a visual diagram of [specific topic from this WP] to accompany this post.

**Best posting time:** Tuesday-Thursday, 8-10am local time

**Character count:** [count]
```