pip install openai pillow modelscope vllm qwen-vl-utils==0.0.14

modelscope download --model Qwen/Qwen3-VL-8B-Instruct --local_dir ./models/Qwen3-VL-8B-Instruct


VLLM_CONFIGURE_LOGGING=0 \
vllm serve ./models/Qwen3-VL-8B-Instruct \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.8 \
    --enforce_eager \
    --served-model-name Qwen3-VL-8B-Instruct\
    --port 8000 &