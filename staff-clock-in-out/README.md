# The main goal

As a restaurant manager I need a simple UI Where I could record employee clock-ins then
automatically calculate daily, weekly and monthly worked hours and send them to payroll
component.

You should be able to create both the frontend and backend of the application:

- Frontend: A simple web interface where employees can clock in and clock out.
- Backend: A server that handles the clock-in and clock-out requests, stores the data in
  a database, and calculates the total worked hours for each employee.

# Technologies

The choice of technologies is up to you, but here are some suggestions that fit with the
Nexo Pizza ecosystem:

- Frontend: [React v19] for building the user interface, [React Router v7] for routing,
  and [MUI v7] for UI components and styling.
- Backend: [NestJS v11] for building the server and handling requests.
- Database: [MongoDB] for storing employee clock-in and clock-out data, using [Mongoose] as
  the ODM (Object Data Modeling) library.
- Deployment: [Vercel] for deploying the frontend and backend applications.
- Authentication: [Firebase] for user authentication and management.
- Error tracking: [Sentry] for monitoring and tracking errors in both frontend and backend.

---

[React v19]: https://react.dev/
[React Router v7]: https://reactrouter.com/
[MUI v7]: https://mui.com/
[NestJS v11]: https://nestjs.com/
[MongoDB]: https://www.mongodb.com/
[Mongoose]: https://mongoosejs.com/
[Vercel]: https://vercel.com/
[Firebase]: https://firebase.google.com/
[Sentry]: https://sentry.io/
