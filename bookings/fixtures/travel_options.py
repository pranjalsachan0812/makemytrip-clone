import json
from datetime import datetime, timedelta

travel_types = ['Flight', 'Train', 'Bus']
sources = ['New York', 'London', 'Paris', 'Tokyo', 'Los Angeles', 'Sydney', 'Rome', 'Mumbai', 'Dubai', 'Beijing']
destinations = ['London', 'Paris', 'Tokyo', 'Bengaluru', 'Melbourne', 'Florence', 'Pune', 'Doha', 'Shanghai', 'Cape Town']

data = []
base_date = datetime(2025, 9, 1, 10, 0)

for pk in range(1, 201):
    t_type = travel_types[(pk - 1) % len(travel_types)]
    source = sources[(pk - 1) % len(sources)]
    destination = destinations[(pk * 3) % len(destinations)]
    date_time = (base_date + timedelta(days=pk // 3, hours=pk % 24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    price = 100 + (pk % 50) * 5
    available_seats = 50 + (pk % 100)

    entry = {
        "model": "bookings.traveloption",
        "pk": pk,
        "fields": {
            "type": t_type,
            "source": source,
            "destination": destination,
            "date_time": date_time,
            "price": price,
            "available_seats": available_seats
        }
    }
    data.append(entry)

with open('travel_options.json', 'w') as f:
    json.dump(data, f, indent=2)
