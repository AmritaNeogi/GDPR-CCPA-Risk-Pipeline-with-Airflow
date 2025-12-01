
# Global Regulatory Insights & Risk Prioritization: 
###  Automated policy-risk forecasting & prioritization for GDPR/CCPA

## Overview <br>

<div class="image-container"><img src="/pictures/pipeline.png" alt="Project Image"> </div>

## 📊 Interactive GDPR–CCPA Regulatory Risk Dashboard

🔗 **View the live interactive dashboard:**  
https://public.tableau.com/views/GDPRDashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&publish=yes&showOnboarding=true&:display_count=n&:origin=viz_share_link

This dashboard includes:
- Time-series severity forecasting  
- Monthly policy volumes  
- Severity breakdown across topics  
- High-severity topics  
- Topic–severity heatmap  

## Architecture (with Severity Modeling) <br>
                        ┌─────────────────────────────────────────┐
                        │        Airflow Orchestration DAG        │
                        │    (gdpr_ccpa_risk_pipeline.py)         │
                        └─────────────────────────────────────────┘
                                       │           │
                                 Schedules & Dependencies
                                       │           │
                                       ▼           ▼
       ┌────────────────────────────────────────────────────────────────────────┐
       │                           DATA INGESTION LAYER                         │
       └────────────────────────────────────────────────────────────────────────┘

                          ┌───────────────────────────────┐
                          │  fetch_policy_data.py         │
                          │  • Scrapes EDPB/CCPA news     │
                          │  • Saves raw JSON             │
                          └───────────────────────────────┘
                                          │
                                          ▼
                          ┌───────────────────────────────┐
                          │  Raw Data (data/raw/)         │
                          └───────────────────────────────┘


       ┌────────────────────────────────────────────────────────────────────────┐
       │                       DATA PROCESSING & CLEANING                       │
       └────────────────────────────────────────────────────────────────────────┘
      
                          ┌───────────────────────────────┐
                          │  process_policy_data.py       │
                          │  • Cleans text                │
                          │  • Standardizes fields        │
                          │  • Outputs CSV                │
                          └───────────────────────────────┘
                                          │
                                          ▼
                          ┌───────────────────────────────┐
                          │ Cleaned Data (data/processed/)│
                          └───────────────────────────────┘

  
         ┌────────────────────────────────────────────────────────────────────────┐
         │                          SEVERITY MODELING MODULE                      │
         └────────────────────────────────────────────────────────────────────────┘
                                            │
                       Manual/Offline Step (Jupyter ML notebooks)
                                            │
                                            ▼
             ┌────────────────────────────────────────────────────────────────────┐
             │      Policy Severity Notebooks (ML Classification Options)         │
             │--------------------------------------------------------------------│
             │ 1. Zero-Shot Classification (BART MNLI)                            │
             │    • No training required                                          │
             │    • Predicts LOW / MEDIUM / HIGH / CRITICAL                       │
             │                                                                    │
             │ 2. T5 Fine-Tuning                                                  │
             │    • Custom model trained on labeled examples                      │
             │    • Higher accuracy, domain-tuned                                 │
             │                                                                    │
             │ (Optional, removed) OpenAI-based Classification                    │
             └────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                              ┌───────────────────────────────┐
                              │ severity_enriched_policies.csv│
                              │  (cleaned + severity column)  │
                              └───────────────────────────────┘


           ┌────────────────────────────────────────────────────────────────────────┐
           │                   TEMPORAL & THEMATIC FORECASTING MODULE               │
           └────────────────────────────────────────────────────────────────────────┘
          
                                              │
                                              ▼
                              ┌───────────────────────────────┐
                              │  forecast_policy_trends.py    │
                              │  • CmdStanPy/Prophet models   │
                              │  • Predicts policy volume     │
                              │  • Identifies trends/topics   │
                              └───────────────────────────────┘
                                              │
                                              ▼
                              ┌───────────────────────────────┐
                              │ Forecast Outputs              │
                              │   (data/forecasts/)           │
                              └───────────────────────────────┘


             ┌────────────────────────────────────────────────────────────────────────┐
             │                          VALIDATION & QA                               │
             └────────────────────────────────────────────────────────────────────────┘
                    
                                              │
                                              ▼
                              ┌───────────────────────────────┐
                              │ validate_forecast.ipynb       │
                              │  • Visual QA of outputs       │
                              │  • Confidence interval checks │
                              │  • Sanity checks before use   │
                              └───────────────────────────────┘


          
           ┌────────────────────────────────────────────────────────────────────────┐
           │                         OUTPUT / ANALYTICS LAYER                       │
           └────────────────────────────────────────────────────────────────────────┘
                                              │ 
                                              ▼           
                                ┌─────────────────────────────┐
                                │    Dashboards               │
                                │   • Severity distribution   │
                                │   • Regulatory trends       │
                                │   • Forecasting plots       │
                                └─────────────────────────────┘


