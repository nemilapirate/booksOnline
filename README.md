booksOnline
Premier projet en python sur booksOnline

Projet: 
Créer une application python exécutable à la demande visant à récupérer les prix au moment de l'exécution de cette appli.

Dans un premier temps récupèration des données une page (un livre) du site http://books.toscrape.com/ et extraire les données vers un fichier CSV. 
Nom de l'application : scraping_one.py
Noms de données extraite dans le fichier CSV.

      - product_page_url
      - universal_ product_code (upc)
      - title
      - price_including_tax
      - price_excluding_tax
      - number_available
      - product_description
      - category
      - review_rating
      - image_url

Ensuite avec une autre appli, on récupère les données de tous les livres d'une catégorie du site http://books.toscrape.com/ vers un fichier CSV. 
Nom de l'application : scraping_category.py
Noms de données extraite dans le fichier CSV.

      - product_page_url
      - universal_ product_code (upc)
      - title
      - price_including_tax
      - price_excluding_tax
      - number_available
      - product_description
      - category
      - review_rating
      - image_url
   
Enfin on récupère toutes les catégories et tous les livres du site http://books.toscrape.com/ vers des fichiers CSV distinct par catégories. 
Nom de l'application : scraping_all_books.py
Les images sont elles dans un dossier à part. 
Noms de données extraite dans le fichier CSV.

      - product_page_url
      - universal_ product_code (upc)
      - title
      - price_including_tax
      - price_excluding_tax
      - number_available
      - product_description
      - category
      - review_rating
      - image_url

----------------------------------------

Pour cloner le projet des applications sur github :

      https://github.com/nemilapirate/booksOnline.git

----------------------------------------

Il vous faudra installé Python et y acceder via le terminal.
Pour installer la dernière version de Python :

      https://www.python.org/downloads/
 
 ---------------------------------------

Pour l'environnement virtuel et installer les dépendances: 

      pip install -r requirements.txt 
      

Pour ouvrir l'environnement : 

      cd booksOnline/env/Scripts/activate

----------------------------------------

Site web à scraper : 

      http://books.toscrape.com

----------------------------------------

Pour executer le scraping : 

Première étape :
python scraping_one.py

Deuxième étape :
python scraping_category.py

troisième étape :
python scraping_all_books.py
