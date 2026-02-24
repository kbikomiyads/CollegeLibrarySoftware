# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

College Library Software is a multi-purpose library management system designed for educational institutions. It supports book cataloging, member management, borrowing/returns tracking, and fine calculations.

## Architecture

This is a multi-technology project with separate directories for:

- **backend/** - Server-side logic, APIs, and business rules
- **frontend/** - User interface components (web/desktop)
- **database/** - Schema definitions, migrations, and seed data
- **tests/** - All test files organized by component

## Development Workflow

1. Work within the appropriate directory based on the component being developed
2. Keep backend and frontend loosely coupled through well-defined APIs
3. Database changes should include both schema files and migration scripts