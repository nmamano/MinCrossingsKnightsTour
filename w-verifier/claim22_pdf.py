from pypdf import PdfReader
from pathlib import Path
r=PdfReader('paper.pdf')
for i,p in enumerate(r.pages):
 if 'Figure 11:' in (p.extract_text() or ''):
  print('page',i+1,'box',p.mediabox)
  print('images',[(im.name,len(im.data)) for im in p.images])
  for j,im in enumerate(p.images):Path(f'w-verifier/claim22_paper_image_{j}.{im.name.split(".")[-1]}').write_bytes(im.data)
  Path('w-verifier/claim22_pdf_page.txt').write_text(p.get_contents().get_data().decode('latin1'))
  print('xobjects',list(p['/Resources'].get('/XObject',{})))
