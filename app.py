# Description: This script is the main Flask application that serves the web interface for the data processing scripts.
import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from urllib.parse import unquote, quote
import discord
from dotenv import load_dotenv

# Import the scripts for processing the data
import scripts.Unictron as Unictron
import scripts.DTJ_H as DTJ_H
import scripts.YONG_LAING as YONG_LAING
import scripts.YONG_LAING_desc as YONG_LAING_desc
import scripts.VLI as VLI

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
discord_token = os.getenv('DISCORD_TOKEN', None)
try: discord_guild_id = int(os.environ['DISCORD_GUILD_ID'])
except: discord_guild_id = None
try: discord_channel_id = int(os.environ['DISCORD_CHANNEL_ID'])
except: discord_channel_id = None

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


def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')


@app.route('/Unictron', methods=['GET', 'POST'])
def upload_file_unictron():
    """Handles file upload and processing for Unictron."""
    message = None
    if request.method == 'POST':
        # Check if a file was included in the request
        if 'file' not in request.files:
            message = "No file part in the request."
            return render_template('Unictron.html', message=message)

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            message = "No file selected."
            return render_template('Unictron.html', message=message)

        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            try:
                # Unquote the filename to handle URL-encoded characters
                filename = unquote(file.filename)

                # Sanitize the filename using secure_filename
                safe_filename = secure_filename(filename)

                # Construct the full file path for saving
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

                # Save the uploaded file
                file.save(filepath)

                # Convert xls to xlsx if needed
                if filename.lower().endswith('.xls'):
                    xlsx_filename = os.path.splitext(filepath)[0] + '.xlsx'
                    if Unictron.convert_xls_to_xlsx(filepath, xlsx_filename):
                        Unictron.organize_data(xlsx_filename)
                else:
                    Unictron.organize_data(filepath)

                # Extract the base name and extension from the original filename
                base_name, extension = os.path.splitext(filename)

                # Construct the processed filename
                processed_filename = f"{base_name} (processed){extension}"

                # Construct the processed filepath
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

                # Rename the processed file
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

                # Redirect to download the processed file
                return redirect(url_for('download_file', name=quote(processed_filename)))

            except Exception as e:
                message = f"An error occurred during processing: {e}"
                if discord_token and discord_guild_id and discord_channel_id:
                    dc_send(f"[Unictron] {filename}\n{message}", discord_token, discord_guild_id, discord_channel_id)

    # Render the upload page with the message if available
    return render_template('Unictron.html', message=message)


@app.route('/DTJ_H', methods=['GET', 'POST'])
def upload_file_dtj_h():
    """Handles file upload and processing for DTJ_H."""
    message = None
    if request.method == 'POST':
        # Check if a file was included in the request
        if 'file' not in request.files:
            message = "No file part in the request."
            return render_template('DTJ_H.html', message=message)

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            message = "No file selected."
            return render_template('DTJ_H.html', message=message)

        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            try:
                # Unquote the filename to handle URL-encoded characters
                filename = unquote(file.filename)

                # Sanitize the filename using secure_filename
                safe_filename = secure_filename(filename)

                # Construct the full file path for saving
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

                # Save the uploaded file
                file.save(filepath)

                # Convert xls to xlsx if needed
                if filename.lower().endswith('.xls'):
                    xlsx_filename = os.path.splitext(filepath)[0] + '.xlsx'
                    if DTJ_H.convert_xls_to_xlsx(filepath, xlsx_filename):
                        DTJ_H.organize_data(xlsx_filename)
                else:
                    DTJ_H.organize_data(filepath)

                # Extract the base name and extension from the original filename
                base_name, extension = os.path.splitext(filename)

                # Construct the processed filename
                processed_filename = f"{base_name} (processed).xlsx"

                # Construct the processed filepath
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

                # Rename the processed file
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

                # Redirect to download the processed file
                return redirect(url_for('download_file', name=quote(processed_filename)))

            except Exception as e:
                message = f"An error occurred during processing: {e}"
                if discord_token and discord_guild_id and discord_channel_id:
                    dc_send(f"[DTJ_H] {filename}\n{message}", discord_token, discord_guild_id, discord_channel_id)

    # Render the upload page with the message if available
    return render_template('DTJ_H.html', message=message)


@app.route('/YONG_LAING', methods=['GET', 'POST'])
def upload_file_yong_laing():
    """Handles file upload and processing for YONG_LAING."""
    message = None
    if request.method == 'POST':
        # Check if a file was included in the request
        if 'file' not in request.files:
            message = "No file part in the request."
            return render_template('YONG_LAING.html', message=message)

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            message = "No file selected."
            return render_template('YONG_LAING.html', message=message)

        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            try:
                # Unquote the filename to handle URL-encoded characters
                filename = unquote(file.filename)

                # Sanitize the filename using secure_filename
                safe_filename = secure_filename(filename)

                # Construct the full file path for saving
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

                # Save the uploaded file
                file.save(filepath)

                # Convert xls to xlsx if needed
                if filename.lower().endswith('.xls'):
                    xlsx_filename = os.path.splitext(filepath)[0] + '.xlsx'
                    if YONG_LAING.convert_xls_to_xlsx(filepath, xlsx_filename):
                        YONG_LAING.organize_data(xlsx_filename)
                else:
                    YONG_LAING.organize_data(filepath)

                # Extract the base name and extension from the original filename
                base_name, extension = os.path.splitext(filename)

                # Construct the processed filename
                processed_filename = f"{base_name} (processed){extension}"

                # Construct the processed filepath
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

                # Rename the processed file
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

                # Redirect to download the processed file
                return redirect(url_for('download_file', name=quote(processed_filename)))

            except Exception as e:
                message = f"An error occurred during processing: {e}"
                if discord_token and discord_guild_id and discord_channel_id:
                    dc_send(f"[YONG_LAING] {filename}\n{message}", discord_token, discord_guild_id, discord_channel_id)

    # Render the upload page with the message if available
    return render_template('YONG_LAING.html', message=message)


@app.route('/YONG_LAING_desc', methods=['GET', 'POST'])
def upload_file_yong_laing_desc():
    """Handles file upload and processing for YONG_LAING_desc."""
    message = None
    if request.method == 'POST':
        # Check if a file was included in the request
        if 'file' not in request.files:
            message = "No file part in the request."
            return render_template('YONG_LAING_desc.html', message=message)

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            message = "No file selected."
            return render_template('YONG_LAING_desc.html', message=message)

        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            try:
                # Unquote the filename to handle URL-encoded characters
                filename = unquote(file.filename)

                # Sanitize the filename using secure_filename
                safe_filename = secure_filename(filename)

                # Construct the full file path for saving
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

                # Save the uploaded file
                file.save(filepath)

                # Construct the output txt filename for the processing
                txt_filename = os.path.splitext(filepath)[0] + '.txt'

                # Process the data from the file
                YONG_LAING_desc.read_xlsx_and_output_txt(filepath, txt_filename)

                # Extract the base name and extension from the original filename
                base_name, extension = os.path.splitext(filename)

                # Construct the processed filename
                processed_filename = f"{base_name} (processed).txt"

                # Construct the processed filepath
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

                # Rename the file
                os.rename(txt_filename, processed_filepath)

                # Redirect to download the processed file
                return redirect(url_for('download_file', name=quote(processed_filename)))

            except Exception as e:
                message = f"An error occurred during processing: {e}"
                if discord_token and discord_guild_id and discord_channel_id:
                    dc_send(f"[YONG_LAING_desc] {filename}\n{message}", discord_token, discord_guild_id, discord_channel_id)

    # Render the upload page with the message if available
    return render_template('YONG_LAING_desc.html', message=message)


@app.route('/VLI', methods=['GET', 'POST'])
def upload_file_vli():
    """Handles file upload and processing for VLI."""
    message = None
    if request.method == 'POST':
        # Check if a file was included in the request
        if 'file' not in request.files:
            message = "No file part in the request."
            return render_template('VLI.html', message=message)

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            message = "No file selected."
            return render_template('VLI.html', message=message)

        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            try:
                # Unquote the filename to handle URL-encoded characters
                filename = unquote(file.filename)

                # Sanitize the filename using secure_filename
                safe_filename = secure_filename(filename)

                # Construct the full file path for saving
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

                # Save the uploaded file
                file.save(filepath)

                # Convert xls to xlsx if needed
                if filename.lower().endswith('.xls'):
                    xlsx_filename = os.path.splitext(filepath)[0] + '.xlsx'
                    if VLI.convert_xls_to_xlsx(filepath, xlsx_filename):
                        VLI.organize_data(xlsx_filename)
                else:
                    VLI.organize_data(filepath)

                # Extract the base name and extension from the original filename
                base_name, extension = os.path.splitext(filename)

                # Construct the processed filename
                processed_filename = f"{base_name} (processed){extension}"

                # Construct the processed filepath
                processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

                # Rename the processed file
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

                # Redirect to download the processed file
                return redirect(url_for('download_file', name=quote(processed_filename)))

            except Exception as e:
                message = f"An error occurred during processing: {e}"
                if discord_token and discord_guild_id and discord_channel_id:
                    dc_send(f"[VLI] {filename}\n{message}", discord_token, discord_guild_id, discord_channel_id)

    # Render the upload page with the message if available
    return render_template('VLI.html', message=message)


@app.route('/uploads/<name>')
def download_file(name):
    """Sends the processed file to the user for download."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], unquote(name), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)