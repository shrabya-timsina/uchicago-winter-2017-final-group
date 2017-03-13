Beer Suggestion Project by Sandeep Malladi, Shrabya Timsina, and Luis Buenaventura

some main project files are:
    crawler.py
    data_analysis.py
    data_process.py
    views.py 

in django/mysite 
and in django/mysite/beer-suggester

To improve vector analysis speed (for user profile comparisons), we stored the user vectors (aggregated by style, normalized with ratings) in a csv.

files like selenium_automation.py and beer_dict.json were functioning parts of various methods
we attempted but ultimately did not use in the final product due to issues we initially did not forsee.


Versions of modules used:
BeautifulSoup: 4.5.3
Sqlite3: 2.6.0
Json: 2.0.9
Pandas: 0.19.1
Sklearn: 0.18.1

#### DJANGO ###### 
Django version: 1.9.4
To run the django interface, run the following command in the terminal in the django/mysite path 
    python3 manage.py runserver

#### SELENIUM ######
Selenium version: 3.0.2
Firefox version: 51.0.1 (64-bit)
Firefox geckodriver is included in submission
to see how our selenium code worked:
1. run the following on terminal:
   export PATH=$PATH:/home/student/team-cs122-project
2. run selenium.py on ipython3
3. type demo_for_graders() and press enter

