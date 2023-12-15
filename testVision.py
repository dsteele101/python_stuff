import os
import csv
import base64
import requests


api_key = ""


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


image_folder = "/Users/dsteele/Documents/Clients/Group1/pics/"

output_csv = "output.csv"

image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f)) and not f.startswith('.')]

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

with open(output_csv, mode='w', newline='') as csv_file:
  csv_writer = csv.writer(csv_file)

  header = ["CAR_MAKE", "CAR_MODEL", "CAR_YEAR", "EXTERIOR_COLOR", "INTERIOR_COLOR", "ENGINE_TYPE", "ENGINE_CYLINDERS",
            "ENGINE_HORSEPOWER", "ENGINE_DISPLACEMENT", "TIRES", "SUNROOF", "PERFORMANCE_FEATURES", "EXTERIOR_FEATURES",
            "INTERIOR_FEATURES", "SAFETY_FEATURES", "TECH_FEATURES", "WARRANTY", "MAINTENANCE", "MSRP", "RETAIL_PRICE",
            "MPG_COMBINED", "MPG_CITY", "MPG_HIGHWAY", "FUEL_ECONOMY_RATING", "SMOG_RATING", "SAFETY_SCORE_OVERALL",
            "SAFETY_SCORE_FRONTAL", "SAFETY_SCORE_SIDE", "SAFETY_SCORE_ROLLOVER", "DEALER_NAME", "DEALER_ADDRESS"]

  csv_writer.writerow(header)

  for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)

    base64_image = encode_image(image_path)

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "You are going to be given a car sticker. Do only one thing. Based on the following SQL column names, CAR_MAKE, CAR_MODEL, CAR_YEAR, EXTERIOR_COLOR, INTERIOR_COLOR, ENGINE_TYPE, ENGINE_CYLINDERS, ENGINE_HORSEPOWER, ENGINE_DISPLACEMENT, TIRES, SUNROOF, PERFORMANCE_FEATURES, EXTERIOR_FEATURES, INTERIOR_FEATURES, SAFETY_FEATURES, TECH_FEATURES, WARRANTY, MAINTENANCE, MSRP, RETAIL_PRICE, MPG_COMBINED, MPG_CITY, MPG_HIGHWAY, FUEL_ECONOMY_RATING, SMOG_RATING, SAFETY_SCORE_OVERALL, SAFETY_SCORE_FRONTAL, SAFETY_SCORE_SIDE, SAFETY_SCORE_ROLLOVER, DEALER_NAME, DEALER_ADDRESS, extract data from the car sticker and associate that data with the given column names. Only provide the data requested and do not provide commentary. If an electric car, return the eMPG values given as MPG. Engine details are likely under the performance section. ENGINE_TYPE values can be gas, electric, or hybrid. If a value is not specified, fill it in as NULL. List all of the features and do not say etc. Return the features as a comma separated list."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 4096
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())

    json_res = response.json()
    content = json_res['choices'][0]['message']['content']
    content_dict = {}
    for item in content.split("\n"):
      key, value = item.split(": ", 1)
      content_dict[key] = value

    csv_writer.writerow([content_dict.get(header_item, "NULL") for header_item in header])

print(f"Results written to {output_csv}")
