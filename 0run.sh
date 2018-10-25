## 1 ##
#divide dataset into storm unique csvs

python3 1split.py -oo

## 2 ##
#convert csv's to midi's
#make num = # of csv's in 1convert.py

python3 2convert.py

## 3 ##

#install conda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
#install magenta
conda create -n magenta python=2.7 jupyter
source activate magenta
sudo apt install build-essential libasound2-dev libjack-dev
pip install magenta
#fix install
pip uninstall tensorflow
pip install tensorflow==1.5
#train on converted midi's
#command to train performance rnn
convert_dir_to_note_sequences --input_dir=. --output_file=notesequences.tfrecord --recursive
performance_rnn_create_dataset --config='multiconditioned_performance_with_dynamics' --input=notesequences.tfrecord --output_dir=. --eval_ratio=0.10
performance_rnn_train --config='multiconditioned_performance_with_dynamics' --run_dir=rundir/ --sequence_example_file=training_performances.tfrecord
#command to run in background
#Ctrl+z
bg
tensorboard --logdir=rundir
#generate prediction
performance_rnn_generate --run_dir=rundir --output_dir=../ --config='multiconditioned_performance_with_dynamics' --num_outputs=1 --num_steps=12000 --notes_per_second=1 --primer_midi=primer.mid

## 4 ##
#convert predicted midi's to weather data
#classify the predicted storm

python3 4predict.py