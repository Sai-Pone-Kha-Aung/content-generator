# AI Content Generator 🤖

A powerful AI-powered content generation tool with Notion integration, built using Streamlit. This application allows you to generate various types of content using multiple LLM providers and automatically save them to your Notion workspace.

## ✨ Features

- **Multi-LLM Support**: Works with Google Gemini and Ollama (local models)
- **Content Types**: Blog posts, social media content, technical documentation, and more
- **Notion Integration**: Automatically save generated content to your Notion database
- **Web Interface**: User-friendly Streamlit interface with multiple pages
- **Content Library**: Browse and manage your generated content
- **System Monitoring**: Real-time status of API connections and services
- **Flexible Configuration**: Easy setup with environment variables

## 📸 Screenshots

![AI Content Generator Interface](<public/ai content agent.png>)

_Main interface showing the content generation form with topic input, content type selection, and tone/length settings._

![Content Library View](<public/ai content agent library.png>)

_Content library page displaying previously generated content with search and filter capabilities._

![System Status Dashboard](<public/ai content agent status.png>)

_System monitoring page showing API connection status and service health metrics._

![System Setting](<public/ai content agent settings.png>)

_Add your api key to run this agent_

## 🏗️ Project Structure

```
content-generator/
├── main.py                    # Main Streamlit application
├── requirements.txt           # Python dependencies
├── config/
│   └── config.py             # Configuration management with Pydantic
├── src/
│   ├── components/
│   │   └── components.py     # Reusable UI components
│   ├── core/
│   │   └── content_agent.py  # Core content generation logic
│   ├── pages/
│   │   └── pages.py          # Streamlit page definitions
│   ├── utils/
│   │   ├── llm_handler.py    # LLM provider integrations
│   │   ├── notion_handler.py # Notion API wrapper
│   │   ├── settings_validator.py # Configuration validation
│   │   └── utils.py          # Utility functions
│   └── test/                 # Test files and debugging scripts
└── public/
    └── Logo.png              # Application assets
```

## 🚀 Quick Setup

### Prerequisites

- Python 3.8+
- pip or conda
- API keys for your chosen LLM provider
- Notion API token and database ID (optional)

### Installation

1. **Clone or download the project**

   ```bash
   cd /path/to/content-generator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root with the following variables:

   ```env
   # Required: Choose at least one LLM provider
   GEMINI_API_KEY=your_gemini_api_key_here

   # Optional: For local LLM with Ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1

   # Optional: For Notion integration
   NOTION_API_KEY=your_notion_api_token_here
   NOTION_DATABASE_ID=your_notion_database_id_here
   ```

4. **Run the application**

   ```bash
   streamlit run main.py
   ```

5. **Open your browser**

   Navigate to `http://localhost:8501` to access the web interface.

## 🔧 Configuration

### LLM Providers

#### Google Gemini

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file as `GEMINI_API_KEY`

#### Ollama (Local)

1. Install [Ollama](https://ollama.ai/) on your machine
2. Pull a model: `ollama pull llama3.1`
3. Ensure Ollama is running: `ollama serve`
4. Configure the base URL and model in your `.env` file

### Notion Integration (Optional)

1. **Create a Notion Integration**:

   - Go to [Notion Developers](https://www.notion.so/my-integrations)
   - Click "New integration"
   - Copy the API token

2. **Set up a Database**:

   - Create a new page in Notion
   - Add a database with properties like "Title", "Content", "Type", etc.
   - Share the page with your integration
   - Copy the database ID from the URL

3. **Add credentials to `.env`**:
   ```env
   NOTION_API_KEY=secret_xyz...
   NOTION_DATABASE_ID=abc123...
   ```

## 🎯 Usage

### Content Generation

1. Navigate to the "Content Generator" page
2. Enter your topic or prompt
3. Select content type (blog, social media, technical, etc.)
4. Choose tone and length
5. Click "Generate Content"
6. Optionally save to Notion

### Content Library

- View all your generated content
- Search and filter by type or date
- Export or edit existing content

### System Status

- Monitor API connection status
- Check LLM provider availability
- View system health metrics

### Settings

- Configure API keys and preferences
- Adjust content generation parameters
- Test API connections

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test files
python src/test/test_llm.py
python src/test/debub_notion.py
```

### Code Formatting

```bash
black .
```

### Project Structure Guidelines

- `src/core/`: Core business logic
- `src/utils/`: Utility functions and API handlers
- `src/pages/`: Streamlit page components
- `src/components/`: Reusable UI components
- `config/`: Configuration and settings management

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**

   - Verify your API keys in the `.env` file
   - Check the Settings page for connection status

2. **Ollama Connection Issues**

   - Ensure Ollama is installed and running
   - Check if the model is pulled: `ollama list`
   - Verify the base URL in your configuration

3. **Notion Integration Problems**
   - Confirm the integration has access to your database
   - Verify the database ID is correct
   - Check if required properties exist in your Notion database

### Environment Variables Reference

| Variable             | Description              | Required | Default                  |
| -------------------- | ------------------------ | -------- | ------------------------ |
| `GEMINI_API_KEY`     | Google Gemini API key    | No\*     | ""                       |
| `OLLAMA_BASE_URL`    | Ollama server URL        | No       | "http://localhost:11434" |
| `OLLAMA_MODEL`       | Ollama model name        | No       | "llama3.1"               |
| `NOTION_API_KEY`     | Notion integration token | No       | ""                       |
| `NOTION_DATABASE_ID` | Notion database ID       | No       | ""                       |

\*At least one LLM provider (Gemini or Ollama) must be configured.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

Made with <3 by SAI PONE KHA AUNG
# content-generator
