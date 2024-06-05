## Project goal/Motivation

This project aims to develop an application that can declutter your photo library by identifying and deleting useless pictures, thereby freeing up disk space. My photo library contains many unnecessary images that could be removed. Several types of pictures could be deleted, such as duplicates, blurry photos, photographed documents, and screenshots. To narrow the project's scope, I will focus on a binary classification of two categories: screenshots and other photos.

The application addresses two main problems:

- Freeing up disk space on my phone.
- Reducing the number of photos in the library, making it easier to find relevant photos quickly.

## Project Setup

create python environment with the version 3.11.4

run "playwright install"

## Data Generation and Collection

For this project, I needed two different classes of photos: one class containing all sorts of pictures except screenshots, and the other class containing only screenshots.

Class 1: General Photos
For the first class, I used approximately 510 random pictures from the following Kaggle dataset: https://www.kaggle.com/datasets/pankajkumar2002/random-image-sample-dataset

Class 2: Screenshots
For the second class, I generated random screenshots from websites using Playwright as a web scraper. The script scrape/scrape.py visits all websites listed in the scrape/websites.txt file using a Chrome Desktop Browser and saves screenshots of each. Subsequently, the same websites are visited again using an iPhone X Browser, and screenshots are taken and saved. Finally, the script visits a website that creates fake WhatsApp chats and captures screenshots of the generated chats. Like this I am ending upt with around 310 screenshots.

run script:

```
python scrape/scrape.py
```

## Modeling

This part is descibed in the image-sweep.ipynb file

## Interpretation and Validation

This part is also descibed in the image-sweep.ipynb file

## Merge two Models

If this were to become a real application, several architectural decisions would need to be made. One of the most crucial decisions is whether the model should run on the backend server or directly in the browser/app of the consumer.

### Feedback Loop Concept

The idea is to implement a feedback loop where users provide feedback on specific photos, indicating whether they are classified correctly or incorrectly. This feedback would allow for fine-tuning the model.

### Pros and Cons of Inference on the Device

**Pros:**

- **Privacy:** No private data leaves the device.
- **Cost Optimization:** Edge computing on the device reduces server costs.

**Cons:**

- **Model Fragmentation:** Each user fine-tunes their own model, leading to fragmented improvements that do not benefit other users.

### Pros and Cons of Inference on the Server

**Pros:**

- **Unified Model:** A single model can be fine-tuned continuously with feedback from all users, leading to a more robust and accurate model.

**Cons:**

- **Privacy Concerns:** Users' private data must be sent to the server, raising potential privacy issues.
- **Increased Costs:** Maintaining and scaling server infrastructure can be costly.

### Proposed Solution

While the idea of running the model on the device is appealing due to privacy and cost benefits, it comes with the downside of individual model fine-tuning. To address this, the solution is to send the fine-tuned models back to the server. The server can then merge these individual models into a new, unified base model. This approach ensures that no private data is sent to the server only the models are. This way, users can benefit from collective improvements without compromising their privacy.

### Proof of Concept

A proof of concept for this mechanism is implemented in the `merge.ipynb` notebook, demonstrating the feasibility of merging multiple fine-tuned models into one new base model.

## Application

The application can be started with the start.sh script. Therefor just run the command ./start.sh in the terminal. The start.sh script will source the virtual environment (if the virtual environment is set up with venv in a .venv folder), build the svelte frontend and the start the flask app.

## ToDo's

- https://prankshit.com/fake-whatsapp-chat-generator.php
- Mehr Daten Sammeln
- Kommentare herausnehmen
- Kommentieren
- Dokumentieren
- pip freeze
