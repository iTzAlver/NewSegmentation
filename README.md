<p align="center">
    <img src="multimedia/logo.png">

<p align="center">
    <a href="https://github.com/iTzAlver/newsegmentation/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/iTzAlver/newsegmentation?color=purple&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/newsegmentation/tree/master/test">
        <img src="https://img.shields.io/badge/tests-passed-green?color=green&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/newsegmentation/blob/master/requirements.txt">
        <img src="https://img.shields.io/badge/requirements-pypi-red?color=red&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/newsegmentation/blob/master/README.md">
        <img src="https://img.shields.io/badge/doc-Not available-green?color=red&style=plastic" /></a>
    <a href="https://github.com/iTzAlver/newsegmentation/releases/tag/1.5.0-release">
        <img src="https://img.shields.io/badge/release-1.5.0-white?color=white&style=plastic" /></a>
</p>

# News Segmentation Package - 1.5.1

This package takes subtitle VTT files (Video Text Track files) and extracts the piece of 
news from the whole newscast inside the file. News are stored into a Tree structure with useful NLP features inside. 
The user can specify their own algorithm for segmentation, however, there are some default. 

## About ##

      Author: A.Palomo-Alonso (a.palomo@uah.es)
      Contributors: D.Casillas-Pérez, S.Jiménez-Fernández, A.Portilla-Figueras, S.Salcedo-Sanz.
      Universidad de Alcalá.
      Escuela Politécnica Superior.
      Departamento de Teoría De la Señal y Comunicaciones (TDSC).
      Cátedra ISDEFE.

## What's new?

### < 0.2.4
1. `NewSegmentation` abstract class for custom algorithms.
2. Architecture implemented.
3. `Segmentation` class for default modules.
4. Precision, Recall, F1, WD, Pk score evaluation for trees.
5. ``plot_matrix()`` method for the matrix generated.
6. ``where_is()`` method for finding pieces of news.
7. ``gtreader()`` for reading reference trees for evaluation in specific format.
8. ``Tree`` and ``Leaf`` structures.
9. Default ``PBMM`` and ``FB-BCM`` algorithms.
10. Default ``TDM``, ``DBM``, ``SDM`` implemented.
11. ``GPA`` implemented inside ``SDM``.

### 0.2.5
1. Code speed up (60% faster).
   1. Implemented cache for embeddings.
2. Data serializer implemented.
   1. Method ``save()`` implemented in Segmentation class.
   2. Function ``load3s`` implemented for reading trees from files.

### 0.2.6 - 0.2.8
1. Documentation bug fixing.
2. Logo added.

### 0.2.9
1. `Segmentation.evaluate()` now can take a path as a parameter!
2. `Segmentation.evaluate(integrity_validation=True)` now takes as default parameter `integrity_validation=True` 
for integrity validation.
> NOTE: If your custom algorithm removes sentences from the original text, you should call 
> ``integrity_validation=False`` as it checks every that every sentence is in each tree.
3. Programmed external cache file in ``Segmentation`` class taking a cache file as a new parameter: 
``Segmentation(cache_file='./myjson.json')``. This speeds up the architecture when the sentences sent to the ``LCM`` are the same. 
For instance, when testing parameters in the same database the process is around 1000% faster.
4. Bug fix: ``'.'`` not inserted when constructing payload from leafs.

### 0.3.0
1. Solved cache bugs.
2. One read and write in cache per call to the architecture.
3. Exception handler blockage for cache. Now an exception with cache won't block the architecture.
4. Best parameters found and set as default.
5. Preprocessing speed up explanation in doc.

### 0.3.1
1. Bug fixing with ```.TXT``` input files and cache.

### 0.3.2
1. Setuptools rework.
2. Updated performance image.
3. To continue: Update CITE AS to IEEE ref.

### 0.3.3 -0.3.5
1. Documentation rework.
2. Now the project is a library!

### 1.0.0
1. Deployment and bug fixing.

### 1.1.0 - 1.1.4
1. User errors and formatting handled.
2. Debugging.

### 1.2.0
1. A bug fix in ``evaluate(<gt>, show=True)`` where the correct segmentation and the performed segmentation switches places
in the plot representation.

### 1.2.1
1. Included logging library instead of print logging information.
2. Try - except clause for googletrans module. Now you can omit it.

### 1.4.5
1. Upated numpy incoherence update. Bug fixing.

### 1.5.0
1. Bug fixing. Added a new parameter to the constructor of the ``Segmentation`` class.
2. Added wikipedia experiments in the ``/experiments`` folder.
3. Added unit tests in the ``/tests`` folder.


## Architecture

The whole architecture and algorithms are described in depht in [this paper](https://???) or in 
[this master thesis](https://???).\
The architecture takes advantage of three main features in order perform news segmentation:
* Temporal distance: Is the distance (measured in jumps) between different pieces of text inside the VTT file.
* Spatial distance: Is the distance (measured in slots) between different pieces of text inside the VTT file.
* Semantic correlation: Is the correlation between the meaning of the sentences of two different pieces of text.

This architecture works with a _correlation matrix_ formed by the semantic correlation between each sentence 
in the news broadcast. Each module modifies the correlation matrix in order to apply temporal / spatial features 
reflected in the matrix. The algorithms shall be able to identify each piece of news inside the matrix.
Three differentiated modules make up the architecture:

* **Database Transformer (DT)**: Takes the original VTT file and converts it to plain text sentences (TXT) with time jumps specified 
at the beginning of each sentence and a temporal information vector at the end pointing the temporal 
length of each sentence measured in seconds. 
* **Specific language model (SLM)**: This module takes the blocks of text as input and outputs the semantic correlation 
between each block of text arranged into a _correlation matrix_.
* **Temporal Distance Manager (TDM)**: This module takes the temporal jumps as input and modifies the initial correlation matrix
depending on the temporal jumps.
* **Spatial Distance Manager (SDM)**: This module implements an algorithm which identifies boundaries between 
consecutive pieces of text and merges it.
* **Late correlation manager (LCM)**: This module implements an algorithm which identifies 
high semantic correlation between separate pieces of text and merges it.

The user can implement their own algorithms depending on their application.\

<p align="center">
    <img src="multimedia/model.png">

The results are stored into a Tree structure with different fields representing different features from 
the piece of news.
* **Payload**: defines the whole text of the piece of news, it involves all sentences related to a same piece of news combined into a single piece of text. It can be defined as a text structure.
* **Embedding**: it is a vector of real numbers which define a semantic representation of the payload. In this model, it is the output of the SLM, output of the specific language model. It can be defined as a high dimensional vector of real numbers. This embedding is stored for computational efficiency reasons, as some models may take long time to compute.
* **ID**: it is a natural number defining the tree identity, this number must be unique for each tree in the results' storage. It can be defined as a natural number. 
* **Time information**: it is a vector containing the whole temporal length of the piece of news. It can be defined as a real positive number.
* **Correlation power (CP)**: it is a real number indicating how correlated the sentences of the leafs are within the tree. This number can become very interesting when studying the reliability of algorithms. It can be defined as a real positive number.
Where M is the size of R1+K and R is, in our architecture, the very last output matrix R1+K. This function does not take into account the main diagonal of the correlation matrix as it does not provide any information about the correlation between sentences. The correlation power is defined on the (0, 1) interval, meaning 0 no correlation between any sentence in the tree and 1 meaning absolute correlation between all the sentences within the tree. This measurement helps to evaluate the reliability of the model.

<p align="center">
    <img src="multimedia/eqp.png">




* **Reference**: when several trees share the same results storage system, it is convenient to define a group of trees which make reference to a group. For example, if an analysis for several days when some piece of news can be repeated and those trees are lately merged into a subsequent tree, it is convenient to reference the day those trees belongs to. It can be done by its reference field, and it can be defined as a natural number. 
* **Leafs**: this structure stores information about the initial state of the model. Each leaf stores a unique _ID_ value and a _Payload_ value containing the minimum text size element considered; in this architecture this element is a sentence, but a single word or any group of words could be also considered.

<p align="center">
    <img src="multimedia/tree.png">


## Usage

First, install the python package. After this, you can use your ``VTT`` files to get the 
news. Any other type of file can be considered, but the user must implement their own database
transformer according to the file and language used. Spanish news segmentation is the default model.

### Install:

You can install the package via pip:

    pip install newsegmentation -r requirements.txt

If any error occurred, try installing the requirements before the installation:

    numpy
    matplotlib
    googletrans == 4.0.0rc1
    sentence_transformers >= 2.2.0
    sklearn
    nltk

### Basic Usage:

In this demo, we extract the news inside the first 5 minutes of the ``VTT`` file:

    $ python
    >>> import newsegmentation as ns
    >>> myNews = ns.Segmentation(r'./1.vtt')
    >>> print(myNews)

    NewsSegmentation object: 8 news classified.

    >>> myNews.info()

    News segmentation package:
    --------------------------------------------
    FAST USAGE:
    --------------------------------------------
    PATH_TO_MY_FILE = <PAHT>
    import newsegmentation as ns
    news = ns.NewsSegmentation(PATH_TO_MY_FILE)
    for pon in news:
        print(pon)
    --------------------------------------------

    >>> myNews.about()

    Institution:
    ------------------------------------------------------
    Universidad de Alcalá.
    Escuela Politécnica Superior.
    Departamento de Teoría De la Señal y Comunicaciones.
    Cátedra ISDEFE.
    ------------------------------------------------------
    Author: Alberto Palomo Alonso
    ------------------------------------------------------

    >>> for pieceOfNews in myNews:
    >>>     print(pieceOfNews)

    No hay descanso. Desde hace más de 24 horas se trabaja sin tregua para encontrar a Julen. El niño de 2 años se cayó en un pozo en Totalán, en Málaga. Las horas pasan, los equipos de rescate luchan contrarreloj y buscan nuevas opciones en un terreno escarpado y con riesgo de derrumbes bajo tierra. Buenas noches. Arrancamos este Telediario, allí, en el lugar del rescate. ¿Cuáles son las opciones para encontrar a Julen? Se trabaja en 3 frentes retirar la arena que está taponando el pozo de prospección. Excavar en 2 pozo, y abrir en el lateral de la montaña
    El objetivo rescatar al pequeño. El proyecto de presupuestos llega al Congreso. Son las cuentas con más gasto público desde 2010 Destacan más partidas para programas sociales, contra la pobreza infantil o la dependencia, y también el aumento de inversiones en Cataluña. El gobierno necesita entre otros el apoyo de los independentistas catalanes que por ahora mantienen el NO a los presupuestos, aunque desde el ejecutivo nacional se escuchan voces más optimistas
    La familia de Laura Sanz Nombela, fallecida en París por una explosión de gas espera poder repatriar su cuerpo este próximo miércoles. Hemos hablado con su padre, que está en Francia junto a su yerno y nos ha contado que se sintieron abandonados en las primeras horas tras el accidente. La guardia civil busca en una zona de grutas volcánicas de difícil acceso el cuerpo de la joven desaparecida en Lanzarote, Romina Celeste. Su marido está detenido en relación con su muerte aunque él defiende que no la mató, que solo discutieron y que luego se la encontró muerta la noche de Año Nuevo
    Dormir poco hace que suba hasta un 27 por ciento el riesgo de enfermedades cardiovasculares
    Es la conclusión de un estudio que ha realizado durante 10 años el Centro Nacional para estas dolencias
    Y una noticia de esta misma tarde de la que estamos muy pendientes: Un tren ha descarrilado esta tarde cerca de Torrijos en Toledo sin causar heridos. Había salido de Cáceres con dirección a Madrid. Los 33 pasajeros han sido trasladados a la capital en otro tren. La circulación en la vía entre Madrid y Extremadura está interrumpida. Renfe ha organizado un transporte alternativo en autobús para los afectados
    A 15 días de la gran gala de los Goya hoy se ha entregado ya el primer premio. La cita es el próximo 2 de febrero en Sevilla, pero hoy, aquí en Madrid, en el Teatro Real gran fiesta de los denominados a los Premios Goya. Solo uno de ellos se llevará hoy su estatuilla. Chicho Ibáñez Serrador consigue el Premio Goya de Honor por toda una vida dedicada al cine de terror
    Y en los deportes Nadal gana en Australia, Sergio

    >>> myNews.plotmtx()
<p align="center">
   <img src="multimedia/mtx.png">

### Finding news from text:

You can also find information inside the news using the method ``whereis()``:
    
    >>> myNews.whereis('Nadal')

    [7]

    >>> myNews.whereis('2')

    [0, 1, 3, 6]

### Evaluate performance:

If you can create a tree from any ground truth database, this package also has a method por evaluation:
    
First, you have to import a custom ground truth / golden data tree with ``gtreader()``:

    >>> from newsegmentation import gtreader
    >>> myGt = gtreader('path.txt')
    
Then evaluate the news with the reference, use the argument ``evaluate(ref, show=True)`` to plot some graphics about the evaluation:

    >>> myNews.evaluate(myGt, show=True)
  
<p align="center">
    <img src="multimedia/evaluation.png">


### Save and load trees:
This package defines a data structure called news trees, this format is parsed by the code via parsers:

    >>> save_file = './testing' # or save_file = './testing.3s'
    >>> myNews.save(save_file)
    >>> sameNews = ns.load3s(save_file)
    >>> results = myNews.evaluate(sameNews)
    >>> print(results)

    {'Precision': 1.0, 'Recall': 1.0, 'F1': 1.0, 'WD': 0.0, 'Pk': 0.0}

This saves the trees generated (not the ``Segmentation`` instance) inside a ``.3s`` file given as a parameter. 

### Speeding up process:
If you want to run the same database several times (for algorithm design, parameter testing or other reasons) you should
use the cache serialization system. This system stores into a ``.json`` file all the embeddings generated in the ``SLM``. 
If any sentence is repeated, the system will not compute the embeddings again. All sentences computed in the ``SLM`` are 
stored into the ``cache_file`` if provided. Here is an example of speeding up process:

      >>> import time
      >>>
      >>> myDatabase = ['./1.vtt', './2.vtt', './3.vtt']
      >>> cache_file = './cache.json'
      >>> lcm_parameters = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
      >>> ellapsed_time = list()
      >>>
      >>> for parameter in lcm_parameters:
      >>>   initial_time = time.perf_counter()
      >>>   for news in database:
      >>>      myNews = ns.Segmentation(news, lcm=(parameter,), cache_file=cache_file)
      >>>   ellapsed_time.append(time.perf_counter() - initial_time)
      >>>
      >>>   [print(f'{i + 1} iteration: {seconds} seconds.') for i, seconds in enumerate(ellapsed_time)]

      1: iteration 89.23 seconds.
      2: iteration 9.28 seconds.
      3: iteration 8.91 seconds.
      4: iteration 12.2 seconds.
      5: iteration 7.22 seconds.
      6: iteration 13.9 seconds.

If any further speed up is needed. The model reads the original files ``(.VTT)`` and stores it as temporal ``.TXT`` files. If the 
model is reading continuously this files, it is better to process the ``.VTT`` files to ``.TXT`` once, store it, and give the model the ``.TXT`` files instead. 
This skips the first preprocessing step in every iteration. You can do something similar to this:

      >>> in_files = ['./1.vtt', './2.vtt', './3.vtt', './4.vtt', './5.vtt']
      >>> txt_files = [default_dbt(vtt_file) for vtt_file in in_files]
      >>> times = 200
      >>> for i in range(times):
      >>>   for txt_file in txt_files:
      >>>      myNews = ns.Segmentation(txt_file)

This method speeds slightly up the process, and it is only adequate if the file is going to be transformed more than once.

### Custom Algorithms:

Implement the abstract class ``NewSegmentation`` for implementing custom algorithms, use this demo as a template:

    import newsegmentation as ns

    class MySegmentation(ns.NewsSegmentation):
        @staticmethod
        def _spatial_manager(r, param):
            # return ns.default_sdm(r, param)
            return myown_sdm(r, param)
    
        @staticmethod
        def _specific_language_model(s):
            # return ns.default_slm(s)
            return myown_slm(s)
    
        @staticmethod
        def _later_correlation_manager(lm, s, t, param):
            # return ns.default_lcm(lm, s, t, param)
            return myown_lcm(lm, s, t, param)
    
        @staticmethod
        def _database_transformation(path, op):
            # return ns.default_dbt(path, op)
            return myown_dbt(path, op)

Note that _``ns.default_xxx``_ is the default manager for the architecture and can be replaced by your own functions. 
Take into account the following constraints before implementing your own module managers:

* SDM: Takes as input the correlation matrix (r) and the algorithm parameters (param). It returns a list of integers 
pointing the index of the block in (r) where each pieces of news start.
* SLM: Takes as input the list of sentences and returns the embeddings of the sentence. For further information about 
word embeddings check the master thesis cited.
* LCM: Takes as input the SLM function reference (lm), the list of sentences (s), the temporal information vector (t) 
and the algorithm parameters (param). It returns (rk, sk, tk): the very last correlation matrix (rk), the last blocks of
text (sk) and their corresponding temporal information (tk). Note that you don't need to manage the embeddings, the SLM works on that job.
* DT: Takes as input (path) the path of the VTT file and the requested output path (op) returns the actual output path.
Note that the architecture creates temporary TXT files for reading the news from the DT.
## Performance

Comparing two different algorithms inside the architecture. LGA is a kernel-based algorithm with cellular automation techniques. PBMM algorithm is 
the default algorithm and has better F1 score performance and reliability. This is tested over Spanish news broadcast database with 10 files.

<p align="center">
    <img src="multimedia/perf.png">

### Cite as:
~~~
@<not_available_yet>{palomo2022alonso,
  title={A Flexible Architecture using Temporal, Spatial and Semantic
Correlation-based algorithms for Story Segmentation of Broadcast News},
  author={A.Palomo-Alonso, D.Casillas-Pérez, S.Jiménez-Fernández, A.Portilla-Figueras, S.Salcedo-Sanz},
  year={2022}
}
~~~