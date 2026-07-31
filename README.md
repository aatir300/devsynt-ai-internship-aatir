#### \# DevSynt AI Automation Internship

#### 

#### Aatir Aziz

#### 

#### DevSynt AI Automation Internship – Summer 2026

#### 

This repo contains my weekly task progress, notes, and screenshots for the internship.

---

#### &#x20;Task 2 — WhatsApp Automation: Phase 1 (Design + Sandbox Setup)

#### 

#### \*\*Niche chosen:\*\* Restaurant reservations — a fictional restaurant called "The Olive Table."

#### 

#### \*\*What's in this folder (`task2-whatsapp-phase1/`):\*\*

#### \- `assets/flow-diagram.png` — full conversation flow diagram (Mermaid), covering language detection, greeting/intent, booking states, FAQ loop, no-reply nudges, and human handoff

#### \- `assets/webhook-test-screenshot.png` — screenshot showing a real WhatsApp test message successfully arriving in the n8n workflow via Meta Cloud API

#### \- `workflow.json` — exported n8n workflow (webhook setup for receiving WhatsApp messages)

#### \- `messages.md` — all bot messages (State 0 through 5, 3 nudges, and handoff), written in both English and Arabic

#### 

#### \*\*Why the human handoff step matters:\*\*

#### The bot is designed to never improvise on anything sensitive — medical/health questions, complaints, or pricing negotiations always escalate to a real person instead of the bot guessing an answer. This protects the business from the bot giving wrong or inappropriate information in situations that need real judgment, and keeps the customer experience trustworthy.

#### 

#### \*\*Bilingual behavior:\*\*

#### State 0 detects whether the customer is writing in English or Arabic (checked by looking for Arabic script in the message). From State 1 onward, every message exists in both languages, and the bot always replies in whichever language the customer is currently using — including switching mid-conversation if the customer changes language partway through.

#### 

#### \*\*Note on credentials:\*\*

#### No Meta access token or verify token is committed to this repo. To run this workflow yourself, add your own Meta WhatsApp access token as a credential inside n8n, and set your own Verify Token value in the Code node and in your Meta app's webhook configuration.

