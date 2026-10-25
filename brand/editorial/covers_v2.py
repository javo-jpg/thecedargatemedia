import sys, subprocess
sys.path.insert(0, '/home/claude/tpl')
from editorial import fullbleed
C = {'pheasant': (2, 1.2, 'NOW BOOKING', 'Pheasant season', 'at The Cedar Gate.'),
     'kingfisher': (0, 1.0, '', 'Kingfisher,', 'Oklahoma.'),
     'vets': (1, 1.0, 'VETERANS DAY · NOVEMBER 11', 'To every veteran,', 'thank you.'),
     'jl': (2, 1.0, 'TOMORROW · FRIDAY, NOV 6', "Jacob's Ladder", 'Clay Classic.'),
     'retreat27': (1, 1.0, 'PLANNING 2027?', 'Plan your retreat', 'at The Cedar Gate.')}
for r in sys.argv[1:]:
    k, t, kick, l1, l2 = C[r]
    fr = f'/home/claude/v2/covers/{r}_frame.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f'/home/claude/nov2/seg2/{r}_{k}.mp4', '-frames:v', '1', fr], check=True)
    fullbleed(fr, f'/home/claude/v2/covers/{r}_cover.jpg', kick, l1, l2, '', W=1080, H=1920, align='center',
              hsize=104, ksize=30, pregraded=True, pad=330)
    print(r)
