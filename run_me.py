from flask import Flask, render_template, send_from_directory, request, redirect
from zipfile import ZipFile
import cv2
import base64
import os
import shutil





app = Flask(__name__)

def clearOldImgFolder()->None:
    shutil.rmtree("assets/img/scenery")
    os.mkdir("assets/img/scenery")
    return

def writeLineByLineToFile(addMeToFile, fileName)->None:
    with open(fileName, 'w') as f:
        for line in addMeToFile:
            f.write(line)
            f.write('\n')
    return

def moveImagesToAssets(listOfImages)->None:
    for image in listOfImages:
        newPath:str = "assets/img/scenery/" + image.split("/").pop()
        os.popen(f"cp {image} {newPath}")
    return

def generateHtmlFileContents(listOfImages)->str:

    thisGoesOnceAtTheBegining:str = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, shrink-to-fit=no\"><title>gallery</title><link rel=\"stylesheet\" href=\"assets/bootstrap/css/bootstrap.min.css\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=Montserrat:400,400i,700,700i,600,600i&amp;display=swap\"><link rel=\"stylesheet\" href=\"assets/css/baguetteBox.min.css\"><link rel=\"stylesheet\" href=\"assets/css/vanilla-zoom.min.css\"></head><body><nav class=\"navbar navbar-light navbar-expand-lg fixed-top bg-white clean-navbar\"><div class=\"container\"><a class=\"navbar-brand logo\" href=\"metrics\">COCO Dataset Viewer</a><button data-bs-toggle=\"collapse\" class=\"navbar-toggler\" data-bs-target=\"#navcol-1\"><span class=\"visually-hidden\">Toggle navigation</span><span class=\"navbar-toggler-icon\"></span></button><div class=\"collapse navbar-collapse\" id=\"navcol-1\"><ul class=\"navbar-nav ms-auto\"><li class=\"nav-item\"><a class=\"nav-link active\" href=\"gallery\">Gallery</a></li><li class=\"nav-item\"><a class=\"nav-link\" href=\"metrics\">Metrics</a></li><li class=\"nav-item\"><a class=\"nav-link\" href=\"upload\">Upload</a></li></ul></div></div></nav><main class=\"page gallery-page\"><section class=\"clean-block clean-gallery dark\"><div class=\"container\"><div class=\"block-heading\"><h2 class=\"text-info\">DATASET</h2></div><div class=\"row\">"


    beginingOfLine:str = "<div class=\"col-md-6 col-lg-4 item\"><a class=\"lightbox\" href=\""

    middleOfLine:str = "\"><img class=\"img-thumbnail img-fluid image\" src=\""

    endOfLine:str = "\"></a></div>"


    appendMeToHtml = ""

    for imageName in listOfImages:
        print(f"Image_{imageName}")
        runMeForEachImage = beginingOfLine + imageName + middleOfLine + imageName + endOfLine
        appendMeToHtml += runMeForEachImage

    addMeAfterImages:str = "</div></div></section></main><footer class=\"page-footer dark\"><div class=\"footer-copyright\"><p>© 2023 Keith H. Bova</p></div></footer><script src=\"assets/bootstrap/js/bootstrap.min.js\"></script><script src=\"assets/js/baguetteBox.min.js\"></script><script src=\"assets/js/vanilla-zoom.js\"></script><script src=\"assets/js/theme.js\"></script></body></html>"

    return thisGoesOnceAtTheBegining + appendMeToHtml + addMeAfterImages

def getPathsToAllImagesFromADirectory(path):
    listOfImages = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith(".jpg") and not file.startswith(".")):
                currentFile = os.path.join(root,file)
                listOfImages.append(currentFile)

    return listOfImages

def generate_new_gallery():
    listOfImages = getPathsToAllImagesFromADirectory("coco_dataset")

    moveImagesToAssets(listOfImages)

    newListOfImages = getPathsToAllImagesFromADirectory("assets/img/scenery")

    addMeToFile = [generateHtmlFileContents(newListOfImages)]

    writeLineByLineToFile(addMeToFile, "templates/gallery.html")

    return

def update_program_with_new_data(fileName):
    with ZipFile(fileName) as zipObject:
        zipObject.extractall("coco_dataset/")
    generate_new_gallery()
    return



@app.route('/')
def gallery():
    return render_template('metrics.html')

@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html')

@app.route('/metrics')
def metrics_page():
    class_names = "person, car, dog"
    number_of_images = 1000
    duplicates = 20
    return render_template('metrics.html', class_names=class_names, number_of_images=number_of_images, duplicates=duplicates)


@app.route('/success')
def success_page():
    return render_template('metrics.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # save the file and do any other processing you need
            fileName = 'coco_dataset/my_dataset.zip'
            file.save(fileName)
            update_program_with_new_data(fileName)
            return redirect('/success')
    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>'''






@app.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory('assets', path)

if __name__ == "__main__":
    clearOldImgFolder()
    contents = [generateHtmlFileContents([])]
    writeLineByLineToFile(contents, "templates/gallery.html")

    app.run(debug=True, host="0.0.0.0")
