#!/usr/bin/env python3
"""
build_zoom_skills.py
Generates the comprehensive 80 Zoom Professional & Developer Skills database across 8 categories:
1. Zoom Core Skills (1-10)
2. Zoom Webinar & Event Management (11-20)
3. Zoom API & Webhooks (21-30)
4. Zoom Marketing Automation (31-40)
5. Zoom Analytics & Tracking (41-50)
6. Zoom AI & Advanced Automation (51-60)
7. Zoom Contact Center & Business Communication (61-70)
8. Advanced Technical Skills (71-80)

Outputs:
- zoom_skills_data.py (Python module)
- zoom_skills.js (Browser module window.ZOOM_SKILLS)
- zoom_skills.json (Structured JSON)
"""

import json
import os

ZOOM_CATEGORIES = [
    {"id": 1, "name": "Zoom Core Skills", "range": "1-10", "icon": "⚙️", "desc": "Meeting configuration, Workplace administration, user management, and core security."},
    {"id": 2, "name": "Zoom Webinar & Event Management", "range": "11-20", "icon": "🎥", "desc": "High-capacity webinars, registration funnels, landing page embeds, and replay automation."},
    {"id": 3, "name": "Zoom API & Webhooks", "range": "21-30", "icon": "🔌", "desc": "Server-to-Server OAuth, REST API endpoints, real-time event webhooks, and custom app tokens."},
    {"id": 4, "name": "Zoom Marketing Automation", "range": "31-40", "icon": "⚡", "desc": "CRM pipelines: GoHighLevel, HubSpot, Salesforce, ActiveCampaign, Zapier, Make, and n8n."},
    {"id": 5, "name": "Zoom Analytics & Tracking", "range": "41-50", "icon": "📈", "desc": "Full-funnel attribution: GA4, Google Tag Manager, Meta Pixel, Google Ads CAPI, and conversion tracking."},
    {"id": 6, "name": "Zoom AI & Advanced Automation", "range": "51-60", "icon": "🤖", "desc": "Zoom AI Companion, automated meeting summaries, transcription, action items, and virtual agents."},
    {"id": 7, "name": "Zoom Contact Center & Business Communication", "range": "61-70", "icon": "📞", "desc": "Omnichannel cloud contact center, Zoom Phone, IVR call routing, and CRM sales integration."},
    {"id": 8, "name": "Advanced Technical Skills", "range": "71-80", "icon": "💻", "desc": "Zoom Meeting SDK, Video SDK, Node.js & Python integrations, and custom webhook listeners."}
]

# Raw Data Definition for all 80 skills
SKILLS_RAW = [
    # Category 1: Zoom Core Skills (1-10)
    (1, 1, "Zoom Meeting Setup", 
     "Configuring HD video/audio, waiting rooms, passcodes, and scheduling recurring meetings.",
     "প্রফেশনাল মিটিং শিডিউলিং, এইচডি অডিও/ভিডিও অপ্টিমাইজেশন, ওয়েটিং রুম ও পাসকোড সিকিউরিটি সেটআপ।",
     "Zoom Web Portal, Desktop Client, Outlook/Google Calendar Plugins",
     "I configure hardened meeting templates with waiting rooms, AES-256 bit encryption, and auto-calendar sync.",
     "How do you ensure a recurring executive Zoom meeting is completely secure from unauthorized attendees?",
     "I enforce authenticated user logins, mandatory waiting rooms with host-controlled admission, unique meeting IDs instead of PMI, and passcode protection with end-to-end encryption."),

    (2, 1, "Zoom Workplace Administration",
     "Enterprise tenant governance, domain verification, SSO (SAML/Okta), and policy enforcement.",
     "এন্টারপ্রাইজ অ্যাকাউন্ট ম্যানেজমেন্ট, এসএসও (Okta/Azure AD) ইন্টিগ্রেশন ও ওয়ার্কপ্লেস পলিসি প্রয়োগ।",
     "Zoom Admin Portal, SAML 2.0, Okta, Azure AD, SCIM Provisioning",
     "I manage corporate Zoom tenants with Okta SSO SAML 2.0 and automated SCIM user provisioning.",
     "What steps do you take to enforce SSO and SCIM provisioning across a 500-person enterprise?",
     "I configure SAML 2.0 with IdP metadata in Zoom Admin Portal, verify corporate domains via DNS TXT records, and map user groups via SCIM attributes for auto-license assignment."),

    (3, 1, "Zoom Account Management",
     "Managing multi-tier licensing (Pro, Business, Enterprise), billing, and add-on subscriptions.",
     "লাইসেন্স অপ্টিমাইজেশন (Pro/Business), অ্যাড-অন ক্যাপাসিটি ম্যানেজমেন্ট ও বিলিং অডিট।",
     "Billing Portal, License Allocation Engine, Add-on Pool (Webinar 500/1000, Large Meeting)",
     "I audit enterprise license pools to prevent idle seats and provision webinar capacity dynamically.",
     "How do you optimize Zoom licensing costs for an agency with rotating seasonal presenters?",
     "I set up floating webinar licenses and reassign Pro/Large Meeting add-on tiers via automated admin workflows based on event calendars."),

    (4, 1, "Zoom User Management",
     "Role-Based Access Control (RBAC), user groups, department tagging, and automated de-provisioning.",
     "রোল-বেসড অ্যাক্সেস কন্ট্রোল (RBAC), ইউজার গ্রুপ পারমিশন ও অফবোর্ডিং অটোমেশন।",
     "User Management API, RBAC Roles (Owner, Admin, Member, Custom Roles)",
     "I configure custom RBAC roles so marketing teams can manage webinars without accessing billing or logs.",
     "How do you restrict recording deletion privileges while allowing team members to host meetings?",
     "By creating a custom role in Zoom Admin with 'Manage Recordings' set to view-only, disallowing hard delete permissions."),

    (5, 1, "Zoom Security & Permissions",
     "Watermarking, audio signatures, end-to-end encryption (E2EE), and IP range restrictions.",
     "ভিজ্যুয়াল ওয়াটারমার্ক, অডিও সিগনেচার, E2EE এনক্রিপশন ও নির্দিষ্ট আইপি রেঞ্জ পারমিশন।",
     "E2EE Cryptography, Visual Watermark, IP Allowlisting, In-meeting Security Toolbar",
     "I implement visual watermarks with attendee email overlays and enforce IP allowlisting for sensitive calls.",
     "What measures protect confidential client presentations against screen leaks during Zoom meetings?",
     "We enable individual attendee email visual watermarks, audio signatures, disable local recording, and mandate E2EE."),

    (6, 1, "Zoom Recording Management",
     "Cloud recording rules, auto-transcription, auto-deletion retentions, and secure share links.",
     "ক্লাউড রেকর্ডিং রুলস, অটো-ট্রান্সক্রিপশন, পাসওয়ার্ড প্রোটেকশন ও অটো-ডিলিশন রিটেনশন পলিসি।",
     "Zoom Cloud Storage, Smart Chapters, Retention Policy, AWS S3 Archival",
     "I configure auto-cloud recording with smart chapters and automated retention pipelines to AWS S3.",
     "How do you automate cloud recording archival to avoid exceeding Zoom cloud storage limits?",
     "We listen to the 'recording.completed' webhook and push the MP4/VTT files to an AWS S3 bucket, then purge cloud copies after 30 days."),

    (7, 1, "Zoom Rooms Configuration",
     "Hardware deployment (Neat, Poly, Logitech), calendar resource mailboxes, and digital signage.",
     "কনফারেন্স রুম হার্ডওয়্যার সেটআপ (Logitech/Poly), ক্যালেন্ডার রিসোর্স ইন্টিগ্রেশন ও ডিজিটাল সাইনেজ।",
     "Zoom Rooms Controller, Google Workspace / M365 Resource Mailboxes, SIP/H.323 Gateways",
     "I deploy Zoom Rooms with Microsoft 365 calendar resource mailboxes and one-touch join hardware.",
     "How do you link a physical conference room to a Google Workspace calendar for one-touch join?",
     "By provisioning a dedicated Google Calendar resource mailbox, sharing delegate access with Zoom Rooms, and pairing the controller."),

    (8, 1, "Zoom Phone Setup",
     "Cloud PBX migration, number porting, call queues, emergency address E911, and desk phone provisioning.",
     "ক্লাউড পিবিএক্স টেলিফোনি, লোকাল নম্বর পোর্টিং, কল কিউ ও ইমার্জেন্সি E911 রাউটিং সেটআপ।",
     "Zoom Phone Native PBX, SIP Trunking, E911 Nomad Routing, Poly/Yealink Provisioning",
     "I configure Zoom Phone native cloud PBX with multi-level auto-attendants and compliant E911 routing.",
     "What is critical when configuring E911 emergency call routing for hybrid remote employees?",
     "Enabling Nomadic E911 so the client auto-detects network BSSID and IP subnets to push real-time physical dispatch addresses."),

    (9, 1, "Zoom Webinar Setup",
     "Scheduling 500-10,000 attendee webinars, Q&A moderation, practice sessions, and live streaming.",
     "৫০০ থেকে ১০,০০০ অডিয়েন্স ওয়েবিনার, প্র্যাকটিস সেশন, প্যানেলিস্ট ম্যানেজমেন্ট ও ইউটিউব/ফেসবুক লাইভ।",
     "Zoom Webinar 500-10k, Practice Session, Q&A Upvoting, Custom RTMP Streaming",
     "I architect high-capacity webinars with backstage practice sessions, moderated Q&A, and RTMP multicasting.",
     "How do you test audio/video with keynote speakers without exposing the session to early attendees?",
     "We enable 'Webinar Practice Session', allowing panelist rehearsals in backstage mode before clicking 'Broadcast' to attendees."),

    (10, 1, "Zoom Events Management",
     "Multi-day, multi-track hybrid summits, event hubs, expo booths, and ticketing passes.",
     "মাল্টি-ডে ভার্চুয়াল সামিট, এক্সপো বুথ, টিকিট ভেন্ডিং ও মাল্টি-ট্র্যাক এজেন্ডা কনফিগারেশন।",
     "Zoom Events Hub, Ticket Types (General/VIP), Expo Floor, Session Tracks",
     "I build multi-track virtual summits in Zoom Events with VIP networking lounges and sponsor booths.",
     "How do you configure VIP vs General Admission ticket permissions for a multi-session Zoom summit?",
     "Within Zoom Events Hub, I define distinct ticket tiers with role-based access rules mapped to specific track sessions."),

    # Category 2: Zoom Webinar & Event Management (11-20)
    (11, 2, "Webinar Registration Setup",
     "Custom registration questions, approval workflows (manual/automatic), and unique join links.",
     "কাস্টম রেজিস্ট্রেশন ফর্ম, অটোমেটিক অ্যাপ্রুভাল ফিল্টারিং ও ইউনিক জয়েন লিংক জেনারেশন।",
     "Webinar Registration Engine, Custom Fields, reCAPTCHA, Domain Blocking",
     "I build custom registration forms with corporate domain validation and automated approved join links.",
     "How do you block free email providers (Gmail/Yahoo) on Zoom webinar registrations for B2B leads?",
     "By enabling domain restriction in registration settings or validating through an external landing page API webhook before approving."),

    (12, 2, "Webinar Landing Page Integration",
     "Embedding Zoom registration widgets on Webflow, WordPress, ClickFunnels, and custom React sites.",
     "ক্লিকফানেলস, ওয়ার্ডপ্রেস বা ওয়েবফ্লো ল্যান্ডিং পেজে জুম রেজিস্ট্রেশন উইজেট বা এপিআই কানেক্ট করা।",
     "Zoom Embedded Widget, REST API Registrant Endpoint, Webflow/WordPress Webhooks",
     "I integrate high-converting custom landing pages that push registrant payloads seamlessly to Zoom.",
     "Why use a custom landing page instead of default Zoom registration pages?",
     "Custom pages enable full brand immersion, custom tracking scripts (GTM/GA4/Meta), higher conversion rates, and split testing."),

    (13, 2, "Webinar Branding",
     "Custom banners, speaker headshots, branded virtual backgrounds, and personalized email templates.",
     "ব্যানার, ব্র্যান্ডেড ভার্চুয়াল ব্যাকগ্রাউন্ড, স্পিকার হেডশট ও কাস্টম কালার প্যালেট ব্র্যান্ডিং।",
     "Zoom Branding Studio, HTML Email Customizer, Virtual Background Presets",
     "I apply corporate brand guidelines across the webinar console, invitation emails, and speaker lower-thirds.",
     "How do you ensure all remote presenters maintain brand consistency on video?",
     "By enforcing centrally managed Zoom Virtual Backgrounds and branded lower-third overlays via administrative room controls."),

    (14, 2, "Webinar Host & Panelist Management",
     "Assigning co-hosts, managing panelist invites, unmuting controls, and breakout rooms.",
     "কো-হোস্ট অ্যাসাইনমেন্ট, প্যানেলিস্ট ইনভাইট লিঙ্ক ম্যানেজমেন্ট ও ব্যাকস্টেজ কো-অর্ডিনেশন।",
     "Co-host Delegation, Panelist Direct Join Links, Backstage Video Chat",
     "I manage backstage logistics, panelist technical dry-runs, and instant co-host privilege delegation.",
     "What happens if the primary host loses internet connection during a live 1,000-person webinar?",
     "An assigned alternative co-host immediately inherits full host privileges without interrupting the broadcast."),

    (15, 2, "Automated Webinar Reminders",
     "Configuring automated 1-week, 1-day, 1-hour, and 15-minute countdown reminders.",
     "১ সপ্তাহ, ১ দিন, ১ ঘণ্টা ও ১৫ মিনিট আগের অটোমেটিক এসএমএস এবং ইমেইল কাউন্টডাউন রিমাইন্ডার।",
     "Zoom Native Reminder Engine, Twilio SMS API, SendGrid, ActiveCampaign Sequences",
     "I configure multi-channel SMS and email reminder sequences that boost live attendance rates past 45%.",
     "How do you increase webinar show-up rates from the industry average of 25% to over 45%?",
     "By combining Zoom native reminders with 15-minute SMS nudges containing 1-click personalized join links via Twilio."),

    (16, 2, "Webinar Email Notifications",
     "Customizing HTML invitation, registration confirmation, cancellation, and thank-you emails.",
     "কাস্টম এইচটিএমএল কনফার্মেশন, ক্যালেন্ডার ICS অ্যাটাচমেন্ট ও ফলো-আপ নোটিফিকেশন।",
     "Dynamic ICS Calendar Generator, Liquid Email Templates, DKIM/SPF Custom Sender",
     "I customize Zoom transactional emails with one-click Google/Outlook calendar invites (.ics).",
     "How do you prevent Zoom automated confirmation emails from landing in spam or promotions folders?",
     "By configuring custom DKIM and SPF sender signatures in Zoom Admin for the corporate email domain."),

    (17, 2, "Webinar Attendance Tracking",
     "Logging precise join times, leave times, minutes attended, and attendance percentage per lead.",
     "ইউজারের জয়েন টাইম, লিভ টাইম এবং মোট কত মিনিট উপস্থিত ছিলেন তা রিয়েলটাইম ক্যাপচার করা।",
     "Participant API, Attendance Webhooks, Zoom Report Center, CSV Streamer",
     "I track minute-by-minute attendee duration to score prospect buying intent and segment leads.",
     "How do you identify webinar leads who watched more than 80% of your presentation?",
     "By polling the Webinar Participant Report endpoint and filtering `user_duration >= (webinar_duration * 0.8)` for CRM routing."),

    (18, 2, "Webinar Engagement Analytics",
     "Analyzing poll responses, Q&A upvotes, chat logs, and attendee attentiveness scores.",
     "লাইভ পোল রেসপন্স, চ্যাট লগ অ্যানালাইসিস ও বায়ারদের এনগেজমেন্ট স্কোরের হিটম্যাপ তৈরি।",
     "Zoom Poll Reports, Q&A Transcripts, Engagement API, Looker Studio Connector",
     "I extract live poll and Q&A interactions into analytics dashboards to gauge buyer interest.",
     "How do you utilize live poll responses to trigger automated sales follow-up calls?",
     "Poll responses exported via API feed into CRM tags, triggering immediate Slack notifications to account executives."),

    (19, 2, "Webinar Replay Automation",
     "Gated on-demand replay rooms with automatic registration capture and CRM tagging.",
     "অন-ডিমান্ড ওয়েবিনার রিপ্লে ফানেল, গেটেড অ্যাক্সেস ও পুনরায় সেলস সিকোয়েন্স ট্রিগারিং।",
     "Zoom On-Demand Recording, Wistia/Vimeo Sync, EverWebinar, HubSpot Replay Workflow",
     "I build automated evergreen on-demand replay funnels that capture and score leads 24/7.",
     "How do you automatically send webinar replays only to registered leads who missed the live call?",
     "We segment CRM contacts who have the tag `webinar_registered` but lack `webinar_attended` via post-event webhooks."),

    (20, 2, "Virtual Event Management",
     "End-to-end technical production of full-day virtual conferences and sponsor summits.",
     "ফুল-ডে ভার্চুয়াল কনফারেন্স, লাইভ স্ট্রিম সুইচিং ও স্পন্সর বুথ টেকনিক্যাল ডিরেকশন।",
     "vMix / OBS Integration, NDI Video Feeds, Zoom ISO, Live Audio Mastering",
     "I serve as technical director for virtual summits, routing high-bitrate NDI feeds into Zoom ISO.",
     "How do you ingest multi-camera broadcast quality feeds into Zoom for a keynote speaker?",
     "We use OBS or vMix via Virtual Camera and Zoom ISO to pipe high-definition isolated 1080p feeds with custom audio mixing."),

    # Category 3: Zoom API & Webhooks (21-30)
    (21, 3, "Zoom REST API",
     "Full mastery of Zoom API v2 architecture, rate limits, pagination, and error codes.",
     "জুম রেস্ট এপিআই v2 স্ট্রাকচার, রেট লিমিট হ্যান্ডলিং ও পেজিনেশন ইঞ্জিনিয়ারিং।",
     "REST API v2, Bearer Token Auth, Rate Limiter (Heavy/Medium/Light), HTTP 429 Retry",
     "I build resilient API services with exponential backoff to handle Zoom's heavy rate limit tiers.",
     "How do you handle HTTP 429 Too Many Requests errors when making batch calls to Zoom API?",
     "By reading the `Retry-After` header and implementing exponential backoff with jitter using a Redis task queue."),

    (22, 3, "Zoom OAuth Authentication",
     "User-level OAuth 2.0 authorization code flow, refresh token rotation, and secure token storage.",
     "ইউজার-লেভেল OAuth 2.0 অথরাইজেশন কোড ফ্লো, রিফ্রেশ টোকেন রোটেশন ও ডাটাবেস এনক্রিপশন।",
     "OAuth 2.0 RFC 6749, PKCE Flow, Refresh Token Rotation, AES-256 Storage",
     "I implement standard OAuth 2.0 with PKCE and automated refresh token rotation for multi-user apps.",
     "Why is refresh token rotation critical in Zoom OAuth integrations?",
     "Zoom invalidates old refresh tokens upon single use; apps must store the newly issued refresh token atomically to prevent auth failure."),

    (23, 3, "Zoom Server-to-Server OAuth",
     "Replacing deprecated JWT apps with modern Server-to-Server OAuth for secure backend automation.",
     "JWT-এর আধুনিক বিকল্প: অ্যাকাউন্ট-লেভেল Server-to-Server OAuth দিয়ে সুরক্ষিত অটোমেশন।",
     "Server-to-Server OAuth, Account ID, Client ID, Client Secret, Token Cache",
     "I configure modern Server-to-Server OAuth applications to power headless enterprise automation.",
     "How do you authenticate backend microservices with Zoom without requiring any user login?",
     "Using Server-to-Server OAuth: I POST client credentials and Account ID to `https://zoom.us/oauth/token?grant_type=account_credentials`."),

    (24, 3, "Zoom Webhooks",
     "Webhook event subscriptions, secret token validation (CRC check), and event-driven pipelines.",
     "রিয়েল-টাইম ইভেন্ট সাবস্ক্রিপশন, সিক্রেট টোকেন HMAC-SHA256 CRC ভ্যালিডেশন।",
     "Zoom Webhooks v2, HMAC-SHA256 Challenge-Response, Event Subscriptions",
     "I validate Zoom webhook challenge-response CRC checks with HMAC-SHA256 signatures.",
     "How does Zoom's Webhook Challenge-Response Check (CRC) verification work?",
     "When subscribing, Zoom sends a `plainToken`; the webhook endpoint must compute an HMAC-SHA256 hash using the Webhook Secret Token and return JSON."),

    (25, 3, "Meeting API Integration",
     "Programmatically creating, updating, and deleting meetings with dynamic passcodes and hosts.",
     "কোডের মাধ্যমে স্বয়ংক্রিয়ভাবে মিটিং তৈরি, আপডেট ও হোস্ট ডিলিগেশন হ্যান্ডলিং।",
     "POST /v2/users/{userId}/meetings, Patch Meeting, Meeting Passcode Policy",
     "I integrate meeting creation endpoints into client booking portals for instant calendar generation.",
     "What payload parameters are mandatory when generating a secure Zoom meeting via API?",
     "`topic`, `type` (usually 2 for scheduled), `start_time`, `duration`, `timezone`, `password`, and `settings: {waiting_room: true}`."),

    (26, 3, "Webinar API Integration",
     "Automating webinar scheduling, panelist creation, and custom Q&A configuration via code.",
     "এপিআই দিয়ে ওয়েবিনার সিডিউলিং, প্যানেলিস্ট ইনভাইট পাঠানো ও লাইভ স্ট্রিম কী কনফিগারেশন।",
     "POST /v2/users/{userId}/webinars, POST /v2/webinars/{id}/panelists",
     "I automate high-volume webinar scheduling and panelist credential delivery via Node.js scripts.",
     "How do you add multiple external panelists to a Zoom webinar programmatically?",
     "By calling `POST /v2/webinars/{webinarId}/panelists` with an array of objects containing `name` and `email`."),

    (27, 3, "Registrant API Integration",
     "Pushing leads into Zoom webinars from external forms and receiving unique attendee join URLs.",
     "এক্সটার্নাল ওয়েবসাইট থেকে সরাসরি রেজিস্ট্র্যান্ট এপিআই-এ লিড পুশ করে ইউনিক লিংক নেওয়া।",
     "POST /v2/webinars/{id}/registrants, Unique `join_url`, Custom Question Answers",
     "I pipe external landing page submissions directly to Zoom to generate personalized `join_url` tokens.",
     "What is returned in the API response when you successfully register an attendee for a webinar?",
     "The `registrant_id`, approval `status`, and the attendee's personalized `join_url` containing their secure session token."),

    (28, 3, "Participant API Integration",
     "Fetching live participant metrics, network jitter, packet loss, and real-time session logs.",
     "মিটিং চলাকালীন লাইভ পার্টিসিপেন্ট কোয়ালিটি, প্যাকেট লস ও লেটেন্সি মেট্রিক্স ট্র্যাক করা।",
     "GET /v2/metrics/meetings/{id}/participants, QoS Audio/Video Jitter Reports",
     "I monitor live call quality metrics via Zoom Dashboard API to troubleshoot executive connection issues.",
     "How do you identify whether a call drop was caused by the host's ISP or Zoom's data centers?",
     "By inspecting the participant QoS report: high jitter and packet loss on the participant uplink confirms a local ISP bottleneck."),

    (29, 3, "Recording API Integration",
     "Automating cloud recording downloads, transcript parsing, and web publishing workflows.",
     "ক্লাউড রেকর্ডিং MP4, অডিও ও VTT ট্রান্সক্রিপ্ট স্বয়ংক্রিয়ভাবে ডাউনলোড ও প্রসেসিং।",
     "GET /v2/meetings/{id}/recordings, OAuth Download Token, VTT WebVTT Parser",
     "I parse VTT transcription files from completed meetings to extract client sentiment and key quotes.",
     "How do you authenticate download requests for Zoom cloud recording MP4 files programmatically?",
     "By appending the Bearer access token in the `Authorization` header or passing `?access_token=` query string for authorized download URLs."),

    (30, 3, "Zoom App Development",
     "Building custom in-meeting Zoom Apps running on the Zoom Client runtime with WebSockets.",
     "জুম ক্লায়েন্টের ভেতরে লাইভ চলাকালীন কাস্টম অ্যাপ, কুইজ ও সিআরএম পপআপ তৈরি।",
     "Zoom Apps SDK, In-meeting Webview, `zoomSdk.config()`, Context APIs",
     "I build interactive Zoom Apps that display real-time CRM lead profiles inside the video client.",
     "What runtime environment powers in-meeting Zoom Apps?",
     "A sandboxed Chromium-based embedded webview running inside the native Zoom desktop client, interfacing via the `zoomSdk` JS bridge."),

    # Category 4: Zoom Marketing Automation (31-40)
    (31, 4, "Zoom + GoHighLevel Integration",
     "Syncing Zoom webinar leads into GHL pipelines, booking calendars, and SMS follow-up triggers.",
     "GoHighLevel (GHL)-এর সাথে জুম কানেক্ট করে লিড সিঙ্ক, ক্যালেন্ডার বুকিং ও অটোমেটিক এসএমএস।",
     "GHL Workflows, Zoom Native App, Custom Webhook Trigger, Opportunity Pipeline",
     "I connect Zoom webinars to GoHighLevel to trigger automated SMS reminder funnels and lead pipeline updates.",
     "How do you route a Zoom webinar no-show into a GoHighLevel automated re-engagement campaign?",
     "Using a webhook triggered on webinar completion that evaluates attendee status and tags the contact as `No-Show` in GHL."),

    (32, 4, "Zoom + HubSpot Integration",
     "Syncing webinar registration and attendance timeline events into HubSpot contact properties.",
     "HubSpot-এ জুম রেজিস্ট্রেশন ও অ্যাটেনডেন্স টাইমলাইন ইভেন্ট হিসেবে সিঙ্ক করা।",
     "HubSpot Zoom App, Marketing Events API, Custom Behavioral Events, Contact Properties",
     "I log Zoom webinar registrations as HubSpot Marketing Events to calculate campaign attribution.",
     "How do you trigger a HubSpot automated workflow based on attendance duration?",
     "By capturing Zoom's `webinar.participant_joined` and `webinar.participant_left` webhooks to update a `Zoom Duration Minutes` property."),

    (33, 4, "Zoom + Salesforce Integration",
     "Mapping Zoom meetings to Salesforce Leads, Contacts, and Campaign Members with ROI tracking.",
     "সেলসফোর্সে লিড, কন্টাক্ট ও ক্যাম্পেইন মেম্বার হিসেবে জুম মিটিং ডেটা ম্যাপিং।",
     "Zoom for Salesforce AppExchange, Campaign Member Status, Lightning Sync",
     "I configure the Zoom for Salesforce package to automatically update Campaign Member statuses to 'Attended'.",
     "How do you reconcile Zoom webinar leads with existing Salesforce Accounts?",
     "Through duplicate lead matching rules based on corporate email addresses, merging webinar attendees into existing contact records."),

    (34, 4, "Zoom + ActiveCampaign Integration",
     "Triggering email drip campaigns and deal stage progressions based on webinar engagement.",
     "ওয়েবিনার রেজিস্ট্রেশনের সাথে সাথে অ্যাক্টিভ-ক্যাম্পেইনে ডিল স্টেজ পরিবর্তন ও ড্রিপ ইমেইল পাঠানো।",
     "ActiveCampaign Zoom Integration, Event Tracking, Automation Tags, Deal Stages",
     "I design ActiveCampaign workflows that tag contacts and route hot prospects to sales reps immediately.",
     "How do you personalize ActiveCampaign emails with the attendee's unique Zoom join URL?",
     "By storing Zoom's returned `join_url` in a custom contact field `%ZOOM_JOIN_URL%` and embedding it as a CTA button."),

    (35, 4, "Zoom + Zapier Automation",
     "Multi-step Zaps for registration notifications, Google Sheets logging, and Slack alerts.",
     "Zapier দিয়ে মাল্টি-স্টেপ অটোমেশন: গুগল শিটস লগিং, স্ল্যাক নোটিফিকেশন ও এসএমএস সেন্টারিং।",
     "Zapier Multi-step Zaps, Webhooks by Zapier, Formatter by Zapier, Slack Webhooks",
     "I build reliable multi-step Zaps that notify sales teams on Slack the moment a high-value lead registers.",
     "What is the best practice for handling high-volume Zoom webinar registrations in Zapier?",
     "Using Webhooks by Zapier to ingest bulk webhook batches or throttling triggers via Storage by Zapier to avoid task overrun."),

    (36, 4, "Zoom + Make.com Automation",
     "Complex scenario routing, data parsing, branch logic, and error handlers for Zoom events.",
     "Make.com (Integromat) দিয়ে জটিল ব্রাঞ্চিং লজিক, রাউটার ও ডেটা ট্রান্সফর্মেশন।",
     "Make.com Scenarios, Custom Webhook Modules, Routers, Aggregators, Error Breakpoints",
     "I architect advanced Make.com scenarios that clean attendee phone numbers and route data across 5 systems.",
     "Why choose Make.com over Zapier for high-throughput Zoom webinar integrations?",
     "Make provides visual branching routers, lower cost per operation, built-in data aggregation, and robust error-handling rollback paths."),

    (37, 4, "Zoom + n8n Automation",
     "Self-hosted, privacy-compliant workflow automation connecting Zoom to internal databases.",
     "সেলফ-হোস্টেড n8n দিয়ে নিজস্ব সার্ভারে সম্পূর্ণ ফ্রি ও আনলিমিটেড জুম অটোমেশন ও ডেটাবেস সিঙ্ক।",
     "n8n Self-hosted Node, Webhook Trigger Node, PostgreSQL, Encryption Nodes",
     "I deploy self-hosted n8n workflows that process Zoom attendance data directly into client PostgreSQL databases.",
     "What security benefit does n8n provide for healthcare or financial Zoom integrations?",
     "Patient and financial attendee data never passes through third-party cloud iPaaS servers, ensuring full HIPAA and GDPR compliance."),

    (38, 4, "Automated Lead Capture",
     "Capturing high-intent webinar attendees into sales pipelines with firmographic enrichment.",
     "উচ্চমানের লিড স্বয়ংক্রিয়ভাবে ক্যাপচার করে ক্লিয়ারবিট/অ্যাপোলো দিয়ে কোম্পানি ডেটা সমৃদ্ধ করা।",
     "Clearbit API, Apollo.io Enrichment, Zoom Registrant Webhook, CRM Pipeline",
     "I enrich Zoom registrant emails with company revenue and employee size before passing them to SDRs.",
     "How do you instantly enrich incoming Zoom webinar leads with company data?",
     "By passing the registrant email to the Apollo or Clearbit API upon registration and attaching company size to the CRM lead."),

    (39, 4, "Automated Follow-up Emails",
     "Dynamic follow-ups segmented into Attendees vs No-Shows with personalized offers and replays.",
     "উপস্থিত বনাম অনুপস্থিত অডিয়েন্স আলাদা করে ভিন্ন ভিন্ন ফলো-আপ সেলস অফার ইমেইল পাঠানো।",
     "Conditional Branching, Dynamic Video Thumbs, Personalized Booking Links (Calendly)",
     "I set up post-webinar follow-up emails that split recipients based on their exact watch duration.",
     "What should be the core difference between attendee and no-show follow-up emails?",
     "Attendees receive a summary of key insights and an immediate consultation call CTA; no-shows receive the replay link and a teaser hook."),

    (40, 4, "Webinar-to-CRM Automation",
     "Automated full-lifecycle sync: Registration -> Reminder -> Attendance -> Opportunity Creation.",
     "রেজিস্ট্রেশন থেকে শুরু করে সেলস পাইপলাইনে ডিল ওপেন করা পর্যন্ত ফুল-লাইফসাইকেল অটোমেশন।",
     "Full Lifecycle CRM Architecture, HubSpot/Salesforce Deals, Webhook Listeners",
     "I build zero-touch end-to-end pipelines that convert webinar attendance into qualified sales pipeline value.",
     "How do you attribute closed revenue to a specific Zoom webinar campaign in your CRM?",
     "By tagging the Contact with the Webinar Campaign ID, which auto-associates with the created Opportunity for multi-touch attribution."),

    # Category 5: Zoom Analytics & Tracking (41-50)
    (41, 5, "Zoom Registration Tracking",
     "Tracking form submissions with UTM parameters, referrer sources, and Google Analytics 4.",
     "ইউটিএম প্যারামিটার, রেফারেল ট্রাফিক ও জিএ৪-এ জুম রেজিস্ট্রেশন কনভার্সন ট্র্যাক করা।",
     "UTM Parameters (`utm_source`, `utm_campaign`), Custom JavaScript, dataLayer",
     "I track every webinar registrant back to their paid ad source using clean UTM parameter capture.",
     "How do you preserve UTM parameters when redirecting users from an ad to a Zoom registration form?",
     "By capturing URL query parameters via JavaScript and writing them to hidden input fields or passing them in API payloads."),

    (42, 5, "Zoom Attendance Tracking",
     "Measuring live attendance drop-off curves and mapping engagement against session minutes.",
     "লাইভ সেশনের কোন মিনিটে কতজন ড্রপ করছে তার ড্রপ-অফ কার্ভ ও রিটেনশন রেট তৈরি।",
     "Session Retention Curve, Drop-off Analysis, Looker Studio, GA4 Measurement Protocol",
     "I plot attendance drop-off graphs to show clients exactly which slide caused attendees to disconnect.",
     "Why is a webinar attendance drop-off curve valuable for marketing leadership?",
     "It pinpoints the exact presentation timestamp where prospect attention was lost, revealing weak slides or premature pitches."),

    (43, 5, "Zoom Conversion Tracking",
     "Measuring post-webinar checkout purchases and calendar call bookings with deduplication.",
     "ওয়েবিনার শেষ হওয়ার পর বায়ার কত ডলারের প্রোডাক্ট কিনল তা ডিডুপ্লিকেটেড ভাবে ট্র্যাকিং।",
     "Stripe / Shopify Webhooks, Server-side Conversion Tracking, Event ID Deduplication",
     "I track dollar-for-dollar revenue generated from each Zoom webinar to calculate exact ROAS.",
     "How do you attribute a Shopify purchase made 3 days after a Zoom webinar back to the event?",
     "By matching the customer's email or `external_id` between Zoom attendee records and Shopify order data Layer."),

    (44, 5, "Zoom + Google Analytics 4",
     "Sending `webinar_registration` and `webinar_attended` custom events into GA4 via Measurement Protocol.",
     "জিএ৪ মেজারমেন্ট প্রোটোকল দিয়ে সার্ভার থেকে সরাসরি কনভার্সন ইভেন্ট পাঠানো।",
     "GA4 Measurement Protocol, Custom Definitions, Key Events, User-ID Tracking",
     "I send server-side `webinar_attended` events into GA4 with minutes watched as a custom metric.",
     "How do you send offline Zoom attendance events into GA4 without client-side browser cookies?",
     "By firing a POST request to GA4's Measurement Protocol endpoint `/mp/collect` with `client_id` and custom event parameters."),

    (45, 5, "Zoom + Google Tag Manager",
     "Implementing GTM container setups on webinar landing pages and thank-you confirmation funnels.",
     "ওয়েবিনার ল্যান্ডিং পেজে GTM সেটআপ, কাস্টম ডেটালেয়ার ইভেন্ট ও স্ক্রিপ্ট ম্যানেজমেন্ট।",
     "GTM Server Container, Stape.io, dataLayer push (`event: webinar_lead`)",
     "I build rock-solid GTM implementations that push clean user data into marketing pixels.",
     "What dataLayer push structure do you recommend for a webinar registration form?",
     "`window.dataLayer.push({event: 'webinar_registration', webinar_id: '123', email_hashed: sha256(email)})`."),

    (46, 5, "Zoom + Meta Pixel",
     "Tracking Meta Lead and CompleteRegistration events with Conversions API (CAPI) deduplication.",
     "মেটা পিক্সেল ও সার্ভার-সাইড CAPI কনভার্সন দিয়ে ফেসবুক এডের রেজাল্ট সর্বোচ্চ করা।",
     "Meta Pixel, Meta Conversions API (CAPI), Event Match Quality (EMQ), Event ID",
     "I set up Meta CAPI for webinar registrations achieving 8.5+ Event Match Quality with hashed emails.",
     "How do you achieve an Event Match Quality score above 8.5 on Meta CAPI for webinar leads?",
     "By passing normalized SHA-256 hashed email, phone, first name, city, and client IP/User-Agent in the server payload."),

    (47, 5, "Zoom + Google Ads Conversion Tracking",
     "Configuring Enhanced Conversions for Leads to feed high-intent webinar attendee signals to Smart Bidding.",
     "গুগল এডসে Enhanced Conversions ফর লিডস দিয়ে স্মার্ট বিডিং অপ্টিমাইজেশন।",
     "Google Ads Enhanced Conversions for Leads, GCLID Capture, Offline Conversion Import",
     "I pipe Zoom attendee conversions into Google Ads offline imports to optimize Target CPA campaigns.",
     "How do Enhanced Conversions for Leads benefit Google Ads campaigns promoting Zoom webinars?",
     "They allow Google's AI bidding models to optimize for high-quality attendees rather than cheap, non-showing clicks."),

    (48, 5, "Webinar Funnel Analytics",
     "Calculating Impression -> Pageview -> Registration -> Attendance -> Call Booked funnel conversion rates.",
     "বিজ্ঞাপন থেকে শুরু করে পেজভিউ, রেজিস্ট্রেশন, উপস্থিতি ও সেলস কনভার্সনের সম্পূর্ণ ফানেল অডিট।",
     "Full Funnel Math, Conversion Ratio Analysis, Drop-off Optimization",
     "I analyze the entire webinar funnel drop-off to identify bottlenecks between page views and sales calls.",
     "What is a healthy benchmark for landing page conversion and live attendance on a B2B webinar?",
     "A strong B2B benchmark is 30-40% landing page conversion and 35-45% live attendance rate for scheduled registrants."),

    (49, 5, "Lead Attribution",
     "Multi-touch attribution models (First Touch, Last Touch, Linear, Data-driven) for Zoom registrations.",
     "মাল্টি-টাচ অ্যাট্রিবিউশন মডেল দিয়ে কোন চ্যানেল সবচেয়ে বেশি পেইং বায়ার এনে দিচ্ছে তা নির্ণয়।",
     "W-Shaped Attribution, Data-driven Attribution, First-party Cookie Identifiers",
     "I build multi-touch attribution models that prove the revenue ROI of executive Zoom webinar series.",
     "Why is single-touch 'last click' attribution misleading for high-ticket Zoom webinar funnels?",
     "Because high-ticket buyers interact with multiple touchpoints (LinkedIn ad, retargeting, email) before attending a live webinar."),

    (50, 5, "Webinar Performance Dashboard",
     "Building executive Looker Studio / Power BI dashboards visualizing registration, attendance, and CAC.",
     "লুকার স্টুডিও বা পাওয়ার বিআই-এ ক্লায়েন্ট ড্যাশবোর্ড তৈরি: লিড সংখ্যা, শো-আপ রেট ও কস্ট পার লিড।",
     "Looker Studio, BigQuery Data Sync, Power BI, Real-time Visualizations",
     "I build interactive Looker Studio dashboards that give CMOs real-time visibility into webinar show-up and CAC.",
     "What key metrics should appear on the executive summary slide of a webinar performance dashboard?",
     "Total Registrations, Show-up Rate (%), Average Minutes Attended, Pipeline Value Generated, and Customer Acquisition Cost (CAC)."),

    # Category 6: Zoom AI & Advanced Automation (51-60)
    (51, 6, "Zoom AI Companion",
     "Enabling and configuring administrative governance for Zoom AI Companion across company tiers.",
     "জুম এআই কম্প্যানিয়ন কনফিগারেশন, প্রাইভেসি পলিসি প্রয়োগ ও মিটিং অটোমেশন।",
     "Zoom AI Companion Admin Settings, Data Retention Governance, Meeting Summary Toggles",
     "I deploy Zoom AI Companion across enterprise accounts with strict zero-data-retention training policies.",
     "Does Zoom AI Companion use customer audio/video data to train third-party AI models?",
     "No, Zoom's enterprise privacy policy explicitly states customer audio, video, and chat content is not used to train AI models."),

    (52, 6, "AI Meeting Summaries",
     "Automated generation of structured meeting summaries with chapter timestamps and key decisions.",
     "মিটিং শেষে স্বয়ংক্রিয়ভাবে বুলেট পয়েন্টে সারসংক্ষেপ, সিদ্ধান্ত ও চ্যাপ্টার টাইমস্ট্যাম্প তৈরি।",
     "AI Companion Summaries, Webhook `meeting.summary_completed`, Email Distribution",
     "I automate the distribution of AI meeting summaries to attendee Slack channels within 60 seconds.",
     "How do you automatically deliver AI meeting summaries to clients who couldn't attend the call?",
     "We listen for the `meeting.summary_completed` webhook and push the structured Markdown summary via automated email or Slack."),

    (53, 6, "AI Meeting Transcription",
     "Real-time multilingual transcription, speaker diarization, and searchable keyword indexing.",
     "রিয়েল-টাইম বহুভাষিক সাবটাইটেল, স্পিকার ডায়রাইজেশন (কে কী বলেছে) ও কি-ওয়ার্ড ইনডেক্সিং।",
     "Speaker Diarization, Multi-language Audio Translation, VTT Subtitle Files",
     "I configure real-time multilingual transcription with speaker diarization for global corporate boards.",
     "How does speaker diarization improve the utility of Zoom meeting transcripts?",
     "It accurately labels each transcript line with the exact participant name and timestamp, making audit search trivial."),

    (54, 6, "AI Action Item Extraction",
     "Extracting agreed-to deliverables and action items with assignee names and deadlines.",
     "মিটিংয়ে কে কোন কাজটি করবে (অ্যাকশন আইটেম) তা স্বয়ংক্রিয়ভাবে আলাদা করে টাস্ক তৈরি করা।",
     "LLM Prompt Engineering, Action Item Parser, ClickUp/Asana/Jira Integration",
     "I pipe Zoom AI-generated action items directly into ClickUp and Asana task boards with assigned owners.",
     "How do you automate project task creation directly from Zoom meeting conversations?",
     "By parsing the AI Companion action items payload via webhook and mapping tasks to Asana or ClickUp APIs with due dates."),

    (55, 6, "AI Follow-up Automation",
     "Drafting personalized follow-up emails instantly based on spoken commitments made in the call.",
     "মিটিংয়ে যা যা কথা হয়েছে তার ওপর ভিত্তি করে অটোমেটিক প্রফেশনাল ড্রাফট ইমেইল তৈরি।",
     "GPT-4o / Claude API, Zoom Webhook Summary Payload, Gmail / Outlook Drafts API",
     "I connect Zoom meeting transcripts to Gemini and GPT-4 to draft custom client follow-ups in Outlook.",
     "How does AI follow-up automation speed up the sales cycle for agency founders?",
     "Instead of spending 30 minutes writing recap emails, the founder finds a personalized draft waiting in their inbox immediately."),

    (56, 6, "AI Meeting Insights",
     "Measuring talk-to-listen ratios, sentiment analysis, speech speed, and objection timestamps.",
     "সেলস কলে আপনি কতক্ষণ কথা বলেছেন আর বায়ার কতক্ষণ বলেছে (Talk vs Listen Ratio) তার এআই অডিট।",
     "Zoom Revenue Accelerator (Zoom IQ), Speech Pace Analytics, Sentiment Heatmaps",
     "I analyze sales call recordings with Zoom Revenue Accelerator to optimize rep talk-to-listen ratios.",
     "What talk-to-listen ratio indicates high conversion probability in a B2B discovery call?",
     "Top-performing sales calls maintain a 45% talk / 55% listen ratio, ensuring the prospect shares their core business pain points."),

    (57, 6, "Zoom Virtual Agent",
     "Building intelligent conversational bots for customer self-service and ticket deflection.",
     "কাস্টমার সার্ভিসের জন্য জুম ভার্চুয়াল এআই এজেন্ট তৈরি যা অটোমেটিক সমস্যার সমাধান করে।",
     "Zoom Virtual Agent (ZVA), Intent Recognition, Knowledge Base Crawler, CRM Hand-off",
     "I design conversational AI flows in Zoom Virtual Agent that resolve 60% of tier-1 support inquiries.",
     "How does Zoom Virtual Agent seamlessly hand off a frustrated user to a live human agent?",
     "Through sentiment threshold monitoring: when sentiment dips, the bot routes context and chat history to Zoom Contact Center."),

    (58, 6, "AI Customer Support Integration",
     "Connecting Zoom Virtual Agent to Zendesk, Freshdesk, and internal knowledge bases.",
     "জেনডেস্ক বা ফ্রেশডেস্কের সাথে জুম এআই কানেক্ট করে টিকিট ম্যানেজমেন্ট ও অটো-রিপ্লাই।",
     "Zendesk API, Freshdesk, Vector Database Search, RAG Architecture",
     "I connect Zoom Virtual Agent to Zendesk knowledge bases to answer complex product inquiries.",
     "What architecture ensures Zoom Virtual Agent gives hallucination-free answers from internal docs?",
     "Retrieval-Augmented Generation (RAG): the bot retrieves factual documentation snippets before synthesizing responses."),

    (59, 6, "AI-powered Meeting Workflows",
     "Triggering multi-agent backend actions based on meeting outcomes (e.g. Contract Generation).",
     "মিটিং শেষ হলে এআই স্বয়ংক্রিয়ভাবে ক্লায়েন্ট চুক্তিপত্র (NDA/SOW) তৈরি করে ড্রাফট পাঠানো।",
     "LangChain / LlamaIndex, DocuSign API, Pandadoc API, Meeting Webhooks",
     "I build automated pipelines where an approved Zoom verbal agreement triggers instant DocuSign contracts.",
     "How can a Zoom call trigger an automated legal contract generation workflow?",
     "When the transcript confirms deal terms, a webhook triggers a contract template in PandaDoc or DocuSign via API."),

    (60, 6, "AI Communication Automation",
     "Automating meeting scheduling, rescheduling, and audio briefings using conversational AI.",
     "এআই ভয়েস অ্যাসিস্ট্যান্ট দিয়ে মিটিং রিশিডিউলিং ও অডিও ব্রিফিং অটোমেশন।",
     "Conversational AI Bots, Voice Synthesis (ElevenLabs), Calendar Orchestration",
     "I build AI voice assistants that handle scheduling calls and deliver 2-minute spoken meeting briefings.",
     "What is an AI pre-meeting briefing and how does it help executives?",
     "It parses attendee LinkedIn profiles and previous email threads into a 2-minute audio brief delivered before joining Zoom."),

    # Category 7: Zoom Contact Center & Business Communication (61-70)
    (61, 7, "Zoom Contact Center",
     "Deploying omnichannel cloud contact center for inbound voice, video, SMS, and web chat.",
     "ইনবাউন্ড ভয়েস, ভিডিও কল, এসএমএস ও লাইভ চ্যাট সাপোর্ট সহ ক্লাউড কন্টাক্ট সেন্টার সেটআপ।",
     "Zoom Contact Center (ZCC), Omnichannel Queues, Agent Desktop, Supervisor Console",
     "I architect enterprise Zoom Contact Centers supporting voice, video escalation, and SMS routing.",
     "What is the unique advantage of Zoom Contact Center over legacy providers like Genesys or Avaya?",
     "Seamless native escalation from phone or web chat directly into a high-definition video call with screen sharing."),

    (62, 7, "Zoom Phone Integration",
     "Integrating Zoom Phone with desktop softphones, physical IP phones, and mobile apps.",
     "ডেস্কটপ সফটফোন, আইপি ফোন ও মোবাইল অ্যাপের সাথে জুম ফোন কল সিস্টেম কানেক্ট করা।",
     "SIP Protocol, Provisioning Templates, Zoom Phone Mobile SDK, Desk Phone Auto-provisioning",
     "I migrate corporate telephony from legacy on-prem PBX systems to flexible Zoom Phone cloud seats.",
     "How do you ensure zero downtime when porting 100+ business phone numbers to Zoom Phone?",
     "By setting up Zoom Phone users with temporary DIDs and configuring forwarding rules prior to the FOC porting date."),

    (63, 6, "Cloud Contact Center Setup",
     "Configuring agent skill groups, business hours, holiday calendars, and SLA thresholds.",
     "এজেন্ট স্কিল গ্রুপ, কাজের সময়সূচী, ছুটির ক্যালেন্ডার ও এসএলএ থ্রেশহোল্ড কনফিগারেশন।",
     "Skill-based Routing Groups, Operating Hours Rules, Overflow Queues, SLA Monitors",
     "I configure skill-based routing in Zoom Contact Center to ensure bilingual agents receive Spanish calls.",
     "How do you handle call queue overflow when wait times exceed SLA thresholds?",
     "By triggering automated overflow rules that route excess callers to secondary agent tiers or offer an automated callback."),

    (64, 7, "Call Routing Configuration",
     "Designing complex call routing algorithms: Round-Robin, Longest Idle, and Priority Cascades.",
     "কল রাউটিং অ্যালগরিদম: রাউন্ড-রবিন, লঙ্গেস্ট আইডল ও প্রায়োরিটি অনুযায়ী কল ট্রান্সফার।",
     "Call Queue Algorithms, Round-Robin, Simultaneous Ring, Tiered Cascade",
     "I design intelligent call routing algorithms that connect high-value callers to senior account managers.",
     "Which call distribution method is best for high-volume sales lines vs customer service lines?",
     "Simultaneous Ring or Round-Robin for fast sales pickups; Longest Idle for fair workload balance in customer service."),

    (65, 7, "IVR Configuration",
     "Building multi-level Interactive Voice Response (IVR) auto-attendant flowcharts.",
     "ইন্টারেক্টিভ ভয়েস রেসপন্স (IVR) - 'প্রেস ১ ফর সেলস, প্রেস ২ ফর সাপোর্ট' ফ্লোচার্ট তৈরি।",
     "IVR Flow Designer, Text-to-Speech Prompts, DTMF Key Routing, Multi-level Trees",
     "I build professional multi-level IVR voice menus with natural neural text-to-speech audio prompts.",
     "What makes an IVR menu user-friendly and efficient for inbound callers?",
     "Keeping menu options under 4 choices, placing common requests first, and offering an immediate zero-key bypass to human agents."),

    (66, 7, "Customer Support Automation",
     "Automating ticket creation, caller verification, and database lookups during inbound rings.",
     "কল আসার সাথে সাথে কলারের হিস্টোরি দেখে অটোমেটিক টিকিট তৈরি ও সিআরএম পপআপ।",
     "CTI Screen Pop, CRM Lookup via Caller ID, Automated Ticket Webhook",
     "I configure Computer Telephony Integration (CTI) screen pops that open caller account histories instantly.",
     "How does a CTI screen pop improve agent resolution time during inbound customer support?",
     "It auto-identifies the caller by ANI (phone number) and loads their open orders on screen before the agent says hello."),

    (67, 7, "Call Analytics",
     "Tracking Average Handle Time (AHT), First Call Resolution (FCR), and abandonment rates.",
     "কল হ্যান্ডেল টাইম (AHT), ফার্স্ট কল রেজোলিউশন ও কল ড্রপ অ্যানালাইটিক্স রিপোর্ট।",
     "Historical Queue Reports, Real-time Dashboard, Abandonment Rate Analytics",
     "I analyze Contact Center queue metrics to identify peak call hours and reduce customer abandonment.",
     "What causes high call abandonment in customer service queues and how do you fix it?",
     "Long hold times and opaque queue position; fixed by adding estimated wait announcements and automated virtual callbacks."),

    (68, 7, "CRM + Call Integration",
     "Bidirectional sync between Zoom Phone call logs, recordings, and CRM customer profiles.",
     "জুম ফোনের কল রেকর্ডিং ও লগ সরাসরি হাবস্পট/সেলসফোর্স কন্টাক্ট টাইমলাইনে সিঙ্ক।",
     "HubSpot Calling Extensions, Salesforce OpenCTI, Auto Call Logging",
     "I connect Zoom Phone to Salesforce and HubSpot so all call recordings attach to contact records automatically.",
     "Why is automated call recording sync important for compliance and quality assurance?",
     "It guarantees an immutable audit trail attached directly to the deal history without relying on manual rep note-taking."),

    (69, 7, "Sales Call Tracking",
     "Attributing closed won deals to specific outbound phone campaigns and inbound hotlines.",
     "কোন ফোন ক্যাম্পেইন বা হটলাইন থেকে কত টাকার সেলস এসেছে তা নিখুঁতভাবে ট্র্যাকিং।",
     "Dynamic Number Insertion (DNI), CallRail + Zoom Phone, Deal Attribution",
     "I attribute closed-won revenue to inbound phone calls using dynamic number tracking across channels.",
     "How do you track which Google Ad click resulted in a phone call answered on Zoom Phone?",
     "By combining website Dynamic Number Insertion (DNI) with Google Ads GCLID tracking, matching call timestamps to ad sessions."),

    (70, 7, "Customer Experience Automation",
     "Automated post-call SMS CSAT surveys, sentiment grading, and supervisor escalation alerts.",
     "কল শেষ হওয়ার সাথে সাথে অটোমেটিক এসএমএস সার্ভে (CSAT/NPS) ও অসন্তুষ্ট কলারদের অ্যালার্ট।",
     "Twilio SMS Survey, CSAT / NPS Calculators, Sentiment Alert Webhooks",
     "I build automated post-call CSAT survey workflows that alert supervisors to unsatisfied customers immediately.",
     "How do you set up an automated CSAT survey triggered right after a Zoom Phone call ends?",
     "A `phone.call_ended` webhook sends an SMS survey via Twilio, logging 1-5 customer ratings back into the CRM."),

    # Category 8: Advanced Technical Skills (71-80)
    (71, 8, "Zoom SDK",
     "Understanding the differences, capabilities, and architectures of Zoom SDK variants.",
     "জুম মিটিং এসডিকে, ভিডিও এসডিকে ও অ্যাপস এসডিকে-এর মধ্যে পার্থক্য ও আর্কিটেকচার বোঝা।",
     "Meeting SDK vs Video SDK, WebAssembly, Client Runtime Architecture",
     "I guide engineering teams in choosing between Zoom Meeting SDK and fully custom Video SDK.",
     "What is the core architectural difference between Zoom Meeting SDK and Zoom Video SDK?",
     "Meeting SDK embeds the standardized Zoom UI/ecosystem; Video SDK provides raw, headless audio/video streams for custom UIs."),

    (72, 8, "Zoom Meeting SDK",
     "Embedding the complete Zoom meeting client into custom React, Angular, or Vue web apps.",
     "ওয়েব অ্যাপ্লিকেশনের ভেতরে সরাসরি সম্পূর্ণ জুম মিটিং উইন্ডো এম্বেড করা।",
     "@zoom/meetingsdk npm, WebAssembly (Wasm), JWT Signature Generator, Client View",
     "I embed full Zoom meeting capabilities into client SaaS portals using the Web Meeting SDK.",
     "How do you generate the secure signature required to join a meeting via Zoom Web Meeting SDK?",
     "By signing an HMAC-SHA256 payload with your SDK Key, Secret, meeting number, and role on a secure backend server."),

    (73, 8, "Zoom Video SDK",
     "Building custom, white-label video call experiences with raw audio, video, and canvas elements.",
     "নিজস্ব ব্র্যান্ডের সম্পূর্ণ কাস্টম ভিডিও কলিং সিস্টেম তৈরি (Raw Audio/Video Canvas)।",
     "@zoom/videosdk, HTML5 Canvas Rendering, Raw Audio Worklets, White-label UX",
     "I build bespoke telehealth and gaming video apps with raw canvas rendering via Zoom Video SDK.",
     "Why choose Zoom Video SDK over Twilio Video or WebRTC for custom video applications?",
     "Zoom Video SDK provides Zoom's global routing infrastructure, superior packet-loss recovery, and predictable flat-rate pricing."),

    (74, 8, "Zoom Apps SDK",
     "Interfacing web applications with the native desktop client via `zoomSdk` JavaScript bridge.",
     "ডেস্কটপ জুম সফটওয়্যারের সাথে ব্রাউজারের জাভাস্ক্রিপ্ট ব্রিজ কানেকশন (`zoomSdk`)।",
     "`zoomSdk.onMyMediaChange()`, `zoomSdk.sendAppInvitation()`, In-meeting Collaboration",
     "I build collaborative whiteboard and note-taking apps that run natively inside the Zoom desktop client.",
     "How do you share an app's state with other participants inside a live Zoom meeting?",
     "Using `zoomSdk.postMessage()` over the in-meeting WebSocket data channel to synchronize state across connected clients."),

    (75, 8, "Zoom Developer Platform",
     "App Marketplace publishing, OAuth scopes auditing, security reviews, and functional testing.",
     "জুম মার্কেটপ্লেসে অফিসিয়াল অ্যাপ পাবলিশিং, ওঅথ স্কোপ অডিট ও সিকিউরিটি রিভিউ পাশ করা।",
     "Zoom App Marketplace, Scope Auditing, Security & Compliance Review, Production Keys",
     "I guide SaaS companies through the rigorous Zoom App Marketplace technical and security review.",
     "What is the most common reason third-party apps fail Zoom Marketplace security reviews?",
     "Requesting excessive OAuth scopes and failing to implement secure refresh token rotation and data privacy guidelines."),

    (76, 8, "Custom Zoom Applications",
     "Building custom internal tools that orchestrate meetings, manage users, and parse recordings.",
     "কোম্পানির অভ্যন্তরীণ কাজের জন্য কাস্টম জুম টুলস তৈরি (ইউজার শিডিউলিং ও রেকর্ডিং প্রসেসর)।",
     "Full-stack Web Apps (React + Node.js), Redis Queue, Database Sync Engine",
     "I build specialized internal dashboards for educational academies to manage 200+ daily Zoom classes.",
     "How do you automatically assign alternative hosts across 200 concurrent Zoom classrooms?",
     "Through a scheduled Node.js worker that queries the teacher timetable and updates the meeting via API before class begins."),

    (77, 8, "Web Application Integration",
     "Integrating Zoom scheduling and join buttons into customized member portals and LMS platforms.",
     "লার্নিং ম্যানেজমেন্ট সিস্টেম (LMS) বা মেম্বারশিপ সাইটে ১-ক্লিক জুম জয়েন বাটন ইন্টিগ্রেশন।",
     "LMS Integration (Moodle/Canvas), Single-Click Join, Custom Webhook Listeners",
     "I integrate seamless single-click Zoom classroom join buttons into custom university LMS portals.",
     "How do you prevent students from sharing their Zoom class join links with outsiders?",
     "By generating individualized registration tokens via API and embedding them behind authenticated student login sessions."),

    (78, 8, "Node.js + Zoom API",
     "Writing high-performance asynchronous TypeScript/Node.js microservices for Zoom automations.",
     "নোড.জেএস (Node.js/TypeScript) ও এক্সপ্রেস দিয়ে হাই-পারফরম্যান্স জুম মাইক্রোসার্ভিস তৈরি।",
     "Node.js, TypeScript, Axios / Got, Express.js, Crypto Module (HMAC verification)",
     "I write robust TypeScript microservices that process thousands of Zoom webhook events per minute.",
     "How do you verify Zoom webhook signatures in a Node.js Express application?",
     "Using `crypto.createHmac('sha256', secret).update(message).digest('hex')` and checking against the `x-zm-signature` header."),

    (79, 8, "Python + Zoom API",
     "Developing Python data engineering pipelines to extract meeting metrics and transcript insights.",
     "পাইথন (Python/FastAPI) দিয়ে মিটিং মেট্রিক্স, ডেটা সায়েন্স ও ট্রান্সক্রিপ্ট অ্যানালাইটিক্স পাইপলাইন।",
     "Python 3, FastAPI, Pandas, Requests, SQLAlchemy, Celery Worker",
     "I build Python automation scripts with Pandas to analyze company-wide meeting duration trends.",
     "How do you authenticate Python backend scripts with Zoom Server-to-Server OAuth?",
     "Using `requests.post()` with Basic Auth containing client ID and secret to fetch the bearer token and caching it for 1 hour."),

    (80, 8, "Custom Webhook Development",
     "Building enterprise webhook receivers with queue buffering, idempotency keys, and retry workers.",
     "এন্টারপ্রাইজ ওয়েবহুক রিসিভার তৈরি: কিউ বাফারিং, রিট্রাই লজিক ও ডুপ্লিকেট ইভেন্ট ফিল্টারিং।",
     "Redis BullMQ, AWS SQS, Idempotency Guard, Microservice Architecture",
     "I build fault-tolerant webhook listeners using Redis queues to ensure zero dropped Zoom events during peak traffic.",
     "How do you handle duplicate Zoom webhook deliveries in an event-driven architecture?",
     "By checking the event's unique timestamp and payload hash against an in-memory Redis cache with an idempotency TTL guard.")
]

def main():
    print("=== GENERATING 80 ZOOM PROFESSIONAL & DEVELOPER SKILLS DATASET ===")

    skills_list = []
    for raw in SKILLS_RAW:
        skill_id, cat_id, title, summary, bangla, tech, spoken, q, a = raw
        category_name = next(c["name"] for c in ZOOM_CATEGORIES if c["id"] == cat_id)
        skills_list.append({
            "id": skill_id,
            "catId": cat_id,
            "category": category_name,
            "title": title,
            "summary": summary,
            "bangla": bangla,
            "tech": tech,
            "spoken": spoken,
            "interview_q": q,
            "interview_a": a
        })

    print(f"Total skills generated: {len(skills_list)}")

    dataset = {
        "categories": ZOOM_CATEGORIES,
        "skills": skills_list
    }

    # 1. Output zoom_skills.json
    json_path = os.path.join(os.path.dirname(__file__), "zoom_skills.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Saved {json_path} ({os.path.getsize(json_path):,} bytes)")

    # 2. Output zoom_skills.js for Web App
    js_path = os.path.join(os.path.dirname(__file__), "zoom_skills.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Antigravity English Tutor - 80 Zoom Enterprise & Developer Skills Engine\n")
        f.write("window.ZOOM_SKILLS_DATA = ")
        json.dump(dataset, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Saved {js_path} ({os.path.getsize(js_path):,} bytes)")

    # 3. Output zoom_skills_data.py for Telegram Bot
    py_path = os.path.join(os.path.dirname(__file__), "zoom_skills_data.py")
    with open(py_path, "w", encoding="utf-8") as f:
        f.write('"""\nzoom_skills_data.py\nPython data module for 80 Zoom Professional & Technical Skills.\n"""\n\n')
        f.write(f"ZOOM_CATEGORIES = {repr(ZOOM_CATEGORIES)}\n\n")
        f.write(f"ZOOM_SKILLS = {repr(skills_list)}\n\n")
        f.write("""
def get_zoom_skill_by_id(skill_id: int):
    for s in ZOOM_SKILLS:
        if s["id"] == skill_id:
            return s
    return None

def search_zoom_skills(term: str, limit: int = 8):
    term_lower = term.lower().strip()
    results = []
    for s in ZOOM_SKILLS:
        if (term_lower in s["title"].lower() or 
            term_lower in s["category"].lower() or 
            term_lower in s["tech"].lower() or 
            term_lower in s["bangla"].lower()):
            results.append(s)
            if len(results) >= limit:
                break
    return results

def get_skills_by_category(cat_id: int):
    return [s for s in ZOOM_SKILLS if s["catId"] == cat_id]
""")
    print(f"Saved {py_path} ({os.path.getsize(py_path):,} bytes)")
    print("=== ZOOM SKILLS GENERATION COMPLETE! ===")

if __name__ == "__main__":
    main()
