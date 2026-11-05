# LLM SmartRouter Analytics

An interactive analytics dashboard that demonstrates semantic caching, intelligent request routing, and performance evaluation.

## About the Project

LLM SmartRouter Analytics is a Python-based Streamlit application designed to demonstrate how intelligent request management can improve the efficiency of AI-powered applications.

It analyses incoming requests, identifies similar questions using semantic similarity, checks for cache matches, and demonstrates different routing strategies based on request complexity.

## Key Features

- **Semantic Caching:** Identifies similar questions and demonstrates cache reuse.
- **Intelligent Routing:** Classifies requests into different complexity levels.
- **Performance Dashboard:** Visualizes latency, cache hit rate, and request performance.
- **Cost Optimization Analysis:** Demonstrates estimated cost savings using illustrative assumptions.
- **Advanced Analytics:** Interactive charts and performance insights.
- **Request-Level Analytics:** Search, filter, analyse, and export request history.
- **CSV Upload:** Explore datasets through the interactive application.

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Data visualization libraries
- Scikit-learn

## Project Workflow

1. Submit a question or request.
2. Analyse the request complexity.
3. Check for a similar cached request.
4. Reuse a cached response when a match is found.
5. Otherwise, select a routing strategy.
6. Display the response and performance metrics.
7. Analyse request-level and overall performance.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/Chiiradeep/LLM-SmartRouter-Analytics.git
```

Navigate into the project folder:

```bash
cd LLM-SmartRouter-Analytics
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Important Notes

This project is an educational and analytical demonstration. Routing is performed locally, and cost-related metrics use illustrative assumptions rather than actual LLM provider billing. Performance measurements reflect the local execution environment and are not production benchmarks.

## Future Improvements

- Integration with real LLM providers.
- Persistent request history and analytics.
- Advanced routing strategies.
- More comprehensive performance evaluation.

## Author

**Chiiradeep R.**

LLM SmartRouter Analytics – An Interactive AI Request Routing and Performance Analytics Project.
