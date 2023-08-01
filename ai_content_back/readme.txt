AI content aggregration application - This application is version 1.0 of the backend of AI content 
aggregrator. We implement scrapers within this backend to scrape popular AI
websites, summarize AI content using chatGPT API and store the resulting summarizes,
including salient information about the articles in our database.


To run code from this repository

1. Install Docker and run
    Use this link on mac - https://docs.docker.com/desktop/install/mac-install/
    Use this link on windows - https://docs.docker.com/desktop/install/windows-install/

2. Make sure you are inside the "ai_content_back" directory

3. Build docker image - docker-compose build 

4. Make migrations and migrate database -  
    docker-compose run --rm app sh -c "python manage.py makemigrations"
    docker-compose run --rm app sh -c "python manage.py migrate"

5. Start up local server - docker-compose up

6. Navigate to admin panel to confirm that our setup works
    127.0.0.1/admin


    