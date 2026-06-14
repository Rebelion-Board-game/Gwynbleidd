# Gwynbleidd Backend

Lightweight Backend-as-a-Service (BaaS) for Godot 4.x. Built with FastAPI and PostgreSQL.

## Core Architecture

* **Framework**: FastAPI (Asynchronous ASGI)
* **Database**: PostgreSQL (Relational schema with ON DELETE CASCADE constraints)
* **Authentication**: Hybrid architecture:
  * Secure Mode: JWT (JSON Web Tokens) for developer and persistent player sessions.
  * Guest Mode: Server-side HMAC-SHA256 signature verification via X-API-Key and request payload hashing.
* **Security and Rate Limiting**: Token bucket algorithm via Slowapi (IP-based middleware protection).

## Hardcoded Limits

The system enforces resource constraints directly at the database and middleware level:
* Global rate limiter enabled on godot endpoints.
* Maximum 3 games per developer account.
* Maximum 500 rows inside the leaderboards and users tables per individual game_id.