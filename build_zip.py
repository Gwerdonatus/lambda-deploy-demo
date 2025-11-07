import zipfile
import os

def build_zip():
    zip_name = "lambda.zip"
    with zipfile.ZipFile(zip_name, "w") as z:
        z.write("lambda_function.py")
    print(f"{zip_name} created successfully!")

if __name__ == "__main__":
    build_zip()
