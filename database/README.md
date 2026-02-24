# Database Setup Instructions

## MySQL Setup

1. **Install MySQL** (if not already installed)
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Or use XAMPP/WAMP for local development

2. **Create Database and Tables**
   ```bash
   mysql -u root -p < schema.sql
   ```

3. **Configure Backend**
   - Copy `.env.example` to `.env` in the backend folder
   - Update MySQL credentials:
     ```
     MYSQL_HOST=localhost
     MYSQL_USER=root
     MYSQL_PASSWORD=your_password
     MYSQL_DB=college_library
     ```

## Alternative: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open `schema.sql` file
4. Execute the script (Ctrl+Shift+Enter)

## Sample Data

The schema includes sample data:
- 8 books across different categories
- 3 sample members

## Database Configuration

The Flask app uses SQLAlchemy ORM, so you can also let it create tables automatically by running the app. However, you need to create the database first:

```sql
CREATE DATABASE college_library;
```