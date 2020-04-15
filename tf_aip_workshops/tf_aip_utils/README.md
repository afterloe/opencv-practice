TensorFlow
===

```shell script
python3 object_detection/model_main.py \
    --pipeline_config_path=/mount/data/Project/detector_tensorflow/digimon/scripts/pipeline.config \
    --model_dir=/mount/data/Project/detector_tensorflow/digimon/annotations \
    --num_train_steps=5000 \
    --sample_1_of_n_eval_examples=1 \
    --alsologtostderr
```