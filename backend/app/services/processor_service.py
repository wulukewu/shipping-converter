import os
from datetime import datetime
from fastapi import UploadFile, HTTPException
from werkzeug.utils import secure_filename
from app.core.config import settings
from app.utils.file_utils import allowed_file, generate_timestamped_filename, create_processed_filename
from app.utils.discord_utils import send_discord_message

# Import processor modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from scripts import Unictron, Unictron_2, DTJ_H, YONG_LAING, YONG_LAING_desc, VLI, ASECL

PROCESSORS = {
    "unictron": {"module": Unictron, "name": "Unictron", "extension": ".xlsx"},
    "unictron_2": {"module": Unictron_2, "name": "Unictron_2", "extension": ".xlsx"},
    "dtj_h": {"module": DTJ_H, "name": "DTJ_H", "extension": ".xlsx"},
    "yong_laing": {"module": YONG_LAING, "name": "YONG_LAING", "extension": ".xlsx"},
    "yong_laing_desc": {"module": YONG_LAING_desc, "name": "YONG_LAING_desc", "extension": ".txt"},
    "vli": {"module": VLI, "name": "VLI", "extension": ".xlsx"},
    "asecl": {"module": ASECL, "name": "ASECL", "extension": ".xlsx"},
}

async def process_file(file: UploadFile, processor_type: str) -> dict:
    """Process uploaded file with specified processor."""
    
    # Validate processor type
    if processor_type not in PROCESSORS:
        raise HTTPException(status_code=400, detail="Invalid processor type")
    
    processor_config = PROCESSORS[processor_type]
    processor_module = processor_config["module"]
    processor_name = processor_config["name"]
    output_extension = processor_config["extension"]
    
    # Validate file
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    try:
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save uploaded file
        safe_filename = secure_filename(file.filename)
        timestamped_filename = f"{timestamp}_{safe_filename}"
        filepath = os.path.join(settings.UPLOAD_FOLDER, timestamped_filename)
        
        with open(filepath, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the file
        base_name, _ = os.path.splitext(file.filename)
        
        if processor_type == "yong_laing_desc":
            # Special handling for YONG_LAING_desc (outputs .txt)
            txt_filename = os.path.splitext(filepath)[0] + '.txt'
            processor_module.read_xlsx_and_output_txt(filepath, txt_filename)
            
            processed_filename = create_processed_filename(base_name, timestamp, '.txt')
            processed_filepath = os.path.join(settings.UPLOAD_FOLDER, processed_filename)
            os.rename(txt_filename, processed_filepath)
        else:
            # Standard Excel processing
            if file.filename.lower().endswith('.xls'):
                xlsx_filename = os.path.splitext(filepath)[0] + '.xlsx'
                if processor_module.convert_xls_to_xlsx(filepath, xlsx_filename):
                    processor_module.organize_data(xlsx_filename)
            else:
                processor_module.organize_data(filepath)
            
            processed_filename = create_processed_filename(base_name, timestamp, output_extension)
            processed_filepath = os.path.join(settings.UPLOAD_FOLDER, processed_filename)
            os.rename(os.path.join(settings.UPLOAD_FOLDER, "Organized_Data.xlsx"), processed_filepath)
        
        return {
            "success": True,
            "message": "File processed successfully",
            "filename": processed_filename,
            "download_url": f"/api/download/{processed_filename}"
        }
        
    except Exception as e:
        error_message = f"An error occurred during processing: {str(e)}"
        
        # Send Discord notification
        if settings.DISCORD_WEBHOOK_URL or (settings.DISCORD_TOKEN and settings.DISCORD_GUILD_ID and settings.DISCORD_CHANNEL_ID):
            send_discord_message(f"[{processor_name}] {file.filename}\n{error_message}")
        
        raise HTTPException(status_code=500, detail=error_message)
