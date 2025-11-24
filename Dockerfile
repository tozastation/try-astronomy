FROM pytorch/pytorch:2.9.1-cuda13.0-cudnn9-runtime

# 作業ディレクトリの設定
WORKDIR /workspace

# 環境変数の設定
ENV JUPYTER_ENABLE_LAB=yes \
    PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512 \
    DEBIAN_FRONTEND=noninteractive

# システムパッケージの更新とクリーンアップ
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    vim \
    fonts-ipaexfont \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージのインストール（キャッシュ利用）
RUN pip install --no-cache-dir \
    jupyterlab \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    astropy \
    scikit-learn \
    plotly \
    ipywidgets \
    datasets \
    japanize-matplotlib \
    vpython 

# ポート公開
EXPOSE 8888

# 起動コマンド
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]