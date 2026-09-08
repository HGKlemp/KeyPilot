# KeyPilot – API Endpoints

## MVP

The KeyPilot REST API is used to manage employees, keys, rooms and key loans.

In the MVP, API access is restricted to authenticated operators.
Authentication will be implemented using Auth0 and JWT.

---

## Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | Get all employees |
| GET | `/employees/{id}` | Get a single employee |
| POST | `/employees` | Create a new employee |
| PATCH | `/employees/{id}` | Update an employee |

## Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/keys` | Get all keys |
| GET | `/keys/{id}` | Get a single key |
| POST | `/keys` | Create a new key |
| PATCH | `/keys/{id}` | Update a key |

## Rooms

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rooms` | Get all rooms |
| GET | `/rooms/{id}` | Get a single room |
| POST | `/rooms` | Create a new room |
| PATCH | `/rooms/{id}` | Update a room |

## Key-Room Assignments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/keys/{id}/rooms` | Get all rooms assigned to a key |
| POST | `/keys/{id}/rooms/{room_id}` | Assign a room to a key |
| DELETE | `/keys/{id}/rooms/{room_id}` | Remove a room from a key |

## Key Loans

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/loans` | Get key loan history |
| GET | `/loans/{id}` | Get a single key loan |
| POST | `/loans` | Issue a key to an employee |
| PATCH | `/loans/{id}/return` | Return an issued key |

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/me` | Get the authenticated operator |

Authentication itself is handled by Auth0. KeyPilot validates the JWT sent with protected API requests.