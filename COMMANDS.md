# Property Manager App Commands

## Virtual Environment
```bash
# Create a new virtual environment
python3.13 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install/upgrade dependencies
pip install --upgrade -r requirements.txt
```

## Database Setup
```bash
# Start PostgreSQL service
brew services start postgresql@17

# Create database and user
createdb property_manager
psql postgres
ALTER USER postgres WITH PASSWORD 'postgres';
\q

# Verify database connection
psql -U postgres -d property_manager -h localhost
```

## Running the Application
```bash
# Start the FastAPI application with auto-reload
uvicorn app.main:app --reload
```

## Development Tools
```bash
# Launch DBeaver (Database GUI)
open -a DBeaver

# Check PostgreSQL status
brew services list | grep postgres

# Check PostgreSQL version
psql --version
```

## Environment Variables
The following environment variables should be set in `.env`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/property_manager
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Common Issues
- If `postgres` command not found: Add to PATH
  ```bash
  echo 'export PATH="/usr/local/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc
  source ~/.zshrc
  ```
- If database connection fails:
  1. Check if PostgreSQL is running
  2. Verify password is set correctly
  3. Ensure database exists