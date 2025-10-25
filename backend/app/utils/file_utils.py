import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app.core.config import settings

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

def generate_timestamped_filename(original_filename: str) -> str:
    """Generate a filename with timestamp prefix."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = secure_filename(original_filename)
    name, ext = os.path.splitext(safe_filename)
    return f"{timestamp}_{name}{ext}"

def create_processed_filename(base_name: str, timestamp: str, extension: str = '.xlsx') -> str:
    """Create processed filename with timestamp for uploads folder."""
    return f"{timestamp}_{base_name}_processed{extension}"
