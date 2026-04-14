# 🌐 World History Globe

An interactive 3D globe built with Python where you can click any country and read about its history, powered by Claude AI.

## Demo

Click any country on the globe → the AI generates an engaging historical summary covering ancient origins, key historical periods, the formation of the modern state, and cultural legacy.

## Features

- Rotatable 3D globe (drag to rotate, scroll to zoom)
- Each country highlighted in gold when selected
- Historical summaries generated in real time by Claude AI
- Colorful map with dark space-like background

## Step-by-step setup

**1. Clone the repository**
```bash
git clone https://github.com/sofiapereira2/world-history-map.git
cd world-history-map
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Get your Anthropic API key**
- Go to [console.anthropic.com](https://console.anthropic.com)
- Sign in with your Anthropic/Claude account
- Go to **Settings → API Keys → Create Key**
- Copy the key (it is only shown once)

**4. Create a `.env` file with your key**
```bash
echo 'ANTHROPIC_API_KEY="sk-ant-your-key-here"' > .env
```

**5. Run the app**
```bash
ANTHROPIC_API_KEY="sk-ant-your-key-here" python3 app.py
```

**6. Open in your browser**
```
http://localhost:8050
```

That's it! Click any country on the globe to read its history.

## Stack

- [Dash](https://dash.plotly.com/) — Python web framework
- [Plotly](https://plotly.com/python/) — interactive globe
- [Claude AI](https://www.anthropic.com/) — history generation (claude-haiku-4-5)
- [pycountry](https://pypi.org/project/pycountry/) — country data

## Requirements

- Python 3.10+
- Anthropic API key → [console.anthropic.com](https://console.anthropic.com)
