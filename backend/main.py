from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mapreduce_twitter import mapreduce_twitter

app = FastAPI()

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/user/{user_id}")
def get_user_stats(user_id: str):
    # Use S3 path - the mapreduce_twitter function will handle it
    file_path = "s3a://sneha-lab1-photo-public/twitter_combined.txt"
    results = mapreduce_twitter(file_path)
    if user_id in results:
        return {
            "user_id": user_id,
            "followers": results[user_id]["followers"],
            "followees": results[user_id]["followees"]
        }
    else:
        return {"error": "User not found"}
