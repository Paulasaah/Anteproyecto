"""Ajuste conservador de trazos y tipografía sobre los SVG de distribución."""
from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas'
for name in ['01_diagnosticos_2x2','04_pad_fst_ita','05_ita_otsu_2x2']:
 p=D/(name+'.svg');s=p.read_text()
 widths={'0.85':'0.45','0.75':'0.5'} if name.startswith('01') else {'1.1':'0.45','0.75':'0.5'}
 s=re.sub(r'stroke-width: ([\d.]+)',lambda m:'stroke-width: '+widths.get(m[1],m[1]),s)
 if name.startswith('04'):s=s.replace('font-size: 14.79px','font-size: 11.5px').replace('font-size: 12.94px','font-size: 11px')
 if name.startswith('05'):s=s.replace('font-size: 11.67px','font-size: 11px')
 # Títulos de dataset y notas de cobertura: discretos, manteniendo coordenadas.
 def title(m):
  v=m[0]
  if any(k in v for k in ['HAM10000','ISIC2019','ISIC2020','PAD-UFES-20','Válidos:','Abstenciones:']):v=re.sub(r'font-size: [\d.]+px','font-size: 10.5px',v)
  return v
 s=re.sub(r'<text\b[^>]*>.*?</text>',title,s,flags=re.S);p.write_text(s)
p=D/'procedencia.json';data=json.loads(p.read_text())
for row in data['figuras']:
 if Path(row['svg']).stem in ['01_diagnosticos_2x2','04_pad_fst_ita','05_ita_otsu_2x2']:row['svg_sha256']=hashlib.sha256((D/row['svg']).read_bytes()).hexdigest()
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
