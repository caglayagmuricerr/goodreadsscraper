# ✮ Goodreads Scraper

A web scraper built with Scrapy in Python to extract data from Goodreads. It starts scraping the [Best Books Ever](https://www.goodreads.com/list/show/1.Best_Books_Ever) page.

⚠ **Warning** : The scraper runs indefinitely until manually stopped. To stop the scraper, use `Ctrl + C` **2 times**.

##  ๋࣭⭑ Features 

- Extracts book details such as title, author, rating, and reviews
- Saves the scraped data in JSON or CSV format
- Can be configured to scrape various book categories

##  ๋࣭⭑ Requirements

- Python 3.x
- Scrapy

##  ๋࣭⭑ Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/caglayagmuricerr/goodreadsscraper.git
    ```
2. Change to the project directory:
    ```sh
    cd goodreads-scraper
    ```
3. Install the required packages:
    ```sh
    pip install scrapy
    ```

##  ๋࣭⭑ Usage

1. To start the scraper, run:
    ```sh
    scrapy crawl goodreads
    ```
2. To save the output to a JSON file:
    ```sh
    scrapy crawl goodreads -o output.json
    ```
3. To save the output to a CSV file:
    ```sh
    scrapy crawl goodreads -o output.csv
    ```

##  ๋࣭⭑ Configuration

You can configure the scraper by modifying the `settings.py` file and the `goodreads.py` file located in the `goodreads_scraper/spiders` directory.

##  ๋࣭⭑ Output

The scraped data includes the following fields:
- Title
- Author
- Rating
- URL
- Description
- Number of Pages
- Cover Type
- First Publish Date
- Genres
- Rating Count
- Review Count
- Star Ratings (Count and Percentage) for:
  - 5 Stars
  - 4 Stars
  - 3 Stars
  - 2 Stars
  - 1 Star
    
##  ๋࣭⭑ Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements!

##  ๋࣭⭑ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

