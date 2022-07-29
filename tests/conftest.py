from fastapi.testclient import TestClient
import pytest
from app.database import get_db
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
from alembic import command
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

SessionLocalTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)





@pytest.fixture(scope="function") #default is function
def session():
    Base.metadata.drop_all(bind=engine) # drop all first so you can see database entries if test fails
    Base.metadata.create_all(bind=engine)
    db = SessionLocalTesting()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function") #default is function
def client(session):    # session runs first
    # run code before test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # use test database instead of development database
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # runcode after test finishes
    
@pytest.fixture(scope="function")
def test_user(client):
    user_data = {"email": "testuser@gmail.com", "password": "testuser"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture(scope="function")
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture(scope="function")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client