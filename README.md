```Markdown
# Climate Analysis and API

This project is part of a climate data analysis challenge using Python, SQLAlchemy,
and Flask to analyze weather data in Honolulu, Hawaii.

The application allows users to explore climate data, such as precipitation levels
and temperature observations, through a RESTful API built with Flask.

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Code Source](#code-source)
```

## Project Overview

The goal of this project is to perform climate analysis on weather data collected from various weather stations in Honolulu, Hawaii.
The data analysis is conducted using Python libraries such as Pandas, SQLAlchemy, and Matplotlib.
A Flask API is created to serve the results of this analysis, allowing users to access the data through different endpoints.

## Dataset

The dataset used for this project is an SQLite database file named `hawaii.sqlite`, which contains weather data such as
precipitation levels and temperature observations from various weather stations in Hawaii.

## Setup and Installation

To run this project locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/hamiltonbrba/sqlalchemy-challenge.git

2. **Navigate to the Project Directory:**

   ```bash
   cd sqlalchemy-challenge
   ```

3. **Make sure your Virtual Environment is Set-up First**

4. **Run the Flask Application:**

   ```bash
   python app.py
   ```

5. **Open the Application in Your Browser:**

   Navigate to `http://127.0.0.1:5000/` to access the API and view available routes. Or 'CTRL' + Left Click the link in the terminal

## Usage

This application provides a RESTful API with various endpoints to access and analyze climate data within the provided module resources. 
Users can query data such as precipitation, station information, and temperature statistics over specific date ranges.

### API Endpoints

- `/api/v1.0/precipitation` - Returns a JSON representation of the last 12 months of precipitation data.
- `/api/v1.0/stations` - Returns a JSON list of weather stations.
- `/api/v1.0/tobs` - Returns temperature observations for the most active station over the last year.
- `/api/v1.0/<start>` - Returns minimum, average, and maximum temperatures for all dates from the given start date.
- `/api/v1.0/<start>/<end>` - Returns minimum, average, and maximum temperatures for the given date range.

## Code Source

The code for this project is structured as follows:

- **Main Application Code:**
  - `app.py` - Contains the Flask application and API route definitions.
- **Jupyter Notebook Analysis:**
  - `climate_analysis.ipynb` - Jupyter Notebook containing initial data exploration and analysis.
- **Data:**
  - `Resources/hawaii.sqlite` - The SQLite database file containing weather data.

> **Note:** The primary code source for the Flask API is located in `app.py`. The data analysis conducted in the Jupyter Notebook is located in `climate_analysis.ipynb`.
