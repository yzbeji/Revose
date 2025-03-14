import pyarrow.parquet
import scraper
import converter
from PIL import Image, ImageFilter
import numpy
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Acces table from parquet file
table = pyarrow.parquet.read_table('logos.snappy.parquet')

data = table.to_pandas()

# Set the flags to false if you want to start scraping or resize images

scraping_done = True
adjusting_images = True

if scraping_done == False:
    for domain in data['domain']:
        favicon_url = scraper.retrieve_icon(domain)


if adjusting_images == False:
    converter.convert_to_png('./data')
    converter.remove_duplicates('./data')
    converter.resize_images('./data')

images = numpy.array([(numpy.array(Image.open(os.path.join('./data', file))
                                        .resize((32, 32)) # If image is cropped, change the size to (32, 32)
                                        .convert('L').filter(ImageFilter.GaussianBlur(radius = 3))))
                                        .flatten() / 255.0 for file in os.listdir('./data')])

# Trying to find the optimal number of clusters using Elbow Technique
def optimise_cluster(data, number_of_clusters):
    means = numpy.array([])
    inertias = numpy.array([])
    for cluster in range(1, number_of_clusters + 1):
        model = KMeans(n_clusters = cluster, random_state = 32)
        model.fit(data)
        means = numpy.append(means, cluster)
        inertias = numpy.append(inertias, model.inertia_)
    plt.plot(means, inertias, 'o-')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Technique')
    plt.grid(True)
    plt.show()

optimise_cluster(images, 15)

# Found the optimal number of clusters is 4 (maybe 3)

model = KMeans(n_clusters = 4, random_state = 25)
model.fit(images)
labels = model.labels_
centroids = model.cluster_centers_
image_names = os.listdir('./data')
image_labels = dict(zip(image_names, labels))

output_folder = './output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for image_name, label in image_labels.items():
    if not os.path.exists(os.path.join(output_folder, str(label))):
        os.makedirs(os.path.join(output_folder, str(label)))
    image = Image.open(os.path.join('./data', image_name))
    image.save(os.path.join(output_folder, str(label), image_name))

# Visualize the clusters in 2D

pca = PCA(n_components=2)
bidimensional_data = pca.fit_transform(images)
print(bidimensional_data)
plt.figure(figsize=(10, 10))
for label_number in range(0, 4):
    plt.scatter(bidimensional_data[labels == label_number, 0], bidimensional_data[labels == label_number, 1], label=f'Cluster {label_number}')
centroids_2d = pca.transform(centroids)  
plt.scatter(centroids_2d[:, 0], centroids_2d[:, 1], marker='X', s=200, c='black', label='Centroids')
plt.title("KMeans Clustering")
plt.legend()
plt.show()


