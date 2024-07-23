<h1 align="center">
  Python cli exif cleaner
  <br>
</h1>

<h4 align="center">
    Clean exif data from your images
    <br>
</h4>

<div align="center">

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

</div>
<hr>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#how-to-use">How To Use</a>
</p>


## Features
* Clean exif information from the images
* Create json file with exif information from the original image


## How To Use
To clone and run this project, you'll need:
- [Git](https://git-scm.com)
- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)


<details>

<summary><strong>Local run from python</strong></summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/exif_cleaner.git
   ```

2. Setup poetry
   ```bash
    poetry config virtualenvs.in-project true
    poetry shell
    poetry install --only dev
	```

3. Run script
   ```bash
   python app.py [OPTIONS]
   ```

**Parameters**

| Parameter          | Type   | Description                                         | Required | Default value |
|--------------------|--------|-----------------------------------------------------|----------|---------------|
| `--input-folder`   | `str`  | Path to images folder.                              | True     | -             |
| `--output-folder`  | `str`  | Path to folder where save images without exif data. | True     | -             |
| `--create-json`    | `bool` | Create Json file with exif image data.              | False    | True          |
| `--clean-exif`     | `bool` | Clean exif from images.                             | False    | True          |


**Examples**

   ```bash
    python app.py -i pictures -o pictures
   ```


</details>


<br>
<br>
<p align="center">
  <a href="https://github.com/mrKazzila">GitHub</a> •
  <a href="https://mrkazzila.github.io/resume/">Resume</a> •
  <a href="https://www.linkedin.com/in/i-kazakov/">LinkedIn</a>
</p>
