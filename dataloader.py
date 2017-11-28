import cv2
import numpy as np
from config import args
from utils import get_combination_miniImageNet_5way1shot_random_pathonly_episode_variableWays



def randomCrop(img, centralCrop=False):
  '''
  perform random crop and normalize an image
  :param 
     img: original image 
     centralCrop: crop from center if True, default False
  :return
     imgNormalize: random Cropped / normalized image
  '''
  dx = np.random.randint(4)
  dy = np.random.randint(4)

  if centralCrop is False:
      imgNormalize = img[dx:dx+80, dy:dy+80, :]
  else:
      imgNormalize = img[2:82,2:82,:]

  imgNormalize = imgNormalize.astype('float64')
  imgNormalize_R = (imgNormalize[:, :, 0]  / 255.0 - 0.4710) / 0.2741 #R
  imgNormalize_G = (imgNormalize[:, :, 1]  / 255.0 - 0.4498) / 0.2661 #G
  imgNormalize_B = (imgNormalize[:, :, 2]  / 255.0 - 0.4034) / 0.2809 #B

  imgNormalize[:, :, 0] = imgNormalize_R
  imgNormalize[:, :, 1] = imgNormalize_G
  imgNormalize[:, :, 2] = imgNormalize_B

  return imgNormalize


def Producer(list, batch_size, epoch_size, mode):
  '''
  produce customized dataset (5 way 1 shot images and labels)
     
    :param 
        queue: train or test queue to fill in
        list: pre-generated list of a training data or testing data
        batch_size: batch size
        epoch_size: total number of sampling
        mode: either training or testing
    :return: 
        queue: fill the queue with generated data
  '''

  total_batch = int(epoch_size/batch_size)
  epochNum = 0
  while 1:
    print ("epoch num = " + str(epochNum))
    epochNum = epochNum + 1

    if mode is "training":
        WAYS_TRAIN_TEST = args.way_train
    else:
        WAYS_TRAIN_TEST = args.way_test

    print ('generating ' + mode + ' combination.. ')
    # [0] is trueLabel; [-1] is t0;
    trueLabel_supportSet_query = get_combination_miniImageNet_5way1shot_random_pathonly_episode_variableWays(list, visualize=False,episode_num=args.num_episode, ways = WAYS_TRAIN_TEST, query_num = args.num_query)
    print('done')

    return trueLabel_supportSet_query

def loadImg(sample_list):
    mode = "training"
    train_images_data = []
    for way in range(1, len(sample_list)):
        img = cv2.imread(sample_list[way])
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = RGB_img
        if np.random.choice([True, False]) and mode is "training":
            img = cv2.flip(RGB_img,1)
        imgNormalize = randomCrop(img)
        train_images_data.append(imgNormalize.reshape(80, 80, 3))

    return sample_list[0], train_images_data[0], train_images_data[1], train_images_data[2], train_images_data[3], train_images_data[4], train_images_data[5] #TODO fix me

def loadImg_testing(sample_list):
    mode = "testing"
    train_images_data = []
    for way in range(1, len(sample_list)):
        img = cv2.imread(sample_list[way])
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = RGB_img
        if np.random.choice([True, False]) and mode is "training":
            img = cv2.flip(RGB_img, 1)
        imgNormalize = randomCrop(img)
        train_images_data.append(imgNormalize.reshape(80, 80, 3))

    return sample_list[0], train_images_data[0], train_images_data[1], train_images_data[2], train_images_data[3], \
               train_images_data[4], train_images_data[5]
