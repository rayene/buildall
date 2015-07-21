# buildall
[![Build Status](https://travis-ci.org/rayene/buildall.svg?branch=master)](https://travis-ci.org/rayene/buildall)
[![Coverage Status](https://coveralls.io/repos/rayene/buildall/badge.svg?branch=master&service=github)](https://coveralls.io/github/rayene/buildall?branch=master)

Presentation
============
Buildall is an easy to use pipeline building tool. You may need it if you have
long running tasks that you want to :

1. run once and avoid running them again if their dependencies did not change.
2. parallelize (not implemented yet)

Examples of tasks :
- Downloading a file
- Decompressing a file
- Copying a file
- Any shell command
- Any python function (not implemented yet)

Why a new tool ?
================
Because all the Python build tools available but, as far as I've seen, their
learning curve is too steep. It takes a lot of time and efforts to be able
to achieve simple tasks. Buildall is simple !

Buildall offers the same interface as Python's standard library classes

1/ pathlib.Path for object oriented file manipulation
2/ subprocess.Popen for lanching external programs

If you already know how these classes are used, you have 80% of the knowledge
necessary to build a pipeline with buildall.

How to use it ?
===============
The pipeline construction is graphical. For example, if a TaskA has a
dependency on TaskB, your pipeline will look like this :
```python
pipeline = TaskA << TaskB
pipeline.make()
```
If TaskA depends on both TaskB and TaskC, it looks like this :
```python
pipeline = TaskA << TaskB + TaskC
pipeline.make()
```

If you want to run the pipeline in parallel. Set the parallel parameter to
True. TaskB and TaskC will be lanched at the same time (not implemented yet).
```python
pipeline = TaskA << TaskB + TaskC
pipeline.make(parallel=True)
```

Example
=======

Downloading a movie and a movie player :


```python
movie_url = 'http://example.com/movie.avi'
player_url = 'http://example.com/movie_player.tar.bz2'
download_movie = buildall.Download(url=movie_url, destination='movie.avi')
download_movie_player = buildall.Download(url=player_url,
                                    destination='movie_player.tar.bz2')
decompress_movie_player= buildall.Decompress(destination='movie_player')
play_movie = buildall.Popen('movie_player movie.avi', shell=True)

pipeline = play_movie << download_movie + (decompress_player << download_player)

# Now, the pipeline is ready. We can call the run() method
pipeline.run()  # Will last for a while.


# When we run the pipeline for the first time, all the tasks are triggered. This
may take some time. But if you run() it again, it is immediate.
pipeline.run()  # Very fast since nothing changed

All intermediate files are kept and checked at every run. For example, if we delete
the movie_player.tar.bz2 file, it will be redownloaded and decompressed.
Path('movie_player.tar.bz2').unlink()
pipeline.run()  # Re-downloads the movie player archive and decompresses it.
```

Status
======
Buildtool is still in its early development.

Requirements
============
Python 3.4.
