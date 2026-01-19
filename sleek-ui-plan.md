# Plan: Next-Generation "Sleek" UI for Contrarian Screener

## 1. Executive Summary
The current Streamlit interface is functional but limited in design flexibility and interactivity. To achieve a "sleek," modern, and professional financial terminal experience, we will decouple the application into a **Modern Web Frontend** and a **Robust API Backend**.

This architecture allows for:
- **Pixel-Perfect Design:** Complete control over typography, spacing, and animations.
- **Rich Interactivity:** Instant feedback, smooth transitions, and interactive charts.
- **Scalability:** The backend can serve multiple frontends (web, mobile, CLI) simultaneously.

---

## 2. Technology Stack

### **Frontend (The "Sleek" Part)**
- **Framework:** **Next.js 14+ (React)**
  - *Why?* Industry standard, excellent performance, server-side rendering for SEO/speed.
- **Styling:** **Tailwind CSS**
  - *Why?* Rapid styling, ease of maintenance, dark mode built-in.
- **Component System:** **Shadcn/UI**
  - *Why?* Beautiful, accessible, copy-paste components that look professional out of the box (based on Radix UI).
- **Icons:** **Lucide React** (Clean, consistent SVG icons).
- **Charting:** **Recharts** (Composable React charts) or **Tremor** (Dashboard-specific components).
- **State Management:** **TanStack Query (React Query)**
  - *Why?* Handles caching, loading states, and background refetching seamlessly.

### **Backend (The "Brain")**
- **Framework:** **FastAPI**
  - *Why?* High-performance Python framework. We can reuse 100% of our existing `contrarian` logic (scoring, data fetching) without rewriting it in JavaScript.
  - *Docs:* Automatic Swagger UI documentation.

---

## 3. Visual Language & UX Goals

**Aesthetic:** "Modern Financial Terminal"
- **Dark Mode First:** Deep slate/gray backgrounds, high-contrast text.
- **Typography:** Inter (UI) + JetBrains Mono (Numbers/Tickers).
- **Color Palette:**
  - `Emerald-500` for Bullish/Long signals.
  - `Rose-500` for Bearish/Short signals.
  - `Amber-400` for Contrarian alerts.
- **Interactions:**
  - **Command Palette (Cmd+K):** Instantly jump to any ticker or screen.
  - **Optimistic UI:** Buttons react immediately; data loads in the background with "skeleton" loaders (no jumping layout).
  - **Hover Cards:** Hover over a metric to see its definition or history.

---

## 4. Implementation Phases

### **Phase 1: The API Bridge (Backend)**
*Goal: Expose our existing Python logic as JSON endpoints.*
1. Initialize `backend/` directory with FastAPI.
2. Create endpoints mapping to our core functions:
   - `GET /api/stock/{ticker}` -> Calls `fetch_and_score(ticker)`
   - `GET /api/screen?universe=sp500` -> Calls `batch_screen()`
   - `GET /api/watchlist` -> Reads `watchlist.json`
3. Add CORS middleware to allow the frontend to talk to the backend.

### **Phase 2: Frontend Foundation**
*Goal: Set up the Next.js scaffolding and design system.*
1. Initialize `frontend/` with `create-next-app`.
2. Configure Tailwind and Shadcn/UI.
3. Build the **App Layout**:
   - **Sidebar:** Collapsible navigation (Dashboard, Screen, Watchlist).
   - **Header:** Global search bar (Cmd+K), Theme toggle.
   - **Main Content Area:** Scrollable viewport.

### **Phase 3: Core Features**
*Goal: Rebuild the existing features with the new UI.*

#### **A. The Dashboard (Home)**
- **Top Movers:** Horizontal scroll of cards showing today's highest contrarian scores.
- **Market Pulse:** A grid of mini-charts showing S&P500 vs. Market Sentiment.

#### **B. The Screener (Data Grid)**
- Use **TanStack Table** for a powerful data grid.
- Features: Sortable columns, live filtering (e.g., "Show me Score > 80"), row selection.
- visual: Instead of raw numbers, use colored badges and progress bars inside table cells.

#### **C. Deep Dive (Stock Detail)**
- **Hero Section:** Large Ticker, Price, and a **Radial Gauge** for the Contrarian Score.
- **Tabbed View:**
  - *Overview:* Key metrics cards.
  - *Sentiment:* Bar charts of Analyst vs. Reddit vs. Short Interest.
  - *Fundamentals:* Historical trend lines (Revenue, P/E) using Recharts.

### **Phase 4: Polish & "Sleekness"**
1. **Command Palette:** Implement `cmdk` library for keyboard-first navigation.
2. **Loading States:** Create specific skeleton screens for the dashboard (pulsing gray boxes) while Python fetches data.
3. **Animations:** Use `framer-motion` for smooth page transitions and card entrances.

---

## 5. Folder Structure
```
contrarian-screener/
├── backend/               # Python/FastAPI
│   ├── main.py            # API Routes
│   └── ... (imports from ../contrarian)
├── frontend/              # Next.js/React
│   ├── app/               # Routes
│   ├── components/        # UI Building Blocks (Buttons, Cards)
│   ├── lib/               # API clients
│   └── public/
├── contrarian/            # Existing Shared Logic (Core)
└── ...
```

## 6. Execution Plan
1. **Approve this plan.**
2. I will setup the **FastAPI backend** first to ensure data is ready.
3. I will setup the **Next.js frontend** and connect the first page (Dashboard).
