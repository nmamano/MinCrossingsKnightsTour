from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json
p=Path('w-verifier/claim21_figures'); files=sorted(p.glob('*.png')); out=Image.new('RGB',(1600,400*((len(files)+3)//4)),'white');D=ImageDraw.Draw(out);compare={}
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((390,370));x=(i%4)*400;y=(i//4)*400;out.paste(im,(x,y+25));D.text((x+5,y+5),f.name,fill='black')
 old=Path('writeup/crossings/figures')/f.name
 if old.exists():
  a=Image.open(old).convert('RGB');b=Image.open(f).convert('RGB');compare[f.name]={'old_size':a.size,'new_size':b.size,'same_pixels':a.size==b.size and ImageChops.difference(a,b).getbbox() is None}
 else:compare[f.name]={'missing_original':True}
out.save(p/'contact.jpg');(p/'image_comparison.json').write_text(json.dumps(compare,indent=2))
