#!/usr/bin/env bash
# Provisiona o treino da voz numa VM GPU Spot (auto-curavel + auto-terminate).
# Rodar no Cloud Shell:  curl -sL https://raw.githubusercontent.com/rafaelvs/06_Automacao_Instagram/main/voz/provision_gcp.sh | bash
set -uo pipefail

PROJECT=$(gcloud config get-value project 2>/dev/null)
REGION=${REGION:-us-central1}
ZONES=(${ZONES:-us-central1-a us-central1-b us-central1-f us-central1-c})
BUCKET="gs://${PROJECT}-voz-ckpt"
TEMPLATE=voz-tpl
MIG=voz-mig
RAW=https://raw.githubusercontent.com/rafaelvs/06_Automacao_Instagram/main/voz/gcp_train.py

echo "== Projeto: $PROJECT | Regiao: $REGION | Bucket: $BUCKET =="
echo "== Habilitando APIs (compute) =="
gcloud services enable compute.googleapis.com -q 2>/dev/null
echo "== Bucket de checkpoints =="
gsutil ls -b "$BUCKET" >/dev/null 2>&1 || gsutil mb -l "$REGION" "$BUCKET"

echo "== Startup-script (instala driver + deps + roda treino) =="
cat > /tmp/voz_startup.sh <<EOS
#!/bin/bash
exec > /var/log/voz_startup.log 2>&1
set -x
if ! nvidia-smi; then
  apt-get update -y
  apt-get install -y python3-pip ffmpeg libsndfile1 git curl
  curl -fsSL https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py -o /opt/gpu.py
  python3 /opt/gpu.py || true
fi
for i in \$(seq 1 80); do nvidia-smi && break; sleep 15; done
pip3 install --break-system-packages -q --upgrade coqui-tts soundfile librosa
export VOZ_BUCKET=\$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/attributes/bucket)
export VOZ_MIG=\$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/attributes/mig)
curl -sL $RAW -o /opt/gcp_train.py
python3 /opt/gcp_train.py
EOS

echo "== Instance template (Spot T4 + debian-12) =="
gcloud compute instance-templates describe "$TEMPLATE" >/dev/null 2>&1 && gcloud compute instance-templates delete "$TEMPLATE" -q
gcloud compute instance-templates create "$TEMPLATE" \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --image-family=debian-12 --image-project=debian-cloud \
  --maintenance-policy=TERMINATE \
  --provisioning-model=SPOT \
  --boot-disk-size=120GB --boot-disk-type=pd-balanced \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata=bucket="$BUCKET",mig="$MIG" \
  --metadata-from-file=startup-script=/tmp/voz_startup.sh || { echo "FALHOU criar template"; exit 1; }

echo "== MIG size 1 (tenta zonas) =="
for Z in "${ZONES[@]}"; do
  gcloud compute instance-groups managed describe "$MIG" --zone "$Z" >/dev/null 2>&1 && gcloud compute instance-groups managed delete "$MIG" --zone "$Z" -q
done
CREATED=0
for Z in "${ZONES[@]}"; do
  echo "  tentando $Z ..."
  if gcloud compute instance-groups managed create "$MIG" --base-instance-name voz --size 1 --template "$TEMPLATE" --zone "$Z" 2>/tmp/migerr; then
    echo "  >> MIG criado em $Z"; CREATED=1; ZONE_OK=$Z; break
  else
    echo "  >> $Z indisponivel: $(tail -1 /tmp/migerr)"
  fi
done

if [ "$CREATED" = 1 ]; then
  echo "OK VM subindo em $ZONE_OK. Progresso: gsutil cat $BUCKET/progress.txt (apos ~10 min). Autodestroi no DONE."
else
  echo "FALHOU criar VM (cota/capacidade T4): $(tail -1 /tmp/migerr)"; exit 2
fi
