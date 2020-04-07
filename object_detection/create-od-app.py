"""
Currents Object Detection Directory Structure
@author Jeraldy
./DirName
    - /models (create on colab) 
    - /data
        - /images -> store all images
        - /annontations -> store all annonated xml 
        - /train labels -> 70% of annontated xml file
        - /test labels -> 30% of annontated xml file
    - /training -> training logs 
    - /pretrained_model -> Download the pretrained model for transfer learning
    - /fine_tuned_model -> export the final model here

"""
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', dest='name',help='create name of the app',
                        default="object_detection")
parser.add_argument('-d', '--dest', dest='dest', help='add destination path',
                        default=os.getcwd())
args = parser.parse_args()

#create object detection directory
def createTemplate():
    os.makedirs("{}/{}/data".format(args.dest, args.name))
    os.makedirs("{}/{}/data/images".format(args.dest, args.name))
    os.makedirs("{}/{}/data/annontations".format(args.dest, args.name))
    os.makedirs("{}/{}/data/train_labels".format(args.dest, args.name))
    os.makedirs("{}/{}/data/test_labels".format(args.dest, args.name))
    os.makedirs("{}/{}/training".format(args.dest, args.name))
    os.makedirs("{}/{}/pretrained_model".format(args.dest, args.name))
    os.makedirs("{}/{}/fine_tuned_model".format(args.dest, args.name))

#Check if Directory Exist
if not os.path.exists("{}/{}".format(args.dest, args.name)):
    createTemplate()
    print("Created {} in {}".format(args.name, args.dest))
else:
    print("{} already exist!".format(args.dest, args.name))

