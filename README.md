# Automatic Prostate segmentation from MR images
This provides some deep Learning code for training a deep learning model for segmentation from Magnetic Resonance(MR) Images. There is also a pyqt software avaialble to allow users to explore the use of the deep learning model that was trained as part of this project. More details on the model can be found at [here](https://arxiv.org/abs/2011.07795)

![results of segmentation of the prostate mri](imgs/figure_1.png)
## Dependencies
Before running the python software, you need install its dependecies, which relies on Pytorch, FastAi, and PyDicom.You can install the dependences from the command line using the following command: 

```
pip install -r requirements.txt
```
## Usage
The segmentation model file can be downloaded from [here](https://www.dropbox.com/s/a2rwhy29wx9s448/export_orig.pkl?dl=0)

You can either run the jupyter notebooks, to use the code, or run the code in the app folder. 

```
cd app
python ui.py
```
A windows executable file is also downloadable from the releases pages [here].

If you use this software as part of your research, please cite our paper. 
```
@article{gillespie2020deep,
  title={Deep learning in magnetic resonance prostate segmentation: A review and a new perspective},
  author={Gillespie, David and Kendrick, Connah and Boon, Ian and Boon, Cheng and Rattay, Tim and Yap, Moi Hoon},
  journal={arXiv preprint arXiv:2011.07795},
  year={2020}
}
```
