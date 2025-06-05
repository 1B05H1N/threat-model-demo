#!/usr/bin/env python3
from pytm import (
    TM,
    Actor,
    Boundary,
    Classification,
    Data,
    Dataflow,
    Datastore,
    ExternalEntity,
    Lambda,
    Process,
    Server,
    DatastoreType,
)

tm = TM("Todo API Threat Model")
tm.description = "Threat model for a secure Todo API with authentication and rate limiting"

# Actors
user = Actor("User")

# Boundaries
browser = Boundary("Browser")
api = Boundary("API")
db = Boundary("Database")

# Set actor boundary
user.inBoundary = browser

# Components
flask_app = Process("Flask App")
flask_app.inBoundary = api
flask_app.controls.sanitizesInput = True
flask_app.controls.validatesInput = True
flask_app.controls.encryptsOutput = True
flask_app.controls.authenticatesSource = True
flask_app.controls.authorizesSource = True

postgres = Datastore("PostgreSQL")
postgres.inBoundary = db
postgres.type = DatastoreType.SQL
postgres.controls.encryptsDataAtRest = True
postgres.controls.encryptsDataInTransit = True

# Security Components
csrf_protection = Process("CSRF Protection")
csrf_protection.inBoundary = api
csrf_protection.controls.validatesInput = True

rate_limiter = Process("Rate Limiter")
rate_limiter.inBoundary = api
rate_limiter.controls.validatesInput = True

auth_manager = Process("Auth Manager")
auth_manager.inBoundary = api
auth_manager.controls.authenticatesSource = True
auth_manager.controls.authorizesSource = True

# Dataflows
Dataflow(user, flask_app, "HTTPS GET /", data=Data("HTML"))
Dataflow(flask_app, user, "HTTPS 200 OK", data=Data("HTML"))

Dataflow(user, csrf_protection, "HTTPS POST /login", data=Data("JSON"))
Dataflow(csrf_protection, rate_limiter, "Validated Request", data=Data("JSON"))
Dataflow(rate_limiter, auth_manager, "Rate Limited Request", data=Data("JSON"))
Dataflow(auth_manager, flask_app, "Authenticated Request", data=Data("JSON"))
Dataflow(flask_app, user, "HTTPS 200 OK", data=Data("JSON"))

Dataflow(user, csrf_protection, "HTTPS POST /logout", data=Data("JSON"))
Dataflow(csrf_protection, auth_manager, "Validated Request", data=Data("JSON"))
Dataflow(auth_manager, flask_app, "Authenticated Request", data=Data("JSON"))
Dataflow(flask_app, user, "HTTPS 200 OK", data=Data("JSON"))

Dataflow(user, csrf_protection, "HTTPS GET /dashboard", data=Data("HTML"))
Dataflow(csrf_protection, auth_manager, "Validated Request", data=Data("HTML"))
Dataflow(auth_manager, flask_app, "Authenticated Request", data=Data("HTML"))
Dataflow(flask_app, user, "HTTPS 200 OK", data=Data("HTML"))

Dataflow(user, csrf_protection, "HTTPS GET /todos", data=Data("JSON"))
Dataflow(csrf_protection, rate_limiter, "Validated Request", data=Data("JSON"))
Dataflow(rate_limiter, auth_manager, "Rate Limited Request", data=Data("JSON"))
Dataflow(auth_manager, flask_app, "Authenticated Request", data=Data("JSON"))
Dataflow(flask_app, postgres, "Query", data=Data("SQL"))
Dataflow(postgres, flask_app, "Results", data=Data("SQL"))
Dataflow(flask_app, user, "HTTPS 200 OK", data=Data("JSON"))

Dataflow(user, csrf_protection, "HTTPS POST /todos", data=Data("JSON"))
Dataflow(csrf_protection, rate_limiter, "Validated Request", data=Data("JSON"))
Dataflow(rate_limiter, auth_manager, "Rate Limited Request", data=Data("JSON"))
Dataflow(auth_manager, flask_app, "Authenticated Request", data=Data("JSON"))
Dataflow(flask_app, postgres, "Insert", data=Data("SQL"))
Dataflow(postgres, flask_app, "Confirmation", data=Data("SQL"))
Dataflow(flask_app, user, "HTTPS 201 Created", data=Data("JSON"))

Dataflow(user, csrf_protection, "HTTPS PUT /todos/<id>", data=Data("JSON"))
Dataflow(csrf_protection, rate_limiter, "Validated Request", data=Data("JSON"))
Dataflow(rate_limiter, auth_manager, "Rate Limited Request", data=Data("JSON"))
Dataflow(auth_manager, flask_app, "Authenticated Request", data=Data("JSON"))
Dataflow(flask_app, postgres, "Update", data=Data("SQL"))
Dataflow(postgres, flask_app, "Confirmation", data=Data("SQL"))
Dataflow(flask_app, user, "HTTPS 200 OK", data=Data("JSON"))

Dataflow(user, csrf_protection, "HTTPS DELETE /todos/<id>", data=Data("JSON"))
Dataflow(csrf_protection, rate_limiter, "Validated Request", data=Data("JSON"))
Dataflow(rate_limiter, auth_manager, "Rate Limited Request", data=Data("JSON"))
Dataflow(auth_manager, flask_app, "Authenticated Request", data=Data("JSON"))
Dataflow(flask_app, postgres, "Delete", data=Data("SQL"))
Dataflow(postgres, flask_app, "Confirmation", data=Data("SQL"))
Dataflow(flask_app, user, "HTTPS 204 No Content", data=Data("JSON"))

if __name__ == "__main__":
    tm.process() 