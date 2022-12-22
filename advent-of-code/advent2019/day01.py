sample_in = {
    '12': 2,
    '14': 2,
    '1969': 654,
    '100756': 33583,
}

def get_input(s):
    return int(s.strip())

def prob1_part(s):
    result = (get_input(s) // 3) - 2
    return result

def prob1(s):
    result = 0
    for t in s.strip().split('\n'):
        result += prob1_part(t)
    return result
my_in = """
51360
95527
72603
128601
68444
138867
67294
134343
62785
53088
134635
137884
97654
103704
138879
87561
83922
68414
84876
105143
76599
98924
57080
63590
50126
111872
55754
64410
78488
56557
105446
127182
59451
87249
61652
131698
148820
95742
68223
121744
65678
99745
64089
75610
106085
100364
116959
122862
56580
109631
82895
79666
133474
50579
83473
140028
125999
68225
131345
90797
84914
81915
65369
71230
50379
106385
118503
119640
138540
70678
95881
100282
123060
147368
93030
82553
131271
147675
111126
115183
82956
145698
99261
52768
99207
123551
64738
117275
98136
111592
78576
118613
130351
68567
72356
85608
129414
66521
76924
130449
"""

for k, v in sample_in.items():
    test1 = prob1_part(k)
    assert test1 == v, f'f({k})={repr(test1)} (expected {repr(v)})'
print('OK tests part1')
print('prob1:', prob1(my_in))

def prob2_part(s):
    result = 0
    aux = get_input(s)
    while True:
        aux = (aux // 3) - 2
        if aux > 0:
            result += aux
        else:
            break
    return result
sample_in2 = {
    '12': 2,
    '14': 2,
    '1969': 966,
    '100756': 50346,
}
for k, v in sample_in2.items():
    test1 = prob2_part(k)
    assert test1 == v, f'f({k})={repr(test1)} (expected {repr(v)})'

def prob2(s):
    result = 0
    for t in s.strip().split('\n'):
        result += prob2_part(t)
    return result
print('prob2:', prob2(my_in))