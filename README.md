# E-commerce Analytics Platform

An end-to-end analytics platform for e-commerce, providing insights into sales, customer behavior, and inventory management.

## Project Structure

- `ecom-analytics-frontend`: Next.js 16.2 web application.
- `ecom-analytics-backend`: FastAPI Python backend service.

## Tech Stack

### Frontend
- **Framework:** Next.js 16.2 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS (default in create-next-app)
- **State Management:** React Hooks / Context API

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.12+
- **API Documentation:** Swagger UI (automatic)

## Features (Planned)
- Real-time sales dashboard
- Customer segmentation analytics
- Inventory tracking and alerts
- Revenue forecasting

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.12+

### Running the Frontend
1. Navigate to the frontend directory:
   ```bash
   cd ecom-analytics-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### Running the Backend
1. Navigate to the backend directory:
   ```bash
   cd ecom-analytics-backend
   ```
2. (Recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```
