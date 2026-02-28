import json
import logging

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from .documents import ItemDocument

logger = logging.getLogger(__name__)

import json
import logging

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

import logging

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def product_catalog_view(request):
    query = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", 1))
    per_page = 25  # items per page

    start = (page - 1) * per_page
    end = start + per_page

    schema = connection.schema_name
    index_name = f"{schema}_items"

    try:
        search = ItemDocument.search(index=index_name)

        if query:
            search = search.query(
                "multi_match",
                query=query,
                fields=["name^3", "sku"],
                type="phrase_prefix",
            )
        else:
            search = search.query("match_all")

        # 🔥 Apply pagination
        search = search[start:end]

        response = search.execute()

        total_count = response.hits.total.value

        product_list = [
            {
                "id": hit.id,
                "name": hit.name,
                "price": float(hit.price),
                "sku": hit.sku,
            }
            for hit in response
        ]

    except Exception as e:
        logger.error(f"Elasticsearch error: {e}")
        product_list = []
        total_count = 0

    if (
        request.GET.get("ajax") == "1"
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        return JsonResponse(
            {
                "products": product_list,
                "total": total_count,
                "page": page,
                "per_page": per_page,
            }
        )

    return render(
        request,
        "tenant_app/catalog.html",
        {
            "products": product_list,
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
        },
    )
