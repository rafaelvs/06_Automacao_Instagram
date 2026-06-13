# Bootstrap headless do Kaggle: roda SEMPRE a versao mais nova do voz_train.py
# (assim, corrigir o recipe e' so dar push no GitHub — nao precisa reeditar o kernel).
import urllib.request
URL = "https://raw.githubusercontent.com/rafaelvs/06_Automacao_Instagram/main/voz_train.py"
print(">> baixando voz_train.py de", URL, flush=True)
src = urllib.request.urlopen(URL).read().decode("utf-8")
exec(compile(src, "voz_train.py", "exec"))
