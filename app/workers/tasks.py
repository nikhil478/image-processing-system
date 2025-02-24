from app.core import SyncSessionLocal
from app.models import ProcessingRequest, ProcessedImage
from .celery import celery
import os
import uuid
import asyncio
from io import BytesIO
from PIL import Image
import aiohttp
import re

STATIC_IMAGE_PATH = "static/images"

async def download_image(url):
    """Download an image from a given URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            return None

def save_image_to_static(image_bytes, filename):
    """Save an image as a static file and return the file path."""
    os.makedirs(STATIC_IMAGE_PATH, exist_ok=True)
    file_path = os.path.join(STATIC_IMAGE_PATH, filename)
    
    with open(file_path, "wb") as f:
        f.write(image_bytes)
    
    return f"/static/images/{filename}"

def sanitize_url(url):
    """Ensure the URL is properly formatted before fetching."""
    url = url.strip().strip('"').strip("'")  # Remove quotes
    if not re.match(r'^https?://', url):
        return None  # Reject invalid URLs
    return url

def process_image(url):
    """Download, compress, and store an image synchronously."""
    url = sanitize_url(url)
    if not url:
        print(f"Skipping invalid URL: {url}")
        return None

    try:
        image_bytes = asyncio.run(download_image(url))  # Convert async to sync
        if not image_bytes:
            return None

        image = Image.open(BytesIO(image_bytes))
        output_io = BytesIO()
        image.save(output_io, format=image.format, quality=50)
        output_filename = f"{uuid.uuid4()}.{image.format.lower()}"
        output_path = save_image_to_static(output_io.getvalue(), output_filename)

        return output_path
    except Exception as e:
        print(f"Error processing image {url}: {e}")
        return None


@celery.task(name="app.workers.tasks.process_csv")
def process_csv(request_id, file_path):
    """Process the uploaded CSV file synchronously for Celery."""
    db: Session = SyncSessionLocal()
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            csv_data = f.read().splitlines()
        
        headers = csv_data[0].split(",")
        
        if len(headers) < 3 or headers[1].strip().lower() != "product name":
            db.query(ProcessingRequest).filter_by(request_id=request_id).update({"status": "FAILED"})
            db.commit()
            return
        
        for row in csv_data[1:]:
            columns = row.split(",")
            serial_number = columns[0].strip()
            product_name = columns[1].strip()
            input_image_urls = [url.strip() for url in columns[2:]]

            output_image_urls = []
            for url in input_image_urls:
                output_url = process_image(url)  # Now it's a synchronous function
                if output_url:
                    output_image_urls.append(output_url)
            
            processed_image = ProcessedImage(
                request_id=request_id,
                serial_number=serial_number,
                product_name=product_name,
                input_images=",".join(input_image_urls),
                output_images=",".join(output_image_urls),
            )
            db.add(processed_image)

        db.query(ProcessingRequest).filter_by(request_id=request_id).update({"status": "COMPLETED"})
        db.commit()

    except Exception as e:
        db.query(ProcessingRequest).filter_by(request_id=request_id).update({"status": "FAILED"})
        db.commit()
        print(f"Error processing CSV: {e}")

    finally:
        db.close()