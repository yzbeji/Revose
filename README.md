# RevoseAI

RevoseAI is an unsupervised AI that implements K-Means clustering to group company logos based on visual features.
The logos are scraped from company websites using the BeautifulSoup library and stored in the dataset `logos.snappy.parquet` for analysis.
After scraping, the logos are saved in the data folder, then converted to PNG format, remove duplicates, resized, flipped, cropped, and rotated for data augmentation.
For selecting the best value of K for clustering, the Elbow technique is used.

![Figure_1](https://github.com/user-attachments/assets/6b4384e5-40a1-4f61-9912-7380fc831d40)

After determining the best K, the AI was trained on the images, and the logos were separated into different folders to evaluate the results. 
Initially, the model was trained using only the raw images scraped from the websites, with no preprocessing, and the accuracy was quite low. 
However, after using data augmentation to obtain over 20,000 images, the model's accuracy improved significantly to an acceptable level.

![Figure_2](https://github.com/user-attachments/assets/33110fa4-a418-4bf7-b666-09af538ffb13)
