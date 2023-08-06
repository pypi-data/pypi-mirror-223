import kuto
from kuto import title, MultipartEncoder


class TestHome(kuto.Case):

    @title("一般请求")
    def test_normal_req(self):
        payload = {"type": 2}
        headers = {"user-agent-web":
                       "X/b67aaff2200d4fc2a2e5a079abe78cc6"}
        self.post('/qzd-bff-app/qzd/v1/home/getToolCardListForPc',
                  json=payload, headers=headers)
        self.assertEqual('code', 0)

    @title("文件上传")
    def test_upload_file(self):
        path = '/qzd-bff-patent/patent/batch/statistics/upload'
        files = {'file': open('data/号码上传模板_1.xlsx', 'rb')}
        self.post(path, files=files)
        self.assertEqual('data', ["CN212306629U", "CN210449594U",
                                  "CN110849114A", "CN209129562U",
                                  "CN208620801U", "CN110562653B",
                                  "CN213064984U", "CN211402151U"])

    @title("form请求")
    def test_form_req(self):
        url = '/qzd-bff-patent/image-search/images'
        m = MultipartEncoder(
            fields={
                'key1': 'value1',  # 参数
                'imageFile': (
                    'data/companyLogo.png',
                    open('../data/companyLogo.png', 'rb'),
                    'image/png'),  # 文件1
            }
        )
        h = {'Content-Type': m.content_type}
        r = self.post(url, data=m, headers=h)
        print(r.text)


if __name__ == '__main__':
    kuto.main(host='https://app-test.qizhidao.com')
