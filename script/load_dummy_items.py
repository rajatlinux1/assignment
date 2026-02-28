import os
import re
import sys

import django
from faker import Faker
from tqdm import tqdm

# ------------------ DJANGO SETUP ------------------ #
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project.settings")
django.setup()

from tenant_schemas.utils import schema_context

from customers.models import Client

# ------------------ IMPORT MODELS ------------------ #
from tenant_app.models import Item

fake = Faker()


def get_last_index():
    """
    Safely get last SKU numeric index.
    """
    last_item = Item.objects.order_by("-id").only("sku").first()

    if not last_item or not last_item.sku:
        return 0

    number_part = re.sub(r"\D", "", last_item.sku)
    return int(number_part) if number_part else 0


def main(count: int, schema_name: str) -> None:
    with schema_context(schema_name):

        last_index = get_last_index()
        batch_size = 1000
        items_batch = []

        for i in tqdm(range(1, count + 1), desc="Creating items"):
            items_batch.append(
                Item(
                    name=f"{fake.word().capitalize()} {fake.word().capitalize()}",
                    sku=f"SKU{(last_index + i):05d}",
                    price=round(
                        fake.pyfloat(left_digits=3, right_digits=2, positive=True),
                        2,
                    ),
                )
            )

            # Insert in batches (memory efficient)
            if len(items_batch) >= batch_size:
                Item.objects.bulk_create(items_batch, batch_size=batch_size)
                items_batch.clear()

        # Insert remaining
        if items_batch:
            Item.objects.bulk_create(items_batch, batch_size=batch_size)

        print(f"\nFinished. Created {count} Item records.")


# ------------------ CLI ENTRY ------------------ #
if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.exit("Usage: python load_dummy_items.py <schema_name> <count>")

    schema_name = sys.argv[1]
    count = int(sys.argv[2])  # ✅ FIXED (convert to int)

    if not Client.objects.filter(schema_name=schema_name).exists():
        sys.exit("Schema not found.")

    main(count, schema_name)
