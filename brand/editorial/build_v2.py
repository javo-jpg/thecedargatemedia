"""November 2026 posts and Stories in the v2 look (same grade, palette, type; varied layouts)."""
import sys, os
sys.path.insert(0, '/home/claude/tpl')
from editorial import editorial, fullbleed, framed, typecard
from PIL import Image

S = '/mnt/user-data/uploads/Videos/CedarGate_Nov/stills/'
DB = '/home/claude/dbx/tmp/'
T = '/home/claude/tpl/'
O = '/home/claude/v2/'
for d in ['week', 'holiday', 'thankful', 'rso', 'stories']: os.makedirs(O + d, exist_ok=True)
ST = dict(W=1080, H=1920)
ann_st = dict(W=1080, H=1920, photo_h=0.62, top_y=330, hsize=104, dsize=30)

# ---- Nov 3 RSO carousel ----
editorial(T + 'f_8201.jpg', O + 'rso/01_cover.jpg', 'Members only.', 'Become a Range Safety Officer.',
          'NRA RSO CERTIFICATION · ONE DAY · ON OUR RANGE', 'SATURDAY, DECEMBER 5 · DM US "RSO"', cx=0.35, cy=0.45)
framed(T + 'f_8213.jpg', O + 'rso/02_reserve.jpg', 'LIMITED SPOTS · MEMBERS ONLY', 'Earn your certification',
       'alongside fellow members.', 'DM us "RSO" or contact Abi Hill or Stacey Holden to reserve your spot.', cx=0.35, cy=0.5)
fullbleed(S + 's31.jpg', O + 'rso/03_membership.jpg', 'NOT A MEMBER YET?', 'This is what',
          'membership looks like.', 'Member trainings, events, the range and the lodge. DM us "MEMBER" to learn more.', cx=0.5)

# ---- Nov 10 This week on the course ----
editorial(S + 's87.jpg', O + 'week/01_cover.jpg', 'Two shoots.', 'Two good causes.',
          'THIS WEEK AT THE CEDAR GATE', 'THURSDAY AND FRIDAY ON THE COURSE', cx=0.55, cy=0.4, photo_h=0.62)
framed(S + 's88.jpg', O + 'week/02_haven_of_hope.jpg', 'THURSDAY · NOVEMBER 12', 'Clay Shoot for', 'Haven of Hope',
       'Sponsored by the Butterfield Foundation.', cx=0.3)
fullbleed(S + 's7.jpg', O + 'week/03_southwestern.jpg', 'FRIDAY · NOVEMBER 13', 'Southwestern University', 'Clay Shoot',
          'A day on the course for a great cause.')
typecard(O + 'week/04_register.jpg', 'JOIN US', 'Come shoot for', 'something good.',
         'Registration information is on our profile.')

# ---- Nov 24 Holiday party ----
editorial(DB + 'hol_5852.jpg', O + 'holiday/01_cover.jpg', 'Host your holiday party', 'at The Cedar Gate.',
          'NOW BOOKING DECEMBER', 'COMPANY PARTIES · TEAM DINNERS · FAMILY CELEBRATIONS', cx=0.5, cy=0.45, photo_h=0.62)
fullbleed(DB + 'hol_5777.jpg', O + 'holiday/02_room.jpg', 'THE BARNS', 'Room for', 'the whole company.',
          'Space to gather, celebrate and give thanks for the year.', cy=0.15)
framed(DB + 'hol_5941.jpg', O + 'holiday/03_table.jpg', 'THE TABLE', 'Dinner is', 'taken care of.',
       'Chef-prepared food and the warmth of the season.', cy=0.4)
typecard(O + 'holiday/04_plan.jpg', "LET'S PLAN IT", 'Celebrate the season', 'at The Cedar Gate.', '',
         'DM US "EVENT" FOR DECEMBER DATES')

# ---- Nov 26 Thanksgiving ----
fullbleed('/mnt/user-data/uploads/Videos/CedarGate_Nov/probe/p79.3.jpg', O + 'thankful/01_thanksgiving.jpg',
          'HAPPY THANKSGIVING', 'From our family', 'to yours.', '', align='center', hsize=88, logo=True, cx=0.47)

# ---- Stories ----
sd = O + 'stories/'
def ann(i, name, l1, l2, det, foot, cx=0.5):
    editorial(S + f's{i}.jpg', sd + name, l1, l2, det, foot, cx=cx, **ann_st)
def full(i, name, kick, l1, l2, body, cx=0.5, path=None):
    fullbleed(path or S + f's{i}.jpg', sd + name, kick, l1, l2, body, cx=cx, hsize=96, bsize=34, ksize=28, **ST)
def fr(i, name, kick, l1, l2, body, cx=0.5, path=None):
    framed(path or S + f's{i}.jpg', sd + name, kick, l1, l2, body, cx=cx, hsize=84, bsize=32, ksize=26, photo_frac=0.5, **ST)
def card(name, kick, l1, l2, body='', foot=''):
    typecard(sd + name, kick, l1, l2, body, foot, hsize=110, bsize=36, ksize=30, **ST)

card('02-11 Story - Jacobs Ladder this Friday.jpg', 'THIS FRIDAY · NOVEMBER 6', "Jacob's Ladder", 'Clay Classic.', 'A day on the course for a meaningful cause.', 'REGISTER THROUGH THE LINK ON OUR PROFILE')
ann(65, '05-11 Story - Shriners this Saturday.jpg', 'Shriners', 'Clay Shoot.', 'THIS SATURDAY · NOVEMBER 7', 'DM US "EVENT" FOR DETAILS')
full(99, '06-11 Story - Jacobs Ladder today (event photo to add).jpg', 'TODAY', "Jacob's Ladder", 'Clay Classic', 'Thank you to every team shooting with us today.')
full(94, '07-11 Story - Shriners today (event photo to add).jpg', 'TODAY', 'Shriners', 'Clay Shoot', 'Thank you to every team shooting with us today.')
ann(92, '09-11 Story - This week on the course.jpg', 'Haven of Hope · Thu', 'Southwestern · Fri', 'THIS WEEK ON THE COURSE', 'DM US "EVENT" FOR REGISTRATION INFO')
card('11-11 Story - Veterans Day.jpg', 'VETERANS DAY · NOVEMBER 11', 'Thank you', 'for your service.', 'To every veteran and every family who served alongside them.')
full(4, '12-11 Story - Haven of Hope today (event photo to add).jpg', 'TODAY', 'Clay Shoot for', 'Haven of Hope', 'Thank you to the Butterfield Foundation and every team shooting with us today.')
full(11, '13-11 Story - Southwestern today (event photo to add).jpg', 'TODAY', 'Southwestern', 'Clay Shoot', 'Thank you to every team shooting with us today.')
fr(12, '13-11 Story 2 - Find your squad.jpg', 'SHOT WITH US THIS WEEK?', 'Find', 'your squad.', 'Squad photos are on our page. Tag yourself and your team.')
full(2, '16-11 Story - American Cancer Society today (event photo to add).jpg', 'TODAY', 'American Cancer Society', 'Clay Shoot', 'Every clay for the fight against cancer. Thank you to every team out here today.')
ann(5, '18-11 Story - Plan your 2027 retreat.jpg', 'Book your', "team's retreat.", 'PLANNING 2027?', 'DM US "RETREAT" FOR DATES AND OPTIONS')
ann(19, '19-11 Story - API tomorrow.jpg', 'API Woodward', 'Clay Shoot.', 'TOMORROW · FRIDAY, NOVEMBER 20', 'LAST CHANCE TO JOIN A TEAM · LINK ON OUR PROFILE')
full(6, '20-11 Story - API today (event photo to add).jpg', 'TODAY', 'API Woodward', 'Clay Shoot', 'Thank you to every team shooting with us today.')
ann(118, '24-11 Story - Holiday parties.jpg', 'Host your', 'holiday party here.', 'NOW BOOKING DECEMBER', 'DM US "EVENT" FOR OPEN DATES')
full(49, '24-11 Story 2 - Members Christmas Party (Close Friends).jpg', 'MEMBERS · THURSDAY, DECEMBER 3', 'Christmas Party', 'at The Cedar Gate', 'Contact Abi to RSVP.')
full(35, '26-11 Story - Happy Thanksgiving.jpg', 'HAPPY THANKSGIVING', 'Grateful', 'for you.', 'From our family to yours.')
# RSO countdown
ann(113, '03-11 Story - NRA RSO training.jpg', 'Members only.', 'NRA RSO training.', 'SATURDAY, DECEMBER 5 · AT THE CEDAR GATE', 'DM US "RSO" TO SAVE YOUR SPOT')
fr(117, '21-11 Story - Not a member yet.jpg', 'NRA RSO TRAINING · DECEMBER 5', 'Not a member yet?', 'Members train here first.', 'DM us "MEMBER" to learn more.')
full(3, '01-12 Story - NRA RSO this Saturday.jpg', 'NRA RSO TRAINING · DECEMBER 5', 'This Saturday.', 'Last spots for members.', 'DM us "RSO" today.')
card('04-12 Story - NRA RSO tomorrow.jpg', 'NRA RSO TRAINING · SATURDAY, DECEMBER 5', 'Tomorrow.', "We'll save you a seat.", '', 'QUESTIONS? DM US "RSO"')
print('built')
