# Project 2 — Phase 1: LangChain & LangGraph Learning

A static HTML learning showcase covering what I learned this week about LangChain and LangGraph — chains, prompt templates, output parsers, memory, tool-calling, graphs, and orchestrator agents.

## How to run it

Open `index.html` in any browser (double-click the file, or right-click → Open with → your browser). No server or build step needed — it's a plain HTML + CSS page.

## What I learned this week

LangChain gave me proper vocabulary for things I'd already half-built by hand in my SlotWise bot — prompt templates and output parsers are essentially the structured version of hardcoding a prompt and regex-matching a tag out of an AI's reply. LangGraph was the bigger shift in thinking: instead of a fixed sequence of steps, it means designing around nodes, edges, and conditional branches from the start — much closer to how my n8n IF-node branches already worked, just formalized as a proper graph. Orchestrator agents are the concept I understand now but haven't built yet — that's next.

## Folder contents

- `index.html` — the learning showcase page
- `style.css` — styling
- `screenshots/page-preview.png` — screenshot proving the page renders correctly in a browser
