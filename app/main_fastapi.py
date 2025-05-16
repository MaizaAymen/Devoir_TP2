from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List

from app import models, schemas
from app.database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Movies API")


@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    """
    Create a new movie with its actors.
    
    First create and commit the movie record, then create the actor records
    that depend on the movie's primary key.
    """
    # Create movie first
    db_movie = models.Movies(
        title=movie.title,
        year=movie.year,
        director=movie.director
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)  # Refresh to get the generated id
    
    # Now create actors with the movie_id FK
    for actor in movie.actors:
        db_actor = models.Actors(
            actor_name=actor.actor_name,
            movie_id=db_movie.id
        )
        db.add(db_actor)
    
    db.commit()
    db.refresh(db_movie)  # Refresh again to get the actors
    
    return db_movie


@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    """
    Get a random movie from the database along with its actors.
    
    Uses eager loading to fetch the actors along with the movie in a single query.
    """
    # Query for a random movie with its actors
    movie = db.query(models.Movies).options(
        joinedload(models.Movies.actors)
    ).order_by(func.random()).first()
    
    # Handle case where no movies exist
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found in the database")
    
    return movie


@app.get("/")
def read_root():
    return {"message": "Welcome to Movies API. Go to /docs for the API documentation."}
