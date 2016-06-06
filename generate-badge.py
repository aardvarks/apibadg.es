import svgwrite

dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(dwg.rect((0, 0), (87, 20), fill='rgb(85,85,85)'))
dwg.add(dwg.text('build', insert=(6, 14), fill='rgb(255,255,255)', font_family = 'DejaVu Sans,Verdana,Geneva,sans-serif', font_size = '11px'))
dwg.add(dwg.rect((37, 0), (51, 20), fill='rgb(68,204,17)'))
dwg.add(dwg.text('passing', insert=(40.5, 14), fill='rgb(255,255,255)', font_family = 'DejaVu Sans,Verdana,Geneva,sans-serif', font_size = '11px'))
dwg.save()
