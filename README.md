# Advanced Move Bot

## Overview
**Advanced Move Bot** is a Telegram bot designed for logistics services. This bot efficiently handles various operations by integrating:
- **PostgreSQL**: For secure and scalable database management.
- **Google Sheets**: For updating and syncing data from the database to sheets in real-time.

This project builds on the foundation of the `MoveMe Group Bot` with advanced features for better data handling and operational efficiency.

---

## Features
- **PostgreSQL Integration**:
  - Centralized and secure database for storing user credentials, load details, and operational logs.
  - Efficient data retrieval and update operations.
  
- **Google Sheets Integration**:
  - Automated updates of Google Sheets from the PostgreSQL database.
  - Seamless syncing of data for reporting and analysis.

- **Role-Based Functionality**:
  - Custom commands and features for different roles: Dispatchers, Drivers, Admins, and Super Admins.

- **Error Handling and Logging**:
  - Errors are logged and notified to dedicated Telegram channels.
  - Configurable error notification frequency (hourly/daily).

---

## Project Structure
The project follows a modular structure for ease of development and maintenance:
