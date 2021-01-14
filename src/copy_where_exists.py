""" usage: copy_where_exists.py [-i IMAGEDIR] [-a ANNOTATIONSDIR] [-d COPYTODIR]

Copy *.jpg files to a destination where there exists a corresponding .xml file in the annotations directory
Useful when you've annotated only some of the images in a directory (based on, say, quality) and you want to pull those out for
training

"""
from pathlib import Path
import shutil
import argparse

def copy_where_exists(image_dir, annotations_dir, copy_image_to_dir):
    #pull the list of .xml files from the annotations directory and then pull all the associated imaged from the output dir into the copy_to dir

    p_annotations = Path(annotations_dir)

    files = list(p_annotations.glob('**/*.xml'))

    for file in files:
        print('File to copy {}'.format(file.stem))
        p_source = Path(image_dir+file.stem+'.jpg')
        p_destination = Path(copy_image_to_dir+file.stem+'.jpg')
        #p_destination.symlink_to(p_source)
        shutil.copy(p_source, p_destination)


def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Copy *.jpg files to a destination based on .xml existance",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--imageDir',
        help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-a', '--annotationsDir',
        help='Path to the folder where the annotations data is stored.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-d', '--copyToDir',
        help='Path to the folder where the images should be copied to.',
        default=None,
        type=str)
    args = parser.parse_args()

    # Now we are ready to start the iteration
    iterate_dir(args.imageDir, args.annotationsDir, args.copyToDir)


if __name__ == '__main__':
    main()