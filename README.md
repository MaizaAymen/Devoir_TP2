# Movies API with FastAPI, PostgreSQL, SQLAlchemy

A simple API for managing movies and their actors.

## Setup

1. Create a PostgreSQL database named `movies_db`

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the `.env` file with your database credentials

4. Run the FastAPI server:
```bash
uvicorn app.main_fastapi:app --reload
```

5. Access the API documentation at: http://localhost:8000/docs

## API Endpoints

- `POST /movies/`: Create a new movie with actors
- `GET /movies/random/`: Get a random movie with its actors
- `GET /`: Welcome message

## Questions

### Why is it often necessary to commit the primary record (Movies) before creating the related records (Actors) that depend on its foreign key?

It's necessary to commit the primary record (Movies) before creating related records (Actors) because:

1. The primary record needs to be persisted to the database to generate its primary key (id).
2. The related records need this primary key value as their foreign key (movie_id).
3. Without committing first, the primary key might not be available, resulting in foreign key constraint violations.
4. The `db.refresh(db_movie)` call after commit ensures the SQLAlchemy object has the database-generated ID.

### What is the difference between lazy loading and eager loading (like joinedload) for relationships in SQLAlchemy?

**Lazy Loading:**
- Relationships are loaded only when explicitly accessed
- Results in N+1 query problem (one query for parent, then one for each child)
- Good for when you don't always need the related data
- Default behavior in SQLAlchemy

**Eager Loading (joinedload):**
- Relationships are loaded upfront in a single query using JOINs
- More efficient when you know you'll need the related data
- Prevents the N+1 query problem
- Must be explicitly specified using methods like `joinedload()`

In our `/movies/random/` endpoint, we use eager loading with `joinedload(models.Movies.actors)` to fetch both the movie and its actors in a single database query, which is more efficient than lazy loading would be.
