FROM kalilinux/kali-rolling

RUN apt update && apt install -y python3 python3-pip git curl wget ruby-full golang-go snapd

WORKDIR /opt/DeepReconHawk

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "deep_recon.py"]