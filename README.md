# Mobile Systems Project

This project is a proof of concept (PoC) demonstrating the integration of a notification system in an Android application using the Web Push protocol. It leverages the Firebase Cloud Messaging (FCM) push proxy as part of the Google development environment.

## Web Push Protocol

The Web Push Protocol is an IETF standard (RFC 8030) that defines how an application server can send asynchronous push messages to a user agent (typically a browser or mobile device), through an intermediary push service using HTTP/HTTPS. The protocol is specifically designed to work over standard web infrastructure.
The publisher can publish a notification on the Proxy server using an HTTP POST, meanwhile clients open a connection using an HTTP GET. The Proxy server will send notifications a persistent channel client intiated (often using an HTTP/2 or other proprietary protocols).

## Project Structure

- **Android App** — the client that receives notifications.
- **Web Server** — acts as a broker that stores subscriber tokens and forwards notifications to Firebase.
- **News Generator** — simulates or generates new messages and sends them to the Web Server.

The Web Server decouples the news generator from Firebase, and the Android app from the news generator. This architecture allows each component to be independent and reusable.

## Flow

1. The Android app registers with the Firebase platform and receives a unique token identifying the app instance.
2. The app sends this token to the Web Server to register as a subscriber.
3. The News Generator sends a new message to the Web Server.
4. The Web Server forwards this message to Firebase for each registered subscriber.
5. Firebase delivers the notification to each device using its token.

## Limitations

Using Firebase as a push proxy requires integrating the Firebase SDK into the Android app and the backend. While this simplifies development by abstracting the Web Push protocol, it also creates a dependency on the Firebase ecosystem.

This dependency is acceptable for the Android client but can be limiting for the backend. Fortunately, the current architecture keeps the news generator independent of Firebase, allowing easier future replacement of the push provider.

## Future Developments

- Store subscriber tokens in a persistent data store (e.g., SQLite, PostgreSQL) rather than in memory.
- Add an admin dashboard to manage subscribers and view delivery status.
- Replace Firebase with a standards-compliant Web Push service for a fully open solution.
