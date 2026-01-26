# Agents & Dragons - Frontend

A Vue.js-based chat interface for the AI-powered narrative roleplaying game.

## Features

- 🎨 Beautiful fantasy-themed UI with Tailwind CSS
- 📝 Markdown rendering for rich narrative content
- 💬 Real-time chat interface
- 🐳 Docker containerized for easy deployment
- ⚡ Fast development with Vite

## Development

### Prerequisites

- Node.js 20+
- npm or yarn

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:5173

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Docker

### Build Docker image

```bash
docker build -t agents-dragons-frontend .
```

### Run container

```bash
docker run -p 80:80 agents-dragons-frontend
```

## Architecture

The frontend communicates with the orchestrator agent via REST API:

- `POST /api/chat` - Send user messages and receive narrative responses

The orchestrator coordinates with other agents (Storyteller, NPC, Rules) and MCPs (RAG, Dice) to generate the game narrative.

## Technologies

- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **marked** - Markdown parser and compiler
- **DOMPurify** - XSS sanitizer for HTML
- **nginx** - Production web server
