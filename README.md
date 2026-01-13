# PadhAI Dost 🤖📚

**Your AI-Powered Study Companion**

> PadhAI Dost (Scholar Friend) is an intelligent learning assistant that helps students study smarter, not harder. By combining RAG (Retrieval Augmented Generation) with intuitive study cards, it transforms static documents into interactive learning experiences.

[![Live Demo](https://img.shields.io/badge/Live-Demo-2ea44f?style=for-the-badge&logo=vercel)](https://your-demo-link.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

## 🚀 Key Features

*   **📚 Auto-Flashcards**: Upload any PDF/Text and instantly generate flashcards with key concepts.
*   **🧠 Intelligent Chat**: Ask questions about your documents and get answers cited from the source.
*   **📊 Study Analytics (Coming Soon)**: Track your learning progress, streaks, and mastery levels.
*   **🔄 Hybrid Search RAG**: Combines semantic vector search with keyword matching for high-precision answers.
*   **🎨 Minimalist UI**: Distraction-free interface designed for deep work, inspired by Notion.

---

## 🛠️ Tech Stack

*   **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Shadcn UI
*   **Backend**: Python (FastAPI), LangChain
*   **AI/ML**: OpenAI (GPT-4o), Google Gemini Pro
*   **Database**: PostgreSQL (Neon), ChromaDB (Vector Store)
*   **Deployment**: Vercel (Frontend), Railway/Render (Backend)

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User] -->|Uploads PDF| Frontend[Next.js Frontend]
    User -->|Asks Question| Frontend
    
    subgraph "Backend Infrastructure"
        Frontend -->|API Request| Backend[FastAPI Backend]
        Backend -->|Process Text| Chunker[Text Splitter]
        Chunker -->|Embed| EmbedModel[Embedding Model]
        EmbedModel -->|Store| VectorDB[(ChromaDB)]
        
        Backend -->|Query| LLM[LLM (OpenAI/Gemini)]
        VectorDB -->|Retrieve| LLM
    end
    
    LLM -->|Answer/Flashcards| Backend
    Backend -->|Response| Frontend
```

---

## ⚡ Getting Started

### Prerequisites
*   Node.js 18+
*   Python 3.10+
*   Docker (Optional)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/padhai-dost-v2.git
    cd padhai-dost-v2
    ```

2.  **Frontend Setup**
    ```bash
    npm install
    npm run dev
    ```

3.  **Backend Setup**
    ```bash
    cd python-backend
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn api:app --reload
    ```

4.  **Environment Variables**
    Create a `.env` file in the root:
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    OPENAI_API_KEY=your_key_here
    DATABASE_URL=your_postgres_url
    ```

---

## 📸 Screenshots

| Dashboard | Study Mode |
|:---:|:---:|
| ![Dashboard Placeholder](http://placehold.it/600x400) | ![Study Mode Placeholder](http://placehold.it/600x400) |

---

## 🤝 Contributing

Contributions are always welcome! Please see `CONTRIBUTING.md` for details.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📬 Contact

**Abhi Bhardwaj** - [LinkedIn](https://linkedin.com/in/abhi-bhardwaj) - abhi@example.com

Project Link: [https://github.com/AB0204/PadhAI-Dost](https://github.com/AB0204/PadhAI-Dost)
