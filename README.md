conda env create -f environment.yml

conda activate linkedin-generator

cp .env.example .env

python app.py
