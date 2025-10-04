# X Startup Idea Finder

A lightweight SaaS-style FastAPI application that surfaces startup ideas from X (formerly Twitter) using curated prompt phrases such as "I'd pay for" and "Someone please build". It automatically appends `-filter:links -filter:retweets -filter:replies` to concentrate on authentic, original posts.

## Features

- 🔍 Build powerful X search queries combining the base prompts with your own keywords.
- 🧠 Uses `snscrape` to fetch public posts without relying on the official API.
- 🧾 Displays tweet metadata including engagement metrics and direct links.
- 🖥️ Responsive UI tuned for quick scanning of potential startup opportunities.

## Getting started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the development server**

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Open in your browser**

   Navigate to [http://localhost:8000](http://localhost:8000) and enter comma-separated keywords.

## Query format

Every search uses the following structure:

```
("I'd pay for" OR "Someone please build") <your keywords> -filter:links -filter:retweets -filter:replies
```

The filters remove external links, retweets, and replies to focus on original posts containing actionable startup ideas.
