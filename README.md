# Subscription & Billing API (Learning Project)
This repository contains a learning-directed backend project that implements a simplified subscription and billing platform using Python, FastAPI, and PostgreSQL.
It is designed to simulate a production-style backend service that may be found behind SaaS products, streaming platforms, or fintech applications, whilst also serving as a structured way for me to learn modern backend engineering practices, coming from a frontend focused background.

> This project is built as a learning tool, with experiemental commits, and documentation of trade-offs, learning outcomes and possible next steps rather than a finalised product.
## Project Overview
The goal of this project is to model the core building blocks of a subscription and billing system:
- Users and organisations
- Plans and subscriptions
- Basic invoicing and simulated payments
- Access control
Although some concepts are simpliied, the design aims to reflect how real services approach data modeling, correctness and API design.
This project is not a production ready billing solution and should not be used in real business scenarios, its is deliberately aimed at demonstrating backend fundamentals and learning progress.
## Goals & Learning Outcomes
The project is primarily about learning and showcasing software engineering development. My key goals are:
### Technical Goals
- Backend Foundations
  - Learn FastAPI for building modern REST APIs.
  - Design clean API routes with well structured request/response models.
- Relational Data Modeling
  - Use PostgreSQL with SQLAlchemy for relational data.
  - Model users, organisations, memberships, plans, subscriptions, and invoices.
- Auth & Authorisation
  - Implement a basic user registration and login with hashed passwords and JWT-based authentication.
  - Enforce simple authorisation rules, and role based access control.
- Business Logic & Invariants
  - Encapsulate realistic rules and clear subscription status transisions.
  - Generate invoices from subscription and plan data with a focus on correctness over complexity.
- Quality & Testing
  - Write tests using pytest for critical flows.
  - Containerise the app with a minimal Docker setup and add a bais CI workflow with GitHub Actions to run tests on each push (Optional goal as my skills develop and I learn more about these areas.)
### Personal Learning Outcomes
By working through this project, I aim to:
- Develop from a student with experience in Python to an entry-level backend engineer, familiar with API design, and relational databases.
- Build confidence with tools commonly used within indsutry: FastAPI, PostgreSQL, SQLAlchemy, Docker and Github Actions.
- Create a project that can be discussed in depth during internship and junior role interviews, and what skills I learnt from them.

## Tech Stack
Core technolgies are:
- **Language**: Python
- **Web Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM Layer**: SQLAlchemy
- **Auth**: JWT based authorisation
- **Testing**: pytest
- **Containerisation**: Docker (Stretch goal)
- **CI**: Github Actions (Stretch goal)
This stack has been chosen to reflect modern backend teams whilst remaining approachable for a student project at my current level.

## Why this project exists?
This repository is **not** a polished product but rather:
- A demonstration of how I have learnt and applied new backend technologies.
- A tool to practice system design thinking at a small but non-trivial scale.
- A portfolio piece that can be discussed in detail during recruitment processes.
> If you are reviewing this as part of recruitment, feel free to look at the commit history to see my progression and development over time.
