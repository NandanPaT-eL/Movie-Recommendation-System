# Movie-Recommendation-System
A smart and interactive movie recommendation system that suggests movies based on user preferences using Content-Based Filtering and Collaborative Filtering techniques. It also includes a simple GUI interface built with Tkinter for user interaction.

📌 Table of Contents

Introduction
Tech Stack
Recommendation Approaches
Content-Based Filtering
Collaborative Filtering
How to Run
Interface Demo
Project Structure
Future Work
License
🧠 Introduction

This project is a hybrid movie recommendation system built with Python. It leverages machine learning techniques to recommend movies to users by analyzing either movie metadata or collaborative viewing patterns. The system includes:

Content-Based Filtering: Recommends movies similar in genre, keywords, cast, etc.
Collaborative Filtering: Suggests movies based on the ratings of similar users.
A simple GUI interface for user-friendly interaction.
🛠️ Tech Stack

Python 3.x
Pandas, NumPy, scikit-learn
Surprise (for collaborative filtering)
Tkinter (for GUI)
Jupyter Notebooks (for development and prototyping)
🔍 Recommendation Approaches

1. Content-Based Filtering
Utilizes metadata like genre, director, cast, and keywords.
Cosine similarity is calculated between movie vectors created from combined features.
Suggests similar movies to the one a user likes.
Implemented in: /Content based/content_model.ipynb
2. Collaborative Filtering
Based on user-item interactions.
Matrix factorization using the SVD algorithm from the Surprise library.
Recommends movies based on similar users' preferences.
Implemented in: /Colaborative Filtering/collaborative_filtering.ipynb
▶️ How to Run

1. Clone the repository
git clone https://github.com/NandanPaT-eL/Movie-Recommendation-System.git
cd Movie-Recommendation-System
2. Install dependencies
pip install -r requirements.txt
(If requirements.txt is not available, install manually: pandas, numpy, scikit-learn, scipy, surprise, tkinter.)

3. Run Jupyter Notebooks
jupyter notebook
Navigate to:

/Content based/content_model.ipynb for content-based
/Colaborative Filtering/collaborative_filtering.ipynb for collaborative filtering
4. GUI Interface (optional)
cd interface
python main.py
A basic GUI will open where you can type a movie name and get recommendations.

🖼️ Interface Demo

✨ A simple interface using Tkinter that takes a movie name as input and returns the top 10 similar movies.

(Add screenshots if possible)

📂 Project Structure

Movie-Recommendation-System/
│
├── Content based/
│   └── content_model.ipynb
│
├── Colaborative Filtering/
│   └── collaborative_filtering.ipynb
│
├── interface/
│   └── main.py
│
├── .idea/
│
└── README.md
🚀 Future Work

Integrate both models to create a hybrid recommender system
Add user login and personalized watch history
Host on Flask/Django web server
Deploy using Streamlit or Gradio for web-based GUI
📜 License

This project is open-source and available under the MIT License.

Let me know if you want me to add badges (e.g., Python version, license), interactive demo links, or convert it to a PDF version!
