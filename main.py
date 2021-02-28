import os
import re
import numpy as np
from keras.applications import resnet50
from keras.preprocessing import image
from keras.models import load_model

def display_prediction(pred_class, breed, f):
    for imagenet_id, name, likelihood in pred_class[0]:
        print(" - {}: {:2f} likelihood ------- Real Breed -------> {}".format(name, likelihood, breed), file=f)
        if name != breed:
            return -1    
        return 0

def run_model(img, model, breed, f, total):
    image_width = 224
    image_length = 224
    img = image.load_img(path='Images/' + breed + '/' + img, target_size=(image_width, image_length))
    X = image.img_to_array(img)
    X = np.expand_dims(X, axis=0)
    X = resnet50.preprocess_input(X)
    X_Pred = model.predict(X)
    comparision = display_prediction(resnet50.decode_predictions(X_Pred, top=1), breed, f)
    return comparision

def program():

    # images_array = ["data/boxer.jpg", "data/chiuauau.jpeg", "data/Pit_Bull_Terrier.jpg", "data/greatdane.jpg", "data/dalmata.jpg"]

    model = load_model('savedModel/ResNet50', compile=False)

    # The model can be trained with model.fit() using model.compile() first

    # for img in images_array:
    counter = 0

    breed_sum = 0
    total_percentage = 0

    f = open("prob_resnet50.txt", "w")
    for root, dirs, files in os.walk('Images'):
        for dir in dirs:
            total_imgs = len([name for name in os.listdir('Images/' + dir) if os.path.isfile(os.path.join('Images/' + dir, name))])
            counting_total = total_imgs
            for img in os.listdir('Images/' + dir):
                print(counter)
                counting_total += run_model(img, model, dir, f, total_imgs)
                counter+=1
            percentage_per_breed = counting_total * 100 / total_imgs    
            print('################################################', file=f)
            print('End of ' + dir + ' samples ', file = f)
            print('Resulting accuracy: ' + str(counting_total) + ' out of: ' + str(total_imgs), file=f)
            print('Percentage: ' + str(percentage_per_breed) + '%', file=f)
            print('################################################', file=f)
            total_percentage += percentage_per_breed
            breed_sum += 1
    
    print('.', file=f)
    print('.', file=f)
    print('.', file=f)
    print('.', file=f)
    print('.', file=f)
    print('.', file=f)
    print('.', file=f)

    print('################################################', file=f)
    print('End of all samples', file=f)
    print('Average accuracy over all breeds: ' + str(percentage_per_breed / breed_sum) + '%', file=f)
    print('################################################', file=f)
    f.close
    
    # Load and Save model
    # model = resnet50.ResNet50()
    # model.save('savedModel/ResNet50')

def main():
    print("Running...\n")
    program()
    
if __name__== "__main__" :
    main()