# Commute Weather Kiosk

A Python-based information dashboard designed for Raspberry Pi Zero 2W with direct framebuffer rendering. Displays real-time weather, time, and public transportation departures on a 1920x1200 display.

## Features

- **Weather Information**: Current conditions, hourly forecast, temperature, wind speed, sunrise/sunset times
- **Clock & Date**: Real-time display with custom formatting
- **Public Transport Departures**: Stockholm SL bus and train schedules with live updates
- **System Status**: Network info, CPU temperature, memory usage, and load
- **Direct Framebuffer Rendering**: Optimized for Raspberry Pi displays using `/dev/fb0`

## Requirements

- Raspberry Pi Zero 2W (or compatible)
- Python 3.8+
- Display connected via framebuffer (`/dev/fb0`)
- Internet connection for API data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/m3211n/commute-weather-kiosk.git
cd commute-weather-kiosk
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API settings in `settings.py`:
   - OpenWeatherMap API credentials
   - Stockholm SL transport site IDs
   - Sunrise/sunset API settings
   - Screen dimensions and refresh rate

## Usage

### Production Mode (Framebuffer)
Run on the device with direct framebuffer rendering:
```bash
python main.py --fb
```

### Development Mode (Debug)
Generate preview images for development without a framebuffer:
```bash
python main.py
```
Output will be saved to `__preview/output.png`

## Configuration

### `settings.py`
Key configuration parameters:

- **Display Settings**: Screen dimensions, framebuffer path, refresh rate
- **API Endpoints**: Weather, transport, and sunrise/sunset APIs
- **Location**: Latitude/longitude for weather data
- **Transport**: SL site IDs and stop point IDs for Stockholm transit

### `layout.py`
Widget layout and positioning configuration:

- Clock widget (1160x386px)
- Weather widget (688x1112px)
- Departures widget (1160x702px)
- Status bar (1920x64px)

## Project Structure

```
.
├── main.py              # Entry point and main loop
├── dashboard.py         # Dashboard manager and widget orchestration
├── layout.py            # Widget layout definitions
├── settings.py          # Configuration and API settings
├── updaters.py          # Data fetching and formatting functions
├── requirements.txt     # Python dependencies
├── core/
│   ├── data_sources.py  # Local and remote data source handlers
│   ├── framebuffer.py   # Direct framebuffer I/O
│   ├── styles.py        # Colors and text styling
│   └── ui.py           # Widget and UI component classes
└── assets/
    ├── fonts/          # Custom fonts
    ├── icons/          # Weather and UI icons
    └── images/         # Background and decorative images
```

## Architecture

### Widgets
Each widget is an independent component with:
- **Position and size**: `xy` and `size` parameters
- **Content elements**: Text, images, or other UI components
- **Updater function**: Async function that fetches/formats data
- **Update interval**: Refresh rate in seconds

### Update System
The dashboard runs asynchronous tasks for each widget:
- Independent update cycles per widget
- Dirty flag system for efficient rendering
- RGB565 conversion for framebuffer output

### Rendering Pipeline
1. Widget updaters fetch data at configured intervals
2. State changes mark widgets as "dirty"
3. Main loop renders only dirty widgets
4. Optimized RGB565 conversion for framebuffer
5. Partial screen updates to minimize I/O

## API Dependencies

- **OpenWeatherMap**: Current weather and hourly forecast
- **Sunrise-Sunset.org**: Solar event times
- **SL Transport API**: Stockholm public transport departures

## Performance

- **Update Rate**: 1 second (configurable in `settings.py`)
- **Widget Intervals**: 
  - Clock: 1 second
  - System info: 5 seconds
  - Departures: 60 seconds
  - Weather: 900 seconds (15 minutes)
- **Framebuffer**: RGB565 format for efficient 16-bit color rendering

## Development

### Debug Mode
Test without a physical display by running without `--fb` flag. Preview images are saved to `__preview/output.png`.

### Adding Widgets
1. Define widget in `layout.py` with position, size, and content
2. Create updater function in `updaters.py`
3. Set update interval appropriate for data source

### Custom Styles
Modify text styles and colors in `core/styles.py`.

## License

MIT License - see LICENSE file for details

## Author

m3211n

## Acknowledgments

- OpenWeatherMap for weather data
- Stockholm Lokaltrafik (SL) for public transport API
- Sunrise-Sunset.org for solar event calculations
