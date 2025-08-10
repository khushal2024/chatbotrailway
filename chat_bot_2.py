# import pandas as pd
# from flask import Flask, jsonify, request
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# import os

# app = Flask(__name__)

# df = None
# model = None
# index = None
# question_embeddings = None

# def load_chatbot_resources():
#     """Loads the dataset, sentence transformer model, and FAISS index."""
#     global df, model, index, question_embeddings

#     # Check if resources are already loaded
#     if df is not None and model is not None and index is not None:
#         print("Chatbot resources already loaded.")
#         return

#     print("Loading chatbot resources...")
#     try:
#         csv_file_path = r"C:\Users\Abbas\OneDrive\Desktop\project_chatbot_1\Rentwee_Chatbot_Faqs_Dataset.csv"
#         if not os.path.exists(csv_file_path):
#             print(f"Error: CSV file not found at {csv_file_path}")
           
#             try:
#                 pass
#             except Exception as e:
#                 print(f"Could not automatically fetch CSV: {e}")
#                 raise FileNotFoundError(f"CSV file '{csv_file_path}' not found. Please ensure it's in the same directory as app.py.")


#         df = pd.read_csv(csv_file_path)

#         # Keep only necessary columns
#         df = df[['Category', 'Question', 'Answer']]

#         # Drop duplicates and rows with missing data
#         df.dropna(subset=["Question", "Answer"], inplace=True)
#         df.drop_duplicates(subset=["Question"], inplace=True)

#         # Optional: clean formatting
#         df['Question'] = df['Question'].str.strip().str.lower()

#         # Load a pre-trained model
#         model = SentenceTransformer('all-MiniLM-L6-v2')

#         # Convert questions to embeddings
#         question_embeddings = model.encode(df['Question'].tolist(), show_progress_bar=False) # No progress bar in API

#         # Convert embeddings to float32 (required by FAISS)
#         question_embeddings = np.array(question_embeddings).astype("float32")

#         # Create a FAISS index
#         index = faiss.IndexFlatL2(question_embeddings.shape[1])  # L2 = Euclidean distance
#         index.add(question_embeddings)
#         print("Chatbot resources loaded successfully!")

#     except Exception as e:
#         print(f"Failed to load chatbot resources: {e}")
#         # Exit or handle error appropriately if resources can't be loaded
#         exit(1) # Exit if essential resources cannot be loaded

# # Call this function once when the Flask app starts
# with app.app_context():
#     load_chatbot_resources()

# def search_question(user_query, top_k=1):
#     """
#     Searches the FAISS index for the most relevant question and returns its answer.
#     """
#     if model is None or index is None or df is None:
#         raise RuntimeError("Chatbot resources not loaded. Cannot perform search.")

#     user_query_clean = user_query.strip().lower()
#     query_embedding = model.encode([user_query_clean]).astype("float32")

#     distances, indices = index.search(query_embedding, top_k)
    
#     results = []
#     for i in range(top_k):
#         idx = indices[0][i]
#         results.append({
#             "matched_question": df.iloc[idx]['Question'],
#             "answer": df.iloc[idx]['Answer'],
#             "category": df.iloc[idx]['Category'],
#             "score": float(distances[0][i])
#         })
#     return results

# # --- Flask API Endpoints ---

# @app.route('/')
# def home():
#     """Simple home endpoint to confirm the API is running."""
#     return "Rentwee Chatbot API is running!"

# @app.route('/ask', methods=['POST'])
# def ask_chatbot():
#     """
#     API endpoint to receive user queries and return chatbot responses.
#     Expects a JSON payload like: {"query": "What is Rentwee?"}
#     Returns a JSON payload like: {"answer": "...", "category": "..."}
#     """
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     user_input = request.json.get('query')
#     if not user_input:
#         return jsonify({"error": "No 'query' field found in JSON payload"}), 400

#     try:
#         results = search_question(user_input, top_k=1)
#         if not results:
#             return jsonify({"answer": "I'm sorry, I couldn't find an answer to that question.", "category": "No Match"}), 200
        
#         best_match = results[0]
#         return jsonify({
#             "answer": best_match['answer'],
#             "category": best_match['category']
#         }), 200
#     except RuntimeError as e:
#         return jsonify({"error": str(e)}), 500
#     except Exception as e:
#         return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# if __name__ == '__main__':
   
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load your dataset
df = pd.read_csv("Rentwee_Chatbot_Faqs_Dataset.csv")

# Example route
@app.route("/")
def home():
    return {"message": "Chatbot is live on Railway!"}

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    # TODO: integrate your bot logic here
    reply = f"You said: {user_input}"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
