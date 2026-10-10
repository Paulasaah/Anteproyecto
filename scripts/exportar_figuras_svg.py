"""Regenera las exportaciones vectoriales que utiliza includesvg sin shell-escape."""
from pathlib import Path
import subprocess, hashlib,json
root=Path(__file__).resolve().parents[1]
folder=root/'images/organizadas'
records=[]
for svg in sorted(folder.glob('*.svg')):
 pdf=svg.with_name(svg.stem+'_svg-raw.pdf')
 subprocess.run(['inkscape',str(svg),'--export-area-page','--export-type=pdf','--export-text-to-path','--export-filename='+str(pdf)],check=True,capture_output=True)
 records.append({'svg':svg.name,'svg_sha256':hashlib.sha256(svg.read_bytes()).hexdigest(),'pdf':pdf.name,'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()})
print(f'{len(records)} SVG exportados para compilación; PDF auxiliares no versionados.')
