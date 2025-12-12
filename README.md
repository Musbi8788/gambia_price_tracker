# 🛒 Gambia Price Tracker

A comprehensive price tracking application for The Gambia that helps users monitor and compare prices of common goods across different locations.

## 🌟 Features

### 📊 Core Functionality
- **Price Tracking**: Add and track prices for common goods across The Gambia
- **Location-based Analysis**: Compare prices across different locations
- **Time Series Analysis**: View price trends over time
- **Data Export**: Export data in CSV and JSON formats

### 📈 Advanced Analytics
- **Price Alerts**: Automatic notifications for significant price changes (>15%)
- **Statistical Insights**: Comprehensive price statistics and analysis
- **Multiple Chart Types**: 
  - Price trend charts with trend lines
  - Location comparison charts
  - Price distribution histograms
  - Monthly trend analysis
  - Price heatmaps

### 🎨 User Experience
- **Mobile Responsive**: Optimized for mobile and desktop use
- **Intuitive Interface**: Clean, modern UI with Gambian context
- **Real-time Updates**: Instant data refresh and caching
- **Advanced Filtering**: Filter by item, location, date range, and price range

### 🔧 Technical Features
- **Modular Architecture**: Clean, maintainable code structure
- **Data Validation**: Comprehensive input validation and error handling
- **Automatic Backups**: Data backup system for data safety
- **Performance Optimized**: Efficient data handling and caching

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gambia_price_tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app_v2.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
gambia_price_tracker/
├── app_v2.py              # Main application file
├── app.py                 # Original application (legacy)
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Data storage directory
│   ├── prices.csv        # Main data file
│   └── backups/          # Automatic backups
└── utils/                # Utility modules
    ├── __init__.py
    ├── data_manager.py   # Data handling utilities
    ├── visualizations.py # Chart creation utilities
    └── ui_components.py  # UI components and styling
```

## 🎯 How to Use

### Adding Price Entries
1. Use the form on the right side of the app
2. Select an item from the dropdown or enter a custom item
3. Enter the price in Gambian Dalasi (GMD)
4. Select the location where you found the price
5. Choose the date and unit of measurement
6. Click "Save Entry"

### Viewing Data
- **Charts**: Use the chart selector to view different visualizations
- **Filters**: Use the sidebar filters to narrow down data
- **Table**: View all entries in the data table with sorting options
- **Alerts**: Check the sidebar for price change alerts

### Exporting Data
- Use the export options in the sidebar
- Choose between CSV and JSON formats
- Download filtered or complete datasets

## 🛠️ Configuration

The application can be customized through `config.py`:

- **Common Items**: Add or modify the list of common items
- **Locations**: Update Gambian locations
- **Alert Threshold**: Adjust the price change alert percentage
- **Chart Settings**: Modify chart appearance and behavior

## 📊 Data Schema

The application stores data with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| Item | String | Name of the item |
| Price | Float | Price in GMD |
| Location | String | Location where price was observed |
| Date | Date | Date of observation |
| Timestamp | DateTime | When entry was added |
| Currency | String | Currency (default: GMD) |
| Unit | String | Unit of measurement |

## 🔮 Future Enhancements

### Planned Features
- **User Authentication**: Login system for multiple users
- **Database Integration**: Replace CSV with PostgreSQL/SQLite
- **API Integration**: Connect to external price APIs
- **Notifications**: Email/SMS alerts for price changes
- **Mobile App**: Native mobile application
- **Advanced Analytics**: Machine learning price predictions

### Technical Improvements
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **API Development**: RESTful API for external access
- **Performance Optimization**: Database indexing and query optimization

## 🤝 Contributing

### For Developers
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### For Non-Developers
- Report bugs and suggest features through issues
- Help improve documentation
- Share the app with others in The Gambia

## 📈 Portfolio & Resume Value

This project demonstrates:

### Technical Skills
- **Full-Stack Development**: Frontend (Streamlit) and backend (Python)
- **Data Analysis**: Pandas, statistical analysis, data visualization
- **Software Architecture**: Modular design, separation of concerns
- **Database Design**: Data modeling and management
- **API Development**: Data export and integration capabilities

### Business Skills
- **Problem Solving**: Addressing real-world price transparency issues
- **User Experience**: Mobile-responsive, intuitive interface design
- **Data-Driven Decision Making**: Analytics and insights generation
- **Project Management**: End-to-end application development

### Domain Knowledge
- **Financial Technology**: Price tracking and analysis
- **Local Market Understanding**: Gambian economy and consumer needs
- **Data Visualization**: Chart creation and statistical analysis
- **International Development**: Technology for social impact

## 🌍 Impact & Social Value

This application contributes to:

- **Price Transparency**: Helping consumers make informed decisions
- **Market Efficiency**: Identifying price variations across locations
- **Economic Empowerment**: Providing data for better purchasing decisions
- **Local Development**: Technology solution for Gambian context

## 📞 Support & Contact

- **Issues**: Report bugs and request features on GitHub
- **Documentation**: Check this README and code comments
- **Community**: Share feedback and suggestions

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for The Gambia**

*Empowering consumers through price transparency and data-driven insights.*
