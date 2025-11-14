from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

for root in ['Project_A_BeforeUI/screenshots', 'Project_B_AfterUI/screenshots']:
    p = Path(root)
    p.mkdir(parents=True, exist_ok=True)
    img = Image.new('RGB', (1280, 300), color=(220,220,220) if 'Before' in root else (240,255,240))
    draw = ImageDraw.Draw(img)
    draw.text((16,16), f'Placeholder for {root}', fill=(30,30,30))
    img.save(p / ('screenshot_' + ('pre' if 'Before' in root else 'post') + '_1.png'))

print('Placeholders created')
