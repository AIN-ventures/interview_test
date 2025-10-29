# Pitch Deck Analyzer - Coding Exercise

## Overview

You'll build an **AI-powered pitch deck analyzer** for venture capital investors. Upload a pitch deck PDF, extract key information, assess the investment opportunity, and display comprehensive analysis in a web interface.

**Time**: 3-5 hours  
**Stack**: Django + React + OpenAI API + Your choice of tools  
**Approach**: Creative solutions encouraged!

---

## What You're Building

A full-stack application that:

1. **Accepts pitch deck PDFs** via REST API
2. **Extracts relevant information** from the deck (you decide what matters)
3. **Generates investment analysis** using AI (assess quality, market, team, etc.)
4. **Displays results** in a well-designed frontend interface
5. **Processes asynchronously** (no blocking requests)

**Key Challenge**: Decide what information matters for VC investment decisions and design an effective way to present it.

---

## Setup

### Prerequisites
- Python 3.11+, Node.js 18+, Docker & Docker Compose
- OpenAI API key

### Start the Application

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# 2. Start services
docker-compose up --build

# 3. Run migrations (new terminal)
docker-compose exec web python manage.py migrate

# 4. Start frontend (new terminal)
cd frontend && npm install && npm run dev
```

**Backend**: http://localhost:8000  
**Frontend**: http://localhost:5173

Test the skeleton:
```bash
echo "test" > test.pdf
curl -X POST http://localhost:8000/api/deals/ -F "pitch_deck=@test.pdf"
# Should return: {"error": "Not implemented"}
```

---

## Your Task

### Part 1: Backend - Information Extraction & Analysis

**Implement these files:**

#### `backend/deals/services.py`
Create functions to:
- Extract text/information from PDF pitch decks
- Use OpenAI API to analyze the deck
- Assess investment opportunity quality
- Save results to database

**You decide:**
- What information to extract (company details, market size, team backgrounds, traction, etc.)
- How to structure the data
- What metrics/scores matter for investment decisions
- How to prompt OpenAI for best results

#### `backend/deals/tasks.py`
- Implement async processing with Celery
- Orchestrate the extraction and analysis pipeline
- Handle errors gracefully

#### `backend/deals/views.py`
- Complete the `create()` endpoint to accept uploads
- Trigger async processing
- Return appropriate responses

**Approach Options** (creativity encouraged):
- **PDF Extraction**: PyPDF2, pdfminer, DocumentAI, multimodal vision models, etc.
- **AI Analysis**: GPT-4o with vision, structured outputs, function calling, etc.
- **Data Structure**: Design your own schema - what fields matter?

### Part 2: Frontend - Investment Analysis Display

**Redesign: `frontend/src/components/DealDetail.tsx`**

The current frontend shows minimal information (just company name, website, location). 

**Your task**: Design and implement a comprehensive investment analysis view.

**Consider displaying:**
- Company overview and key metrics
- Founder/team backgrounds and assessment
- Market opportunity and size
- Product/technology innovation
- Business model and traction
- Investment scores/ratings across relevant dimensions
- Key strengths and concerns
- Visual charts, graphs, or metrics
- Any other insights useful for investment decisions

**Design principles:**
- Clear information hierarchy
- Easy to scan and digest
- Professional appearance
- Appropriate visualizations

You can modify types, add new components, restructure data - complete creative freedom.

---

## Technical Requirements

### Must Have
- PDF processing (extract information from uploaded decks)
- OpenAI API integration
- Investment quality assessment across multiple dimensions
- Async processing (Celery or similar)
- Working end-to-end flow
- Enhanced frontend displaying comprehensive analysis
- Error handling

### Nice to Have
- Sophisticated extraction techniques (vision models, structured outputs)
- Thoughtful assessment criteria reflecting real VC thinking
- Beautiful, well-designed frontend interface
- Data visualizations (charts, graphs, progress bars)
- Comprehensive error handling and edge cases
- Tests

---

## Project Structure

```
backend/
├── deals/
│   ├── models.py          [Complete] Deal, Founder, Assessment models
│   ├── serializers.py     [Complete]
│   ├── views.py           [Skeleton] YOU COMPLETE
│   ├── tasks.py           [Empty] YOU IMPLEMENT
│   └── services.py        [Empty] YOU IMPLEMENT
└── core/utils.py          [Complete] Helper functions provided

frontend/
├── components/
│   ├── DealUpload.tsx     [Complete]
│   ├── DealList.tsx       [Complete]
│   └── DealDetail.tsx     [Basic] YOU REDESIGN & ENHANCE
└── api/client.ts          [Complete]
```

---

## What's Provided

**Backend Infrastructure:**
- Django + DRF configuration
- Database models (Deal, Founder, Assessment)
- Celery + Redis setup
- API routing and serializers
- Admin interface

**Frontend:**
- React + TypeScript + Vite
- Upload interface
- List view
- Basic detail page (minimal - you enhance this!)
- API client with polling

**Utilities:**
- Text sanitization helper
- Logging decorator
- Docker configuration

---

## Testing

```bash
# Manual test
curl -X POST http://localhost:8000/api/deals/ \
  -F "pitch_deck=@your_deck.pdf"

# Get status
curl http://localhost:8000/api/deals/{deal_id}/status/

# View in browser
open http://localhost:5173/deals/{deal_id}
```

The frontend polls every 2 seconds while processing, automatically updating when complete.

---

## Evaluation Criteria

### 1. Information Extraction (30%)
- Successfully extracts text/data from PDFs
- Identifies relevant information for investment decisions
- Handles various PDF formats and structures
- Graceful error handling

### 2. Investment Analysis Quality (30%)
- Thoughtful assessment of startup quality
- Evaluation across relevant dimensions (team, market, product, etc.)
- Scores/ratings reflect reasonable VC thinking
- Clear identification of strengths and risks

### 3. Frontend Design & Implementation (30%)
- Well-designed, professional interface
- Clear information hierarchy
- Appropriate visualizations
- Good UX (easy to understand analysis at a glance)
- Clean, maintainable code

### 4. Code Quality (10%)
- Clean, readable code
- Proper error handling
- Good architecture
- Appropriate documentation

---

## Submission

### 1. Implement Your Solution
Complete the required files and enhance the frontend.

### 2. Document Your Approach
Add a section to `README.md` explaining:
- **Your approach**: What did you extract? How did you assess quality?
- **Design decisions**: Why did you structure the frontend this way?
- **Trade-offs**: What compromises did you make?
- **Future improvements**: What would you add with more time?

### 3. Commit & Push
```bash
git add .
git commit -m "Implement pitch deck analyzer"
git push origin main
```

### 4. Share Repository
Send us the link to your fork.

---

## Tips

- **Start with data extraction** - Get basic PDF → structured data working first
- **Think like a VC** - What information would you want when evaluating a deal?
- **Design the data model** - What fields/structure make sense?
- **Iterate on the frontend** - Sketch the layout before implementing
- **Test incrementally** - Don't wait until everything is done
- **Be creative** - There's no single "right" answer

---

## Architecture Overview

```
User uploads PDF
  ↓
Django REST API endpoint
  ↓
Celery async task triggered
  ↓
Extract information from PDF (your approach)
  ↓
Analyze with OpenAI API (your prompts)
  ↓
Save structured data to database
  ↓
Frontend polls for updates
  ↓
Display comprehensive analysis (your design)
```

---

## Domain Context: What VCs Look For

When evaluating startups, investors typically assess:

- **Team**: Founder backgrounds, relevant experience, complementary skills, execution ability
- **Market**: Size (TAM/SAM/SOM), growth rate, timing, competition
- **Product**: Differentiation, technical moats, innovation, IP
- **Traction**: Revenue, users, growth rate, metrics
- **Business Model**: Unit economics, scalability, path to profitability
- **Risks**: Technical, market, execution, competitive, regulatory

Your analysis should reflect understanding of these dimensions.

---

## Resources

- **Django REST Framework**: https://www.django-rest-framework.org/
- **Celery**: https://docs.celeryq.dev/
- **OpenAI API**: https://platform.openai.com/docs/
- **React Query**: https://tanstack.com/query/latest
- **TailwindCSS**: https://tailwindcss.com/docs

---

## Questions?

Note any questions or assumptions in your README submission. Clear communication is valued.

Good luck - we're excited to see your solution!
