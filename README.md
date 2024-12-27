
# ChargeMonitor

ChargeMonitor is an application that monitors the availability of electric vehicle (EV) charging stations at a specific location. The application provides real-time data collection, email notifications, and integrates with Prometheus for monitoring purposes.

## Features

- **Check EV Charging Station Availability**: The application fetches the availability of electric vehicle charging stations at a specified location using an API and makes requests to retrieve the data.
- **Email Notifications**: If the number of available charging stations changes, the application sends email notifications using SMTP to two predefined email addresses.
- **Real-Time Monitoring**: The availability data is collected every 5 minutes and stored in Prometheus metrics for continuous monitoring.
- **Flask Server**: The application runs a Flask server on port 5000, exposing the Prometheus metrics at the `/metrics` endpoint for easy access.
- **Multithreaded Operation**: The system operates in a multithreaded environment, with one thread running the Flask server and another monitoring the charging station’s status and sending alerts when availability changes.

## Prerequisites

- Python 3.x
- Flask
- Prometheus Client
- SMTP Server for email notifications

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ChargeMonitor.git
   cd ChargeMonitor
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your SMTP settings to enable email notifications.

4. Run the application:

   ```bash
   python app.py
   ```

   The application will start running on port 5000, and you can access the Prometheus metrics at `http://localhost:5000/metrics`.

## Configuration

- **Charging Station API**: Make sure the application is configured to use the correct API for fetching the EV charging station data.
- **Email Settings**: Set up the SMTP server and predefined email addresses for notifications in the application's configuration file.

## Usage

- The application checks the availability of EV charging stations every 5 minutes.
- If the availability changes, an email will be sent to the predefined recipients.
- You can access the Prometheus metrics at `http://localhost:5000/metrics` for real-time monitoring of station availability.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


![Charge Monitor](C:/Users/user/Downloads/DALL·E%202024-12-27%2021.05.43%20-%20A%20modern,%20sleek%20design%20representing%20an%20electric%20vehicle%20charging%20station%20monitoring%20system.%20The%20image%20should%20feature%20a%20stylized%20electric%20vehicle%20charg.webp)