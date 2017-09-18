RoomieRec
==============================

| **Name**  | Mikaela Hoffman-Stapleton, Arda Aysu  |
|----------:|:-------------|
| **Email** | mhoffmanstapleton@usfca.edu, aaysu@usfca.edu |

RoomieRec is a Flask application that was hosted on AWS (not currently running). We created a web application that used scraped data from Craigslist to recommend possible good-fit housing situations for those looking to rent in the Bay Area. Our solution filtered room listings according to the typical Craigslist filters, and additionally used the Google Maps API to show commute time and local amenities. Most importantly, we added a feature that implemented k-means clustering to find like-minded roommates and desirable living environments. This algorithm used TFIDF on the listing descriptions as well as a description entered by the user to find potential matches.
