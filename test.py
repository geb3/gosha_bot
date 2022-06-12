
import re

banned = {"дурак", "мудак", "козел", "козёл", "черт", "чёрт", "гей", "хуй"}


chk_pat = '(?:{})'.format('|'.join(banned))
re.search(chk_pat, s, flags=re.I)

