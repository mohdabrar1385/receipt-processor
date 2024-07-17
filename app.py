from flask import Flask, request, jsonify
import uuid
import math

app = Flask(__name__)

# Dictionary to store receipt points by their IDs
receipt_points_store = {}

def calculate_receipt_points(receipt):
    """
    This function calculates points awarded to a receipt based on defined rules.

    Args:
    - receipt (dict): It takes one argument that has receipt data containing retailer, purchaseDate, purchaseTime, items, and total.

    Returns:
    - int: Returns the total points awarded for the receipt.
    """
    # Initially total points are zero
    total_points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name
    retailer_name = receipt['retailer']
    total_points += sum(c.isalnum() for c in retailer_name)

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total_amount = float(receipt['total'])
     if total_amount.is_integer():
         total_points += 50
    # if abs(total_amount - round(total_amount)) < 0.01:
    #     total_points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if total_amount % 0.25 == 0:
        total_points += 25

    # Rule 4: 5 points for every two items on the receipt
    num_items = len(receipt['items'])
    total_points += (num_items // 2) * 5

    # Rule 5: Points for item descriptions
    # If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer. 
    # The result is the number of points earned.
    for item in receipt['items']:
        description_length = len(item['shortDescription'].strip())
        if description_length % 3 == 0:
            total_points += math.ceil(float(item['price']) * 0.2)

    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = receipt['purchaseDate']
    purchase_day = int(purchase_date.split('-')[2])
    if purchase_day % 2 == 1:
        total_points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = receipt['purchaseTime']
    purchase_hour = int(purchase_time.split(':')[0])
    purchase_minute = int(purchase_time.split(':')[1])
    if (purchase_hour == 14 and purchase_minute > 0) or (purchase_hour == 15):
        total_points += 10



    # Return the total points calculated/awarded
    return total_points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """
    This is an Endpoint to submit a receipt for processing and calculate points.

    It Expects a JSON payload with retailer, purchaseDate, purchaseTime, items, and total.
    Returns a JSON response with an ID for the receipt.

    Returns: 
    It return a JSON id or error based on success or not
    - JSON: {"id": receipt_id} if successful, or {"error": "Invalid receipt"} if missing required fields.
    """
    receipt_data = request.json

    # Check for required fields in the received JSON
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    for field in required_fields:
        if field not in receipt_data:
            return jsonify({"error": "Invalid receipt"}), 400

    # Generate a unique ID for the receipt
    receipt_id = str(uuid.uuid4())

    # Calculate points awarded for the receipt
    points_awarded = calculate_receipt_points(receipt_data)

    # Store the receipt ID with its awarded points
    receipt_points_store[receipt_id] = points_awarded

    # Return the receipt ID as JSON response
    return jsonify({"id": receipt_id}), 200

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_receipt_points(receipt_id):
    """
    Endpoint to retrieve points awarded for a specific receipt ID.

    Args:
    - receipt_id (str): ID of the receipt to retrieve points for.

    Returns:
    - JSON: {"points": points_awarded} if receipt found, or {"error": "Receipt not found"} if not found.
    """
    # Retrieve points awarded for the given receipt ID
    points_awarded = receipt_points_store.get(receipt_id)

    # Return JSON response with points awarded or error if receipt ID not found
    if points_awarded is None:
        return jsonify({"error": "Receipt not found"}), 404
    return jsonify({"points": points_awarded}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
