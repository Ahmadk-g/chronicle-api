<p align="center">
  <img src="documentation/logo.png" alt="Chronicle Logo" style="width: 250px; height: auto;">
</p>
<h1 align="center">Chronicle API - Django Rest Framework</h1>

# Chronicle-Api

## Project Goals

[Chronicle](https://chronicle-ci-fad840fb8771.herokuapp.com/) - Your Social Hub for Connection and Discovery

Chronicle is a vibrant social media platform that combines the best of networking and event discovery, creating a seamless space for sharing experiences, building relationships, and staying connected. Whether you're here to connect with friends, explore engaging content, or discover exciting events, Chronicle empowers you to interact meaningfully and make the most of every moment.

### Key Features:
- **Discover and Engage:**
  - View posts from the community and interact by liking, commenting, and following users.
  - Stay updated with a personalized feed showcasing posts from people you follow.

- **Events Management:**
  - Explore a dedicated Events Page to find events created by users.
  - Mark your attendance status as Attending or Interested to stay involved.
  
- **User Profiles:**

  - Every user has a detailed profile showcasing their posts, events, followers, and followings.
  - Profile pictures and activity stats make it easy to connect and learn more about others.

- **Real-Time Notifications:**

  - Get notified when someone likes or comments on your posts, follows you, or interacts with your events.


## Planning

### Project Overview
Chronicle is a dynamic social media platform designed to foster connections, share experiences, and explore events. It enables users to sign up, create posts and events, interact with a personalized feed, follow other users, and discover exciting community events. 

The project is powered by a Django backend with a REST API, paired with a responsive React frontend. Key features include user authentication, a content discovery system, a dedicated events page, and real-time notifications to keep users engaged.

### Objectives
1. Develop a secure and scalable backend API using Django and Django REST Framework.
2. Create an intuitive and interactive frontend using React.
3. Implement user authentication and profile management.
4. Build a feed system that showcases posts from followed users.
5. Develop a robust events management system, allowing users to browse, create, and interact with events.
6. Implement a notification system to alert users of interactions such as likes, comments, or new followers.
7. Ensure the platform supports responsive design, delivering a seamless experience across devices.

## Data Models

The data models for this website are designed to create a cohesive and interconnected system that supports a dynamic platform for user interactions, event and post management, and content sharing. These models provide the foundation for key features such as user notifications, social interactions (likes, comments, followers), event attendance, and content-based activities. Together, they form a robust architecture that caters to both the functional and social needs of the application.

### **Database Schema**
The database schema leverages Django's ORM (Object-Relational Mapping) to establish a reliable and scalable structure. It encompasses built-in Django models along with custom-defined models tailored to the specific requirements of the platform. The schema emphasizes efficiency, maintainability, and clarity, ensuring that data relationships are optimized for seamless functionality across features.

Key entities in the schema include:

- **User-related Models:** Managing profiles, social interactions, and notifications.
- **Content-based Models:** Enabling posts, likes, and comments.
- **Event-related Models:** Supporting event creation, attendance tracking, and notifications.
- **Notifications:** Delivering real-time updates for likes, comments, follows, and event status changes.

#### **Entity Relationship Diagram (ERD**)
The ERD visually maps out the relationships and dependencies among various entities in the system. It provides a clear representation of how users interact with posts, events, and other users, while also highlighting the notification and social engagement processes. This diagram acts as a blueprint for developers, making it easier to understand the data flow and identify key relationships within the application. [dbdiagram.io](https://dbdiagram.io) was utilized to design the ERD.

![Chronicle ERD](documentation/erd.png)

### **Technical Architecture**
The data models in Chronicle are designed with scalability, modularity, and efficiency at their core, leveraging Django's ORM to streamline data handling and interactions. The architecture ensures a robust and well-structured system that supports Chronicle’s features, including social interactions, notifications, and event management.



#### **Core Design Principles**

1. **Modularity**: The architecture is divided into distinct modules, such as Users, Profiles, Posts, Notifications, Events, and Interactions(likes, comments, attendings), each responsible for a specific domain of functionality.
2. **Relational Integrity**: By utilizing Django’s relational database capabilities, the models enforce strict foreign key relationships, ensuring data consistency and integrity across the system.
3. **Extensibility**: The schema is built to accommodate future features without major refactoring, enabling the platform to grow organically.
4. **Optimized Performance**: Indexing of commonly queried fields and efficient query design help reduce latency and improve scalability as the user base grows.

<br>

### **Key Model Relationships**

- Users:
  - **Profile**: Extends the default Django User model with additional fields for personalization.
  - **Followers**: Creates a many-to-many relationship, enabling users to follow and unfollow one another, fostering a social network.

- Posts:
  - **User-generated content**: Posts include text, images, and multimedia to encourage user engagement.
  - **Likes and Comments**: Linked to Likes and Comments for user interaction with posts, enabling likes and threaded discussions.
  - **Notifications**: Post interactions trigger notifications, keeping users updated on likes, comments, and more.
  - **Timestamps**: Tracks creation and update times, ensuring content freshness.

- Followers
  - **User Connections**: Manages who follows whom by using two ForeignKey fields, creating a many-to-many relationship between users.
  - **Notifications**: Following users triggers notifications, alerting new followers and activity.
  - **Dynamic Relationship**: Users can follow and unfollow at any time, with real-time updates.

- Notifications:
  - **Event-Driven**: Triggered by user actions (likes, comments, follows, event participation) to keep users informed.
  - **Notification Types**: Flexible notification_type field allows new notification types to be added easily.
  - **User-Centric**: Notifications are linked to users, ensuring personalized updates.

- Events:
  - **User-Generated**: Users create events for social gatherings, online meetups, etc.
  - **RSVP & Status**: Tracks participation with statuses like "interested" or "attending" via the Attending model.
  - **Notifications**: Event updates trigger notifications to participants and hosts.
  - **Timestamps**: Events have start and end times to track scheduling.

- Interactions
  - **Likes, Comments & Attendings**: Users interact with posts and events through likes, comments, and attending statuses.
  - **Nested Comments**: Supports threaded comments for deeper discussions.
  - **Dynamic Updates**: Interactions update in real-time, with notifications for new likes, comments, followers or event RSVP's.

<br>

#### **Entity Relationships Overview:**
- **One-to-One:** Each user profile is uniquely tied to a Django User model instance.
- **One-to-Many:** 
  - Users can create multiple posts, comments, likes, or events.
  - Posts can have multiple comments and likes.
- **Many-to-Many:**
  - Follower relationships enable users to connect with each other.
  - Event attendance is facilitated through intermediary models.

<br>  

<u>Comprehnsive Relationship Table</u>

| Primary Model |  Related Model | Relationship Type | Description |
|---------|---------|----------|------------------|
| User | Profile | One-to-One | Each user has one profile. |
| User | Post | One-to-Many | One user can create multiple posts. |
| User | Event | One-to-Many | One user can create multiple events. |
| User | Comment | One-to-Many | One user can create multiple comments. |
| User | Like | One-to-Many | One user can like many posts. |
| User | Attendings | One-to-Many | One user can attend multiple Events. |
| User | Follower | Many-to-Many | Users can follow each other. |
| Post | Like | One-to-Many | A post can have many likes. |
| Post | Comment | One-to-Many | A post can have many comments. |
| Event | Attendings | Many-to-Many | Events can have multiple participants. |
| Notification | User | Many-to-One | Many Notifications belong to one users |
| Notification | Post | Many-to-One | Many Notifications belong can be associated with one post |
| Notification | Events | Many-to-One | Many Notifications belong can be associated with one event |

<br>

#### **Validation and Constraints**

Custom validation methods ensure logical consistency within the models:

- **Notifications**: Require associated posts or events based on notification_type, ensuring notifications are only triggered when valid entities exist.
- **Events**: Enforce date and participant constraints.
- **Followers, Likes, and Attendings**: Use 'unique_together' to prevent circular or duplicate relationships.

<br>

#### **Data Flow and Dependencies**
- **Trigger-Driven Notifications:** Signals (post_save, post_delete) are used to automatically create or delete notifications based on user interactions.




