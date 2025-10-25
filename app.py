# Description: This script is the main Flask application that serves the web interface for the data processing scripts.
import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from urllib.parse import unquote, quote
import discord
import requests
from dotenv import load_dotenv
from datetime import datetime

# Import the scripts for processing the data
import scripts.Unictron as Unictron
import scripts.Unictron_2 as Unictron_2
import scripts.DTJ_H as DTJ_H
import scripts.YONG_LAING as YONG_LAING
import scripts.YONG_LAING_desc as YONG_LAING_desc
import scripts.VLI as VLI
import scripts.ASECL as ASECL
app = Flask(__name__)

# Configure upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'xlsm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the Discord env from the environment
load_dotenv()
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL', None)
discord_token = os.getenv('DISCORD_TOKEN', None)
try: discord_guild_id = int(os.environ['DISCORD_GUILD_ID'])
except: discord_guild_id = None
try: discord_channel_id = int(os.environ['DISCORD_CHANNEL_ID'])
except: discord_channel_id = None

# Send a message to Discord via webhook
def dc_send_webhook(message, webhook_url):
    """Send message to Discord using webhook URL."""
    try:
        payload = {
            "content": message
        }
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Message sent successfully via webhook")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message via webhook: {e}")
        return False

# Send a message to a Discord channel
def dc_send(message, token, guild_id, channel_id):
    # Set up Discord client with default intents
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Print login information
        print(f'We have logged in as {client.user}')
        # Get the guild (server) by ID
        guild = discord.utils.get(client.guilds, id=guild_id)
        if guild is None:
            print(f'Guild with ID {guild_id} not found')
            await client.close()
            return

        # Get the channel by ID
        channel = discord.utils.get(guild.channels, id=channel_id)
        if channel is None:
            print(f'Channel with ID {channel_id} not found in guild {guild_id}')
            await client.close()
            return

        # Send the message to the channel
        await channel.send(message)
        # Close the client after sending the message
        await client.close()

    # Run the Discord client with the provided token
    client.run(token)

# Send message to Discord - prefer webhook if available, fallback to bot
def send_discord_message(message):
    """Send message to Discord using webhook if available, otherwise use bot."""
    if discord_webhook_url:
        success = dc_send_webhook(message, discord_webhook_url)
        if success:
            return
    
    # Fallback to bot if webhook fails or is not configured
    if discord_token and discord_guild_id and discord_channel_id:
        dc_send(message, discord_token, discord_guild_id, discord_channel_id)


def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_timestamped_filename(original_filename):
    """Generate a filename with timestamp prefix."""
    # Get current timestamp in format: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sanitize the original filename
    safe_filename = secure_filename(original_filename)
    
    # Split filename and extension
    name, ext = os.path.splitext(safe_filename)
    
    # Return timestamped filename
    return f"{timestamp}_{name}{ext}"


def validate_file_upload(request):
    """Validate file upload request and return error message if any."""
    if 'file' not in request.files:
        return "No file part in the request."
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected."
    
    if not allowed_file(file.filename):
        return "File type not allowed."
    
    return None


def save_uploaded_file(file, filename, timestamp):
    """Save uploaded file with timestamped filename."""
    timestamped_filename = f"{timestamp}_{secure_filename(filename)}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], timestamped_filename)
    file.save(filepath)
    return filepath, timestamped_filename


def process_excel_file(filepath, filename, processor_module):
    """Process Excel file with the given processor module."""
    if filename.lower().endswith('.xls'):
        xlsx_filename = os.path.splitext(filepath)[0] + '.xlsx'
        if processor_module.convert_xls_to_xlsx(filepath, xlsx_filename):
            processor_module.organize_data(xlsx_filename)
    else:
        processor_module.organize_data(filepath)


def create_processed_filename(base_name, timestamp, extension='.xlsx'):
    """Create processed filename with timestamp for uploads folder."""
    return f"{timestamp}_{base_name}_processed{extension}"


def handle_file_processing_error(error, filename, processor_name):
    """Handle processing errors and send Discord notification if configured."""
    message = f"An error occurred during processing: {error}"
    if discord_webhook_url or (discord_token and discord_guild_id and discord_channel_id):
        send_discord_message(f"[{processor_name}] {filename}\n{message}")
    return message


def process_upload_request(request, processor_module, processor_name, template_name, output_extension='.xlsx'):
    """Generic function to handle file upload and processing."""
    message = None
    if request.method == 'POST':
        # Validate file upload
        error_message = validate_file_upload(request)
        if error_message:
            return render_template(template_name, message=error_message)

        file = request.files['file']
        filename = unquote(file.filename)

        try:
            # Generate timestamp once for this upload session
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Save uploaded file
            filepath, timestamped_filename = save_uploaded_file(file, filename, timestamp)

            # Process the file
            if processor_name == 'YONG_LAING_desc':
                # Special handling for YONG_LAING_desc (outputs .txt)
                txt_filename = os.path.splitext(filepath)[0] + '.txt'
                processor_module.read_xlsx_and_output_txt(filepath, txt_filename)
                
                base_name, _ = os.path.splitext(filename)
                processed_filename_uploads = create_processed_filename(base_name, timestamp, '.txt')
                processed_filename_download = f"{base_name}_processed.txt"
                
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename_uploads)
                os.rename(txt_filename, processed_filepath)
            else:
                # Standard Excel processing
                process_excel_file(filepath, filename, processor_module)
                
                base_name, _ = os.path.splitext(filename)
                processed_filename_uploads = create_processed_filename(base_name, timestamp, output_extension)
                processed_filename_download = f"{base_name}_processed{output_extension}"
                
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename_uploads)
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

            # Redirect to download
            return redirect(url_for('download_file', name=processed_filename_uploads, download_name=processed_filename_download))

        except Exception as e:
            message = handle_file_processing_error(e, filename, processor_name)

    return render_template(template_name, message=message)


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')


@app.route('/Unictron', methods=['GET', 'POST'])
def upload_file_unictron():
    """Handles file upload and processing for Unictron."""
    return process_upload_request(request, Unictron, 'Unictron', 'Unictron.html')


@app.route('/Unictron_2', methods=['GET', 'POST'])
def upload_file_unictron_2():
    """Handles file upload and processing for Unictron_2."""
    return process_upload_request(request, Unictron_2, 'Unictron_2', 'Unictron_2.html')


@app.route('/DTJ_H', methods=['GET', 'POST'])
def upload_file_dtj_h():
    """Handles file upload and processing for DTJ_H."""
    return process_upload_request(request, DTJ_H, 'DTJ_H', 'DTJ_H.html')


@app.route('/YONG_LAING', methods=['GET', 'POST'])
def upload_file_yong_laing():
    """Handles file upload and processing for YONG_LAING."""
    return process_upload_request(request, YONG_LAING, 'YONG_LAING', 'YONG_LAING.html')


@app.route('/YONG_LAING_desc', methods=['GET', 'POST'])
def upload_file_yong_laing_desc():
    """Handles file upload and processing for YONG_LAING_desc."""
    return process_upload_request(request, YONG_LAING_desc, 'YONG_LAING_desc', 'YONG_LAING_desc.html', '.txt')


@app.route('/VLI', methods=['GET', 'POST'])
def upload_file_vli():
    """Handles file upload and processing for VLI."""
    return process_upload_request(request, VLI, 'VLI', 'VLI.html')


@app.route('/ASECL', methods=['GET', 'POST'])
def upload_file_asecl():
    """Handles file upload and processing for ASECL."""
    return process_upload_request(request, ASECL, 'ASECL', 'ASECL.html')


@app.route(f'/{UPLOAD_FOLDER}/<name>')
def download_file(name):
    """Sends the processed file to the user for download."""
    download_name = request.args.get('download_name', name)
    return send_from_directory(app.config["UPLOAD_FOLDER"], unquote(name), as_attachment=True, download_name=download_name)


if __name__ == '__main__':
    app.run(debug=True)