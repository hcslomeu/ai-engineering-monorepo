---
name: landing-page-copy-optimizer
description: Analyze and optimize landing page copy using April Dunford's positioning methodology. Use when user wants to evaluate SaaS landing page copy, improve conversion-focused messaging, apply positioning framework (competitive alternatives, unique features, value themes, target customers, market category), or generate prompts for vibe coding tools (Replit, Lovable). Triggers on requests like "analyze my landing page", "improve my website copy", "help with positioning", "optimize my SaaS page", or when user shares a landing page URL for review.
user-invocable: true
---

# Landing Page Copy Optimizer

Analyze and optimize SaaS landing page copy using April Dunford's positioning methodology, then generate implementation-ready prompts for vibe coding tools.

## Workflow Overview

1. **Fetch & Analyze** - Read current copy from user's URL
2. **Positioning Analysis** - Apply April Dunford methodology
3. **Validation** - Confirm features/alternatives with user
4. **Positioning Draft** - Present for approval
5. **New Copy** - Generate optimized copy for all sections → approval
6. **Asset Collection** - Request screenshots + visual reference
7. **Final Prompt** - Generate detailed vibe coding prompt with design.json

## Step 1: Fetch & Analyze

Use `web_fetch` on the user's URL. Extract:
- Current copy (headlines, descriptions, CTAs)
- Product/service being sold
- Apparent target audience
- Existing social proof
- Current page structure
- **Language and tone** (match these in output)

## Step 2: Positioning Analysis

Apply April Dunford's methodology **in this exact order**:

### 2.1 Competitive Alternatives
Infer what customers would use if this product didn't exist:
- **Direct competitors**: Similar SaaS products
- **Indirect alternatives**: Spreadsheets, manual processes, hiring someone, doing nothing

### 2.2 Unique Features/Capabilities
Identify features ONLY this product has. Look for:
- Explicit features mentioned on the page
- Implicit differentiators in the copy
- **Always ask user to confirm/add features**

### 2.3 Value Themes
For each unique feature, define the customer benefit. Then group into **maximum 3 value themes** to avoid diluted messaging.

### 2.4 Target Customer Characteristics
Define who cares most about these value themes:
- Behaviors that make them value the differentiators
- Common characteristics/pain points
- Why alternatives don't work for them

### 2.5 Market Category
Suggest a category that:
- Already exists in customer's mind (CRM, Meeting Assistant, etc.)
- Add a differentiating modifier (e.g., "AI-native CRM", "Undetectable Meeting Assistant")
- **Avoid category creation** - use existing categories with a twist

## Step 3: Validation Questions

**Always ask these questions**, even when answers seem clear:

```
Based on my analysis, here's what I found:

**Competitive Alternatives:**
[list inferred alternatives]
→ Is this correct? Any alternatives I missed?

**Unique Features:**
[list features found]
→ Are these accurate? What features do YOU have that competitors don't?

**Target Customer:**
[describe inferred target]
→ Does this match your ideal customer?
```

## Step 4: Positioning Draft

Present positioning summary for approval:

```
## Positioning Summary

**Market Category:** [category + modifier]
**Competitive Alternatives:** [list]
**Unique Features:** [list with brief descriptions]
**Value Themes:** [max 3 themes, each with supporting features]
**Target Customer:** [characteristics and behaviors]

---
Does this positioning feel right? Any adjustments before I create the copy?
```

**Wait for explicit approval before proceeding.**

## Step 5: New Copy Generation

Generate copy for all sections. See [references/copy-structure.md](references/copy-structure.md) for detailed requirements.

### Section Structure (SaaS Landing Page)

1. **Hero** - Title (≤70 chars), Subtitle (≤150 chars), CTA (≤20 chars), Image spec
2. **Social Proof** - User count or company logos
3. **Product vs. Alternatives** - Comparison highlighting differentiators
4. **Features & Value** - Unique features with screenshots, titles, descriptions
5. **How It Works** - Step-by-step process
6. **Testimonials** - Quotes reinforcing competitive claims (can be invented)
7. **Target Customers** - Cards showing ideal user profiles
8. **CTA** - Final call to action
9. **FAQ** - Address common objections
10. **Footer** - Standard links

### Copy Guidelines

- Match original site's **language** (PT-BR, EN, etc.)
- Match original site's **tone** (formal, casual, technical, etc.)
- Hero must answer: "What is this?" and "Why is it different?"
- Features section: ONLY unique features (table stakes are implied by category)
- Testimonials format: Name + Inferred Role (based on ICP) + Quote reinforcing differentiators
- FAQ: Address objections that prevent conversion

**Present copy for approval before proceeding.**

## Step 6: Asset Collection

### Product Screenshots
Ask user for screenshots of key product screens:
```
To create the final prompt, I need some product visuals:

1. Do you have screenshots of these key screens?
   - Main dashboard/interface
   - Key unique features in action
   - Any screens that showcase your differentiators

2. Do you have a visual reference (screenshot) of a landing page style you like?

If you don't have screenshots yet, I'll create image generation prompts for each needed visual.
```

### Visual Reference
If user provides a reference screenshot:
- Analyze design patterns (colors, typography, spacing, components)
- Extract into design.json format

If no reference provided:
- Suggest a style based on product category and target audience
- Create a default design.json appropriate for the product

## Step 7: Final Prompt Generation

Generate a comprehensive prompt for Replit/Lovable. See [references/prompt-template.md](references/prompt-template.md) for full structure.

### Prompt Components

1. **design.json** - Complete design system extracted from reference or generated
2. **Section-by-section specs** - Layout, columns, copy, components, animations
3. **Image prompts** - For each visual, include Midjourney/Nanobanana prompt
4. **Video/animation suggestions** - Where motion would enhance the page

### Image Prompt Format
For each image needed:
```
[Generate] Description for image generation tool
- Style: [realistic/3D/illustration/flat]
- Content: [what should be shown]
- Mood: [professional/friendly/technical/etc.]
- Colors: [reference design.json palette]
```

### Video/Animation Suggestions
Include where appropriate:
- Hero section: Subtle floating animations, parallax
- Feature demos: Short looping videos showing feature in action
- Transitions: Smooth scroll-triggered animations
- Hover states: Micro-interactions on cards and buttons

## Output Format

Final prompt should be copy-paste ready for Replit Agent or Lovable, structured as:

```
[BRIEF DESCRIPTION]
[DESIGN.JSON - complete design system]
[SECTION SPECIFICATIONS - each section with layout, copy, visuals, animations]
[ADDITIONAL NOTES - responsive behavior, interactions, etc.]
```
