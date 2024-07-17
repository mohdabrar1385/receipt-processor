# Receipt Processor

This is a web service to process receipts and calculate points based on specified rules.

## Requirements

- Docker

## Running the Application

1. Build the Docker image:

    ```
    docker build -t receipt-processor .
    ```

2. Run the Docker container:

    ```
    docker run -p 8080:8080 receipt-processor
    ```

3. The application will be running on `http://localhost:8080`.

## To test the Application, use Postman

## API Endpoints

### Process Receipts

- **Endpoint:** `/receipts/process`
- **Method:** `POST`
- **Payload:** Receipt JSON
- **Response:** JSON containing an id for the receipt


### Retrieve Points for a Receipt
- **Endpoint:** '/receipts/{id}/points'
- **Method:** GET
- **Payload:** id (String)
- **Response:** JSON containing the points awarded for the receipt


## POST using Postman:

- Open Postman and set up a new request.

- Set the request type to POST.

- Enter the URL http://localhost:8080/receipts/process.

- Go to the Body tab, select raw, and choose JSON (application/json) from the dropdown.

- Paste the following JSON payload in the body section:

    ```
    {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
        ],
        "total": "35.35"
    }
    ```


## GET using Postman:

- Set up a new request in Postman.

- Set the request type to GET.

- Enter the URL http://localhost:8080/receipts/{id}/points, replacing {id} with the actual receipt ID obtained from the previous step.

- Click on Send to submit the request.

- You will receive a JSON response containing the points awarded for the specified receipt ID.
