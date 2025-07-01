import os
import pandas as pd
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import UploadedFile
from collections import defaultdict


def load_files_from_directory():
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    for fname in os.listdir(upload_dir):
        fpath = os.path.join(upload_dir, fname)
        if not os.path.isfile(fpath):
            continue

        if not (fname.endswith(".csv") or fname.endswith(".xls") or fname.endswith(".xlsx")):
            continue

        if not UploadedFile.objects.filter(title=fname).exists():
            UploadedFile.objects.create(title=fname, path=fpath)

from collections import defaultdict

def home(request):
    upload_dir = os.path.join("media", "uploads")
    files = os.listdir(upload_dir)
    files = [f for f in files if f.endswith(".csv") or f.endswith(".xlsx")]

    grouped = defaultdict(dict)

    for f in files:
        base = f.replace(".csv", "").replace(".xlsx", "")
        if f.endswith(".csv"):
            grouped[base]['csv'] = f
        elif f.endswith(".xlsx"):
            grouped[base]['xlsx'] = f

    grouped_list = [
        {"date": k, "csv": v.get("csv"), "xlsx": v.get("xlsx")}
        for k, v in sorted(grouped.items(), reverse=True)
    ]

    return render(request, "blog/home.html", {"files": grouped_list})
def view_file(request, filename):
    full_path_csv = os.path.join("media", "uploads", f"{filename}.csv")
    full_path_xlsx = os.path.join("media", "uploads", f"{filename}.xlsx")

    if os.path.exists(full_path_csv):
        df = pd.read_csv(full_path_csv)
    elif os.path.exists(full_path_xlsx):
        df = pd.read_excel(full_path_xlsx)
    else:
        return render(request, "blog/error.html", {"message": "File not found."})

    table_html = df.to_html(classes='table', index=False)
    return render(request, "blog/view_file.html", {
        "filename": filename,
        "table_html": table_html
    })