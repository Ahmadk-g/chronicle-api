# Manual Testing

The following tables provides the results of manual testing conducted on various API endpoints for the application. Each endpoint was tested for functionality, expected behavior, and the response provided by the API. The testing process involved verifying the authentication flow, profile management, and other essential features exposed by the API.

### Admin and Authentication Endpoints

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/admin/` | GET | Access the Django admin interface. | Pass |
| `/dj-rest-auth/logout/` | POST | Logs out the user and invalidates their token. | Pass |
| `/dj-rest-auth/login/` | POST | Returns tokens after successful login.  | Pass |
| `/dj-rest-auth/user/` | GET | Retrieves authenticated user details.   | Pass |
| `/dj-rest-auth/user/` | PUT | Updates authenticated user details.   | Pass |
| `/dj-rest-auth/registration/` | POST | Registers a new user and returns their details.  | Pass |

### Profiles Endpoints

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/profiles/` | GET | Lists all profiles. | Pass |
| `/profiles/<id>/` | GET | Retrieves specific profile details by ID. | Pass |
| `/profiles/<id>/` | PUT | Updates a profile (requires authorization). | Pass |
| `/profiles/<id>/` | PATCH | Uploads or updates a profile image. | Pass |

### Posts Endpoints 

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/posts/` | GET | Retrieve all posts. | Pass |
| `/posts/` | POST | Create a new post. | Pass |
| `/posts/<id>/` | GET | Retrieves details of a specific post. | Pass |
| `/posts/<id>/` | PUT | Updates a specific post (requires ownership). | Pass |
| `/posts/<id>/` | DELETE | Deletes a specific post (requires ownership). | Pass |

### Comments Endpoints 

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/comments/` | GET | Retrieves all comments. | Pass |
| `/comments/` | POST | Creates a new comment on a post. | Pass |
| `/comments/<id>/` | GET | Retrieves details of a specific comment. | Pass |
| `/comments/<id>/` | PUT | Updates a specific comment (requires ownership). | Pass |
| `/comments/<id>/` | DELETE | Deletes a specific comment (requires ownership). | Pass |

### Likes Endpoints 

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/likes/` | GET | Lists all likes. | Pass |
| `/likes/` | POST | Likes a post (post ID required). | Pass |
| `/likes/<id>/` | GET | Retrieves details of a specific like. | Pass |
| `/likes/<id>/` | DELETE | Removes a like (requires ownership). | Pass |

### Followers Endpoints

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/followers/` | GET | Retrieves all followers. | Pass |
| `/followers/` | POST | Follows a user (followed user ID required). | Pass |
| `/followers/<id>/` | GET | Retrieves a specific follower relationship. | Pass |
| `/followers/<id>/` | DELETE | Unfollows a user (requires ownership). | Pass |

### Events Endpoints

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/events/` | GET | Retrieves all events. | Pass |
| `/events/` | POST | Creates a new event. | Pass |
| `/events/<id>/` | GET | Retrieves details of a specific event. | Pass |
| `/events/<id>/` | PUT | Updates a specific event (requires ownership). | Pass |
| `/events/<id>/` | DELETE | Deletes a specific event (requires ownership). | Pass |

### Attendings Endpoints

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/attendings/` | GET | Retrieves all attendances. | Pass |
| `/attendings/` | POST | Marks attendance for an event. | Pass |
| `/attendings/<id>/` | GET | Retrieves details of a specific attendance. | Pass |
| `/attendings/<id>/` | PUT | Updates attendance status (requires ownership). | Pass |
| `/attendings/<id>/` | DELETE | Removes an attendance record (requires ownership). | Pass |

### Notifications Endpoints

| Endpoint | Method | Expected Result | Result | 
|----------|--------|-----------------|--------|
| `/notifications/` | GET | Retrieves all notifications for the user. | Pass |
| `/notifications/<id>/` | GET | Retrieves details of a specific notification. | Pass |
| `/notifications/` | POST | Creates a new notification. | Pass |
| `/notifications/<id>/` | DELETE | Deletes a specific notification. | Pass |
| `/notifications/mark-all-as-read/` | PUT  | Marks all notifications as read. | Pass |

