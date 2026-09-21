# MASTER BUILD PROMPT — DATAPILOT AI

## ROLE

You are a senior staff-level full-stack engineer, AI engineer, data engineer, SaaS architect, UI/UX designer, DevOps engineer, QA engineer, and product engineer.

Your task is to design, implement, test, debug, and prepare for deployment a complete production-grade SaaS product called:

# DataPilot AI

### Tagline

**Turn Your Data Into Decisions.**

### Product Description

DataPilot AI is an AI-powered business intelligence SaaS platform that allows users and companies to upload Excel/CSV datasets and automatically transform raw business data into:

- Cleaned datasets
- Data-quality reports
- KPIs
- Interactive dashboards
- Charts
- Business insights
- AI-generated explanations
- Natural-language data chat
- Forecasts
- Anomaly detection
- Executive reports
- PDF reports
- Saved analyses
- Scheduled reports
- Multi-user business workspaces
- Subscription-based plans
- Usage limits
- White-label capabilities



---

# PROJECT EXECUTION CONTEXT — MANDATORY

## Local Project Root

The complete project MUST live inside this exact Windows directory:

```text
D:\Downloads\datapilot-ai
```

Treat this directory as the single source of truth for the entire project.

Every source file, configuration file, documentation file, test, script, asset, Docker configuration, migration, and repository file that belongs to DataPilot AI MUST be created under:

```text
D:\Downloads\datapilot-ai
```

Do not create a second copy of the project elsewhere.
Do not silently switch to another working directory.
Before creating or modifying files, verify that the current project root is exactly:

```text
D:\Downloads\datapilot-ai
```

Expected top-level structure:

```text
D:\Downloads\datapilot-ai\
├── frontend\
├── backend\
├── docs\
├── tests\
├── scripts\
├── data\
├── docker\
├── .github\
├── .gitignore
├── .env.example
├── README.md
├── LICENSE
├── docker-compose.yml
└── ...
```

The structure may evolve when technically justified, but the project root MUST remain the specified path.

### Local File Rules

- Do not place project files outside the project root.
- Do not create duplicate copies of the project.
- Temporary files must be removed after use when safe.
- Real customer data must never be committed.
- Only synthetic/demo datasets may be part of the Git repository.

## Canonical GitHub Repository

The canonical remote repository is:

```text
https://github.com/mhmd-ebrahim-1/datapilot-ai.git
```

Repository full name:

```text
mhmd-ebrahim-1/datapilot-ai
```

Use this repository as the canonical `origin`.

Before changing Git configuration:

1. Inspect existing Git status.
2. Inspect existing branches.
3. Inspect existing remotes.
4. Inspect the current repository state.
5. Preserve useful history and existing implementation.

If the local directory is not yet a Git repository:

1. Initialize Git inside `D:\Downloads\datapilot-ai`.
2. Create `.gitignore`.
3. Stage only safe files.
4. Create a meaningful commit.
5. Set `origin` to the canonical repository.
6. Push the implementation.

Do not create a different repository unless the specified repository is genuinely unavailable.

## GitHub Safety

Never commit:

```text
.env
.env.local
.env.production
API keys
passwords
tokens
private keys
database credentials
real customer datasets
uploaded user files
local secrets
```

Use `.env.example` for configuration documentation.

Before every push, review staged files and diffs.

Do not claim a successful GitHub push unless the remote state has actually been verified.

If GitHub authentication or permission is unavailable:

- continue implementing locally;
- prepare Git correctly;
- document the exact authentication step required;
- never fabricate a successful push or repository state.

## Gemini Agent Operating Mode

You are an autonomous coding agent.

Do not merely describe the implementation. Actually inspect, create, edit, run, test, debug, and verify the project.

### Before Writing Code

1. Verify `D:\Downloads\datapilot-ai`.
2. Inspect existing files and directories.
3. Inspect Git status.
4. Inspect Git branches.
5. Inspect Git remotes.
6. Inspect the canonical GitHub repository when access is available.
7. Determine the existing stack and package managers.
8. Identify incomplete and broken areas.
9. Preserve useful existing code.
10. Create an implementation plan based on the actual repository state.

### During Implementation

Work incrementally.

After every major feature:

1. Run relevant tests.
2. Run linting.
3. Run type checking.
4. Build or start the affected application.
5. Fix discovered errors.
6. Verify the workflow.
7. Continue only after the phase is stable.

Do not stop after generating files.

Actually run the application whenever the environment allows it.

### Windows Working Directory

When using shell commands, explicitly work from:

```powershell
Set-Location "D:\Downloads\datapilot-ai"
```

Then run project commands from that location.

Do not silently create project files under another path.

## Git Workflow

Use meaningful commits.

Suggested sequence:

```text
feat: initialize DataPilot AI architecture
feat: add authentication and workspaces
feat: add dataset upload and processing
feat: add data profiling and cleaning
feat: add analytics and KPI engine
feat: add interactive dashboard
feat: add AI insights
feat: add AI data chat
feat: add forecasting
feat: add anomaly detection
feat: add executive reporting
feat: add usage limits and subscriptions
feat: add admin and workspace management
feat: add scheduled reports
test: add automated test coverage
security: harden file handling and authorization
docs: improve project documentation
```

Do not create meaningless commit messages.

## GitHub Repository Quality

The repository must look professional to a recruiter, client, technical reviewer, or collaborator.

At minimum include:

```text
README.md
LICENSE
.gitignore
.env.example
```

Also include relevant:

- architecture documentation;
- installation instructions;
- API documentation;
- screenshots when available;
- demo instructions;
- testing instructions;
- deployment instructions;
- environment variable documentation;
- security notes.

The README must state the canonical local path and GitHub repository.

## GitHub Verification

After pushing, verify:

- repository is accessible;
- expected branch exists;
- intended latest commit exists remotely;
- local working tree is clean or explicitly documented;
- README exists;
- no secrets were pushed;
- no private data was pushed.

Use available Git/GitHub tooling to verify both local and remote state.

## Final Agent Report

At the end, provide:

### Project Root

```text
D:\Downloads\datapilot-ai
```

### GitHub Repository

```text
https://github.com/mhmd-ebrahim-1/datapilot-ai.git
```

### Implementation Status

List what was actually implemented.

### Verification Status

Report:

- tests executed;
- lint/type checks;
- builds;
- application startup;
- end-to-end workflow results.

### Git Status

Report whether the working tree is clean.

### GitHub Status

Report whether the implementation was successfully pushed and verified.

### Remaining Configuration

List only real external requirements, such as:

- Gemini/API credentials;
- production database;
- storage;
- email provider;
- payment provider;
- OAuth.

Never claim an external integration is live unless it was actually configured and tested.

## Critical Rules

Do not:

- create a different project root;
- create a different GitHub repository;
- silently fork or rename the repository;
- push secrets;
- fabricate GitHub success;
- stop at a plan when implementation is possible.

Continue until the application is implemented and verified as far as the available environment permits.

---
The application must feel like a real commercial SaaS product.

DO NOT build a toy project.
DO NOT build a static mockup.
DO NOT use fake buttons that do nothing.
DO NOT leave major functionality as placeholders.
DO NOT hardcode dashboard results.
DO NOT pretend AI functionality exists when it does not.
Every important button and workflow must have a real implementation.

---

# 1. PRIMARY OBJECTIVE

Build a complete SaaS platform where this workflow works end-to-end:

User
→ Registration/Login
→ Dashboard
→ Upload Excel/CSV
→ Validate File
→ Parse Dataset
→ Profile Dataset
→ Detect Dataset Type
→ Clean Dataset
→ Generate Data Quality Score
→ Calculate KPIs
→ Automatically select meaningful visualizations
→ Generate interactive dashboard
→ Generate AI business insights
→ Ask questions about the dataset using AI
→ Generate forecasts where applicable
→ Detect anomalies
→ Generate executive report
→ Export PDF
→ Save analysis
→ View history
→ Manage subscription
→ Manage usage
→ Delete data

Everything must be connected.

---

# 2. TECHNOLOGY STACK

Use the following architecture unless there is a strong technical reason to change something.

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Lucide icons
- Recharts or Plotly
- React Hook Form
- Zod
- TanStack Query where useful

Use modern App Router architecture.

---

# 3. BACKEND

Use:

- Python
- FastAPI
- Pydantic
- Pandas
- NumPy
- Scikit-learn
- openpyxl
- python-dateutil

Use a clean service-oriented architecture.

Do not put business logic directly inside API route handlers.

Recommended structure:

backend/

```text
app/
├── main.py
├── config/
│   ├── settings.py
│   └── logging.py
├── api/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── datasets.py
│   │   ├── analyses.py
│   │   ├── insights.py
│   │   ├── chat.py
│   │   ├── forecasts.py
│   │   ├── anomalies.py
│   │   ├── reports.py
│   │   ├── billing.py
│   │   ├── users.py
│   │   └── workspaces.py
│   └── dependencies.py
├── models/
├── schemas/
├── services/
│   ├── ingestion/
│   ├── profiling/
│   ├── cleaning/
│   ├── analytics/
│   ├── visualization/
│   ├── ai/
│   ├── forecasting/
│   ├── anomaly_detection/
│   ├── reporting/
│   └── billing/
├── repositories/
├── utils/
└── tests/

```

---

# 4. DATABASE

Use PostgreSQL.

Use SQLAlchemy or SQLModel.

Database must support:

## users

Fields:

- id
- name
- email
- password_hash
- avatar_url
- role
- created_at
- updated_at
- last_login_at

## workspaces

- id
- name
- owner_id
- logo_url
- brand_color
- created_at

## workspace_members

- id
- workspace_id
- user_id
- role
- created_at

Roles:

- owner
- admin
- analyst
- viewer

## datasets

- id
- workspace_id
- uploaded_by
- name
- original_filename
- file_type
- file_size
- storage_path
- row_count
- column_count
- dataset_type
- quality_score
- status
- created_at
- updated_at

Statuses:

- uploaded
- processing
- ready
- failed
- deleted

## analyses

- id
- dataset_id
- workspace_id
- created_by
- status
- summary_json
- kpis_json
- metadata_json
- created_at

## insights

- id
- analysis_id
- title
- category
- severity
- description
- recommendation
- supporting_metrics_json
- created_at

Categories:

- performance
- growth
- risk
- anomaly
- opportunity
- recommendation

Severity:

- info
- warning
- critical

## chat_sessions

- id
- workspace_id
- dataset_id
- user_id
- created_at

## chat_messages

- id
- session_id
- role
- content
- metadata_json
- created_at

## forecasts

- id
- dataset_id
- analysis_id
- metric
- horizon
- model
- predictions_json
- confidence_intervals_json
- metrics_json
- created_at

## anomalies

- id
- dataset_id
- analysis_id
- column
- row_reference
- value
- score
- explanation
- created_at

## reports

- id
- workspace_id
- dataset_id
- analysis_id
- created_by
- title
- format
- storage_path
- created_at

## subscriptions

- id
- workspace_id
- provider
- provider_customer_id
- provider_subscription_id
- plan
- status
- current_period_start
- current_period_end
- created_at

## usage

Track:

- analyses
- uploads
- AI requests
- chat requests
- reports
- storage
- forecast requests

Include monthly counters.

---

# 5. AUTHENTICATION

Implement secure authentication.

Support:

- Email/password
- Google OAuth if practical

Requirements:

- Password hashing
- Secure sessions/JWT
- Protected routes
- Refresh mechanism if JWT is used
- Logout
- Password reset
- Email verification if practical
- Rate limiting
- Brute-force protection

Never store plaintext passwords.

Never expose secrets to the frontend.

---

# 6. USER ONBOARDING

After registration show onboarding:

## Step 1

"What best describes you?"

Options:

- Business Owner
- Data Analyst
- Freelancer
- Marketing Professional
- Finance Professional
- Student
- Other

## Step 2

"What type of data do you usually work with?"

- Sales
- Marketing
- Finance
- HR
- Operations
- Inventory
- Customer Data
- Other

## Step 3

"Create your workspace"

Default:

```text
My Workspace

```

Then:

**Upload your first dataset**

---

# 7. LANDING PAGE

Build a highly polished commercial landing page.

Sections:

1. Navbar
2. Hero
3. Social proof placeholder area
4. How it works
5. Features
6. Dashboard preview
7. AI insights preview
8. AI chat preview
9. Forecasting preview
10. Reports
11. Security
12. Pricing
13. FAQ
14. CTA
15. Footer

Hero:

# Turn Your Data Into Decisions.

Subtitle:

Upload your Excel or CSV files and let DataPilot AI automatically clean, analyze, visualize, and explain your business data.

Buttons:

**Start Free**

**See Demo**

Use a premium B2B SaaS aesthetic.

Avoid excessive gradients and unnecessary animations.

Design should communicate trust, intelligence, data, and professionalism.

---

# 8. UI DESIGN SYSTEM

Create a consistent design system.

Use:

- White/light backgrounds
- Dark text
- Professional blue/indigo accent
- Neutral gray surfaces
- Clear success/warning/error states
- Rounded cards
- Subtle shadows
- Generous spacing

Do not make it look like a generic AI wrapper.

The product should look closer to a professional analytics platform.

Responsive design is mandatory.

Desktop:

- Sidebar
- Top navigation
- Main content

Mobile:

- Collapsible navigation
- Responsive cards
- Scrollable charts
- Mobile-friendly tables

---

# 9. DASHBOARD

Main dashboard should show:

## Overview

Cards:

- Total Datasets
- Analyses
- AI Insights
- Reports

Then:

### Recent Datasets

Show:

- Dataset
- Rows
- Columns
- Status
- Created
- Actions

### Recent Insights

Show latest important findings.

### Usage

Show:

```text
Analyses
18 / 30

AI Requests
74 / 100

Storage
1.2 GB / 5 GB

```

### Quick Actions

- Upload Dataset
- Analyze Dataset
- Generate Report
- Ask AI

---

# 10. FILE UPLOAD

Supported:

- CSV
- XLSX
- XLS if supported safely

Requirements:

- Drag & drop
- File picker
- Upload progress
- File size validation
- MIME validation
- Extension validation
- Error handling

Show:

```text
File uploaded successfully

```

Then process asynchronously if necessary.

Do not load massive files entirely into memory.

Design for chunking/streaming where practical.

---

# 11. DATASET PREVIEW

Show:

- File name
- Rows
- Columns
- Size
- Data type
- Preview first 100 rows
- Missing values
- Duplicate count

Table should support:

- Search
- Sorting
- Pagination
- Horizontal scrolling
- Column type display

---

# 12. DATA PROFILING ENGINE

Automatically calculate:

- row count
- column count
- data types
- missing values
- missing percentage
- unique values
- duplicates
- min
- max
- mean
- median
- standard deviation
- quantiles
- cardinality
- correlations where appropriate

Detect:

- numeric columns
- categorical columns
- datetime columns
- text columns
- ID columns
- target-like columns

Return structured JSON.

---

# 13. DATA QUALITY SCORE

Calculate a transparent quality score.

Example dimensions:

- completeness
- uniqueness
- validity
- consistency
- type correctness

Score:

```text
0–59 Poor
60–79 Fair
80–89 Good
90–100 Excellent

```

Show exactly why the score exists.

Example:

```text
Data Quality: 92/100

Completeness: 95
Validity: 93
Consistency: 89
Uniqueness: 97

```

Never invent scores.

Calculate them from actual dataset characteristics.

---

# 14. AUTOMATIC DATA CLEANING

Create a safe cleaning pipeline.

Operations may include:

- trim whitespace
- normalize column names
- convert numeric strings
- parse dates
- remove exact duplicates
- standardize null representations
- handle obvious formatting issues

Do not silently modify ambiguous business data.

Before destructive transformations, maintain a record of changes.

Show:

```text
127 duplicate rows removed
342 missing values detected
Date format standardized
Revenue converted to numeric

```

Allow the user to inspect the cleaning summary.

---

# 15. DATASET TYPE DETECTION

Automatically classify datasets.

Possible types:

- Sales
- Marketing
- Finance
- HR
- Inventory
- Operations
- Customer
- General Analytics

Use deterministic heuristics first.

Use AI only as a secondary semantic classifier when useful.

Return confidence.

Example:

```text
Dataset Type:
Sales Analytics

Confidence:
94%

```

---

# 16. KPI ENGINE

Do not hardcode KPIs.

Infer KPIs based on dataset structure.

For sales datasets:

- Revenue
- Cost
- Profit
- Profit Margin
- Orders
- Units Sold
- Average Order Value
- Growth

For marketing:

- Spend
- Impressions
- Clicks
- CTR
- CPC
- Conversions
- Conversion Rate
- CPA
- ROAS

For finance:

- Revenue
- Expenses
- Net Income
- Margin
- Growth

For HR:

- Headcount
- Turnover
- Average Salary
- Absence Rate
- Performance

If required columns do not exist, do not fabricate metrics.

---

# 17. AUTOMATIC CHART GENERATION

Generate charts based on actual data.

Possible charts:

- KPI cards
- Line charts
- Bar charts
- Area charts
- Scatter plots
- Histograms
- Heatmaps
- Tables
- Correlation matrix

Do not generate meaningless charts.

Choose visualizations based on data types and analytical usefulness.

Every chart must include:

- Title
- Axis labels
- Tooltip
- Legend when necessary
- Empty state
- Error state

---

# 18. DASHBOARD BUILDER

Create a dashboard automatically after analysis.

Sections:

### Executive Summary

### KPI Overview

### Trends

### Product/Category Performance

### Geographic/Branch Performance

### Customer Performance

### Operational Metrics

Only show sections relevant to the dataset.

Do not show irrelevant empty widgets.

---

# 19. AI INSIGHTS ENGINE

This is a core feature.

Architecture:

```text
Dataset
↓
Python Analytics Engine
↓
Structured Metrics
↓
AI Reasoning Layer
↓
Validated Insights

```

Never ask the LLM to perform raw calculations that Python can perform exactly.

The LLM receives verified structured metrics.

AI should generate:

- Key findings
- Trends
- Risks
- Opportunities
- Recommendations

Each insight must reference supporting metrics.

Example:

```json
{
  "title": "Revenue growth accelerated",
  "category": "growth",
  "severity": "info",
  "description": "...",
  "supporting_metrics": {
    "current_revenue": 1250000,
    "previous_revenue": 1055000,
    "growth_percent": 18.4
  }
}

```

Never allow the AI to invent values.

---

# 20. AI INSIGHT VALIDATION

Before displaying an AI insight:

1. Validate referenced metrics.
2. Ensure numbers exist in the analytics output.
3. Reject unsupported claims.
4. Attach source metric references where possible.

If an insight cannot be verified, do not display it.

---

# 21. AI CHAT WITH DATA

Implement:

# Ask DataPilot

Example:

User:

"What was our best-selling product?"

System:

1. Understand question.
2. Identify relevant columns.
3. Run deterministic analytics/query.
4. Return verified result.
5. Let LLM explain it naturally.

Architecture:

```text
User Question
↓
Intent Detection
↓
Data Query / Analytics
↓
Verified Result
↓
LLM Explanation
↓
Response

```

Do NOT simply send the whole dataset to an LLM.

For larger datasets, use:

- SQL
- Pandas
- Aggregations
- Semantic metadata
- Retrieval where appropriate

---

# 22. NATURAL LANGUAGE QUESTIONS

Support questions such as:

- What was our total revenue?
- Which product sold the most?
- Which branch performed best?
- What was the growth rate?
- Which month had the highest sales?
- Which customers generated the most revenue?
- What changed compared with last month?
- Show me unusual values.
- What are the main business risks?
- What should we investigate?

If the data cannot answer a question:

Say clearly:

"The uploaded dataset does not contain enough information to answer this question."

Never hallucinate.

---

# 23. FORECASTING ENGINE

Implement forecasting only when sufficient time-series data exists.

Requirements:

- Detect datetime column
- Detect numerical target
- Aggregate data appropriately
- Validate time frequency
- Check data sufficiency

Possible models:

- baseline moving average
- exponential smoothing
- Prophet if appropriate
- ARIMA/SARIMA
- XGBoost-based forecasting where appropriate

Do not blindly use one model.

Compare models when practical.

Show:

- Forecast
- Historical data
- Confidence interval
- Forecast horizon
- Model used
- Validation metrics

Metrics:

- MAE
- RMSE
- MAPE when valid

If forecasting is not reliable, explain why.

---

# 24. ANOMALY DETECTION

Implement:

- IQR
- Z-score
- Isolation Forest

Choose based on data type.

Detect:

- unusual sales
- unusual revenue
- unusual quantities
- unusual expenses
- unusual transaction values

Show:

```text
Anomaly Detected

Date: March 14
Metric: Revenue
Value: 485,000
Expected Range: 80,000–120,000

```

Do not call every extreme value a business problem.

Use wording such as:

"Statistical anomaly detected."

---

# 25. REPORT GENERATION

Generate a professional executive report.

Sections:

1. Cover
2. Executive Summary
3. Data Quality
4. KPI Overview
5. Performance Trends
6. Key Findings
7. Risks
8. Opportunities
9. Forecast
10. Anomalies
11. Recommendations
12. Methodology
13. Appendix

Report must contain real data.

Do not fabricate content.

---

# 26. PDF EXPORT

Generate high-quality PDF.

Use a professional layout.

Include:

- company/workspace logo if available
- report date
- dataset period
- KPI cards
- charts
- insights
- recommendations
- page numbers

Support:

**Download PDF**

---

# 27. CSV/EXCEL EXPORT

Allow users to export:

- cleaned dataset
- KPI table
- insight table
- anomaly table
- forecast table

---

# 28. REPORT HISTORY

Users can see:

```text
Report Name
Dataset
Created
Created By
Format
Actions

```

Actions:

- View
- Download
- Delete

---

# 29. DATASET HISTORY

Every uploaded dataset gets its own page:

```text
Overview
Data Quality
Analytics
Charts
AI Insights
Forecast
Anomalies
Reports
AI Chat

```

---

# 30. SUBSCRIPTION SYSTEM

Implement plans:

## Free

- limited datasets
- limited analyses
- limited AI requests
- limited storage
- basic reports

## Pro

- more analyses
- larger files
- AI Chat
- forecasting
- anomaly detection
- advanced reports

## Business

- multiple users
- workspaces
- white-label
- scheduled reports
- higher limits

Use configuration rather than hardcoding limits throughout the code.

Example:

```python
PLAN_LIMITS = {
    "free": {...},
    "pro": {...},
    "business": {...}
}

```

---

# 31. USAGE LIMITS

Before every expensive operation:

Check:

- plan
- monthly usage
- file size
- storage
- AI request count

If limit is reached:

Show:

```text
You've reached your monthly AI analysis limit.

Upgrade your plan to continue.

```

Never allow bypassing limits through frontend manipulation.

Limits must be enforced server-side.

---

# 32. BILLING

Make billing provider abstraction.

Do not tightly couple business logic to one provider.

Support a provider such as Stripe where available.

Structure:

```text
BillingService
PaymentProvider
SubscriptionService
UsageService

```

Support:

- checkout
- subscription
- cancellation
- plan change
- webhook handling
- subscription status

Never trust frontend payment state.

Verify webhooks server-side.

---

# 33. ADMIN PANEL

Create an admin area.

Admin can see:

- users
- workspaces
- subscriptions
- datasets
- usage
- system health
- errors
- AI usage
- revenue metrics if billing is connected

Admin actions:

- deactivate user
- inspect workspace
- change plan
- view usage
- delete abusive data

Protect admin routes strongly.

---

# 34. WORKSPACES

A company should be able to have:

```text
ABC Company
├── Owner
├── Admin
├── Analysts
└── Viewers

```

Permissions:

Owner:

- everything

Admin:

- users
- datasets
- reports
- settings

Analyst:

- upload
- analyze
- reports

Viewer:

- view dashboards
- view reports

Enforce permissions server-side.

---

# 35. SCHEDULED REPORTS

Allow:

```text
Every day
Every week
Every month

```

User selects:

- dataset
- report
- recipients
- schedule

System:

```text
Fetch Data
↓
Analyze
↓
Generate Report
↓
Send Email

```

Use a background job system.

---

# 36. BACKGROUND JOBS

Long-running operations must not block HTTP requests.

Use:

- Celery + Redis
  or
- another production-grade task queue

Jobs:

- file processing
- analysis
- AI insights
- forecasting
- report generation
- scheduled reports

Provide job status:

```text
Queued
Processing
Completed
Failed

```

---

# 37. OBSERVABILITY

Implement:

- structured logging
- error tracking
- request IDs
- job IDs
- audit logs
- performance monitoring

Never log:

- passwords
- tokens
- API keys
- sensitive dataset contents unnecessarily

---

# 38. SECURITY

Implement:

- CORS restrictions
- CSRF protection where applicable
- rate limiting
- input validation
- file validation
- SQL injection prevention
- XSS prevention
- secure cookies
- secure headers
- authentication middleware
- authorization middleware

Validate all user input.

Never trust filenames.

Generate safe storage names.

---

# 39. FILE SECURITY

For uploaded files:

- validate MIME type
- validate extension
- enforce size limits
- sanitize filename
- store outside executable directories
- scan files where practical
- never execute uploaded content
- isolate user files

---

# 40. DATA ISOLATION

Every dataset query must be scoped by:

```text
workspace_id

```

Never allow a user to request another workspace's dataset by changing an ID.

Use authorization checks at service level.

---

# 41. API DESIGN

Create documented REST APIs.

Example:

```text
POST   /api/v1/auth/register
POST   /api/v1/auth/login

POST   /api/v1/datasets/upload
GET    /api/v1/datasets
GET    /api/v1/datasets/{id}
DELETE /api/v1/datasets/{id}

POST   /api/v1/analyses
GET    /api/v1/analyses/{id}

GET    /api/v1/insights/{analysis_id}

POST   /api/v1/chat
GET    /api/v1/chat/{session_id}

POST   /api/v1/forecast
GET    /api/v1/forecast/{id}

GET    /api/v1/anomalies/{analysis_id}

POST   /api/v1/reports
GET    /api/v1/reports
GET    /api/v1/reports/{id}
DELETE /api/v1/reports/{id}

GET    /api/v1/usage

GET    /api/v1/subscription
POST   /api/v1/billing/checkout
POST   /api/v1/billing/webhook

```

Use consistent response structures.

---

# 42. API DOCUMENTATION

FastAPI OpenAPI documentation must work.

Document:

- authentication
- parameters
- request bodies
- responses
- errors

---

# 43. ERROR HANDLING

Every API must return useful errors.

Example:

```json
{
  "error": {
    "code": "INVALID_DATASET",
    "message": "The uploaded file does not contain a usable numerical or categorical dataset."
  }
}

```

Frontend must display human-readable messages.

Never expose stack traces to users.

---

# 44. EMPTY STATES

Every page needs a meaningful empty state.

Example:

"No datasets yet."

Button:

**Upload your first dataset**

Do not leave blank screens.

---

# 45. LOADING STATES

Use:

- skeletons
- progress indicators
- upload progress
- analysis progress

Example:

```text
Analyzing your dataset...

✓ File validated
✓ Data profiled
✓ KPIs calculated
● Generating AI insights
○ Building report

```

---

# 46. FAILURE RECOVERY

If AI fails:

The dashboard should still work.

If forecasting fails:

Show:

"Forecasting could not be generated because the dataset does not contain sufficient time-series data."

If report generation fails:

Allow retry.

Do not crash the whole application.

---

# 47. AI PROVIDER ABSTRACTION

Do not hardcode the AI provider throughout the application.

Create:

```text
AIProvider
├── OpenAIProvider
├── GeminiProvider
└── MockProvider

```

Use environment variables.

Example:

```text
AI_PROVIDER=openai
AI_MODEL=...
AI_API_KEY=...

```

Never commit API keys.

---

# 48. AI PROMPT ENGINEERING

Keep AI prompts in versioned files.

Example:

```text
prompts/
├── dataset_classifier.txt
├── insights.txt
├── chat.txt
├── report_summary.txt
└── recommendations.txt

```

Use structured JSON output whenever possible.

Validate AI responses using Pydantic schemas.

---

# 49. AI COST CONTROL

AI requests cost money.

Implement:

- caching
- request limits
- token limits
- concise context
- structured metrics
- deduplication
- retry limits

Do not send raw 100MB datasets to an LLM.

---

# 50. DEMO DATA

Create realistic demo datasets.

Examples:

```text
demo_sales.csv
demo_marketing.csv
demo_finance.csv
demo_hr.csv

```

Demo mode should allow users to understand the product without uploading their own data.

---

# 51. DEMO ACCOUNT

Create optional demo account:

```text
demo@datapilot.ai

```

But NEVER ship a hardcoded production password.

If demo credentials are required, make them configurable through environment variables.

---

# 52. SEED DATA

Create database seed scripts.

Seed:

- demo workspace
- demo dataset metadata
- demo reports
- sample insights

Use synthetic data only.

---

# 53. TESTING

Create tests for:

## Backend

- authentication
- authorization
- file validation
- CSV parsing
- Excel parsing
- profiling
- cleaning
- KPI calculations
- forecasting
- anomaly detection
- AI response validation
- report generation
- usage limits
- billing webhooks

## Frontend

- login
- upload
- dashboard
- dataset page
- charts
- AI chat
- report generation
- subscription flow

Use:

- pytest
- Playwright or equivalent

---

# 54. TEST DATA

Create test datasets for:

- clean data
- missing values
- duplicate rows
- invalid dates
- large files
- empty files
- unsupported formats
- mixed data types
- no numeric columns
- no date column
- time series
- categorical datasets

---

# 55. PERFORMANCE

Design for:

- large CSV files
- large datasets
- concurrent users

Do not load unnecessary data into frontend.

Use pagination.

Use server-side aggregation.

Cache expensive operations.

Use background jobs.

---

# 56. DATABASE PERFORMANCE

Add indexes for:

- user_id
- workspace_id
- dataset_id
- analysis_id
- created_at
- subscription status

Avoid N+1 queries.

---

# 57. FRONTEND PERFORMANCE

Use:

- code splitting
- lazy loading
- memoization where useful
- pagination
- virtualized tables for large datasets

Charts should not attempt to render 1 million raw points.

Aggregate appropriately.

---

# 58. ACCESSIBILITY

Implement:

- semantic HTML
- keyboard navigation
- accessible forms
- labels
- focus states
- proper contrast
- ARIA only where needed

---

# 59. INTERNATIONALIZATION

Prepare architecture for:

- English
- Arabic

Primary UI can initially be English.

However, support RTL correctly for Arabic.

AI insights should eventually support:

- English
- Arabic

---

# 60. LOCALIZATION

Do not hardcode UI strings throughout components.

Use translation files.

Example:

```text
/locales/en.json
/locales/ar.json

```

---

# 61. SEO

Landing page should include:

- title
- meta description
- Open Graph
- Twitter/X metadata
- structured data where useful
- sitemap
- robots.txt

---

# 62. LEGAL PAGES

Create:

- Privacy Policy
- Terms of Service
- Cookie Policy

Do not invent legal claims.

Use clearly marked configurable business information.

---

# 63. SETTINGS

User settings:

- Name
- Email
- Avatar
- Language
- Theme
- Notifications
- Security

Workspace settings:

- Workspace name
- Logo
- Branding
- Members
- Roles
- Billing

---

# 64. NOTIFICATIONS

Support:

- dataset processing completed
- report generated
- forecast completed
- subscription changes
- scheduled report
- errors

Implement notification preferences.

---

# 65. EMAIL SYSTEM

Create email service abstraction.

Emails:

- welcome
- email verification
- password reset
- report ready
- scheduled report
- subscription confirmation
- usage limit warning

Use environment variables for provider credentials.

---

# 66. WHITE-LABEL

Business plan should support:

- company logo
- company name
- custom accent color
- custom report branding

PDF reports should use workspace branding.

---

# 67. AUDIT LOGS

Record important actions:

- login
- upload
- analysis
- report creation
- dataset deletion
- member invitation
- role change
- subscription change

Do not log sensitive content.

---

# 68. DATA DELETION

User can delete:

- dataset
- analysis
- reports
- account

Deleting a dataset should clean related resources according to retention rules.

Use safe cascading/deletion strategy.

---

# 69. BACKUP STRATEGY

Document:

- database backup
- object storage backup
- disaster recovery
- retention

Do not claim backups exist unless configured.

---

# 70. ENVIRONMENT VARIABLES

Create:

```text
.env.example

```

Include:

```text
DATABASE_URL=
SECRET_KEY=
JWT_SECRET=
AI_PROVIDER=
AI_API_KEY=
AI_MODEL=

STORAGE_PROVIDER=
STORAGE_BUCKET=
STORAGE_ACCESS_KEY=
STORAGE_SECRET_KEY=

REDIS_URL=

EMAIL_PROVIDER=
EMAIL_API_KEY=

PAYMENT_PROVIDER=
PAYMENT_SECRET=
PAYMENT_WEBHOOK_SECRET=

NEXT_PUBLIC_API_URL=

```

Never put real secrets in Git.

---

# 71. DOCKER

Create:

```text
Dockerfile
docker-compose.yml

```

Services:

```text
frontend
backend
postgres
redis
worker

```

Make local development easy.

Command should ideally be:

```bash
docker compose up

```

---

# 72. DEVELOPMENT EXPERIENCE

Create a strong README.

README must contain:

- Product overview
- Architecture
- Requirements
- Installation
- Environment variables
- Database setup
- Running locally
- Running tests
- Docker instructions
- Deployment
- API documentation
- AI configuration
- Billing configuration
- Troubleshooting

---

# 73. GIT

Create:

```text
.gitignore

```

Never commit:

- .env
- API keys
- passwords
- uploaded datasets
- private files

Use meaningful commits if Git is available.

---

# 74. CI/CD

If repository automation is available, create CI pipeline.

On push:

1. Install dependencies
2. Lint
3. Type check
4. Run tests
5. Build frontend
6. Build backend

Do not deploy broken builds.

---

# 75. DEPLOYMENT

Prepare production deployment.

Suggested:

Frontend:

- Vercel

Backend:

- Render / Railway / Fly.io / AWS

Database:

- managed PostgreSQL

Redis:

- managed Redis

Storage:

- S3-compatible storage

But keep architecture provider-agnostic.

---

# 76. PRODUCTION CONFIGURATION

Ensure:

- DEBUG=false
- secure cookies
- HTTPS
- restricted CORS
- production logging
- proper database connection pooling
- rate limiting
- secrets from environment
- no development credentials

---

# 77. ANALYTICS

Track product analytics without collecting unnecessary sensitive data.

Events:

- signup
- login
- dataset_uploaded
- analysis_completed
- report_generated
- ai_question_asked
- forecast_generated
- subscription_started

Use abstraction so analytics provider can be changed.

---

# 78. PRODUCT METRICS

Admin dashboard should eventually track:

- DAU
- WAU
- MAU
- activation rate
- analysis completion rate
- report generation rate
- conversion rate
- churn
- subscription revenue

Do not fake metrics.

---

# 79. COMMERCIAL UX

Every feature should answer:

"What value does this provide to the user?"

Avoid unnecessary technical terminology in the UI.

Use business language.

Instead of:

"Isolation Forest anomaly score"

show:

"Unusual activity detected"

Technical details can appear under:

"Methodology"

---

# 80. UX COPY

Use concise professional English.

Examples:

Button:

"Analyze Dataset"

Not:

"Click Here To Analyze"

Success:

"Your analysis is ready."

Error:

"We couldn't analyze this dataset. Check the data format and try again."

---

# 81. AI TRANSPARENCY

Clearly indicate when content is AI-generated.

For example:

"AI-generated insight based on verified dataset metrics."

Never imply that AI is infallible.

---

# 82. TRUST

Include:

- data quality score
- methodology
- supporting metrics
- confidence where applicable
- source references inside analysis

Users should be able to understand why an insight was generated.

---

# 83. NO FAKE FUNCTIONALITY

This is mandatory.

Do not create:

```text
<button>Generate Report</button>

```

unless it actually generates a report.

Do not create:

```text
Upgrade

```

unless subscription logic exists.

Do not create fake AI responses.

Do not create fake analytics.

Do not create fake charts.

If a feature cannot be fully implemented, implement a graceful, clearly labeled limitation rather than pretending.

---

# 84. SECURITY PRINCIPLE

Never trust:

- frontend
- URL parameters
- user-provided IDs
- uploaded filenames
- client-side subscription state
- client-side roles

Every sensitive operation must be verified server-side.

---

# 85. PRODUCT QUALITY BAR

The final result must feel like a commercial SaaS product.

It must be:

- polished
- responsive
- secure
- modular
- maintainable
- testable
- documented
- deployable
- scalable

---

# 86. AGENT EXECUTION RULES

You are an autonomous coding agent.

Before writing code:

1. Inspect the repository.
2. Identify existing files.
3. Identify the existing stack.
4. Reuse useful existing infrastructure.
5. Do not destroy working functionality.
6. Create an implementation plan.
7. Implement incrementally.

After every major phase:

1. Run tests.
2. Run linting.
3. Run type checking.
4. Start the application.
5. Test important workflows.
6. Fix errors.
7. Continue only after the phase is stable.

Do not stop after generating files.

Actually run the application.

---

# 87. IF THE PROJECT ALREADY EXISTS

Do not recreate the application from scratch.

First inspect:

```text
package.json
requirements.txt
pyproject.toml
docker-compose.yml
README.md
src/
app/
backend/
frontend/

```

Understand the current architecture.

Then improve it.

Preserve working functionality.

---

# 88. IF SOMETHING IS MISSING

Do not ask unnecessary questions.

Make sensible engineering decisions and continue.

Only ask for clarification if a decision is genuinely impossible without user input, such as:

- missing mandatory API credential
- unavailable database
- unavailable payment provider credentials

For development, provide mock/local implementations where appropriate.

---

# 89. NO PLACEHOLDER SECRETS IN CODE

Use:

```text
.env.example

```

not:

```python
API_KEY = "123456"

```

---

# 90. DEMO MODE

Implement development/demo mode where external services are unavailable.

For example:

```text
AI_PROVIDER=mock
PAYMENT_PROVIDER=mock
EMAIL_PROVIDER=mock

```

But make the architecture compatible with real providers.

---

# 91. FINAL ACCEPTANCE TEST

Before declaring the project complete, verify this exact scenario:

### Scenario

1. Open application.
2. Register.
3. Login.
4. Create workspace.
5. Upload demo_sales.csv.
6. File is validated.
7. Dataset is profiled.
8. Data quality score appears.
9. Dataset type is detected.
10. KPI cards appear.
11. Charts appear.
12. AI insights appear.
13. Ask:

"What was the best-selling product?"

14. Receive an answer based on actual data.
15. Open forecast.
16. Generate anomalies.
17. Generate PDF report.
18. Download report.
19. Open report history.
20. Check usage.
21. Delete dataset.
22. Verify deleted dataset cannot be accessed.
23. Logout.
24. Login again.
25. Verify remaining workspace data.

Every step must work.

---

# 92. EDGE CASE ACCEPTANCE TESTS

Test:

### Empty CSV

Expected:
clear validation error.

### Corrupt Excel

Expected:
safe error.

### No numerical columns

Expected:
basic categorical analysis only.

### No date column

Expected:
forecasting unavailable with explanation.

### Huge file

Expected:
size validation or background processing.

### Duplicate data

Expected:
quality warning and cleaning result.

### Missing values

Expected:
quality report.

### AI unavailable

Expected:
analytics dashboard still works.

### Forecasting unavailable

Expected:
dashboard remains functional.

### Unauthorized dataset access

Expected:
403/404.

### Invalid subscription manipulation

Expected:
server rejects request.

---

# 93. FINAL DELIVERABLES

At completion, provide:

1. Complete source code
2. Working frontend
3. Working backend
4. Database schema
5. Database migrations
6. Seed/demo data
7. AI integration
8. Data analysis engine
9. Dashboard
10. Forecasting
11. Anomaly detection
12. PDF report generation
13. Authentication
14. Workspace system
15. Subscription architecture
16. Usage limits
17. Admin panel
18. Tests
19. Docker configuration
20. .env.example
21. README
22. API documentation
23. Deployment instructions

---

# 94. FINAL REPORT FROM THE AGENT

When the implementation is complete, report:

## Completed

List every implemented feature.

## Technology

List actual technologies used.

## Database

List tables.

## API

List major endpoints.

## AI

Explain:

- provider
- models
- prompts
- validation
- cost controls

## Testing

Report:

- tests executed
- results
- remaining known issues

## Deployment

Explain exactly how to run locally and deploy.

## Environment Variables

List required variables without exposing secrets.

## Known Limitations

Be honest.

Do not claim something is production-ready if it has not been tested.

---

# 95. CRITICAL ENGINEERING RULE

Prioritize:

1. Correctness
2. Security
3. Reliability
4. User experience
5. Maintainability
6. Performance
7. Visual polish

Do not sacrifice correctness for visual appearance.

---

# 96. GEMINI AGENT — FINAL EXECUTION SEQUENCE

Start by inspecting:

```text
D:\Downloads\datapilot-ai
```

Also inspect the canonical GitHub repository:

```text
https://github.com/mhmd-ebrahim-1/datapilot-ai.git
```

Do not assume either is empty.

## Mandatory implementation order

### Phase 1 — Repository Assessment

- Verify local project root.
- Inspect existing files.
- Inspect Git status.
- Inspect branches and remote.
- Inspect existing implementation.
- Identify framework/package manager versions.
- Preserve useful work.
- Identify blockers.

### Phase 2 — Foundation

Implement or stabilize:

- frontend
- backend
- database
- environment configuration
- Docker/local development
- shared API contracts

### Phase 3 — Authentication and Workspaces

Implement:

- registration
- login
- logout
- protected routes
- onboarding
- workspace creation
- workspace membership
- roles
- permissions

### Phase 4 — Dataset Pipeline

Implement:

- upload
- validation
- storage
- parsing
- background processing
- dataset preview
- processing status

### Phase 5 — Data Intelligence

Implement:

- profiling
- cleaning
- quality score
- dataset type detection
- KPI engine
- analytics engine

### Phase 6 — Visualization

Implement:

- KPI cards
- charts
- tables
- filters
- responsive dashboard
- loading states
- empty states
- error states

### Phase 7 — AI

Implement:

- AI provider abstraction
- Gemini-compatible provider
- AI insights
- structured output
- validation
- hallucination safeguards
- cost controls

Because this prompt is intended for a Gemini-based agent, make Gemini the first-class supported provider when credentials are available. Use the currently selected/installed Gemini SDK/API correctly rather than assuming an outdated API.

### Phase 8 — AI Data Chat

Implement:

```text
User Question
→ semantic interpretation
→ deterministic analytics/query
→ verified result
→ AI explanation
→ final response
```

Never send the full raw dataset to Gemini.

### Phase 9 — Forecasting

Implement only when the dataset supports meaningful time-series forecasting.

### Phase 10 — Anomaly Detection

Implement statistical anomaly detection and conservative explanations.

### Phase 11 — Reporting

Implement:

- executive summary
- KPI section
- charts
- insights
- recommendations
- methodology
- PDF
- export
- report history

### Phase 12 — SaaS

Implement:

- plan configuration
- usage tracking
- feature gates
- subscription architecture
- billing abstraction

### Phase 13 — Administration

Implement:

- admin dashboard
- users
- workspaces
- subscriptions
- usage
- errors/system health
- audit logs

### Phase 14 — Automation

Implement:

- scheduled reports
- background workers
- notifications
- email abstraction

### Phase 15 — Security Hardening

Review:

- authentication
- authorization
- workspace isolation
- file validation
- rate limiting
- secure storage
- secrets
- CORS
- secure headers
- logging
- deletion

### Phase 16 — Testing

Run:

- unit tests
- integration tests
- end-to-end tests
- frontend build
- backend startup
- lint
- type checking

### Phase 17 — Performance

Verify:

- large-file behavior
- pagination
- background processing
- server-side aggregation
- chart downsampling/aggregation
- database indexes
- caching where appropriate

### Phase 18 — Documentation

Update:

- README
- architecture docs
- API docs
- `.env.example`
- setup instructions
- deployment
- troubleshooting
- demo instructions

### Phase 19 — Local Verification

From:

```text
D:\Downloads\datapilot-ai
```

verify:

```text
git status
git remote -v
git branch --show-current
```

Run the full test/build/startup workflow.

### Phase 20 — GitHub Synchronization

Use:

```text
https://github.com/mhmd-ebrahim-1/datapilot-ai.git
```

Commit and push the completed implementation.

Review staged changes before pushing.

Verify the remote repository after the push.

### Phase 21 — Final Acceptance Test

Verify:

```text
Open application
→ Register
→ Login
→ Create workspace
→ Upload demo_sales.csv
→ Validate
→ Profile
→ Clean
→ Quality score
→ Dataset classification
→ KPI calculation
→ Dashboard
→ AI insights
→ Ask "What was the best-selling product?"
→ Verify answer comes from actual analytics
→ Forecast when supported
→ Detect anomalies
→ Generate PDF
→ Download PDF
→ Open report history
→ Check usage
→ Delete dataset
→ Verify deleted dataset cannot be accessed
→ Logout
→ Login again
→ Verify remaining workspace data
```

Also run the edge-case acceptance tests from this specification.

## Gemini Agent Behavior Rules

### Inspect before editing

Never blindly overwrite an existing repository.

### Implement, don't explain

When tools are available, execute commands and create the actual implementation.

### Verify every major phase

A feature is not complete merely because code exists.

### Prefer existing infrastructure

Avoid unnecessary dependencies and services.

### No fake functionality

Never create fake production analytics, fake AI answers, fake billing state, fake reports, or fake success messages.

### Honest external integrations

When credentials are unavailable:

1. implement the integration abstraction;
2. provide a safe development/mock mode where appropriate;
3. continue with all independent work;
4. document the exact configuration required.

### Data protection

Never commit real customer/user data.

### Secret protection

Never commit API keys, tokens, passwords, private keys, or database credentials.

### Required project root

Always use:

```text
D:\Downloads\datapilot-ai
```

### Required GitHub repository

Always use:

```text
https://github.com/mhmd-ebrahim-1/datapilot-ai.git
```

### No unsupported claims

Only claim successful build/test/deployment/GitHub upload after actual verification.

# BEGIN IMPLEMENTATION.
