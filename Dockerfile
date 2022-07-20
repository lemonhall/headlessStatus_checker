FROM python

RUN pip install streamlit \
    && pwd

ENTRYPOINT ["/bin/bash"]

EXPOSE 8501