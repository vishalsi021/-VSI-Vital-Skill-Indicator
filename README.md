# -VSI-Vital-Skill-Indicator
# AI-Powered Job Market Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Frameworks](https://img.shields.io/badge/FastAPI%20%7C%20Streamlit-green?style=for-the-badge)
![Database](https://img.shields.io/badge/SQLite-blueviolet?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)

An intelligent tool designed to monitor real-time job market trends, analyze in-demand skills, and provide actionable recommendations for students and job seekers.

---

## 🚀 The Problem

In a rapidly shifting job market, students and professionals often pursue skills that are becoming outdated. Educational paths don't always align with real-time industry demands. This project aims to bridge that gap using AI to deliver data-driven, personalized career guidance.

## ✨ Key Features

- **Web Scraping:** Automatically collects job postings from major job portals.
- **NLP-Powered Skill Extraction:** Identifies and extracts key technical and soft skills from unstructured job descriptions.
- **Trend Analysis:** Analyzes the frequency of required skills to identify what's currently in demand.
- **Interactive Dashboard:** A user-friendly interface to view trends, search for jobs, and receive recommendations.
- **Course Recommendations:** Suggests relevant online courses to help users upskill effectively.

## 🏛️ System Architecture

The application is built on a simple, robust, and scalable microservice-style architecture.

```
+-----------------+      +--------------------+      +----------------+
|                 |      |                    |      |                |
|  Web Scraper    |----->|  Data Processor    |----->|   SQLite DB    |
| (BeautifulSoup) |      | (Skill Extraction) |      |                |
|                 |      |                    |      |                |
+-----------------+      +--------------------+      +-------+--------+
                                                             |
                                                             |
                                                    +--------v--------+
                                                    |                 |
                                                    |  Backend API    |
                                                    |    (FastAPI)    |
                                                    |                 |
                                                    +--------+--------+
                                                             |
                                                             |
                                                    +--------v--------+
                                                    |                 |
                                                    |  Frontend UI    |
                                                    |   (Streamlit)   |
                                                    |                 |
                                                    +-----------------+
```

## 🛠️ Tech Stack

- **Data Scraping & Analysis:** Python, BeautifulSoup, NLTK, Pandas
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Database:** SQLite

## ⚙️ Getting Started

Follow these instructions to get a local copy of the project up and running.

### Prerequisites

- Python 3.9 or higher
- Git command-line tools

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/ai-job-analyzer.git
    cd ai-job-analyzer
    ```

2.  **Create and activate a virtual environment:**
    *This isolates the project's dependencies from your system-wide Python installation.*
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    *(Note: We will create this `requirements.txt` file together soon).*
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Backend Server:**
    *Navigate to the backend directory (if you create one) and run:*
    ```sh
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

5.  **Run the Frontend Application:**
    *In a new terminal, navigate to the frontend directory and run:*
    ```sh
    streamlit run app.py
    ```
    The application will open in your web browser.

## 👥 The Team

- **Vishal:** Data & AI Specialist
- **Yashashwani:** Backend Developer
- **Vikshitha:** Frontend Developer

## 🗺️ Future Roadmap

- [ ] **Integration with Resume Builder:** Allow users to generate a resume tailored to a specific job posting.
- [ ] **Employer Dashboard:** A portal for companies to analyze which skills are trending in their sector.
- [ ] **SDG Alignment:** Further align project goals with SDG 4: Quality Education by partnering with educational institutions.
- [ ] **Advanced AI:** Implement a RAG (Retrieval-Augmented Generation) model for natural language queries about the job market.

---
