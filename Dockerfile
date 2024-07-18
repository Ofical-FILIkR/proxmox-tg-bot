FROM python

WORKDIR /app
COPY requirements.txt requirements.txt
COPY bot.py bot.py

RUN pip install --no-cache-dir -r requirements.txt

ENV PROXMOX_HOST=URL_HOST
ENV PROXMOX_TOKEN=TOKEN
ENV VMID=VMID

ENV TELEGRAM_TOKEN=TELEGRAM_TOKEN
ENV ALLOWED_USERS USER1 USER2 ...


CMD ["python", "bot.py"]
