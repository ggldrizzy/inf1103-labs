FROM python:3.11-slim
WORKDIR /app
RUN pip install pytest
COPY . .
CMD ["python", "inventory_manager.py"]