# Hydro-Assess Streamlit Application

A professional web application for rainwater harvesting system assessment and design recommendations.

## Features

- **Multi-language Support**: English, Hindi, and Tamil
- **Interactive Maps**: Location-based analysis with GeoJSON integration
- **Professional PDF Reports**: Comprehensive reports with Unicode support
- **Real-time Calculations**: Dynamic cost and efficiency calculations
- **Responsive Design**: Mobile-friendly interface

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aarya0454/streamlit_hackathon.git
   cd streamlit_hackathon
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run index.py
   ```

## Requirements

- Python 3.8+
- Streamlit
- ReportLab (for PDF generation)
- Matplotlib (for charts)
- Pandas, NumPy (for calculations)
- Requests (for API calls)

## Project Structure

- `index.py` - Main Streamlit application
- `pages/` - Additional pages (calculator, map)
- `pdf_generator.py` - PDF report generation with Unicode support
- `locales.py` - Multi-language translations
- `translator.py` - Translation management
- `requirements.txt` - Python dependencies

## PDF Generation

The application automatically downloads required fonts for Hindi text rendering in PDF reports. The system will:

1. Check for existing system fonts
2. Download Noto Sans Devanagari font if needed
3. Generate professional PDF reports with proper Unicode support

## Environment Variables

No environment variables are required for basic functionality. The application uses local font downloads for Unicode support.

## Production Deployment

For production deployment:

1. Ensure the server has internet access for font downloads
2. Set up proper file permissions for font downloads
3. Configure any reverse proxy or load balancer as needed

## License

This project is developed for demonstration purposes.
