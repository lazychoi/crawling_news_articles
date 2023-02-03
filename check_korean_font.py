import matplotlib.font_manager as fm

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
print(len(font_list))

f = [f.name for f in fm.fontManager.ttflist]
print(f)

for i in f:
    if i == 'NanumBarunGothic':
        print('나눔 고딕 설치되어 있음')