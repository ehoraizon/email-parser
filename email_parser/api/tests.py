from rest_framework.test import APITestCase
from rest_framework import status
from os import path

BASE_DIR = path.sep.join(path.abspath(__file__).split(path.sep)[:-2])

class ApiTest(APITestCase):
    databases = ["default"]

    def test_post(self):
        with open(path.join(BASE_DIR, "test_assets", "test.msg"), "rb") as file:
            response = self.client.post("/api/", {"msg": file}, format='multipart')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            b"""{"id":1,"message_id":"<3709e1a3-663f-464c-a38f-584ae8c9fe24@xtinmta105.xt.local>","to_name":"","to_email":"aeg@cp.delivery.ncrcustomerpower.com","from_name":"","from_email":"enews@events.lagalaxy.com","subject":"April Fool's Day Offer, Save up to 40% with no fees","date":1301673982000}""",
            response.content
        )        
    
    def test_post_bad_request(self):
        response = self.client.post("/api/", {"msg": b""}, format='multipart')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_post_file_type(self):
        with open(path.join(BASE_DIR, "test_assets", "bulk.tar"), "rb") as file:
            response = self.client.post("/api/", {"msg": file}, format='multipart')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete(self):
        self.test_post()
        response = self.client.delete("/api/?id=1")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_delete_not_found(self):
        response = self.client.delete("/api/?id=1")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_bad_request(self):
        response = self.client.delete("/api/")

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


    def test_put_bulk_tar(self):
        with open(path.join(BASE_DIR, "test_assets", "bulk.tar"), "rb") as file:
            response = self.client.put("/api/", {"tar": file}, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            br"""{"size":12,"emails":[{"id":1,"message_id":"<20110401161739.E3786358A9D7B977@contact-darty.com>","to_name":"","to_email":"1000mercis@cp.assurance.returnpath.net","from_name":"","from_email":"infos@contact-darty.com","subject":"Cuit Vapeur 29.90 euros, Nintendo 3DS 239 euros, GPS TOM TOM 139 euros... decouvrez VITE tous les bons plans du weekend !","date":1301689061000},{"id":2,"message_id":"<MP1301631592801EH10491@mindspay.com>","to_name":"","to_email":"aamarketinginc@cp.monitor1.returnpath.net","from_name":"","from_email":"MindsPaysurvey@mindspaymails.com","subject":"Paid Mail : Offer #10491 get $4.00","date":1301627992000},{"id":3,"message_id":"<3709e1a3-663f-464c-a38f-584ae8c9fe24@xtinmta105.xt.local>","to_name":"","to_email":"aeg@cp.delivery.ncrcustomerpower.com","from_name":"","from_email":"enews@events.lagalaxy.com","subject":"April Fool's Day Offer, Save up to 40% with no fees","date":1301673982000},{"id":4,"message_id":"<bx6rw3raupta74au6m0rxbysph09qe.0.15@mta141.avivaemail.co.uk>","to_name":"","to_email":"alchemyworx@cp.assurance.returnpath.net","from_name":"","from_email":"aviva@avivaemail.co.uk","subject":"(TEST-Multipart) =?utf-8?q?=5BRetention_In_Life_ezine=5Fhome=5F050411=5D_Introducing_Your_?=\n =?utf-8?q?Aviva_Essentials=3A_Win_4_tickets_to_the_Aviva_Premiership_Rugb?=\n =?utf-8?q?y_Final=2C_Keep_the_cost_of_driving_down_and_more?=","date":1301681689000},{"id":5,"message_id":"<EF9C090C1310457C97AD9E1279F0BF68@acm.local>","to_name":"","to_email":"americancollegiatemarketing@cp.monitor1.returnpath.net","from_name":"","from_email":"Amway@MagazineLine.com","subject":"April 2011 TPM Amway No Subs Spring Savings from MagazineLine","date":1301668696000},{"id":6,"message_id":"<527817310.344.1301667087687.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] Grant Funding May Be Available for Top Online Colleges. Get\n Free Info Today.","date":1301659920000},{"id":7,"message_id":"<463918295.411.1301674909118.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] The Art of Positive Thinking","date":1301668362000},{"id":8,"message_id":"<20110401173626.15575.2089030531.swift@webadmin.boydgaming.net>","to_name":"Lisa Marshall","to_email":"boydgamingcorporation@cp.assurance.returnpath.net","from_name":"Lisa Marshall","from_email":"suncoast@boydgaming.net","subject":"See What's Happening with our Table Games!","date":1301668586000},{"id":9,"message_id":"<1479419471.1301626641534.JavaMail.pjfpbg1@saixp36>","to_name":"","to_email":"citibanksingaporelimited@cp.monitor1.returnpath.net","from_name":"","from_email":"customer.service@citicorp.com","subject":"Citi Alerts","date":1301641041000},{"id":10,"message_id":"<6426946.1413.1301675117949.JavaMail.tomcat@osadmin02>","to_name":"","to_email":"cobaltgroup@cp.monitor1.returnpath.net","from_name":"","from_email":"klongfield.10162425@dealer.onstation.com","subject":"[SAMPLE] 04-719314-2011 Chevy April DAP #1","date":1301689517000},{"id":11,"message_id":"<58795828.1301655732499.JavaMail.compostadmin@secos-a107>","to_name":"","to_email":"compostmarketingab@cp.monitor1.returnpath.net","from_name":"","from_email":"from@test.carmamail.com","subject":"ComHem Senaste Nyheterna","date":1301677333000},{"id":12,"message_id":"<Corel.6k3yh-636g-.fv4t@email1-corel.com>","to_name":"","to_email":"corel@cp.monitor1.returnpath.net","from_name":"","from_email":"news@email1-corel.com","subject":"PREVIEW:   Save $170 and get special gift with CorelDraw Premium Suite X5","date":1301651575000}]}""",
            response.content
        )
    
    def test_put_bulk_tar_gz(self):
        with open(path.join(BASE_DIR, "test_assets", "bulk.tar.gz"), "rb") as file:
            response = self.client.put("/api/", {"tar": file}, format='multipart')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            br"""{"size":12,"emails":[{"id":1,"message_id":"<20110401161739.E3786358A9D7B977@contact-darty.com>","to_name":"","to_email":"1000mercis@cp.assurance.returnpath.net","from_name":"","from_email":"infos@contact-darty.com","subject":"Cuit Vapeur 29.90 euros, Nintendo 3DS 239 euros, GPS TOM TOM 139 euros... decouvrez VITE tous les bons plans du weekend !","date":1301689061000},{"id":2,"message_id":"<MP1301631592801EH10491@mindspay.com>","to_name":"","to_email":"aamarketinginc@cp.monitor1.returnpath.net","from_name":"","from_email":"MindsPaysurvey@mindspaymails.com","subject":"Paid Mail : Offer #10491 get $4.00","date":1301627992000},{"id":3,"message_id":"<3709e1a3-663f-464c-a38f-584ae8c9fe24@xtinmta105.xt.local>","to_name":"","to_email":"aeg@cp.delivery.ncrcustomerpower.com","from_name":"","from_email":"enews@events.lagalaxy.com","subject":"April Fool's Day Offer, Save up to 40% with no fees","date":1301673982000},{"id":4,"message_id":"<bx6rw3raupta74au6m0rxbysph09qe.0.15@mta141.avivaemail.co.uk>","to_name":"","to_email":"alchemyworx@cp.assurance.returnpath.net","from_name":"","from_email":"aviva@avivaemail.co.uk","subject":"(TEST-Multipart) =?utf-8?q?=5BRetention_In_Life_ezine=5Fhome=5F050411=5D_Introducing_Your_?=\n =?utf-8?q?Aviva_Essentials=3A_Win_4_tickets_to_the_Aviva_Premiership_Rugb?=\n =?utf-8?q?y_Final=2C_Keep_the_cost_of_driving_down_and_more?=","date":1301681689000},{"id":5,"message_id":"<EF9C090C1310457C97AD9E1279F0BF68@acm.local>","to_name":"","to_email":"americancollegiatemarketing@cp.monitor1.returnpath.net","from_name":"","from_email":"Amway@MagazineLine.com","subject":"April 2011 TPM Amway No Subs Spring Savings from MagazineLine","date":1301668696000},{"id":6,"message_id":"<527817310.344.1301667087687.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] Grant Funding May Be Available for Top Online Colleges. Get\n Free Info Today.","date":1301659920000},{"id":7,"message_id":"<463918295.411.1301674909118.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] The Art of Positive Thinking","date":1301668362000},{"id":8,"message_id":"<20110401173626.15575.2089030531.swift@webadmin.boydgaming.net>","to_name":"Lisa Marshall","to_email":"boydgamingcorporation@cp.assurance.returnpath.net","from_name":"Lisa Marshall","from_email":"suncoast@boydgaming.net","subject":"See What's Happening with our Table Games!","date":1301668586000},{"id":9,"message_id":"<1479419471.1301626641534.JavaMail.pjfpbg1@saixp36>","to_name":"","to_email":"citibanksingaporelimited@cp.monitor1.returnpath.net","from_name":"","from_email":"customer.service@citicorp.com","subject":"Citi Alerts","date":1301641041000},{"id":10,"message_id":"<6426946.1413.1301675117949.JavaMail.tomcat@osadmin02>","to_name":"","to_email":"cobaltgroup@cp.monitor1.returnpath.net","from_name":"","from_email":"klongfield.10162425@dealer.onstation.com","subject":"[SAMPLE] 04-719314-2011 Chevy April DAP #1","date":1301689517000},{"id":11,"message_id":"<58795828.1301655732499.JavaMail.compostadmin@secos-a107>","to_name":"","to_email":"compostmarketingab@cp.monitor1.returnpath.net","from_name":"","from_email":"from@test.carmamail.com","subject":"ComHem Senaste Nyheterna","date":1301677333000},{"id":12,"message_id":"<Corel.6k3yh-636g-.fv4t@email1-corel.com>","to_name":"","to_email":"corel@cp.monitor1.returnpath.net","from_name":"","from_email":"news@email1-corel.com","subject":"PREVIEW:   Save $170 and get special gift with CorelDraw Premium Suite X5","date":1301651575000}]}""",
            response.content
        )

    def test_put_file_type(self):
        with open(path.join(BASE_DIR, "test_assets", "test.msg"), "rb") as file:
            response = self.client.put("/api/", {"tar": file}, format='multipart')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_without_parameters(self):
        self.test_put_bulk_tar()
        response = self.client.get("/api/")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            br"""{"limit":25,"offset":0,"size":12,"emails":[{"id":2,"message_id":"<MP1301631592801EH10491@mindspay.com>","to_name":"","to_email":"aamarketinginc@cp.monitor1.returnpath.net","from_name":"","from_email":"MindsPaysurvey@mindspaymails.com","subject":"Paid Mail : Offer #10491 get $4.00","date":1301627992000},{"id":9,"message_id":"<1479419471.1301626641534.JavaMail.pjfpbg1@saixp36>","to_name":"","to_email":"citibanksingaporelimited@cp.monitor1.returnpath.net","from_name":"","from_email":"customer.service@citicorp.com","subject":"Citi Alerts","date":1301641041000},{"id":12,"message_id":"<Corel.6k3yh-636g-.fv4t@email1-corel.com>","to_name":"","to_email":"corel@cp.monitor1.returnpath.net","from_name":"","from_email":"news@email1-corel.com","subject":"PREVIEW:   Save $170 and get special gift with CorelDraw Premium Suite X5","date":1301651575000},{"id":6,"message_id":"<527817310.344.1301667087687.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] Grant Funding May Be Available for Top Online Colleges. Get\n Free Info Today.","date":1301659920000},{"id":7,"message_id":"<463918295.411.1301674909118.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] The Art of Positive Thinking","date":1301668362000},{"id":8,"message_id":"<20110401173626.15575.2089030531.swift@webadmin.boydgaming.net>","to_name":"Lisa Marshall","to_email":"boydgamingcorporation@cp.assurance.returnpath.net","from_name":"Lisa Marshall","from_email":"suncoast@boydgaming.net","subject":"See What's Happening with our Table Games!","date":1301668586000},{"id":5,"message_id":"<EF9C090C1310457C97AD9E1279F0BF68@acm.local>","to_name":"","to_email":"americancollegiatemarketing@cp.monitor1.returnpath.net","from_name":"","from_email":"Amway@MagazineLine.com","subject":"April 2011 TPM Amway No Subs Spring Savings from MagazineLine","date":1301668696000},{"id":3,"message_id":"<3709e1a3-663f-464c-a38f-584ae8c9fe24@xtinmta105.xt.local>","to_name":"","to_email":"aeg@cp.delivery.ncrcustomerpower.com","from_name":"","from_email":"enews@events.lagalaxy.com","subject":"April Fool's Day Offer, Save up to 40% with no fees","date":1301673982000},{"id":11,"message_id":"<58795828.1301655732499.JavaMail.compostadmin@secos-a107>","to_name":"","to_email":"compostmarketingab@cp.monitor1.returnpath.net","from_name":"","from_email":"from@test.carmamail.com","subject":"ComHem Senaste Nyheterna","date":1301677333000},{"id":4,"message_id":"<bx6rw3raupta74au6m0rxbysph09qe.0.15@mta141.avivaemail.co.uk>","to_name":"","to_email":"alchemyworx@cp.assurance.returnpath.net","from_name":"","from_email":"aviva@avivaemail.co.uk","subject":"(TEST-Multipart) =?utf-8?q?=5BRetention_In_Life_ezine=5Fhome=5F050411=5D_Introducing_Your_?=\n =?utf-8?q?Aviva_Essentials=3A_Win_4_tickets_to_the_Aviva_Premiership_Rugb?=\n =?utf-8?q?y_Final=2C_Keep_the_cost_of_driving_down_and_more?=","date":1301681689000},{"id":1,"message_id":"<20110401161739.E3786358A9D7B977@contact-darty.com>","to_name":"","to_email":"1000mercis@cp.assurance.returnpath.net","from_name":"","from_email":"infos@contact-darty.com","subject":"Cuit Vapeur 29.90 euros, Nintendo 3DS 239 euros, GPS TOM TOM 139 euros... decouvrez VITE tous les bons plans du weekend !","date":1301689061000},{"id":10,"message_id":"<6426946.1413.1301675117949.JavaMail.tomcat@osadmin02>","to_name":"","to_email":"cobaltgroup@cp.monitor1.returnpath.net","from_name":"","from_email":"klongfield.10162425@dealer.onstation.com","subject":"[SAMPLE] 04-719314-2011 Chevy April DAP #1","date":1301689517000}]}""",
            response.content
        )

    def test_get_without_parameters(self):
        self.test_put_bulk_tar()
        response = self.client.get("/api/")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            br"""{"limit":25,"offset":0,"size":12,"emails":[{"id":2,"message_id":"<MP1301631592801EH10491@mindspay.com>","to_name":"","to_email":"aamarketinginc@cp.monitor1.returnpath.net","from_name":"","from_email":"MindsPaysurvey@mindspaymails.com","subject":"Paid Mail : Offer #10491 get $4.00","date":1301627992000},{"id":9,"message_id":"<1479419471.1301626641534.JavaMail.pjfpbg1@saixp36>","to_name":"","to_email":"citibanksingaporelimited@cp.monitor1.returnpath.net","from_name":"","from_email":"customer.service@citicorp.com","subject":"Citi Alerts","date":1301641041000},{"id":12,"message_id":"<Corel.6k3yh-636g-.fv4t@email1-corel.com>","to_name":"","to_email":"corel@cp.monitor1.returnpath.net","from_name":"","from_email":"news@email1-corel.com","subject":"PREVIEW:   Save $170 and get special gift with CorelDraw Premium Suite X5","date":1301651575000},{"id":6,"message_id":"<527817310.344.1301667087687.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] Grant Funding May Be Available for Top Online Colleges. Get\n Free Info Today.","date":1301659920000},{"id":7,"message_id":"<463918295.411.1301674909118.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] The Art of Positive Thinking","date":1301668362000},{"id":8,"message_id":"<20110401173626.15575.2089030531.swift@webadmin.boydgaming.net>","to_name":"Lisa Marshall","to_email":"boydgamingcorporation@cp.assurance.returnpath.net","from_name":"Lisa Marshall","from_email":"suncoast@boydgaming.net","subject":"See What's Happening with our Table Games!","date":1301668586000},{"id":5,"message_id":"<EF9C090C1310457C97AD9E1279F0BF68@acm.local>","to_name":"","to_email":"americancollegiatemarketing@cp.monitor1.returnpath.net","from_name":"","from_email":"Amway@MagazineLine.com","subject":"April 2011 TPM Amway No Subs Spring Savings from MagazineLine","date":1301668696000},{"id":3,"message_id":"<3709e1a3-663f-464c-a38f-584ae8c9fe24@xtinmta105.xt.local>","to_name":"","to_email":"aeg@cp.delivery.ncrcustomerpower.com","from_name":"","from_email":"enews@events.lagalaxy.com","subject":"April Fool's Day Offer, Save up to 40% with no fees","date":1301673982000},{"id":11,"message_id":"<58795828.1301655732499.JavaMail.compostadmin@secos-a107>","to_name":"","to_email":"compostmarketingab@cp.monitor1.returnpath.net","from_name":"","from_email":"from@test.carmamail.com","subject":"ComHem Senaste Nyheterna","date":1301677333000},{"id":4,"message_id":"<bx6rw3raupta74au6m0rxbysph09qe.0.15@mta141.avivaemail.co.uk>","to_name":"","to_email":"alchemyworx@cp.assurance.returnpath.net","from_name":"","from_email":"aviva@avivaemail.co.uk","subject":"(TEST-Multipart) =?utf-8?q?=5BRetention_In_Life_ezine=5Fhome=5F050411=5D_Introducing_Your_?=\n =?utf-8?q?Aviva_Essentials=3A_Win_4_tickets_to_the_Aviva_Premiership_Rugb?=\n =?utf-8?q?y_Final=2C_Keep_the_cost_of_driving_down_and_more?=","date":1301681689000},{"id":1,"message_id":"<20110401161739.E3786358A9D7B977@contact-darty.com>","to_name":"","to_email":"1000mercis@cp.assurance.returnpath.net","from_name":"","from_email":"infos@contact-darty.com","subject":"Cuit Vapeur 29.90 euros, Nintendo 3DS 239 euros, GPS TOM TOM 139 euros... decouvrez VITE tous les bons plans du weekend !","date":1301689061000},{"id":10,"message_id":"<6426946.1413.1301675117949.JavaMail.tomcat@osadmin02>","to_name":"","to_email":"cobaltgroup@cp.monitor1.returnpath.net","from_name":"","from_email":"klongfield.10162425@dealer.onstation.com","subject":"[SAMPLE] 04-719314-2011 Chevy April DAP #1","date":1301689517000}]}""",
            response.content
        )
    
    def test_get_with_parameters(self):
        self.test_put_bulk_tar()
        response = self.client.get("/api/?limit=6&offset=2")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            br"""{"limit":6,"offset":2,"size":4,"emails":[{"id":12,"message_id":"<Corel.6k3yh-636g-.fv4t@email1-corel.com>","to_name":"","to_email":"corel@cp.monitor1.returnpath.net","from_name":"","from_email":"news@email1-corel.com","subject":"PREVIEW:   Save $170 and get special gift with CorelDraw Premium Suite X5","date":1301651575000},{"id":6,"message_id":"<527817310.344.1301667087687.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] Grant Funding May Be Available for Top Online Colleges. Get\n Free Info Today.","date":1301659920000},{"id":7,"message_id":"<463918295.411.1301674909118.JavaMail.root@mail.beliefnet.com>","to_name":"","to_email":"beliefnet@cp.monitor1.returnpath.net","from_name":"","from_email":"specialoffers@mail.beliefnet.com","subject":"[SP] The Art of Positive Thinking","date":1301668362000},{"id":8,"message_id":"<20110401173626.15575.2089030531.swift@webadmin.boydgaming.net>","to_name":"Lisa Marshall","to_email":"boydgamingcorporation@cp.assurance.returnpath.net","from_name":"Lisa Marshall","from_email":"suncoast@boydgaming.net","subject":"See What's Happening with our Table Games!","date":1301668586000}]}""",
            response.content
        )

    def test_get_empty(self):
        response = self.client.get("/api/")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            br"""{"limit":25,"offset":0,"size":0,"emails":[]}""",
            response.content
        )