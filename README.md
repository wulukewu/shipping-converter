# ShippingConverter

<p align="center">
  <img src="static/shipping-converter-tool-icon.png" alt="Shipping Converter Icon">
</p>

ShippingConverter is a tool for converting shipping data. This project includes a Flask web application and Docker support.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/wulukewu/shipping-converter.git
   cd shipping-converter
   ```

2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

To run the Flask application locally, use the following command:

```sh
flask run
```

### Build and Run Docker

To build and run the Docker container, use the following commands:

1. Build the Docker image:

   ```sh
   docker build -t shipping-converter .
   ```

2. Run the Docker container:
   ```sh
   docker run -d -p 5000:5000 --name shipping-converter shipping-converter
   ```

### Pull Docker Image

To pull the Docker image from GitHub Hub, use the following command:

```sh
docker pull wulukewu/shipping-converter:latest
```

### Docker Compose

To use Docker Compose, create a `compose.yaml` file with the following content:

```yaml
version: "3.8"

services:
  shipping-converter:
    image: wulukewu/shipping-converter:latest
    container_name: shipping-converter
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
    volumes:
      - ./uploads:/app/uploads
```

### Discord Integration

To enable Discord notifications, create a `.env` file with the following content:

```env
DISCORD_TOKEN=your_discord_token
DISCORD_GUILD_ID=your_discord_guild_id
DISCORD_CHANNEL_ID=your_discord_channel_id
```

Replace `your_discord_token`, `your_discord_guild_id`, and `your_discord_channel_id` with your actual Discord bot token, guild ID, and channel ID.

### GitHub Actions

This project uses GitHub Actions to automate the release process and Docker image publishing.

#### Workflows

1. **Release Please**: Automates the release process based on conventional commits.
2. **Build Docker Image**: Builds and pushes the Docker image to GitHub Container Registry (ghcr.io).

### References

- [Automating Tag Creation, Release, and Docker Image Publish with GitHub Actions](https://dev.to/natilou/automating-tag-creation-release-and-docker-image-publishing-with-github-actions-49jg)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
