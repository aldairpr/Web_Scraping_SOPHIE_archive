# Web_Scraping_SOPHIE_archive
Obtener datos de la pagina [SOPHIE archive](http://atlas.obs-hp.fr/sophie/) page

# [pipeline.py](https://github.com/aldairpr/Web_Scraping_SOPHIE_archive):
Este es el código principal, al correrlo se obtendrá un archivo .csv que sera guardado en la carpeta de 'data' con los siguientes datos.

# Datos de la tabla que se obtendra
- Dates: year-month-date
- fibers: WAVE(por defeto)
- julian_day
- Radial velocity (RV): Km/s
- err_RV: Km/s

# Uso
Al comenzar en la carpeta extract en config.yaml estaran los links de las estrellas de las que se quiere obtener los datos.
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
Si desea bajar los datos de otra estrella de la pagina [SOPHIE archive](http://atlas.obs-hp.fr/sophie/) colocar un nuevo nombre(el de la estrella que se este escogiendo) y la url respectiva. Ejemplo:
``` yaml
  Vega:
    url: http://atlas.obs-hp.fr/sophie/sophie.cgi?n=sophies&a=htab&ob=ra,seq&c=o&o=Vega
    table_body:
      header: table[class="datatable"] thead tr th a
      rows: table[class="datatable"] tbody tr
      view_head: div[class="cizfd"] pre
      search_ccf: table[class="datatable"] tr
```
Y en el archivo pipeline.py coloca el nombre de la nueva estrella, en este caso 'Vega', en news_sites_uids (en esta puede ir más de una estrella)
``` py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

news_sites_uids = ['Vega']
```
Si se desea variar los datos filtrados, ir a la carpeta 'transform', abrir el archivo transform_main.py y cambiar en el código lo que uno quiera obtener:
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
...