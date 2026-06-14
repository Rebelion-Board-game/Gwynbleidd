# src/api_developer.py
import hmac
import hashlib
import secrets
import bcrypt
import jwt
import os
import logging as l
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Header, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from psycopg import Connection
from fun.database import get_db
from datetime import datetime, timedelta, timezone
from typing import Optional
from datetime import datetime


# JWT
SECRET_KEY_DEVELOPER = os.getenv("JWT_SECRET","WhiteWolf")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24h

# Initialize the router
dev_router = APIRouter(tags=["Developer Dashboard"])
security = HTTPBearer()

# --- Pydantic Validation Models ---
class DeveloperRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

class GameCreate(BaseModel):
    game_name: str


class ScoreEntry(BaseModel):
    player_name: str
    score: int
    timestamp: datetime

class ScoresResponse(BaseModel):
    scores: list[ScoreEntry]

class UserEntry(BaseModel):
    id: int
    username: str
    last_login: Optional[datetime] = None
    created_at: datetime

class UserResponse(BaseModel):
    users: list[UserEntry]

class PlayerAuthPayload(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


# --- 1. DEVELOPER JWT ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_DEVELOPER, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY_DEVELOPER, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token claims.")
        return int(user_id)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials / Token expired.")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_DEVELOPER, algorithm=ALGORITHM)
    return encoded_jwt




# --- 3. DEVELOPER MANAGEMENT PANEL ---

@dev_router.post("/api/dev/register", status_code=status.HTTP_201_CREATED)
def register_developer(payload: DeveloperRegister, db: Connection = Depends(get_db)):
    hashed_password = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    with db.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id, email;",
                (payload.email, hashed_password)
            )
            user = cursor.fetchone()
            db.commit()
            return {"message": "Account created successfully", "user": user}
        except Exception:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email already registered.")


@dev_router.post("/api/dev/games", status_code=status.HTTP_201_CREATED)
def create_game(payload: GameCreate, db: Connection = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    l.info("Trying to create game")
    
    with db.cursor() as cursor:
        # Check user limits
        cursor.execute(
            "SELECT current_game_number, max_game FROM users WHERE id = %s;", 
            (current_user_id,)
        )
        user_limits = cursor.fetchone()
        
        if not user_limits:
            raise HTTPException(status_code=404, detail="User not found.")
            
        # If current_game_number >= max_game, block creation
        if user_limits["current_game_number"] >= user_limits["max_game"]:
            raise HTTPException(
                status_code=403, 
                detail=f"Game limit reached. Maximum allowed: {user_limits['max_game']}."
            )
            
        # Generate credentials and insert new game
        api_key = f"ww_key_{secrets.token_hex(64)}"
        api_secret = f"gw_secret_{secrets.token_hex(64)}"
        
        try:
            cursor.execute(
                "INSERT INTO games (user_id, game_name, api_key, api_secret) VALUES (%s, %s, %s, %s) RETURNING *;",
                (current_user_id, payload.game_name, api_key, api_secret)
            )
            game = cursor.fetchone()
            
            # Increment current_game_number
            cursor.execute(
                "UPDATE users SET current_game_number = current_game_number + 1 WHERE id = %s;",
                (current_user_id,)
            )
            
            db.commit()
            return {"message": "Game created successfully", "game": game}
            
        except Exception as e:
            db.rollback()
            l.error(f"Failed to create game workflow: {e}")
            raise HTTPException(status_code=500, detail="Failed to create game workflow.")


@dev_router.get("/api/dev/games")
def get_developer_games(db: Connection = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    with db.cursor() as cursor:
        cursor.execute("SELECT id, game_name, current_users, max_users FROM games WHERE user_id = %s;", (current_user_id,))
        games = cursor.fetchall()
        return {"games": games}


@dev_router.delete("/api/dev/games/{game_id}", status_code=status.HTTP_200_OK)
def delete_developer_game(
    game_id: int, 
    db: Connection = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    with db.cursor() as cursor:
        # Delete the game if it belongs to current_user_id
        cursor.execute(
            "DELETE FROM games WHERE id = %s AND user_id = %s RETURNING id;", 
            (game_id, current_user_id)
        )
        deleted_game = cursor.fetchone()
        
        if not deleted_game:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Game not found or unauthorized."
            )
            
        # Decrement current_game_number for the user (preventing negative values)
        cursor.execute(
            """
            UPDATE users 
            SET current_game_number = GREATEST(0, current_game_number - 1) 
            WHERE id = %s;
            """,
            (current_user_id,)
        )
            
        db.commit()
        return {"message": "Deleted successfully"}


@dev_router.post("/api/dev/login")
def login_developer(payload: DeveloperRegister, db: Connection = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT id, email, password_hash FROM users WHERE email = %s;", (payload.email,))
        user = cursor.fetchone()
        
        if not user or not bcrypt.checkpw(payload.password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid email or password.")
            
        access_token = create_access_token(data={"sub": str(user['id'])})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


@dev_router.get("/api/dev/games/{game_id}/api_key")
def get_game_api(game_id: int,db: Connection = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, game_name, api_key 
                FROM games 
                WHERE id = %s AND user_id = %s;
                """,
                (game_id, current_user_id)
            )
            game = cursor.fetchone()
            if not game:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Game not found or you do not have permission to view it."
                )
            # l.debug(f"api game return {game["api_key"]}")
            return {
                "id": game["id"],
                "game_name": game["game_name"],
                "api_key": game["api_key"]
            }
    except Exception as e:
        l.error(f"download game api error: {e}")
        raise HTTPException(status_code=500, detail="download game api error")


@dev_router.get("/api/dev/games/{game_id}/api_secret")
def get_game_secret(game_id: int,db: Connection = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, game_name, api_secret 
                FROM games 
                WHERE id = %s AND user_id = %s;
                """,
                (game_id, current_user_id)
            )
            game = cursor.fetchone()
            if not game:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Game not found or you do not have permission to view it."
                )
            # l.debug(f"api game return {game["api_secret"]}")
            return {
                "id": game["id"],
                "game_name": game["game_name"],
                "api_secret": game["api_secret"]
            }
    except Exception as e:
        l.error(f"download game aapi_secretpi error: {e}")
        raise HTTPException(status_code=500, detail="download game api_secret error")


@dev_router.put("/api/dev/games/{game_id}/api_key_regenerate")
def regenerate_game_api(game_id: int,db: Connection = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    try:
        new_api_key = f"ww_key_{secrets.token_hex(64)}"
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE games
                SET api_key=%s
                WHERE id = %s AND user_id = %s;
                """,
                (new_api_key, game_id, current_user_id)
            )
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Game not found or you do not have permission to view it"
                )
            db.commit()
            return Response(status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        l.error(f"api regenerate error: {e}")
        raise HTTPException(status_code=500, detail="api regenerate error")


@dev_router.get("/api/dev/games/{game_id}/scores",response_model=ScoresResponse)
def get_scores(game_id: int,db: Connection = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """
    Return best 20 players from leaderboards
    """
    try:    
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM games WHERE user_id = %s AND id = %s;", 
                (current_user_id, game_id)
            )
            game = cursor.fetchone()
            
            if not game:
                raise HTTPException(status_code=403, detail="Game not found or you do not have permission to view it")
                
            cursor.execute(
                """
                SELECT player_name, score, timestamp 
                FROM leaderboards 
                WHERE game_id = %s 
                ORDER BY score DESC 
                LIMIT 20;
                """,
                (game['id'],)
            )
                
            rows = cursor.fetchall()
            return {"scores": rows}
            
    except HTTPException:
        raise
    except Exception as e:
        l.error(f"get_scores endpoint error: {e}")
        raise HTTPException(status_code=500, detail="get_scores endpoint error")


@dev_router.get("/api/dev/games/{game_id}/users",response_model=UserResponse)
def get_users(game_id: int,db: Connection = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """
    Return 20 users from game
    """
    try:    
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM games WHERE user_id = %s AND id = %s;", 
                (current_user_id, game_id)
            )
            game = cursor.fetchone()
            
            if not game:
                raise HTTPException(status_code=403, detail="Game not found or you do not have permission to view it")
                
            cursor.execute(
                """
                SELECT id, username, last_login, created_at 
                FROM players 
                WHERE game_id = %s 
                LIMIT 20;
                """,
                (game['id'],)
            )
                
            rows = cursor.fetchall()
            return {"users": rows}
            
    except HTTPException:
        raise
    except Exception as e:
        l.error(f"get_users endpoint error: {e}")
        raise HTTPException(status_code=500, detail="get_users endpoint error")


@dev_router.delete("/api/dev/games/{game_id}/players/{player_id}", status_code=status.HTTP_200_OK)
def delete_game_player(game_id: int,player_id: int,db: Connection = Depends(get_db),current_user_id: int = Depends(get_current_user_id)):
    l.info(f"delete player!")
    try:
        with db.cursor() as cursor:
            # Verify game ownership
            cursor.execute("SELECT id FROM games WHERE id = %s AND user_id = %s;", (game_id, current_user_id))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Game not found or unauthorized.")

            # Delete player (assuming table is named 'players')
            cursor.execute("DELETE FROM players WHERE id = %s AND game_id = %s RETURNING id;", (player_id, game_id))
            deleted = cursor.fetchone()

            if not deleted:
                db.rollback()
                raise HTTPException(status_code=404, detail="Player not found.")

            # Decrement current_users count in games table
            cursor.execute(
                "UPDATE games SET current_users = GREATEST(0, current_users - 1) WHERE id = %s;",
                (game_id,)
            )

            db.commit()
            return {"message": "Player deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        l.error(f"delete endpoint error: {e}")
        raise HTTPException(status_code=500, detail="delete endpoint error")
 