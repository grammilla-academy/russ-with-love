"""One-time optimization of supplied photo. Requires existing Pillow; no face edits."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import shutil

root = Path(__file__).resolve().parent
source = Path(r'C:\Users\Denis\Dropbox\PC\Downloads\me.png')
(root/'originals').mkdir(exist_ok=True)
shutil.copy2(source, root/'originals'/'me.png')
im = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
for size in (540,1080):
    im.resize((size,size),Image.Resampling.LANCZOS).save(root/'assets'/f'liuba-{size}.webp',quality=88,method=6)
social = Image.new('RGB',(1200,630),'#fbf8f3')
social.paste(im.resize((590,590),Image.Resampling.LANCZOS),(590,20))
draw = ImageDraw.Draw(social)
font_dir = Path('C:/Windows/Fonts')
title = ImageFont.truetype(str(font_dir/'georgia.ttf'),64)
italic = ImageFont.truetype(str(font_dir/'georgiai.ttf'),64)
body = ImageFont.truetype(str(font_dir/'segoeui.ttf'),25)
draw.text((50,170),'Russ',font=title,fill='#292e2b')
draw.text((50,245),'with Love',font=italic,fill='#9e4330')
draw.text((50,365),'Russian lessons with Liuba',font=body,fill='#292e2b')
draw.text((50,410),'English / Italiano',font=body,fill='#595f58')
social.save(root/'assets'/'social.jpg',quality=88,optimize=True)
icon=Image.new('RGBA',(64,64),'#9e4330')
d=ImageDraw.Draw(icon)
d.ellipse((12,14,34,36),fill='#fbf8f3');d.ellipse((30,14,52,36),fill='#fbf8f3');d.polygon([(13,28),(51,28),(32,51)],fill='#fbf8f3')
icon.resize((32,32),Image.Resampling.LANCZOS).save(root/'assets'/'favicon.png')
print('Original backed up; responsive WebP, social JPEG and PNG favicon generated.')
