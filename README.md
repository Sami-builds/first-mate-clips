# First Mate Clips MVP

This folder contains a minimal prototype for the First Mate Clips tool.

## Frontend (React)
- Simple React app with input for Twitch VOD URL, preview player, start/end time inputs, and a **Generate Clip** button.
- Uses the backend endpoint `/api/clip`.

## Backend (Node/Express)
- Endpoint `/api/clip` accepts JSON `{ vodUrl, start, end }`.
- Placeholder implementation that would call Twitch API, download the segment with FFmpeg, and return a URL to the generated clip.

## Next Steps
- Implement Twitch API authentication and video download.
- Deploy backend (e.g., to Render, Railway, or the existing BlueHost server).
- Add clip generation logic and storage.
