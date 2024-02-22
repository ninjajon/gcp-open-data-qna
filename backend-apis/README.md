# Deploy cloud run
gcloud run deploy csm-demo --source . --project rl-llm-dev --region us-central1
--no-traffic --tag v1.x

# Create eventarc for Pubsub + Search
gcloud eventarc triggers create trigger-unstructured-search \
    --destination-run-service=csm-demo \
    --destination-run-path=trigger-unstructured-search \
    --destination-run-region=us-central1 \
    --location=us-central1 \
    --event-filters="type=google.cloud.pubsub.topic.v1.messagePublished" \
    --transport-topic=projects/rl-llm-dev/topics/website-search

# Create eventarc for Pubsub + Recommendations
gcloud eventarc triggers create trigger-unstructured-recommendations \
    --destination-run-service=csm-demo \
    --destination-run-path=trigger-unstructured-recommendations \
    --destination-run-region=us-central1 \
    --location=us-central1 \
    --event-filters="type=google.cloud.pubsub.topic.v1.messagePublished" \
    --transport-topic=projects/rl-llm-dev/topics/website-recommendations


# Run FastAPI locally
docker run -e GOOGLE_APPLICATION_CREDENTIALS=/credentials/rl-llm-dev.json -v /home/renatoleite/workspace/customer-services-modernization/backend-apis/app:/code/app -v /home/renatoleite/workspace/credentials:/credentials -p 8501:8080 gcr.io/rl-llm-dev/csm-demo

# Search with custom embeddings

Multimodal search
0. Prepare the dataset (text, image and metadata) to extract embeddings
1. Extract embeddings with Gecko Multimodal using text and/or image
2. Create search datastore with grounding (citation, summary, snippets)
3. Create API to automatically extract the embedding and upload to Vertex AI Search datastore
4. Create API to search using multimodal (image + text)

# Upload image from UI
f1) Categorize the product
    .Use Vision API to return categories
    .Use product Q&A to extract categories
    .Display similar products and ask the user to find relevant category
f2) Assign attributes and describe the image. Find similar products and use their attributes.
    .Use Vision API to return categories
    .Use product Q&A to extract categories
    .Display similar products and ask the user to find relevant category
f3) Create content for the title and description from the attributes and category.
f4) Translate content into multiple languages.
f5) Edit the image with a canvas or a prompt.
f6) Generate new images based on this, changing with a prompt. User can add these images to the catalog
f7) Bulk upload

This task is to assign a category to the product in the image. This category will be used in a retail website.
Example: chairs > gaming chair


# Deployment Script

1) Create SQL Server (MySQL)
1.1) Load SQL data to DB

2) Create Vertex Search
2.1) Load data

3) Create Vertex Vector Search
3.1) Load data

4) Create Recommendation AI
4.1) Load data
4.2) Load events

5) Deploy to AppEngine
