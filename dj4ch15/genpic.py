from PIL import Image, ImageDraw, ImageFont

msg = u"這是你的命，\n\n不要再混了，\n\n我正在看著你！\n\nI Am Watching YOU"
font_size = 48
fill = (0,0,0,255)
image_file = Image.open('cat_quote.jpg')
im_w, im_h = image_file.size 
im0 = Image.new('RGBA', (1,1))
dw0 = ImageDraw.Draw(im0)
font = ImageFont.truetype('wt014.ttf', font_size)
fn_w, fn_h = dw0.textsize(msg, font=font)

im = Image.new('RGBA', (fn_w, fn_h), (255,0,0,0))
dw = ImageDraw.Draw(im)
dw.text((0,0), msg, font=font, fill=fill)
image_file.paste(im, (30, 50), im)
image_file.save('output.jpg')
