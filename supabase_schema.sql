-- ==========================================================
-- Antigravity English Mentor - Supabase Database Schema
-- Run this in your Supabase SQL Editor (supabase.com/dashboard)
-- ==========================================================

-- 1. Users Profile Table
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    level TEXT DEFAULT 'Intermediate',
    mode TEXT DEFAULT 'Native',
    streak INT DEFAULT 1,
    last_active_date TEXT,
    daily_reminder_time TEXT DEFAULT '09:00',
    notifications_enabled INT DEFAULT 1,
    voice_enabled INT DEFAULT 1,
    accent TEXT DEFAULT 'US',
    interview_state TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Chat Conversation History
CREATE TABLE IF NOT EXISTS chat_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. Vocabulary Bank
CREATE TABLE IF NOT EXISTS vocabulary (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    word TEXT NOT NULL,
    meaning_bn TEXT,
    part_of_speech TEXT,
    example_sentence TEXT,
    learned_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 4. Mistakes & Corrections Log
CREATE TABLE IF NOT EXISTS mistakes_log (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    original_text TEXT,
    corrected_text TEXT,
    explanation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Create indexes for superfast queries
CREATE INDEX IF NOT EXISTS idx_chat_history_user ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_vocabulary_user ON vocabulary(user_id);
CREATE INDEX IF NOT EXISTS idx_mistakes_log_user ON mistakes_log(user_id);
