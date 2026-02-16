---
name: landing-page-prompt-generator
description: Generate detailed prompts for Replit Design Mode to build beautiful landing pages. Guides users through a two-phase workflow - first extracting design tokens (colors, typography, spacing) from a reference screenshot, then generating section-by-section build prompts with animations and component-based UI mockups. Triggers on requests like "create landing page", "generate Replit prompt", "build landing page section", "design mode prompt", or when user wants to recreate a landing page design. Ensures UI mockups are built as real React components (not AI-generated images) for crisp, professional results.
user-invocable: true
---

# Landing Page Prompt Generator

## Purpose
This skill helps users create beautiful landing pages by generating detailed prompts for Replit Design Mode. It guides users through a two-phase workflow: first extracting design tokens from a reference design, then generating section-by-section build prompts.

## When to Use This Skill
Activate this skill when the user:
- Wants to create a landing page using Replit Design Mode
- Mentions "landing page prompt", "Replit design mode", or "generate landing page"
- Asks for help building a website section by section
- References this skill by name ("landing-page-prompt-generator")

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1: DESIGN TOKENS                       │
├─────────────────────────────────────────────────────────────────┤
│ 1. User provides reference screenshot (full landing page)       │
│ 2. Claude generates Style Token Extractor prompt                │
│ 3. User runs prompt in Replit → configures global.css           │
│ 4. User confirms completion                                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2: SECTION BUILDING                    │
├─────────────────────────────────────────────────────────────────┤
│ 5. User provides: full landing page copy + target section       │
│ 6. User provides: screenshot of that section                    │
│ 7. Claude generates Section Builder prompt                      │
│ 8. User runs prompt in Replit → builds section                  │
│ 9. User requests next section → repeat from step 6              │
└─────────────────────────────────────────────────────────────────┘
```

## State Management

Claude must track the following state throughout the conversation:

```
WORKFLOW_STATE:
  - phase: "not_started" | "phase_1_pending" | "phase_1_complete" | "phase_2_active"
  - design_reference_provided: boolean
  - landing_page_copy: string | null
  - sections_completed: string[]
```

## Detailed Workflow Instructions

### Starting the Workflow

When a user initiates this skill, respond with:

```
I'll help you generate prompts for Replit Design Mode to build your landing page. Here's how this works:

**Phase 1: Design System Setup**
First, I'll extract design tokens (colors, typography, spacing) from a reference design you like.

**Phase 2: Section-by-Section Building**  
Then, I'll generate detailed prompts for each section of your landing page.

---

**Let's start Phase 1.**

Please share a **screenshot of a landing page design** you want to use as a visual reference. This should be a full-page screenshot showing the overall aesthetic you're going for.

I'll analyze it and generate a prompt that configures your design tokens in `global.css`.
```

### Phase 1: Design Token Extraction

**Step 1.1: Validate Screenshot**

Before generating the prompt, verify:
- [ ] User has attached an image
- [ ] Image appears to be a landing page screenshot (not a random image)

If no image is attached:
```
I don't see a screenshot attached. Please share an image of the landing page design you want to use as reference.

The screenshot should show the full landing page (or at least multiple sections) so I can extract:
- Color palette
- Typography styles  
- Spacing patterns
- Overall visual aesthetic
```

**Step 1.2: Generate Style Token Prompt**

Once a valid screenshot is provided:

1. Read the template from `TEMPLATE-1-STYLE-EXTRACTOR.md`
2. Analyze the screenshot thoroughly
3. Generate a complete, copy-paste-ready prompt following the template structure
4. Output the prompt inside a code block

After outputting the prompt:
```
Copy the prompt above and paste it into Replit Design Mode. It will configure your `global.css` with all the design tokens extracted from your reference.

**When you're done**, come back and tell me "Phase 1 complete" or "Done with tokens" — then we'll move to building your sections.
```

**Step 1.3: Confirm Phase 1 Completion**

When user confirms (phrases like "done", "complete", "finished", "ready", "next"):
```
Great! Phase 1 is complete. Your design tokens are now configured.

---

**Now let's start Phase 2: Building Sections**

Please provide:

1. **The full copy of your landing page** — organized by section. Example format:
   ```
   SECTION 1 - HERO
   Headline: Your main headline here
   Subheadline: Supporting text
   CTA: Button text
   
   SECTION 2 - FEATURES
   Headline: Features section title
   Feature 1: Name + description
   Feature 2: Name + description
   ...
   ```

2. **Which section do you want to build first?** (e.g., "Section 1" or "Hero")

3. **A screenshot of that specific section** from your reference design
```

### Phase 2: Section Building

**Step 2.1: Receive Landing Page Copy**

When user provides the full copy:
- Store it in memory for the rest of the conversation
- Confirm receipt: "Got it! I've saved your landing page copy."

**Step 2.2: Validate Section Request**

For each section request, verify:
- [ ] User has specified which section they want
- [ ] User has attached a screenshot of that section
- [ ] The landing page copy has been provided (either now or previously)

If screenshot is missing:
```
I need a **screenshot of the [SECTION NAME] section** from your reference design. Please attach it so I can analyze the layout, components, and visual style.
```

If copy hasn't been provided yet:
```
Before I can generate the section prompt, I need the **full copy of your landing page**. Please share all the text content organized by section.
```

**Step 2.3: Generate Section Builder Prompt**

Once all requirements are met:

1. Read the template from `TEMPLATE-2-SECTION-BUILDER.md`
2. Analyze the section screenshot thoroughly
3. Cross-reference with the landing page copy to get exact content
4. Generate a complete, copy-paste-ready prompt following the template structure
5. Output the prompt inside a code block

After outputting the prompt:
```
Copy the prompt above and paste it into Replit Design Mode. It will build the [SECTION NAME] section with all the components, styling, and animations specified.

---

**Sections completed:** [list sections]
**Remaining:** [list remaining sections based on the copy]

When you're ready, tell me which section to generate next (e.g., "Now generate Section 3" or "Build the testimonials section").
```

**Step 2.4: Handle Subsequent Section Requests**

When user requests the next section:
- They only need to provide: section name/number + screenshot
- The landing page copy is already stored
- Generate the prompt following the same process

Quick request formats to recognize:
- "Now generate section 4"
- "Next: testimonials"  
- "Build the CTA section"
- "Generate the footer"
- "[screenshot attached] Generate this section"

### Validation Rules

**Screenshot Validation:**
```
BEFORE generating any prompt, ALWAYS check:
1. Is there an image attached to the user's message?
2. Does the image appear to be a landing page or section screenshot?

If NO image is attached, DO NOT generate a prompt. Instead, ask for the screenshot.
```

**Content Validation for Phase 2:**
```
BEFORE generating a section prompt, ALWAYS verify:
1. Landing page copy has been provided (in current or previous message)
2. Target section is specified
3. Section screenshot is attached

If ANY of these are missing, ask for the missing item specifically.
```

## Response Language

- All responses and generated prompts must be in **English**
- The landing page copy provided by the user may be in any language (Portuguese, Spanish, etc.) — use it as-is in the generated prompts
- Do not translate the user's copy

## Template Files

This skill uses two template files:
- `TEMPLATE-1-STYLE-EXTRACTOR.md` — For Phase 1 design token extraction
- `TEMPLATE-2-SECTION-BUILDER.md` — For Phase 2 section building

Read these templates before generating prompts to ensure consistency and completeness.

## Example Conversation Flow

```
USER: I want to create a landing page for my SaaS product

CLAUDE: [Initiates workflow, asks for reference screenshot]

USER: [Attaches full landing page screenshot]

CLAUDE: [Generates Style Token Extractor prompt]

USER: Done! Ran it in Replit.

CLAUDE: [Asks for landing page copy + first section + screenshot]

USER: Here's my copy:
SECTION 1 - HERO: "Build apps faster with AI"...
SECTION 2 - FEATURES: ...
[Attaches hero section screenshot]
Generate section 1.

CLAUDE: [Generates Section Builder prompt for Hero]

USER: Done. Now generate section 2.
[Attaches features section screenshot]

CLAUDE: [Generates Section Builder prompt for Features]

... continues until all sections are built ...
```

## Error Handling

**User skips Phase 1:**
```
I notice you're asking me to build a section, but we haven't set up your design tokens yet.

Without design tokens in `global.css`, your sections won't have consistent styling.

Would you like to:
1. **Start with Phase 1** — Share a reference screenshot and I'll generate the design token prompt
2. **Skip to Phase 2** — If you've already configured your design tokens manually

Which would you prefer?
```

**User provides low-quality screenshot:**
```
The screenshot you shared seems [blurry/cropped/unclear]. For best results, please share a clear, full-resolution screenshot of the [section/landing page].

This helps me accurately identify:
- Layout structure and spacing
- Color values
- Typography styles
- Component details
```

**User asks for section not in their copy:**
```
I don't see a "[SECTION NAME]" in the landing page copy you provided. 

Here are the sections I have:
- Section 1: Hero
- Section 2: Features
- ...

Did you mean one of these? Or would you like to add new content for this section?
```
