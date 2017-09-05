import datetime
from django.test import TestCase
from django.urls import reverse

from .models import SecnewsItem

# Create your tests here.
class SecnewsItemTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SecnewsItem.objects.bulk_create([
            SecnewsItem(pub_date=datetime.date(2016,4,12),
                        tag=r'Android',
                        author=r'autoprime @utoprime',
                        en_text=r'LG officially opens the European LG G5 H850 bootloader http://forum.xda-developers.com/lg-g5/development/official-european-lg-g5-h850-bootloader-t3363040',
                        cn_text=r'LG 官方发布解锁 G5 H850 手机 Bootloader 的工具： https://t.co/MADc3WOXbr',
                        ),
            SecnewsItem(pub_date=datetime.date(2016,4,22),
                        tag=r'Exploit',
                        author=r'MWR Labs @mwrlabs',
                        en_text=r'New post from @ ukstufus on creating safer implants with environmentally keyed shellcode https://labs.mwrinfosecurity.com/blog/safer-shellcode-implants/  https://t.co/q5Vv8naAdE',
                        cn_text=r'为远控植入的 Shellcode 代码添加环境检查功能，包括：是否第一次执行、是否在指定机器上运行、某个时间点后是否运行过等，来自 MWR Labs： https://t.co/oeUazgeDaA  https://t.co/q5Vv8naAdE  ;',
                        img_link=r'http://pbs.twimg.com/media/CgjjlpSWgAA3RFb.jpg'
            ),
            SecnewsItem(pub_date=datetime.date(2017,7,27),
                        tag=r'WirelessSecurity',
                        cn_text=r'NRSC-5-C 无线电报文的接收和解码： http://theori.io/research/nrsc-5-c',
                        img_link=r'http://pbs.twimg.com/media/DFqwuxAXgAAGpqn.jpg'
            ),
            SecnewsItem(pub_date=datetime.date(2017,7,27),
                        tag=r'Malware',
                        cn_text=r'BlackHat 会议上，来自 Kryptowire 的研究员表示，中国上海 Adups 公司的手机固件升级软件是一款间谍软件，会窃取用户数据： https://threatpost.com/android-sypware-still-collects-pii-despite-outcry/127042/'
            ),
        ])

    def test_get_all(self):
        response = self.client.get(reverse('secnews:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['secnews_list'], 
            ['<SecnewsItem: #3, 2017-07-27>', '<SecnewsItem: #4, 2017-07-27>', '<SecnewsItem: #2, 2016-04-22>', '<SecnewsItem: #1, 2016-04-12>'])

    def test_get_year(self):
        # test 2016
        response = self.client.get(reverse('secnews:year', kwargs={'y': 2016}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['secnews_list'], 
            ['<SecnewsItem: #2, 2016-04-22>', '<SecnewsItem: #1, 2016-04-12>'])
        # test 2017
        response = self.client.get(reverse('secnews:year', kwargs={'y': 2017}))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['secnews_list'], 
            ['<SecnewsItem: #3, 2017-07-27>', '<SecnewsItem: #4, 2017-07-27>'])

    def test_get_month(self):
        # test 2016.4
        response = self.client.get(reverse('secnews:month', kwargs={'y': 2016, 'm': 4}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['secnews_list'], 
            ['<SecnewsItem: #2, 2016-04-22>', '<SecnewsItem: #1, 2016-04-12>'])

    def test_get_day(self):
        # test 2017.7.27
        response = self.client.get(reverse('secnews:day', kwargs={'y': 2017, 'm': 7, 'd': 27}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['secnews_list'], 
            ['<SecnewsItem: #3, 2017-07-27>', '<SecnewsItem: #4, 2017-07-27>'])

    def test_search_keyword_in_cn_text(self):
        response = self.client.get(reverse('secnews:search'), {'keyword':'无线', 'content_type':'cn_text'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['secnews_list'], 
            ['<SecnewsItem: #3, 2017-07-27>'])
    
    def test_search_keyword_in_tag(self):
        response = self.client.get(reverse('secnews:search'), {'keyword':'android', 'content_type':'tag'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['secnews_list'], 
            ['<SecnewsItem: #1, 2016-04-12>'])
