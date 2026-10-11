"""Uso: python scripts/extraer_curvas_isic.py <directorio limpio_canonico_bs64>.
Archiva curvas empíricas exactas desde B71__clean.probas.npz; no carga objetos.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1]
records=json.loads((R/'scripts/datos_clasificacion_isic.json').read_text())['records'];out={}
for ds in ['isic2019','isic2020']:
 path=Path(sys.argv[1])/ds/'B71__clean.probas.npz';data=np.load(path,allow_pickle=False);y=data['y'];p=data['proba'];m=next(r['data']['result']['metrics'] for r in records if r['path'].endswith('/'+ds+'/B71__clean.json'))
 cm=np.zeros((p.shape[1],p.shape[1]),dtype=int);np.add.at(cm,(y,p.argmax(1)),1);assert np.array_equal(cm,m['matriz_confusion'])
 k=0 if ds=='isic2019' else 1;positive=y==k;score=p[:,k];order=np.argsort(-score,kind='stable');score=score[order];v=positive[order];end=np.r_[np.where(np.diff(score))[0],len(score)-1];tp=np.cumsum(v)[end];fp=end+1-tp;recall=tp/positive.sum();precision=tp/(end+1);fpr=fp/(len(y)-positive.sum())
 out[ds]={'source':f'resultados/banco_completo/isic_eval/limpio_canonico_bs64/{ds}/B71__clean.probas.npz','npz_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'n':len(y),'positive_count':int(positive.sum()),'class_index':k,'average_precision':float(np.sum(np.diff(np.r_[0,recall])*precision)),'recall':np.r_[0,recall].tolist(),'precision':np.r_[1,precision].tolist(),'fpr':np.r_[0,fpr].tolist(),'tpr':np.r_[0,recall].tolist()}
(R/'scripts/datos_curvas_isic.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
