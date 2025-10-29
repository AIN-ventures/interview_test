# Pitch Deck Analyzer - Coding Exercise

Build an AI-powered pitch deck analyzer for VC investors. **Time: 2-4 hours**

## What You're Building

A full-stack app that:
1. Accepts pitch deck PDFs via API
2. Extracts relevant information using AI
3. Generates investment analysis
4. Displays results in a well-designed interface
5. Processes asynchronously (Celery)

**Key Challenge**: You decide what information matters for VC decisions and how to present it effectively.

---

## Quick Start

```bash
# 1. Setup
touch .env # create env file with openai key
# Edit .env: add OPENAI_API_KEY=sk-your-key-here

# 2. Start services
docker-compose up --build

# 3. Migrate (new terminal)
docker-compose exec web python manage.py migrate

# 4. Frontend (new terminal)
cd frontend && npm install && npm run dev
```

**Backend**: http://localhost:8000 | **Frontend**: http://localhost:5173

**Sample decks**: https://drive.google.com/drive/folders/1Dz7x752gZCGQDSSMcIMDL6Z5WOzrCUMd

**Note**: Backend code changes auto-reload. If you modify `tasks.py`, restart Celery: `docker-compose restart celery`

---

## Your Task

### Backend (3 files to implement)

**`backend/deals/services.py`**
- Extract information from PDFs (you choose the approach)
- Analyze with AI (OpenAI, Claude, etc.)
- Assess investment quality
- Save to database

**`backend/deals/tasks.py`**
- Implement async processing with Celery
- Orchestrate the pipeline
- Handle errors

**`backend/deals/views.py`**
- Complete the `create()` endpoint
- Trigger async processing

**Creative freedom**: Choose your extraction method (PyPDF2, vision models, DocumentAI), design your data structure, decide what metrics matter.

### Frontend (1 component to enhance)

**`frontend/src/components/DealDetail.tsx`**

Currently shows: company name, website, location (very basic)

**Your task**: Design and implement a comprehensive investment analysis view.

Consider:
- Company metrics and overview
- Founder backgrounds
- Market analysis
- Investment scores/ratings
- Strengths and concerns

**Design principles**: Clear hierarchy, easy to scan, professional, appropriate visualizations.

You can modify types, add components, restructure data - complete creative freedom.

---

## Project Structure

```
backend/deals/
├── models.py       [Complete] - Deal, Founder, Assessment models
├── serializers.py  [Complete]
├── views.py        [Skeleton] - YOU COMPLETE
├── tasks.py        [Empty] - YOU IMPLEMENT  
└── services.py     [Empty] - YOU IMPLEMENT

frontend/components/
├── DealUpload.tsx  [Complete]
├── DealList.tsx    [Complete]
└── DealDetail.tsx  [Basic] - YOU REDESIGN & ENHANCE
```

---

## Evaluation

1. **Information Extraction (30%)** - Successfully extracts relevant data, handles various PDFs
2. **Investment Analysis (30%)** - Thoughtful assessment, reflects VC thinking, clear insights
3. **Frontend Design (30%)** - Professional interface, good UX, appropriate visualizations
4. **Code Quality (10%)** - Clean, maintainable, well-structured

---

## Submission

1. **Fork** this repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/interview_test.git`
3. **Implement** your solution
4. **Push** to your fork
5. **Open a Pull Request** from your forked branch → this repository

In your PR description, include:
- **What you implemented**: Overview of the code you wrote
- **Major design decisions**: Key technical choices and why you made them
- **Trade-offs**: What you optimized for and what you deprioritized

---

## Tips

- Start with data extraction first
- Think like a VC - what info matters?
- Design your data model thoughtfully
- Test incrementally
- Be creative - no single "right" answer

## Troubleshooting

**Celery changes not taking effect?**  
Restart the worker: `docker-compose restart celery`

**Added new Python packages?**  
Rebuild: `docker-compose up --build`

**Database changes?**  
Run migrations: `docker-compose exec web python manage.py makemigrations && docker-compose exec web python manage.py migrate`

---

## What VCs Evaluate

- **Team**: Backgrounds, experience, complementary skills
- **Market**: Size (TAM/SAM/SOM), growth rate, competition
- **Product**: Differentiation, technical moats, innovation
- **Traction**: Revenue, users, growth metrics
- **Business Model**: Unit economics, scalability, profitability path

Your analysis should reflect these dimensions.

---

Good luck!
