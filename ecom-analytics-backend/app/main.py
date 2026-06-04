from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime

from . import models, schemas, database
from .services.data_processor import DataProcessor
from .services.analytics import AnalyticsService

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="E-commerce Analytics API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce Analytics API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload", response_model=Dict[str, str])
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV.")

    try:
        content = await file.read()
        processed_data = DataProcessor.process_csv(content)

        # Insert into DB
        # For simplicity in this demo, we clear old data or just append
        # models.Sale.clear_all(db) # Hypothetical

        # Clear existing data for demo purposes (optional, depends on requirements)
        db.query(models.Sale).delete()

        for item in processed_data:
            db_sale = models.Sale(**item)
            db.add(db_sale)

        db.commit()
        return {"message": f"Successfully processed {len(processed_data)} records"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_analytics_service(db: Session = Depends(database.get_db)):
    sales = db.query(models.Sale).all()
    # If no data, use sample data for demo
    if not sales:
        data = DataProcessor.get_sample_data()
    else:
        # Convert SQLAlchemy models to dicts
        data = [schemas.Sale.from_orm(s).dict() for s in sales]

    return AnalyticsService(data)

@app.get("/kpis", response_model=schemas.KPIResponse)
async def get_kpis(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    region: Optional[str] = None,
    segment: Optional[str] = None,
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    return analytics.filter_data(start_date, end_date, category, region, segment).get_kpis()

@app.get("/sales-trends", response_model=List[schemas.SalesTrend])
async def get_sales_trends(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    region: Optional[str] = None,
    segment: Optional[str] = None,
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    return analytics.filter_data(start_date, end_date, category, region, segment).get_sales_trends()

@app.get("/product-performance", response_model=List[schemas.ProductPerformance])
async def get_product_performance(
    category: Optional[str] = None,
    region: Optional[str] = None,
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    return analytics.filter_data(category=category, region=region).get_product_performance()

@app.get("/customer-insights", response_model=schemas.CustomerInsights)
async def get_customer_insights(
    region: Optional[str] = None,
    segment: Optional[str] = None,
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    return analytics.filter_data(region=region, segment=segment).get_customer_insights()
