import scrapy

class GoodreadsSpider(scrapy.Spider):
    name = 'goodreads'
    allowed_domains = ['goodreads.com']
    start_urls = ['https://www.goodreads.com/list/show/1.Best_Books_Ever']

    def parse(self, response):
        books = response.css('tr')
        for book in books:
            title = book.css('a.bookTitle span::text').get(default='Unknown').strip()
            author = book.css('a.authorName span::text').get(default='Unknown').strip()
            rating = book.css('span.minirating::text').get(default='Unknown').strip()
            rating = rating.split(' ', 1)[0]
            book_url = book.css('a.bookTitle::attr(href)').get()

            if book_url:
                yield response.follow(book_url, self.parse_book, meta={'title': title, 'author': author, 'rating': rating})

        next_page = response.css('a.next_page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        title = response.meta['title']
        author = response.meta['author']
        rating = response.meta['rating']
        
        pages_info = response.css('div.FeaturedDetails p[data-testid="pagesFormat"]::text').get(default='Unknown').strip()
        num_pages, cover_type = (pages_info.split(',')[0].strip(), pages_info.split(',')[1].strip()) if ',' in pages_info else (pages_info, 'Unknown')
        num_pages = num_pages.replace(' pages', '').strip()

        """         
        publish_info = response.css('div.TruncatedContent div[data-testid="contentContainer"]::text').get(default='Unknown').strip()
        publish_time, publisher = (publish_info.split('by')[0].strip(), publish_info.split('by')[1].strip()) if 'by' in publish_info else (publish_info, 'Unknown')
        """

        first_publish_date = response.css('div.FeaturedDetails p[data-testid="publicationInfo"]::text').get(default='Unknown').strip()
        first_publish_date = first_publish_date.replace('First published', '').strip().replace(',', '').strip()

        description_parts = response.xpath('/html/body/div[1]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[4]/div/div[1]/div/div/span//text()').getall()
        description = ' '.join([part.strip() for part in description_parts])
        
        genres = response.xpath('//div[@class="BookPageMetadataSection"]//div[5]/ul/span[1]/span//text()').getall()
        genres = [genre.strip() for genre in genres if genre.strip()]
        if genres[0] == 'Genres':
            genres = genres[1:]

        rating_count = response.css('span[data-testid="ratingsCount"]::text').get(default='Unknown').strip().replace(',', '')
        reviews_count = response.css('span[data-testid="reviewsCount"]::text').get(default='Unknown').strip().replace(',', '')
        
        def extract_star_rating(response, star_number):
            star_rating_selector = f'div[data-testid="ratingBar-{star_number}"] div[data-testid="labelTotal-{star_number}"]::text'
            
            star_rating_text = response.css(star_rating_selector).get(default='Unknown').strip()
            
            if ' (' in star_rating_text and ')' in star_rating_text:
                count_part, percentage_part = star_rating_text.split(' (')
                percentage_part = percentage_part.rstrip(')')
                count_part = count_part.replace(',', '')
            else:
                count_part, percentage_part = 'Unknown', 'Unknown'
            
            return count_part, percentage_part

        star_ratings_5_count, star_ratings_5_percentage = extract_star_rating(response, 5)
        star_ratings_4_count, star_ratings_4_percentage = extract_star_rating(response, 4)
        star_ratings_3_count, star_ratings_3_percentage = extract_star_rating(response, 3)
        star_ratings_2_count, star_ratings_2_percentage = extract_star_rating(response, 2)
        star_ratings_1_count, star_ratings_1_percentage = extract_star_rating(response, 1)
                
        book_details = {
            'title': title,
            'author': author,
            'rating': rating,
            'url': response.url,
            'description': description,
            'num_pages': num_pages,
            'cover_type': cover_type,
            'first_publish_date': first_publish_date,
            'genres': genres,
            'rating_count': rating_count,
            'review_count': reviews_count,
            'star_ratings_5_count': star_ratings_5_count,
            'star_ratings_5_percentage': star_ratings_5_percentage,
            'star_ratings_4_count': star_ratings_4_count,
            'star_ratings_4_percentage': star_ratings_4_percentage,
            'star_ratings_3_count': star_ratings_3_count,
            'star_ratings_3_percentage': star_ratings_3_percentage,
            'star_ratings_2_count': star_ratings_2_count,
            'star_ratings_2_percentage': star_ratings_2_percentage,
            'star_ratings_1_count': star_ratings_1_count,
            'star_ratings_1_percentage': star_ratings_1_percentage,
        }

        yield book_details
