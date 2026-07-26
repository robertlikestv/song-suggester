# Song Suggester

![Backend](https://img.shields.io/badge/status-work--in--progress-yellow)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688)
![Python](https://img.shields.io/badge/python-3.11+-blue)

An end-to-end web application that analyzes a user's top Spotify tracks and leverages the Last.fm API to generate personalized music recommendations and genre insights.

## Project Status & Roadmap

This project is currently under active development.

- [x] Spotify OAuth 2.0 authentication & top track fetching
- [x] Last.fm API client & genre/tag extraction logic
- [ ] Song analysis and recommendation logic
- [ ] FastAPI backend endpoints & request routing
- [ ] React frontend UI integration
- [ ] Unit testing suite (`pytest`)

## Features

* **Spotify Top Track Analysis:** Fetches and parses listening history across different time horizons (`short_term`, `medium_term`, `long_term`).
* **Last.fm Recommendation Engine:** Queries Last.fm API to extract deep genre tags and locate similar track recommendations without API rate-limit crashes.
* **Decoupled Architecture:** Clean separation between the React frontend UI and the FastAPI/Python backend service layer.
* **Type-Safe Configuration:** Centralized environment variable validation using Pydantic Settings.

## Tech Stack

* **Backend:** Python 3.11+, FastAPI, Pydantic V2, Spotipy, PyLast
* **Frontend:** React, JavaScript / TypeScript, CSS Modules
* **APIs:** Spotify Web API (OAuth 2.0), Last.fm REST API
* **Tooling:** Git, `pytest`, `uvicorn`