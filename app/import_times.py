import csv
from app.database import SessionLocal, engine
from app import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# REFERENCE: Code adpated from ChatGPT to store data into the database
# https://chatgpt.com/share/69b54fb1-2280-8002-a596-48be67cd2803
csv_file_path = "data.csv"

try:
    with open(csv_file_path, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        count = 0

        for row in reader:
            performance = models.Performance(
                rank=int(row["Rank"]) if row["Rank"] else None,
                time=row["Time"],
                name=row["Name"],
                country=row["Country"],
                date_of_birth=row["Date of Birth"],
                place=int(row["Place"]) if row["Place"] else None,
                city=row["City"],
                date=row["Date"],
                gender=row["Gender"],
                event=row["Event"]
            )

            db.add(performance)
            count += 1

        db.commit()
        print(f"Successfully imported {count} performances.")

except FileNotFoundError:
    print(f"File not found: {csv_file_path}")

except Exception as e:
    db.rollback()
    print(f"An error occurred: {e}")

finally:
    db.close()
