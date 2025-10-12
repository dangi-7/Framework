# Design Guidelines: Quality Assurance for Educational App Design Platform

## Design Approach
**Selected Approach:** Hybrid - Design System (Material Design principles) + SaaS References (Linear, Notion)

**Justification:** This is a professional evaluation tool requiring clear data presentation, intuitive forms, and analytical visualizations. We'll combine Material Design's structured approach with modern SaaS aesthetics for credibility and usability.

**Key Design Principles:**
- Clarity over decoration: Information hierarchy drives all design decisions
- Data-first visualization: Charts and scores are hero elements, not afterthoughts
- Professional trust: Clean, sophisticated dark theme conveys expertise
- Guided experience: Clear progression through evaluation workflow

---

## Core Design Elements

### A. Color Palette

**Dark Mode (Primary):**
- Background Base: `220 15% 8%` (deep charcoal)
- Surface/Cards: `220 15% 12%` (elevated dark)
- Surface Elevated: `220 15% 16%` (hover states, active cards)
- Border Subtle: `220 10% 20%` (card borders, dividers)

**Brand Colors:**
- Primary (Education Blue): `215 85% 58%` (trust, professionalism)
- Primary Hover: `215 85% 65%`
- Success (High Scores): `142 70% 50%` (achievement, positive results)
- Warning (Medium Scores): `38 95% 60%` (caution, improvement needed)
- Danger (Low Scores): `0 75% 58%` (critical issues)

**Text Colors:**
- Primary Text: `220 10% 95%` (high contrast for readability)
- Secondary Text: `220 5% 65%` (labels, descriptions)
- Muted Text: `220 5% 45%` (timestamps, metadata)

### B. Typography

**Font Families:**
- Primary: 'Inter' (Google Fonts) - UI, body text, data
- Display: 'DM Sans' (Google Fonts) - headings, emphasis
- Monospace: 'JetBrains Mono' (Google Fonts) - scores, percentages

**Type Scale:**
- Hero Headline: text-6xl, font-bold (Home page title)
- Section Headers: text-4xl, font-bold
- Card Titles: text-2xl, font-semibold
- Body Text: text-base, font-normal
- Labels/Captions: text-sm, font-medium
- Micro Text: text-xs (timestamps, helper text)

**Line Height:** Generous for readability - leading-relaxed for body, leading-tight for headings

### C. Layout System

**Spacing Primitives:** Use Tailwind units of **2, 4, 6, 8, 12, 16, 20, 24** for consistency
- Micro spacing: p-2, gap-2 (tight elements)
- Standard spacing: p-4, p-6, gap-4 (cards, forms)
- Section spacing: p-8, py-12, py-16 (page sections)
- Large spacing: py-20, py-24 (page separators)

**Grid System:**
- Container: max-w-7xl mx-auto px-6
- Form layouts: max-w-4xl (optimal form width)
- Dashboard: CSS Grid with gap-6, responsive columns

**Breakpoints:**
- Mobile: Single column, full-width cards
- Tablet (md:): 2-column grids for stats/charts
- Desktop (lg:): 3-column layouts, sidebar + main content

### D. Component Library

**Navigation:**
- Top navbar: Sticky, backdrop-blur-lg, shadow-lg on scroll
- Logo + site title left, navigation links center, CTA button right
- Mobile: Hamburger menu with slide-in drawer

**Cards (Primary UI Pattern):**
- Background: Surface color with border-subtle
- Border radius: rounded-xl
- Padding: p-6 to p-8
- Shadow: shadow-lg on hover with smooth transition
- Each evaluation category gets its own card on form page

**Form Elements:**
- Rating Sliders: Full-width range inputs with custom styling
- Visual feedback: Live value display (1-5) with color coding
- Labels: text-sm font-medium mb-2
- Inputs: Dark background with light border, focus:ring-2 focus:ring-primary
- Submit button: Large, prominent, bg-primary hover:bg-primary-hover

**Data Visualization:**
- Radar Chart (Results page): Overall performance across 5 categories
- Bar Chart: Individual category scores with color-coded bars
- Score Gauge: Large circular percentage display (Quality Score)
- Charts use brand color palette for consistency

**Buttons:**
- Primary: bg-primary text-white px-6 py-3 rounded-lg font-semibold
- Secondary: border border-border bg-surface text-primary
- Outline on images: backdrop-blur-md bg-white/10 border border-white/20
- Icon buttons: p-2 rounded-lg hover:bg-surface-elevated

**Report Cards (Results Page):**
- Prominent Quality Score display at top (large percentage)
- Individual category breakdown cards with icons
- Improvement suggestions in expandable accordion sections
- PDF download button with icon (prominent placement)

### E. Animations

**Use Sparingly:**
- Page transitions: Fade in on mount (duration-300)
- Form submission: Loading spinner + success checkmark animation
- Chart reveals: Stagger animation when data loads (duration-500, delay-100 increments)
- Hover states: Scale 1.02 on cards (transition-transform duration-200)
- NO continuous animations or distracting motion

---

## Images & Visual Assets

**Hero Section (Home Page):**
- Large hero image showing educational app interface mockup or students engaging with technology
- Image overlay: dark gradient (from transparent to bg-base) for text readability
- Hero text over image with backdrop-blur button

**Icons:**
- Use Heroicons (CDN) throughout
- Category icons: Academic cap, Device mobile, Sparkles, Bolt, Chart bar
- Navigation icons: Home, Document text, Chart pie
- 24x24 size for inline icons, 48x48 for feature cards

**Evaluation Form Icons:**
- Each of 5 categories gets a unique Heroicon in its card header
- Icons use primary color for visual cohesion

**No Custom SVGs:** All icons from Heroicons library only

---

## Page-Specific Guidelines

**Home Page:**
- Hero section with large background image (educational theme)
- Value proposition: "Evaluate Educational Apps with Data-Driven Precision"
- 3-column feature grid showcasing evaluation categories
- CTA: "Start Evaluation" button (prominent, primary color)
- Stats section: Total evaluations, average score (if admin data available)

**Evaluation Form Page:**
- Progress indicator at top (visual step tracker)
- 5 category cards stacked vertically, each with:
  - Icon + Category name
  - Description text
  - 1-5 rating slider with live value
  - Helper text explaining rating scale
- Submit button: Fixed to bottom on mobile, inline on desktop

**Report/Results Page:**
- Quality Score hero: Large circular progress indicator (center, top)
- Radar chart: 5-axis visualization of all categories
- Individual scores: Grid of cards with bar indicators
- Improvement suggestions: AI-generated text in collapsible sections
- Action buttons: Download PDF, Start New Evaluation
- Color-coded scoring: Red (<50%), Yellow (50-75%), Green (>75%)

**Admin Dashboard (Optional):**
- Stats overview: Total evaluations, average scores, trends
- Recent evaluations table with sortable columns
- Charts: Time-series line graph of evaluation trends

---

## Accessibility & Dark Mode

- Dark mode is primary (as requested)
- Maintain WCAG AA contrast ratios (text on backgrounds)
- Focus indicators on all interactive elements
- Keyboard navigation support
- Form inputs have clear focus:ring-2 states
- Charts include text labels, not just colors

---

## Technical Notes

- Charts: Use Recharts library (better React integration than Chart.js)
- Smooth scrolling: scroll-smooth on html element
- Transitions: transition-all duration-300 for most interactions
- Responsive images: Use aspect ratio containers for hero
- PDF generation: Use react-pdf or jsPDF with chart screenshots

This design creates a professional, data-focused evaluation platform that feels modern, trustworthy, and purpose-built for educational technology assessment.