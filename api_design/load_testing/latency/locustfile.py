import os
import base64
from dotenv import load_dotenv
from locust import HttpUser, task, between

# Load the ENV variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
print(API_KEY)

# Load a sample image into a memory once
image_path = "./assets/product_image.png"
with open(image_path, "rb") as f:
    IMAGE_BYTES = f.read()


class ImageDetectionUser(HttpUser):
    wait_time = between(1, 3)   # seconds between tasks

    def on_start(self):
        # Set default headers for authentication
        self.client.headers = {"Authorization": f"Bearer {API_KEY}"}

    @task(3)
    def predict_image(self):
        """Test the /predict endpoint with an image upload"""

        files = {
            "file": ("test_image.jpg", IMAGE_BYTES, "image/jpeg")
        }
        self.client.post("/predict", files=files)


    @task(1) 
    def predict_image_url(self):
        """Test the /predict/url endpoint with an image URL"""

        data = {"image_url": "https://images.pexels.com/photos/3801990/pexels-photo-3801990.jpeg"}
        self.client.post("/predict/url", data=data)   # form based submission
        # self.client.post("/predict/url", json=data)     # string based submission

    @task(1)
    def health_check(self):
        """Test the /health endpoint"""
        self.client.get("/health")

        