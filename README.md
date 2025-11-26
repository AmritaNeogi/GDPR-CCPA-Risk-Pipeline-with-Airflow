
# Automated Data Pipeline & Predictive Analytics Platform: Regulatory Data Standards & Reporting (daily ingestion)
Global Regulatory Insights & Risk Prioritization; Automated policy-risk forecasting & prioritization for GDPR/CCPA


## Overview <br>

<div class="image-container"><img src="/pictures/Overview.png" alt="Project Image"> </div>

## Pipeline <br>

<div class="image-container"><img src="/pictures/pipeline.png" alt="Project Image"> </div>


## Risk Pipeline Architecture (with Severity Modeling)
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


