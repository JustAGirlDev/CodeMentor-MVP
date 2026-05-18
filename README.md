# CodeMentor Platform v3.0

Adversarial AI Code Intelligence Platform
Backend: Python/SQLite/Termux | Frontend: Vite/React/TypeScript

## Architecture

Backend (Python CLI) <--> REST API <--> Frontend (React/Vite)

Backend features: AI Explain, Battle Mode, Analytics, Intel DB
Frontend features: AssistantView, SettingsView, PermissionsGate, Challenges

## Quick Start

Backend: cd backend && ./bin/mentor --setup && ./bin/mentor --serve 8080
Frontend: cd frontend && npm install && npm run dev

## API Endpoints

GET  /api/health      - Server status
POST /api/explain     - Analyze + explain code
POST /api/battle      - Queue AI vs AI battle
GET  /api/challenges  - Challenge marketplace
GET  /api/leaderboard - XP rankings
GET  /api/intel       - Competitive intelligence

## SaaS Tiers

Free:       50 explains/mo, basic analytics
Pro:        /mo - Unlimited, battle mode, charts
Enterprise: 9/mo - Custom models, SSO, white-label

## Security

- API keys in config/api.json (gitignored)
- Pain points use anonymized device hashes
- No personal data logged

Built with rage, caffeine, and a refusal to stay down.
- JustAGirlDev
