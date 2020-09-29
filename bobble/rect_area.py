"""
__author__: Anmol Durgapal
"""


def area(coord):
    a, b, c, d = coord
    
    return (c-a)*(d-b)


def covering_rect(rects):
    return (min(r[0] for r in rects),
            min(r[1] for r in rects),
            max(r[2] for r in rects),
            max(r[3] for r in rects))


def clip_rect(bb, rects):
    if not rects:
        return []
    
    (x1, y1, x2, y2) = rects[0]
    
    rs = rects[1:]
    (a1, b1, a2, b2) = bb
    
    if a1 == a2 or b1 == b2:
        return []
    
    if a1 >= x2 or a2 <= x1 or y1 >= b2 or y2 <= b1:
        return clip_rect(bb, rs)
    
    return [(max(a1, x1), max(b1, y1), min(a2, x2), min(b2, y2))] + clip_rect(bb, rs)


def calc_area(cr, rects):
    if not rects:
        return 0

    rc = rects[0]
    rs = rects[1:]
    
    x1, y1, x2, y2 = cr
    l1, m1, l2, m2 = rc
    
    t = (x1, m2, x2, y2)
    b = (x1, y1, x2, m1)
    l = (x1, m1, l1, m2)
    r = (l2, m1, x2, m2)
    
    return area(rc) + sum(calc_area(x, clip_rect(x, rs)) for x in [t, b, l, r])


n = int(input())
arr_rect = []
for i in range(0, n):
    k = list(map(int, input().strip().split(" ")))
    arr_rect.append(k)

print(calc(covering_rect(arr_rect), arr_rect))
