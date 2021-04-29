# Web_Scraping_SOPHIE_archive
Obtener datos de la pagina [SOPHIE archive](http://atlas.obs-hp.fr/sophie/).

# [pipeline.py](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive):
Este es el código principal, al correrlo se obtendrá un archivo .csv que sera guardado en la carpeta de [data](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive/tree/main/data) con los siguientes datos:

- dates: year-month-day
- fibers: WAVE(por defeto)
- julian_day
- Radial velocity (RV): Km/s
- err_RV: Km/s

Para correr el código solo se debe poner:
>py pipeline.py

# Uso
Para comenzar, en la carpeta [extract](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive/tree/main/extract) se encuentra el archivo `config.yaml` donde estaran los links de [SOPHIE archive](http://atlas.obs-hp.fr/sophie/) de las estrellas de las que se quiere obtener los datos.

``` yaml
SOPHIE_archive:
  #url: http://atlas.obs-hp.fr/sophie/
  51_peg:
    url: http://atlas.obs-hp.fr/sophie/sophie.cgi?n=sophies&a=htab&ob=ra,seq&c=o&o=51%20peg
    table_body:
      header: table[class="datatable"] thead tr th a
      rows: table[class="datatable"] tbody tr
      view_head: div[class="cizfd"] pre
      search_ccf: table[class="datatable"] tr
```

Si desea bajar los datos de otra estrella de la pagina [SOPHIE archive](http://atlas.obs-hp.fr/sophie/) se debe colocar un nuevo nombre (de la estrella que se este escogiendo) y la url respectiva. Ejemplo:

``` yaml
  Vega:
    url: http://atlas.obs-hp.fr/sophie/sophie.cgi?n=sophies&a=htab&ob=ra,seq&c=o&o=Vega
    table_body:
      header: table[class="datatable"] thead tr th a
      rows: table[class="datatable"] tbody tr
      view_head: div[class="cizfd"] pre
      search_ccf: table[class="datatable"] tr
```

Y en el archivo `pipeline.py` coloca el nombre de la nueva estrella, en este caso 'Vega', en news_sites_uids (puede contener más de una estrella)

``` py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

news_sites_uids = ['Vega']
```

Si se desea variar los datos filtrados, ir a la carpeta [transform](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive/tree/main/transform), abrir el archivo `transform_main.py` y cambiar en el código lo que uno este pidiendo:

``` py
def _filter_data(df):
    logger.info('Data required for the final dataframe')

    # fibers = WAVE
    df = df[df['fibers'] =='WAVE']
    # sns > 70
    df = df[df['signal_to_noise'] > 70]
    # err_RV < 0.0009
    #df = df[df['err_RV'] < 0.0009]

    return df
```

# Carpeta [extract](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive/tree/main/extract)
En esta carpeta estan los archivos:
- common.py
- config.yaml
- sophie_archive_objects.py
- extract_main.py

Al correr el código 
>py extract_main.py starname

Se obtendra un archivo `starname_datetime.csv` con los datos en bruto. Donde "starname" es el nombre de la estrella que se ponga en el archivo `config.yaml`.

# Carpeta [transform](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive/tree/main/transform)
Hay un solo archivo `transform_main.py`. Si se desea correr solo este código, se enecesitara copiar el archivo .csv que se obtiene en la carpeta [extract](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive/tree/main/extract).

>py transform.py starname_datetime.csv

Se obtendra un archivo `clean_starname_datetime.csv` donde estaran ya los datos listo para su estudio.