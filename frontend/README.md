# Environmental Health Platform - Frontend

React frontend for the Personalized Environmental Health & Air Quality Decision Support Platform.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API URL
```

3. Start the development server:
```bash
npm start
```

The application will open at http://localhost:3000

## Features

- User authentication (login/register)
- Dashboard with:
  - Real-time outdoor air quality display
  - Indoor sensor monitoring
  - Activity recommendations
  - Exposure tracking
- Material-UI based responsive design

## Project Structure

```
frontend/
├── public/
│   └── index.html           # HTML template
├── src/
│   ├── components/
│   │   ├── Dashboard.js            # Main dashboard
│   │   ├── Login.js                # Authentication
│   │   ├── AirQualityDisplay.js    # Outdoor AQ display
│   │   ├── IndoorSensors.js        # Indoor sensor list
│   │   └── ActivityRecommendation.js # Activity suggestions
│   ├── App.js               # Main app component
│   └── index.js             # Entry point
├── package.json             # Dependencies
└── .env.example             # Environment template
```

## Technologies

- React 18
- Material-UI (MUI)
- Axios for API calls
- React Router (ready for multi-page)

## Development

The frontend communicates with the backend API at the URL specified in `.env`. Make sure the backend is running before starting the frontend.
