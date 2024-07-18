FROM python

WORKDIR /app
COPY requirements.txt requirements.txt
COPY bot.py bot.py

RUN pip install --no-cache-dir -r requirements.txt

ENV PROXMOX_HOST=URL_HOST
ENV PROXMOX_TOKEN=TOKEN
ENV VMID=VMID

ENV TELEGRAM_TOKEN=6680268508:AAFMDkfoU3Z3r_tTpiUqyWZoxjwpc4o2g7I
#ENV ALLOWED_USERS USER1 USER2 ...
ENV ALLOWED_USERS 831192089

CMD ["python", "bot.py"]
