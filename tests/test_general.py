import unittest
from atcgen.generator import Generator


class TestGenerate(unittest.TestCase):
    maxDiff = None

    def test_basic(self):
        lyr_content = "&aa&bb&cc\n&dd&ee&ff\n"
        tim_content = ("515 540\n555 578\n585 600\n"
                       "660 710\n724 792\n809 874\n")

        generator = Generator()
        generated_str = generator.generate(lyr_content, tim_content, "tass")
        self.assertEqual(generated_str, r"""[Script Info]
ScriptType: v4.00+
WrapStyle: 5
ScaledBorderAndShadow: yes
YCbCrMatrix: TV.601
PlayResX: 1280
PlayResY: 720
TimingVersion: 4


[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, KaraokeColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default, DejaVu Sans, 25, &H0000FF00, &H0000FFFF, &H000000FF, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 8, 10, 10, 10, 1


[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0, 0:00:04.15, 0:00:06.50, Default, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 25)}aa{\kt(126, 37)}bb{\kt(164, 21)}cc\N{\pc(100, 25)}aa{\pc(126, 37)}bb{\pc(164, 21)}cc
Dialogue: 0, 0:00:05.60, 0:00:09.24, Default, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 50)}dd{\kt(151, 81)}ee{\kt(233, 81)}ff\N{\pc(100, 50)}dd{\pc(151, 81)}ee{\pc(233, 81)}ff


[lyr]
;&aa&bb&cc
;&dd&ee&ff
;


[tim]
;515 540
;555 578
;585 600
;660 710
;724 792
;809 874
;""")

    def test_style_alignment(self):
        lyr_content = "&aa&bb&cc\n%style aligned_down Alignment=2\n&dd&ee&ff\n"
        tim_content = ("515 540\n555 578\n585 600\n"
                       "660 710\n724 792\n809 874\n")

        generator = Generator()
        generated_str = generator.generate(lyr_content, tim_content, "tass")
        self.assertEqual(generated_str, r"""[Script Info]
ScriptType: v4.00+
WrapStyle: 5
ScaledBorderAndShadow: yes
YCbCrMatrix: TV.601
PlayResX: 1280
PlayResY: 720
TimingVersion: 4


[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, KaraokeColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default, DejaVu Sans, 25, &H0000FF00, &H0000FFFF, &H000000FF, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 8, 10, 10, 10, 1
Style: aligned_down, DejaVu Sans, 25, &H0000FF00, &H0000FFFF, &H000000FF, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 2, 10, 10, 10, 1


[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0, 0:00:04.15, 0:00:06.50, Default, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 25)}aa{\kt(126, 37)}bb{\kt(164, 21)}cc\N{\pc(100, 25)}aa{\pc(126, 37)}bb{\pc(164, 21)}cc
Dialogue: 0, 0:00:05.60, 0:00:09.24, aligned_down, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 50)}dd{\kt(151, 81)}ee{\kt(233, 81)}ff\N{\pc(100, 50)}dd{\pc(151, 81)}ee{\pc(233, 81)}ff


[lyr]
;&aa&bb&cc
;%style aligned_down Alignment=2
;&dd&ee&ff
;


[tim]
;515 540
;555 578
;585 600
;660 710
;724 792
;809 874
;""")

    def test_style_alignment_margin(self):
        lyr_content = "&aa&bb&cc\n%style aligned_down Alignment=2 MarginL=25 MarginR=50 MarginV=100\n&dd&ee&ff\n"
        tim_content = ("515 540\n555 578\n585 600\n"
                       "660 710\n724 792\n809 874\n")

        generator = Generator()
        generated_str = generator.generate(lyr_content, tim_content, "tass")
        self.assertEqual(generated_str, r"""[Script Info]
ScriptType: v4.00+
WrapStyle: 5
ScaledBorderAndShadow: yes
YCbCrMatrix: TV.601
PlayResX: 1280
PlayResY: 720
TimingVersion: 4


[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, KaraokeColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default, DejaVu Sans, 25, &H0000FF00, &H0000FFFF, &H000000FF, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 8, 10, 10, 10, 1
Style: aligned_down, DejaVu Sans, 25, &H0000FF00, &H0000FFFF, &H000000FF, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 2, 25, 50, 100, 1


[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0, 0:00:04.15, 0:00:06.50, Default, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 25)}aa{\kt(126, 37)}bb{\kt(164, 21)}cc\N{\pc(100, 25)}aa{\pc(126, 37)}bb{\pc(164, 21)}cc
Dialogue: 0, 0:00:05.60, 0:00:09.24, aligned_down, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 50)}dd{\kt(151, 81)}ee{\kt(233, 81)}ff\N{\pc(100, 50)}dd{\pc(151, 81)}ee{\pc(233, 81)}ff


[lyr]
;&aa&bb&cc
;%style aligned_down Alignment=2 MarginL=25 MarginR=50 MarginV=100
;&dd&ee&ff
;


[tim]
;515 540
;555 578
;585 600
;660 710
;724 792
;809 874
;""")

    def test_tass_complete(self):
        lyr_content = """%credit 0 400 [Kamen Rider OOO - Opening]
%credit 400 800 [Maki Ohguro - Anything Goes!]
%credit 6511 6911 [Kamen Rider OOO - Opening]
%credit 6911 7311 [Maki Ohguro - Anything Goes!]
%info Ligatures 0
%color FF2225 ECFF40 31FF03
%effect passing on 0 500 500 500 500
&YOU &COUNT &THE &ME&DALS &ONE &TWO &AND &THREE
% effect cursor off
&LIFE &GOES &ON &A&NY&THING &GOES &CO&MING &UP &OOO
%effect passing off
%style Main Alignment=8 PrimaryColour=&H0003FF31 SecondaryColour=&H002522FF KaraokeColour=&H0040FFEC
# declare a style derived from "Main"named "Choir"
# with diffrent colours and Alignment
&i&ra&nai &mo&ta&nai &yu&me &mo &mi&na&i
% effect cursor on
&FREE &na &jo&u&tai &so&re &mo &i&i &ke&do
&kok&ka&ra &ha&ji&ma&ru &THE &SHOW &WE'RE &WAI&TING &FOR
%effect move on 640 360 960 480
&COUNT &THE &ME&DALS &ONE &TWO &AND &THREE
%effect move off 0 0 0 0
&un&mei &wa &ki&mi &hout&to&ka&na&i
&kek&kyo&ku &wa &su&su&mu &shi&ka&nai
&mi&chi&na&ru &ten&kai &GIVE &ME &E&NER&GY
%style Choir:Main Alignment=2 PrimaryColour=&H00310FF3 SecondaryColour=&H002FF225 KaraokeColour=&H00ECFF40
&COUNT &THE &ME&DALS &ONE &TWO &AND &THREE
&dai&jo&u&bu &a&shi&ta &wa &i&tsu&dat&te &B&LANK
&ji&bu&n &no &ka&chi &wa &ji&bun &de &ki&me&ru &mo&no &sa
%effect snap 0
&OOO &OOO &OOO &OOO &COME &ON
%effect snap 10
&A&NY&THING &GOES &so&no &ko&ko&ro &ga &a&tsu&ku &na&ru &mo&no
&mi&ta&sa&re&ru &mo&no &wo &sa&ga&shi&te
&LIFE &GOES &ON &hon&ki &da&shi&te &ta&ta&ka&u &no &na&ra
%effect fading 0 0 -100 100
&ma&ke&ru &ki &shi&nai &ha&zu"""
        tim_content = """250 258
263 271
275 284
292 300
304 313
321 350
354 371
375 392
400 425
434 459
467 492
500 525
534 546
546 559
563 571
576 600
609 621
626 638
642 655
659 713
1743 1756
1760 1772
1777 1797
1806 1818
1827 1852
1856 1881
1889 1902
1906 1918
1923 1935
1939 1952
1956 1977
1985 2006
2019 2035
2044 2056
2060 2073
2077 2102
2110 2127
2135 2148
2152 2164
2169 2181
2185 2198
2202 2231
2236 2248
2252 2319
2265 2277
2286 2298
2302 2315
2319 2331
2336 2348
2352 2365
2369 2377
2394 2406
2411 2423
2427 2440
2444 2456
2461 2469
2473 2494
2519 2540
2548 2561
2565 2578
2582 2590
2598 2623
2628 2640
2644 2669
2678 2728
2753 2765
2769 2798
2811 2824
2832 2853
2861 2886
2899 2920
2928 2940
2944 2957
2961 2978
2986 3015
3032 3057
3065 3078
3082 3111
3115 3140
3149 3157
3161 3174
3174 3186
3191 3199
3207 3249
3253 3345
3274 3286
3291 3299
3303 3312
3316 3328
3337 3353
3357 3387
3403 3428
3437 3449
3453 3466
3474 3482
3487 3516
3533 3558
3566 3578
3583 3595
3599 3612
3616 3637
3645 3658
3662 3683
3691 3737
3766 3812
3820 3833
3837 3866
3875 3904
3912 3933
3937 3950
3954 3979
3983 4004
4012 4025
4029 4041
4050 4071
4079 4100
4108 4121
4129 4212
4265 4272
4277 4304
4317 4325
4333 4358
4367 4375
4379 4404
4413 4425
4429 4442
4446 4467
4479 4504
4525 4571
4584 4638
4646 4688
4709 4725
4730 4750
4755 4996
4788 4838
4867 4905
4930 4963
4996 5030
5055 5072
5076 5113
5117 5125
5127 5138
5144 5158
5163 5182
5189 5210
5216 5238
5243 5255
5268 5288
5297 5305
5309 5364
5401 5430
5434 5460
5464 5476
5480 5505
5514 5539
5547 5555
5560 5626
5656 5706
5714 5726
5731 5764
5768 5810
5814 5839
5847 5872
5881 5906
5910 5947
5968 5981
5989 6014
6018 6027
6025 6065
6118 6131
6135 6156
6160 6189
6194 6223
6227 6260
6269 6298
6302 6314
6323 6377
6415 6440
6444 6473
6477 6490
6494 6527
6531 6556
6561 6573
6577 6636
6669 6723
6727 6744
6748 6773
6782 6811
6819 6844
6853 6878
6886 6907
6921 7094"""
        generator = Generator()
        generated_str = generator.generate(lyr_content, tim_content, "tass")
        self.assertEqual(generated_str, r"""[Script Info]
ScriptType: v4.00+
WrapStyle: 5
ScaledBorderAndShadow: yes
YCbCrMatrix: TV.601
PlayResX: 1280
PlayResY: 720
TimingVersion: 4
Ligatures: 0


[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, KaraokeColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Choir, DejaVu Sans, 25, &H00310FF3, &H002FF225, &H00ECFF40, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 2, 10, 10, 10, 1
Style: Credit, DejaVu Sans, 25, &H006044EEEE, &H006044EEEE, &H006044EEEE, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 2, 2, 1, 10, 10, 10, 1
Style: Default1, DejaVu Sans, 25, &H0003FF31, &H002522FF, &H0040FFEC, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 8, 10, 10, 10, 1
Style: Main, DejaVu Sans, 25, &H0003FF31, &H002522FF, &H0040FFEC, &H00000000, &H00000000, 0, 0, 0, 0, 200, 200, 0, 0, 1, 5, 2, 8, 10, 10, 10, 1


[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0, 0:00:00.00, 0:00:04.00, Credit, , 0, 0, 0, , {\fade(500, 500)} [Kamen Rider OOO - Opening]
Dialogue: 0, 0:00:04.00, 0:00:08.00, Credit, , 0, 0, 0, , {\fade(500, 500)} [Maki Ohguro - Anything Goes!]
Dialogue: 0, 0:01:05.11, 0:01:09.11, Credit, , 0, 0, 0, , {\fade(500, 500)} [Kamen Rider OOO - Opening]
Dialogue: 0, 0:01:09.11, 0:01:13.11, Credit, , 0, 0, 0, , {\fade(500, 500)} [Maki Ohguro - Anything Goes!]
Dialogue: 0, 0:00:01.50, 0:00:04.75, Default1, , 0, 0, 0, Passing;0;500;500;500;500, {\fade(750, 500)}{\kt(100, 8)}YOU {\kt(109, 12)}COUNT {\kt(122, 12)}THE {\kt(135, 15)}ME{\kt(151, 12)}DALS {\kt(164, 36)}ONE {\kt(201, 20)}TWO {\kt(222, 20)}AND {\kt(243, 32)}THREE\N{\pc(100, 8)}YOU {\pc(109, 12)}COUNT {\pc(122, 12)}THE {\pc(135, 15)}ME{\pc(151, 12)}DALS {\pc(164, 36)}ONE {\pc(201, 20)}TWO {\pc(222, 20)}AND {\pc(243, 32)}THREE
Dialogue: 0, 0:00:03.34, 0:00:07.63, Default1, , 0, 0, 0, Passing;0;500;500;500;500, {\fade(750, 500)}{\kt(100, 25)}LIFE {\kt(126, 32)}GOES {\kt(159, 32)}ON {\kt(192, 20)}A{\kt(212, 13)}NY{\kt(226, 11)}THING {\kt(238, 28)}GOES {\kt(267, 20)}CO{\kt(288, 16)}MING {\kt(305, 16)}UP {\kt(322, 57)}OOO
Dialogue: 0, 0:00:16.43, 0:00:20.56, Main, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 13)}i{\kt(114, 15)}ra{\kt(130, 24)}nai {\kt(155, 20)}mo{\kt(176, 33)}ta{\kt(210, 28)}nai {\kt(239, 20)}yu{\kt(260, 15)}me {\kt(276, 16)}mo {\kt(293, 16)}mi{\kt(310, 24)}na{\kt(335, 28)}i
Dialogue: 0, 0:00:19.19, 0:00:23.69, Main, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 16)}FREE {\kt(117, 20)}na {\kt(138, 16)}jo{\kt(155, 28)}u{\kt(184, 24)}tai {\kt(209, 20)}so{\kt(230, 15)}re {\kt(246, 16)}mo {\kt(263, 16)}i{\kt(280, 32)}i {\kt(313, 16)}ke{\kt(330, 70)}do\N{\pc(100, 16)}FREE {\pc(117, 20)}na {\pc(138, 16)}jo{\pc(155, 28)}u{\pc(184, 24)}tai {\pc(209, 20)}so{\pc(230, 15)}re {\pc(246, 16)}mo {\pc(263, 16)}i{\pc(280, 32)}i {\pc(313, 16)}ke{\pc(330, 70)}do
Dialogue: 0, 0:00:21.65, 0:00:25.44, Main, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 12)}kok{\kt(113, 20)}ka{\kt(134, 16)}ra {\kt(151, 15)}ha{\kt(167, 16)}ji{\kt(184, 16)}ma{\kt(201, 11)}ru {\kt(213, 28)}THE {\kt(242, 16)}SHOW {\kt(259, 16)}WE'RE {\kt(276, 15)}WAI{\kt(292, 12)}TING {\kt(305, 24)}FOR\N{\pc(100, 12)}kok{\pc(113, 20)}ka{\pc(134, 16)}ra {\pc(151, 15)}ha{\pc(167, 16)}ji{\pc(184, 16)}ma{\pc(201, 11)}ru {\pc(213, 28)}THE {\pc(242, 16)}SHOW {\pc(259, 16)}WE'RE {\pc(276, 15)}WAI{\pc(292, 12)}TING {\pc(305, 24)}FOR
Dialogue: 0, 0:00:24.19, 0:00:27.78, Main, , 0, 0, 0, , {\move(640, 360, 960, 480)}{\fade(750, 500)}{\kt(100, 21)}COUNT {\kt(122, 20)}THE {\kt(143, 16)}ME{\kt(160, 11)}DALS {\kt(172, 32)}ONE {\kt(205, 16)}TWO {\kt(222, 28)}AND {\kt(251, 58)}THREE\N{\pc(100, 21)}COUNT {\pc(122, 20)}THE {\pc(143, 16)}ME{\pc(160, 11)}DALS {\pc(172, 32)}ONE {\pc(205, 16)}TWO {\pc(222, 28)}AND {\pc(251, 58)}THREE
Dialogue: 0, 0:00:26.53, 0:00:30.65, Main, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 12)}un{\kt(113, 32)}mei {\kt(146, 25)}wa {\kt(172, 28)}ki{\kt(201, 32)}mi {\kt(234, 33)}hout{\kt(268, 19)}to{\kt(288, 16)}ka{\kt(305, 20)}na{\kt(326, 36)}i\N{\pc(100, 12)}un{\pc(113, 32)}mei {\pc(146, 25)}wa {\pc(172, 28)}ki{\pc(201, 32)}mi {\pc(234, 33)}hout{\pc(268, 19)}to{\pc(288, 16)}ka{\pc(305, 20)}na{\pc(326, 36)}i
Dialogue: 0, 0:00:29.32, 0:00:33.95, Main, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 25)}kek{\kt(126, 20)}kyo{\kt(147, 32)}ku {\kt(180, 28)}wa {\kt(209, 16)}su{\kt(226, 16)}su{\kt(242, 12)}mu {\kt(255, 12)}shi{\kt(268, 49)}ka{\kt(318, 95)}nai\N{\pc(100, 25)}kek{\pc(126, 20)}kyo{\pc(147, 32)}ku {\pc(180, 28)}wa {\pc(209, 16)}su{\pc(226, 16)}su{\pc(242, 12)}mu {\pc(255, 12)}shi{\pc(268, 49)}ka{\pc(318, 95)}nai
Dialogue: 0, 0:00:31.74, 0:00:35.66, Main, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 12)}mi{\kt(113, 12)}chi{\kt(126, 12)}na{\kt(139, 15)}ru {\kt(155, 24)}ten{\kt(180, 33)}kai {\kt(214, 40)}GIVE {\kt(255, 20)}ME {\kt(276, 16)}E{\kt(293, 15)}NER{\kt(309, 33)}GY\N{\pc(100, 12)}mi{\pc(113, 12)}chi{\pc(126, 12)}na{\pc(139, 15)}ru {\pc(155, 24)}ten{\pc(180, 33)}kai {\pc(214, 40)}GIVE {\pc(255, 20)}ME {\pc(276, 16)}E{\pc(293, 15)}NER{\pc(309, 33)}GY
Dialogue: 0, 0:00:34.33, 0:00:37.87, Choir, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 25)}COUNT {\kt(126, 19)}THE {\kt(146, 16)}ME{\kt(163, 16)}DALS {\kt(180, 24)}ONE {\kt(205, 20)}TWO {\kt(226, 24)}AND {\kt(251, 53)}THREE\N{\pc(100, 25)}COUNT {\pc(126, 19)}THE {\pc(146, 16)}ME{\pc(163, 16)}DALS {\pc(180, 24)}ONE {\pc(205, 20)}TWO {\pc(226, 24)}AND {\pc(251, 53)}THREE
Dialogue: 0, 0:00:36.66, 0:00:42.62, Choir, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 46)}dai{\kt(147, 20)}jo{\kt(168, 32)}u{\kt(201, 37)}bu {\kt(239, 28)}a{\kt(268, 16)}shi{\kt(285, 28)}ta {\kt(314, 24)}wa {\kt(339, 20)}i{\kt(360, 15)}tsu{\kt(376, 29)}dat{\kt(406, 28)}te {\kt(435, 20)}B{\kt(456, 90)}LANK\N{\pc(100, 46)}dai{\pc(147, 20)}jo{\pc(168, 32)}u{\pc(201, 37)}bu {\pc(239, 28)}a{\pc(268, 16)}shi{\pc(285, 28)}ta {\pc(314, 24)}wa {\pc(339, 20)}i{\pc(360, 15)}tsu{\pc(376, 29)}dat{\pc(406, 28)}te {\pc(435, 20)}B{\pc(456, 90)}LANK
Dialogue: 0, 0:00:41.65, 0:00:50.46, Choir, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 7)}ji{\kt(108, 31)}bu{\kt(140, 20)}n {\kt(161, 32)}no {\kt(194, 16)}ka{\kt(211, 28)}chi {\kt(240, 20)}wa {\kt(261, 16)}ji{\kt(278, 24)}bun {\kt(303, 36)}de {\kt(360, 46)}ki{\kt(407, 66)}me{\kt(474, 49)}ru {\kt(544, 16)}mo{\kt(561, 24)}no {\kt(586, 245)}sa\N{\pc(100, 7)}ji{\pc(108, 31)}bu{\pc(140, 20)}n {\pc(161, 32)}no {\pc(194, 16)}ka{\pc(211, 28)}chi {\pc(240, 20)}wa {\pc(261, 16)}ji{\pc(278, 24)}bun {\pc(303, 36)}de {\pc(360, 46)}ki{\pc(407, 66)}me{\pc(474, 49)}ru {\pc(544, 16)}mo{\pc(561, 24)}no {\pc(586, 245)}sa
Dialogue: 0, 0:00:46.88, 0:00:51.63, Choir, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 50)}OOO {\kt(179, 38)}OOO {\kt(242, 33)}OOO {\kt(308, 34)}OOO {\kt(367, 17)}COME {\kt(388, 37)}ON\N{\pc(100, 50)}OOO {\pc(179, 38)}OOO {\pc(242, 33)}OOO {\pc(308, 34)}OOO {\pc(367, 17)}COME {\pc(388, 37)}ON
Dialogue: 0, 0:00:50.17, 0:00:56.76, Choir, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 8)}A{\kt(109, 12)}NY{\kt(122, 19)}THING {\kt(142, 23)}GOES {\kt(166, 27)}so{\kt(194, 27)}no {\kt(222, 16)}ko{\kt(251, 20)}ko{\kt(272, 16)}ro {\kt(289, 58)}ga {\kt(384, 29)}a{\kt(414, 29)}tsu{\kt(444, 15)}ku {\kt(460, 28)}na{\kt(489, 33)}ru {\kt(523, 15)}mo{\kt(539, 70)}no\N{\pc(100, 8)}A{\pc(109, 12)}NY{\pc(122, 19)}THING {\pc(142, 23)}GOES {\pc(166, 27)}so{\pc(194, 27)}no {\pc(222, 16)}ko{\pc(251, 20)}ko{\pc(272, 16)}ro {\pc(289, 58)}ga {\pc(384, 29)}a{\pc(414, 29)}tsu{\pc(444, 15)}ku {\pc(460, 28)}na{\pc(489, 33)}ru {\pc(523, 15)}mo{\pc(539, 70)}no
Dialogue: 0, 0:00:55.56, 0:01:01.15, Choir, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 50)}mi{\kt(151, 19)}ta{\kt(171, 37)}sa{\kt(209, 45)}re{\kt(255, 28)}ru {\kt(284, 32)}mo{\kt(317, 33)}no {\kt(351, 40)}wo {\kt(412, 13)}sa{\kt(426, 32)}ga{\kt(459, 12)}shi{\kt(469, 40)}te\N{\pc(100, 50)}mi{\pc(151, 19)}ta{\pc(171, 37)}sa{\pc(209, 45)}re{\pc(255, 28)}ru {\pc(284, 32)}mo{\pc(317, 33)}no {\pc(351, 40)}wo {\pc(412, 13)}sa{\pc(426, 32)}ga{\pc(459, 12)}shi{\pc(469, 40)}te
Dialogue: 0, 0:01:00.18, 0:01:06.86, Choir, , 0, 0, 0, , {\fade(750, 500)}{\kt(100, 13)}LIFE {\kt(114, 24)}GOES {\kt(139, 32)}ON {\kt(172, 33)}hon{\kt(206, 36)}ki {\kt(243, 37)}da{\kt(281, 15)}shi{\kt(297, 62)}te {\kt(397, 25)}ta{\kt(423, 32)}ta{\kt(456, 16)}ka{\kt(473, 36)}u {\kt(510, 28)}no {\kt(539, 16)}na{\kt(556, 62)}ra\N{\pc(100, 13)}LIFE {\pc(114, 24)}GOES {\pc(139, 32)}ON {\pc(172, 33)}hon{\pc(206, 36)}ki {\pc(243, 37)}da{\pc(281, 15)}shi{\pc(297, 62)}te {\pc(397, 25)}ta{\pc(423, 32)}ta{\pc(456, 16)}ka{\pc(473, 36)}u {\pc(510, 28)}no {\pc(539, 16)}na{\pc(556, 62)}ra
Dialogue: 0, 0:01:05.69, 0:01:11.94, Choir, , 0, 0, 0, , {\fade(0, 0)}{\kt(100, 54)}ma{\kt(155, 20)}ke{\kt(176, 28)}ru {\kt(205, 37)}ki {\kt(243, 32)}shi{\kt(276, 33)}nai {\kt(310, 28)}ha{\kt(352, 173)}zu\N{\pc(100, 54)}ma{\pc(155, 20)}ke{\pc(176, 28)}ru {\pc(205, 37)}ki {\pc(243, 32)}shi{\pc(276, 33)}nai {\pc(310, 28)}ha{\pc(352, 173)}zu


[lyr]
;%credit 0 400 [Kamen Rider OOO - Opening]
;%credit 400 800 [Maki Ohguro - Anything Goes!]
;%credit 6511 6911 [Kamen Rider OOO - Opening]
;%credit 6911 7311 [Maki Ohguro - Anything Goes!]
;%info Ligatures 0
;%color FF2225 ECFF40 31FF03
;%effect passing on 0 500 500 500 500
;&YOU &COUNT &THE &ME&DALS &ONE &TWO &AND &THREE
;% effect cursor off
;&LIFE &GOES &ON &A&NY&THING &GOES &CO&MING &UP &OOO
;%effect passing off
;%style Main Alignment=8 PrimaryColour=&H0003FF31 SecondaryColour=&H002522FF KaraokeColour=&H0040FFEC
;# declare a style derived from "Main"named "Choir"
;# with diffrent colours and Alignment
;&i&ra&nai &mo&ta&nai &yu&me &mo &mi&na&i
;% effect cursor on
;&FREE &na &jo&u&tai &so&re &mo &i&i &ke&do
;&kok&ka&ra &ha&ji&ma&ru &THE &SHOW &WE'RE &WAI&TING &FOR
;%effect move on 640 360 960 480
;&COUNT &THE &ME&DALS &ONE &TWO &AND &THREE
;%effect move off 0 0 0 0
;&un&mei &wa &ki&mi &hout&to&ka&na&i
;&kek&kyo&ku &wa &su&su&mu &shi&ka&nai
;&mi&chi&na&ru &ten&kai &GIVE &ME &E&NER&GY
;%style Choir:Main Alignment=2 PrimaryColour=&H00310FF3 SecondaryColour=&H002FF225 KaraokeColour=&H00ECFF40
;&COUNT &THE &ME&DALS &ONE &TWO &AND &THREE
;&dai&jo&u&bu &a&shi&ta &wa &i&tsu&dat&te &B&LANK
;&ji&bu&n &no &ka&chi &wa &ji&bun &de &ki&me&ru &mo&no &sa
;%effect snap 0
;&OOO &OOO &OOO &OOO &COME &ON
;%effect snap 10
;&A&NY&THING &GOES &so&no &ko&ko&ro &ga &a&tsu&ku &na&ru &mo&no
;&mi&ta&sa&re&ru &mo&no &wo &sa&ga&shi&te
;&LIFE &GOES &ON &hon&ki &da&shi&te &ta&ta&ka&u &no &na&ra
;%effect fading 0 0 -100 100
;&ma&ke&ru &ki &shi&nai &ha&zu


[tim]
;250 258
;263 271
;275 284
;292 300
;304 313
;321 350
;354 371
;375 392
;400 425
;434 459
;467 492
;500 525
;534 546
;546 559
;563 571
;576 600
;609 621
;626 638
;642 655
;659 713
;1743 1756
;1760 1772
;1777 1797
;1806 1818
;1827 1852
;1856 1881
;1889 1902
;1906 1918
;1923 1935
;1939 1952
;1956 1977
;1985 2006
;2019 2035
;2044 2056
;2060 2073
;2077 2102
;2110 2127
;2135 2148
;2152 2164
;2169 2181
;2185 2198
;2202 2231
;2236 2248
;2252 2319
;2265 2277
;2286 2298
;2302 2315
;2319 2331
;2336 2348
;2352 2365
;2369 2377
;2394 2406
;2411 2423
;2427 2440
;2444 2456
;2461 2469
;2473 2494
;2519 2540
;2548 2561
;2565 2578
;2582 2590
;2598 2623
;2628 2640
;2644 2669
;2678 2728
;2753 2765
;2769 2798
;2811 2824
;2832 2853
;2861 2886
;2899 2920
;2928 2940
;2944 2957
;2961 2978
;2986 3015
;3032 3057
;3065 3078
;3082 3111
;3115 3140
;3149 3157
;3161 3174
;3174 3186
;3191 3199
;3207 3249
;3253 3345
;3274 3286
;3291 3299
;3303 3312
;3316 3328
;3337 3353
;3357 3387
;3403 3428
;3437 3449
;3453 3466
;3474 3482
;3487 3516
;3533 3558
;3566 3578
;3583 3595
;3599 3612
;3616 3637
;3645 3658
;3662 3683
;3691 3737
;3766 3812
;3820 3833
;3837 3866
;3875 3904
;3912 3933
;3937 3950
;3954 3979
;3983 4004
;4012 4025
;4029 4041
;4050 4071
;4079 4100
;4108 4121
;4129 4212
;4265 4272
;4277 4304
;4317 4325
;4333 4358
;4367 4375
;4379 4404
;4413 4425
;4429 4442
;4446 4467
;4479 4504
;4525 4571
;4584 4638
;4646 4688
;4709 4725
;4730 4750
;4755 4996
;4788 4838
;4867 4905
;4930 4963
;4996 5030
;5055 5072
;5076 5113
;5117 5125
;5127 5138
;5144 5158
;5163 5182
;5189 5210
;5216 5238
;5243 5255
;5268 5288
;5297 5305
;5309 5364
;5401 5430
;5434 5460
;5464 5476
;5480 5505
;5514 5539
;5547 5555
;5560 5626
;5656 5706
;5714 5726
;5731 5764
;5768 5810
;5814 5839
;5847 5872
;5881 5906
;5910 5947
;5968 5981
;5989 6014
;6018 6027
;6025 6065
;6118 6131
;6135 6156
;6160 6189
;6194 6223
;6227 6260
;6269 6298
;6302 6314
;6323 6377
;6415 6440
;6444 6473
;6477 6490
;6494 6527
;6531 6556
;6561 6573
;6577 6636
;6669 6723
;6727 6744
;6748 6773
;6782 6811
;6819 6844
;6853 6878
;6886 6907
;6921 7094""")