# ShiftMate – Rota to Calendar
ShiftMate is a rota management system that uses OCR to extract shift data from rota images and convert them into downloadable calendar files or Google Calendar entries.
# Setup Instructions
## 1.  Clone the repository
Make sure you have [Git LFS](https://git-lfs.com/) installed before cloning:
```bash
git clone https://github.com/Co11eague/rota-to-calendar.git
cd rota-to-calendar
git lfs pull
```
## 2.  Set Up a Virtual Environment
Make sure you have [Python 3.8+](https://www.python.org/downloads/) installed and run:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
## 3.  Install Python Dependencies
```bash
pip install -r requirements.txt
```
## 4.  Install Frontend (Tailwind) Dependencies
Make sure you have [Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed. Then run:
```bash
npm install
```
## 5.  Build Tailwind CSS
```bash
# This builds output.css from tailwind.css (used in templates)
find . -type f -path "*/static/*/css/tailwind.css" | while read inputFile; do
  outputFile="${inputFile/tailwind.css/output.css}"
  echo "Processing: $inputFile -> $outputFile"
  npx tailwindcss -i "$inputFile" -o "$outputFile" --minify
done
```
## 6.  Create a .env File
Create a `.env` file in the project root with the following database settings:
```env
DB_NAME=shiftmate
DB_USER=root
DB_PASSWORD=labasrytas
DB_HOST=localhost
DB_PORT=5432
```
Make sure your [PostgreSQL](https://www.postgresql.org/download/) instance is running and the database exists.
## 7.  Django Settings
In `settings.py`, set:
```python
DEBUG = True
```
## 8.  Run Migration
```bash
python manage.py makemigrations
python manage.py migrate
```
## 9.  Create a Superuser
```bash
python manage.py createsuperuser
```
## 10. Start the Server
```bash
python manage.py runserver
```
Visit http://localhost:8000 in your browser.
