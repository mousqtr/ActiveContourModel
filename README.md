# Snake segmentation

This project shows the implementation of one of the active contour segmentation methods, the "snakes" method. This method is based on the minimization of two energies: the internal energy related to the shape of the snake and the external energy dependent on the image. 

## Usage
### Clone the project
```
clone https://github.com/mousqtr/ActiveContourModel.git
```
or download and extract the .zip file

### Create and activate the virtual environment in the folder
```
python -m venv venv
venv\Scripts\activate.bat
```
### Install the libraries 
```
pip install -r requirements.txt
```
### Run the program
```
python snake.py filename
```
### Run the examples
```
python snake.py images/goutte.png
python snake.py images/finger.png
```

## Example

Original image |  Image with original snake | Image with final Snake
:----------------------:|:----------------------:|:----------------------:|
<img src="/resources/images/image1.png?raw=true" alt="original_image" style="width: 100px;"/>  |  <img src="/resources/images/image2.png?raw=true" alt="original_snake" style="width: 100px;"/> | <img src="/resources/images/final_snake.png?raw=true" alt="final_snake" style="width: 100px;"/>